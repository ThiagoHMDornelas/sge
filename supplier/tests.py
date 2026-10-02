from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from supplier.forms import SupplierForm
from supplier.models import Supplier


class SupplierModelTest(TestCase):
    def test_str(self):
        self.assertEqual(str(Supplier(name='Distribuidora X')), 'Distribuidora X')

    def test_default_ordering_is_case_insensitive(self):
        Supplier.objects.create(name='zulu')
        Supplier.objects.create(name='Atlas')

        self.assertEqual(
            list(Supplier.objects.values_list('name', flat=True)),
            ['Atlas', 'zulu'],
        )


class SupplierFormTest(TestCase):
    def test_name_is_required(self):
        form = SupplierForm(data={'name': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)


class SupplierViewTest(TestCase):
    def setUp(self):
        User.objects.create_superuser(username='admin', password='senha123')
        self.client.login(username='admin', password='senha123')

    def test_login_is_required(self):
        self.client.logout()
        response = self.client.get(reverse('supplier_list'))
        self.assertEqual(response.status_code, 302)

    def test_list_renders_existing_suppliers(self):
        Supplier.objects.create(name='Distribuidora X')
        response = self.client.get(reverse('supplier_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Distribuidora X')

    def test_create_view_creates_supplier(self):
        response = self.client.post(reverse('supplier_create'), {'name': 'Atlas'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Supplier.objects.filter(name='Atlas').exists())


class SupplierAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        user = User.objects.create_superuser(username='api', password='senha123')
        self.client.force_authenticate(user)

    def test_list_requires_authentication(self):
        response = APIClient().get(reverse('supplier-create-list-api-view'))
        self.assertIn(response.status_code, (401, 403))

    def test_create_supplier(self):
        response = self.client.post(
            reverse('supplier-create-list-api-view'),
            {'name': 'Atlas', 'description': ''},
            format='json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Supplier.objects.filter(name='Atlas').exists())
