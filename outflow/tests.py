from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from brands.models import Brand
from category.models import Category
from outflow.forms import OutflowForm
from outflow.models import OutFlow
from product.models import Product


class OutflowSignalTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Eletrônicos')
        self.brand = Brand.objects.create(name='Sony')
        self.product = Product.objects.create(
            name='Fone', category=self.category, brand=self.brand,
            cost_price=10, selling_price=20, quantity=10,
        )

    def test_outflow_decreases_product_quantity(self):
        OutFlow.objects.create(product=self.product, quantity=4)
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 6)

    def test_zero_quantity_does_not_change_stock(self):
        OutFlow.objects.create(product=self.product, quantity=0)
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 10)


class OutflowFormTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Eletrônicos')
        self.brand = Brand.objects.create(name='Sony')
        self.product = Product.objects.create(
            name='Fone', category=self.category, brand=self.brand,
            cost_price=10, selling_price=20, quantity=3,
        )

    def test_rejects_quantity_above_stock(self):
        form = OutflowForm(data={
            'product': self.product.pk,
            'quantity': 99,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('quantity', form.errors)

    def test_accepts_quantity_within_stock(self):
        form = OutflowForm(data={
            'product': self.product.pk,
            'quantity': 2,
        })
        self.assertTrue(form.is_valid())


class OutflowViewTest(TestCase):
    def setUp(self):
        User.objects.create_superuser(username='admin', password='senha123')
        self.client.login(username='admin', password='senha123')
        self.category = Category.objects.create(name='Eletrônicos')
        self.brand = Brand.objects.create(name='Sony')
        self.product = Product.objects.create(
            name='Fone', category=self.category, brand=self.brand,
            cost_price=10, selling_price=20, quantity=10,
        )

    def test_login_is_required(self):
        self.client.logout()
        response = self.client.get(reverse('outflow_list'))
        self.assertEqual(response.status_code, 302)

    def test_create_view_creates_outflow(self):
        response = self.client.post(reverse('outflow_create'), {
            'product': self.product.pk,
            'quantity': 2,
            'description': '',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(OutFlow.objects.count(), 1)

    def test_order_by_product_name(self):
        zebra = Product.objects.create(
            name='Zebra', category=self.category, brand=self.brand,
            cost_price=1, selling_price=2,
        )
        amarelo = Product.objects.create(
            name='Amarelo', category=self.category, brand=self.brand,
            cost_price=1, selling_price=2,
        )
        OutFlow.objects.create(product=zebra, quantity=1)
        OutFlow.objects.create(product=amarelo, quantity=1)

        response = self.client.get(reverse('outflow_list'), {'order_by': 'product'})

        products = [i.product.name for i in response.context['outflows']]
        self.assertEqual(products, ['Amarelo', 'Zebra'])


class OutflowAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        user = User.objects.create_superuser(username='api', password='senha123')
        self.client.force_authenticate(user)
        self.category = Category.objects.create(name='Eletrônicos')
        self.brand = Brand.objects.create(name='Sony')
        self.product = Product.objects.create(
            name='Fone', category=self.category, brand=self.brand,
            cost_price=10, selling_price=20, quantity=10,
        )

    def test_list_requires_authentication(self):
        response = APIClient().get(reverse('outflows-create-list-api-view'))
        self.assertIn(response.status_code, (401, 403))

    def test_create_outflow(self):
        response = self.client.post(
            reverse('outflows-create-list-api-view'),
            {'product': self.product.pk, 'quantity': 2, 'description': ''},
            format='json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(OutFlow.objects.count(), 1)


class OutflowStockAdjustmentTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Eletrônicos')
        self.brand = Brand.objects.create(name='Sony')
        self.product = Product.objects.create(
            name='Fone', category=self.category, brand=self.brand,
            cost_price=10, selling_price=20, quantity=10,
        )
        self.other_product = Product.objects.create(
            name='Caixa', category=self.category, brand=self.brand,
            cost_price=10, selling_price=20, quantity=5,
        )

    def test_update_decreasing_quantity_restores_stock(self):
        outflow = OutFlow.objects.create(product=self.product, quantity=4)
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 6)

        outflow.quantity = 2
        outflow.save()

        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 8)

    def test_update_increasing_quantity_removes_more(self):
        outflow = OutFlow.objects.create(product=self.product, quantity=2)

        outflow.quantity = 5
        outflow.save()

        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 5)

    def test_update_changing_product_moves_quantity(self):
        outflow = OutFlow.objects.create(product=self.product, quantity=4)

        outflow.product = self.other_product
        outflow.save()

        self.product.refresh_from_db()
        self.other_product.refresh_from_db()
        self.assertEqual(self.product.quantity, 10)
        self.assertEqual(self.other_product.quantity, 1)

    def test_delete_restores_stock(self):
        outflow = OutFlow.objects.create(product=self.product, quantity=4)

        outflow.delete()

        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 10)


class OutflowAPIStockTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        user = User.objects.create_superuser(username='api', password='senha123')
        self.client.force_authenticate(user)
        self.category = Category.objects.create(name='Eletrônicos')
        self.brand = Brand.objects.create(name='Sony')
        self.product = Product.objects.create(
            name='Fone', category=self.category, brand=self.brand,
            cost_price=10, selling_price=20, quantity=10,
        )

    def test_patch_adjusts_stock(self):
        outflow = OutFlow.objects.create(product=self.product, quantity=4)

        response = self.client.patch(
            reverse('outflows-detail-api-view', args=[outflow.pk]),
            {'quantity': 1},
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 9)

    def test_delete_restores_stock(self):
        outflow = OutFlow.objects.create(product=self.product, quantity=4)

        response = self.client.delete(
            reverse('outflows-detail-api-view', args=[outflow.pk])
        )

        self.assertEqual(response.status_code, 204)
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 10)

    def test_create_above_stock_is_rejected(self):
        response = self.client.post(
            reverse('outflows-create-list-api-view'),
            {'product': self.product.pk, 'quantity': 999, 'description': ''},
            format='json',
        )
        self.assertEqual(response.status_code, 400)

    def test_create_zero_is_rejected(self):
        response = self.client.post(
            reverse('outflows-create-list-api-view'),
            {'product': self.product.pk, 'quantity': 0, 'description': ''},
            format='json',
        )
        self.assertEqual(response.status_code, 400)
