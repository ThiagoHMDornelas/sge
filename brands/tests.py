from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from brands.forms import BrandForm
from brands.models import Brand


class BrandModelTest(TestCase):
    def test_str(self):
        self.assertEqual(str(Brand(name='Toyota')), 'Toyota')

    def test_default_ordering_is_case_insensitive(self):
        Brand.objects.create(name='zebra')
        Brand.objects.create(name='Amarelo')
        Brand.objects.create(name='fiat')

        self.assertEqual(
            list(Brand.objects.values_list('name', flat=True)),
            ['Amarelo', 'fiat', 'zebra'],
        )


class BrandFormTest(TestCase):
    def test_valid_form(self):
        form = BrandForm(data={'name': 'Honda', 'description': 'Marca japonesa'})
        self.assertTrue(form.is_valid())

    def test_name_is_required(self):
        form = BrandForm(data={'name': '', 'description': 'x'})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)


class BrandViewTest(TestCase):
    def setUp(self):
        User.objects.create_superuser(username='admin', password='senha123')
        self.client.login(username='admin', password='senha123')

    def test_login_is_required(self):
        self.client.logout()
        response = self.client.get(reverse('brand_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_list_renders_existing_brands(self):
        Brand.objects.create(name='Toyota')
        response = self.client.get(reverse('brand_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Toyota')

    def test_create_view_creates_brand(self):
        response = self.client.post(reverse('brand_create'), {'name': 'Jeep'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Brand.objects.filter(name='Jeep').exists())

    def test_detail_view(self):
        brand = Brand.objects.create(name='Toyota')
        response = self.client.get(reverse('brand_detail', args=[brand.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Toyota')


class BrandAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(username='api', password='senha123')
        self.client.force_authenticate(self.user)

    def test_list_requires_authentication(self):
        response = APIClient().get(reverse('brand-create-list-api-view'))
        self.assertIn(response.status_code, (401, 403))

    def test_list_brands(self):
        Brand.objects.create(name='Toyota')
        response = self.client.get(reverse('brand-create-list-api-view'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_create_brand(self):
        response = self.client.post(
            reverse('brand-create-list-api-view'),
            {'name': 'Mazda', 'description': ''},
            format='json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Brand.objects.filter(name='Mazda').exists())
