from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.users_url = reverse('get_all_users')

        self.user_data = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "Test",
            "lastname": "User"
        }

    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # el modelo no tiene username, verificamos email
        self.assertTrue(User.objects.filter(email="test@example.com").exists())

        self.assertIn("token", response.data)
        self.assertIn("user", response.data)

    def test_user_registration_invalid_data(self):
        invalid_data = {
            "email": "",
            "password": "123"
        }
        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_user_registration(self):
        self.client.post(self.register_url, self.user_data)
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login(self):
        self.client.post(self.register_url, self.user_data)

        login_data = {
            "email": "test@example.com",
            "password": "testpass123"
        }

        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_users(self):
        User.objects.create_user(
            email="u1@example.com",
            password="pass123",
            name="User1",
            lastname="Last1"
        )

        User.objects.create_user(
            email="u2@example.com",
            password="pass123",
            name="User2",
            lastname="Last2"
        )

        response = self.client.get(self.users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # tu API devuelve una lista
        self.assertEqual(len(response.data), 2)
