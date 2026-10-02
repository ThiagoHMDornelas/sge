from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from authentication.models import Profile


class ProfileModelTest(TestCase):
    def test_profile_is_created_with_user(self):
        user = User.objects.create_user(username='mario', password='senha123')
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_profile_str(self):
        user = User.objects.create_user(username='luigi', password='senha123')
        self.assertEqual(str(user.profile), 'luigi Profile')


class ProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='mario', password='senha123'
        )
        self.client.login(username='mario', password='senha123')

    def test_login_is_required(self):
        self.client.logout()
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_profile_is_rendered(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_creates_profile_when_missing(self):
        Profile.objects.filter(user=self.user).delete()

        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Profile.objects.filter(user=self.user).exists())

    def test_updates_user_data(self):
        response = self.client.post(reverse('profile'), {
            'first_name': 'Mário',
            'email': 'mario@example.com',
            'avatar': '',
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Mário')
        self.assertEqual(self.user.email, 'mario@example.com')
