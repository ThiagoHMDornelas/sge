from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from brands.models import Brand
from category.models import Category
from inflow.forms import InflowForm
from inflow.models import InFlow
from product.models import Product
from supplier.models import Supplier


class InflowSignalTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Eletrônicos')
        self.brand = Brand.objects.create(name='Sony')
        self.supplier = Supplier.objects.create(name='Distribuidora X')
        self.product = Product.objects.create(
            name='Fone', category=self.category, brand=self.brand,
            cost_price=10, selling_price=20, quantity=5,
        )

    def test_inflow_increases_product_quantity(self):
        InFlow.objects.create(
            supplier=self.supplier, product=self.product, quantity=3
        )
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 8)

    def test_zero_quantity_does_not_change_stock(self):
        InFlow.objects.create(
            supplier=self.supplier, product=self.product, quantity=0
        )
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 5)


class InflowFormTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Eletrônicos')
        self.brand = Brand.objects.create(name='Sony')
        self.supplier = Supplier.objects.create(name='Distribuidora X')
        self.product = Product.objects.create(
            name='Fone', category=self.category, brand=self.brand,
            cost_price=10, selling_price=20,
        )

    def test_valid_form(self):
        form = InflowForm(data={
            'supplier': self.supplier.pk,
            'product': self.product.pk,
            'quantity': 2,
        })
        self.assertTrue(form.is_valid())

    def test_quantity_is_required(self):
        form = InflowForm(data={
            'supplier': self.supplier.pk,
            'product': self.product.pk,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('quantity', form.errors)


class InflowViewTest(TestCase):
    def setUp(self):
        User.objects.create_superuser(username='admin', password='senha123')
        self.client.login(username='admin', password='senha123')
        self.category = Category.objects.create(name='Eletrônicos')
        self.brand = Brand.objects.create(name='Sony')
        self.supplier = Supplier.objects.create(name='Distribuidora X')
        self.product = Product.objects.create(
            name='Fone', category=self.category, brand=self.brand,
            cost_price=10, selling_price=20,
        )

    def test_login_is_required(self):
        self.client.logout()
        response = self.client.get(reverse('inflow_list'))
        self.assertEqual(response.status_code, 302)

    def test_create_view_creates_inflow(self):
        response = self.client.post(reverse('inflow_create'), {
            'supplier': self.supplier.pk,
            'product': self.product.pk,
            'quantity': 4,
            'description': '',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(InFlow.objects.count(), 1)

    def test_order_by_product_name(self):
        zebra = Product.objects.create(
            name='Zebra', category=self.category, brand=self.brand,
            cost_price=1, selling_price=2,
        )
        amarelo = Product.objects.create(
            name='Amarelo', category=self.category, brand=self.brand,
            cost_price=1, selling_price=2,
        )
        InFlow.objects.create(supplier=self.supplier, product=zebra, quantity=1)
        InFlow.objects.create(supplier=self.supplier, product=amarelo, quantity=1)

        response = self.client.get(reverse('inflow_list'), {'order_by': 'product'})

        products = [i.product.name for i in response.context['inflows']]
        self.assertEqual(products, ['Amarelo', 'Zebra'])


class InflowAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        user = User.objects.create_superuser(username='api', password='senha123')
        self.client.force_authenticate(user)
        self.category = Category.objects.create(name='Eletrônicos')
        self.brand = Brand.objects.create(name='Sony')
        self.supplier = Supplier.objects.create(name='Distribuidora X')
        self.product = Product.objects.create(
            name='Fone', category=self.category, brand=self.brand,
            cost_price=10, selling_price=20,
        )

    def test_list_requires_authentication(self):
        response = APIClient().get(reverse('inflows-create-list-api-view'))
        self.assertIn(response.status_code, (401, 403))

    def test_create_inflow(self):
        response = self.client.post(
            reverse('inflows-create-list-api-view'),
            {
                'supplier': self.supplier.pk,
                'product': self.product.pk,
                'quantity': 2,
                'description': '',
            },
            format='json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(InFlow.objects.count(), 1)


class InflowStockAdjustmentTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Eletrônicos')
        self.brand = Brand.objects.create(name='Sony')
        self.supplier = Supplier.objects.create(name='Distribuidora X')
        self.product = Product.objects.create(
            name='Fone', category=self.category, brand=self.brand,
            cost_price=10, selling_price=20, quantity=5,
        )
        self.other_product = Product.objects.create(
            name='Caixa', category=self.category, brand=self.brand,
            cost_price=10, selling_price=20, quantity=5,
        )

    def test_update_decreasing_quantity_adjusts_stock(self):
        inflow = InFlow.objects.create(
            supplier=self.supplier, product=self.product, quantity=3
        )
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 8)

        inflow.quantity = 1
        inflow.save()

        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 6)

    def test_update_changing_product_moves_quantity(self):
        inflow = InFlow.objects.create(
            supplier=self.supplier, product=self.product, quantity=3
        )

        inflow.product = self.other_product
        inflow.save()

        self.product.refresh_from_db()
        self.other_product.refresh_from_db()
        self.assertEqual(self.product.quantity, 5)
        self.assertEqual(self.other_product.quantity, 8)

    def test_delete_restores_stock(self):
        inflow = InFlow.objects.create(
            supplier=self.supplier, product=self.product, quantity=3
        )

        inflow.delete()

        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 5)


class InflowQuantityValidationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        user = User.objects.create_superuser(username='api', password='senha123')
        self.client.force_authenticate(user)
        self.category = Category.objects.create(name='Eletrônicos')
        self.brand = Brand.objects.create(name='Sony')
        self.supplier = Supplier.objects.create(name='Distribuidora X')
        self.product = Product.objects.create(
            name='Fone', category=self.category, brand=self.brand,
            cost_price=10, selling_price=20,
        )

    def _post(self, quantity):
        return self.client.post(
            reverse('inflows-create-list-api-view'),
            {
                'supplier': self.supplier.pk,
                'product': self.product.pk,
                'quantity': quantity,
                'description': '',
            },
            format='json',
        )

    def test_rejects_zero_quantity(self):
        self.assertEqual(self._post(0).status_code, 400)

    def test_rejects_negative_quantity(self):
        self.assertEqual(self._post(-1).status_code, 400)
