from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from users.models import CustomUser


class RegisterViewTest(TestCase):

    def test_register_user_successfully(self):
        url = reverse('api:register')
        data = {'username': 'newuser', 'password': 'password123', 'email': 'test@example.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(username='newuser').exists())

    def test_register_user_with_existing_username(self):
        CustomUser.objects.create_user(username='existinguser', password='password123', email='test@example.com')
        url = reverse('api:register')
        data = {'username': 'existinguser', 'password': 'password123', 'email': 'test2@example.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_with_missing_credentials(self):
        url = reverse('api:register')
        data = {'username': 'newuser', 'password': '', 'email': ''}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='password123',
                                                   email='test@example.com')

    def test_login_user_successfully(self):
        url = reverse('api:login')
        data = {'username': 'testuser', 'password': 'password123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_user_with_invalid_credentials(self):
        url = reverse('api:login')
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
