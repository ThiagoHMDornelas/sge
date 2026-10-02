from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from brands.models import Brand
from category.models import Category
from product.forms import ProductForm
from product.models import Product


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Eletrônicos')
        self.brand = Brand.objects.create(name='Sony')

    def test_str(self):
        product = Product(name='Fone', category=self.category, brand=self.brand)
        self.assertEqual(str(product), 'Fone')

    def test_default_quantity_is_zero(self):
        product = Product.objects.create(
            name='Fone', category=self.category, brand=self.brand,
            cost_price=10, selling_price=20,
        )
        self.assertEqual(product.quantity, 0)


class ProductFormTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Eletrônicos')
        self.brand = Brand.objects.create(name='Sony')

    def test_valid_form(self):
        form = ProductForm(data={
            'name': 'Fone',
            'category': self.category.pk,
            'brand': self.brand.pk,
            'cost_price': '10.00',
            'selling_price': '20.00',
        })
        self.assertTrue(form.is_valid())

    def test_name_is_required(self):
        form = ProductForm(data={
            'category': self.category.pk,
            'brand': self.brand.pk,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)


class ProductViewTest(TestCase):
    def setUp(self):
        User.objects.create_superuser(username='admin', password='senha123')
        self.client.login(username='admin', password='senha123')
        self.category = Category.objects.create(name='Eletrônicos')
        self.brand = Brand.objects.create(name='Sony')

    def test_login_is_required(self):
        self.client.logout()
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_list_renders_product(self):
        Product.objects.create(
            name='Fone', category=self.category, brand=self.brand,
            cost_price=10, selling_price=20,
        )
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Fone')

    def test_create_view_creates_product(self):
        response = self.client.post(reverse('product_create'), {
            'name': 'Fone',
            'category': self.category.pk,
            'brand': self.brand.pk,
            'cost_price': '10.00',
            'selling_price': '20.00',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Product.objects.filter(name='Fone').exists())

    def test_order_by_brand_name(self):
        zebra = Brand.objects.create(name='Zebra')
        amarelo = Brand.objects.create(name='Amarelo')
        Product.objects.create(name='P1', category=self.category, brand=zebra,
                               cost_price=1, selling_price=2)
        Product.objects.create(name='P2', category=self.category, brand=amarelo,
                               cost_price=1, selling_price=2)

        response = self.client.get(reverse('product_list'), {'order_by': 'brand'})

        brands = [p.brand.name for p in response.context['products']]
        self.assertEqual(brands, ['Amarelo', 'Zebra'])

    def test_order_by_quantity_uses_numeric_order(self):
        Product.objects.create(name='P2', category=self.category, brand=self.brand,
                               cost_price=1, selling_price=2, quantity=2)
        Product.objects.create(name='P10', category=self.category, brand=self.brand,
                               cost_price=1, selling_price=2, quantity=10)

        response = self.client.get(reverse('product_list'), {'order_by': 'quantity'})

        quantities = [p.quantity for p in response.context['products']]
        self.assertEqual(quantities, [2, 10])


class ProductAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        user = User.objects.create_superuser(username='api', password='senha123')
        self.client.force_authenticate(user)
        self.category = Category.objects.create(name='Eletrônicos')
        self.brand = Brand.objects.create(name='Sony')

    def test_list_requires_authentication(self):
        response = APIClient().get(reverse('product-create-list-api-view'))
        self.assertIn(response.status_code, (401, 403))

    def test_create_product(self):
        response = self.client.post(
            reverse('product-create-list-api-view'),
            {
                'name': 'Fone',
                'category': self.category.pk,
                'brand': self.brand.pk,
                'description': '',
                'serie_number': 'SN-1',
                'cost_price': '10.00',
                'selling_price': '20.00',
            },
            format='json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Product.objects.filter(name='Fone').exists())
