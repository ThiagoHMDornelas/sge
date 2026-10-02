from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from category.forms import CategoryForm
from category.models import Category


class CategoryModelTest(TestCase):
    def test_str(self):
        self.assertEqual(str(Category(name='Eletrônicos')), 'Eletrônicos')

    def test_default_ordering_is_case_insensitive(self):
        Category.objects.create(name='zumbis')
        Category.objects.create(name='Acessórios')

        self.assertEqual(
            list(Category.objects.values_list('name', flat=True)),
            ['Acessórios', 'zumbis'],
        )


class CategoryFormTest(TestCase):
    def test_name_is_required(self):
        form = CategoryForm(data={'name': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)


class CategoryViewTest(TestCase):
    def setUp(self):
        User.objects.create_superuser(username='admin', password='senha123')
        self.client.login(username='admin', password='senha123')

    def test_login_is_required(self):
        self.client.logout()
        response = self.client.get(reverse('category_list'))
        self.assertEqual(response.status_code, 302)

    def test_list_renders_existing_categories(self):
        Category.objects.create(name='Eletrônicos')
        response = self.client.get(reverse('category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Eletrônicos')

    def test_create_view_creates_category(self):
        response = self.client.post(reverse('category_create'), {'name': 'Brinquedos'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Category.objects.filter(name='Brinquedos').exists())


class CategoryAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        user = User.objects.create_superuser(username='api', password='senha123')
        self.client.force_authenticate(user)

    def test_list_requires_authentication(self):
        response = APIClient().get(reverse('category-create-list-api-view'))
        self.assertIn(response.status_code, (401, 403))

    def test_create_category(self):
        response = self.client.post(
            reverse('category-create-list-api-view'),
            {'name': 'Games', 'description': ''},
            format='json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Category.objects.filter(name='Games').exists())
