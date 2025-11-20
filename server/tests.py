# server/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class AuthAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.users_url = reverse('get_all_users')
        
        # Datos de prueba
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }

    def test_user_registration(self):
        """Test para registro de usuario"""
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)
        
        # Verificar que el usuario se creó en la BD
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_user_registration_invalid_data(self):
        """Test para registro con datos inválidos"""
        invalid_data = {
            'username': '',  # Username vacío
            'password': '123'
        }
        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_user_registration(self):
        """Test para usuario duplicado"""
        # Crear usuario primero
        self.client.post(self.register_url, self.user_data)
        
        # Intentar crear el mismo usuario otra vez
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login(self):
        """Test para login de usuario"""
        # Primero registrar el usuario
        self.client.post(self.register_url, self.user_data)
        
        # Intentar login
        login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

def test_get_all_users(self):
    """Test para obtener todos los usuarios"""
    # Crear algunos usuarios
    User.objects.create_user('user1', 'user1@example.com', 'pass123')
    User.objects.create_user('user2', 'user2@example.com', 'pass123')
    
    response = self.client.get(self.users_url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # Dependiendo de lo que devuelva tu vista:
    if isinstance(response.data, list):
        # Si devuelve una lista directamente
        self.assertEqual(len(response.data), 2)
    elif isinstance(response.data, dict) and 'users' in response.data:
        # Si devuelve un diccionario con clave 'users'
        self.assertEqual(len(response.data['users']), 2)
    else:
        # Si devuelve otro formato
        self.assertEqual(len(response.data), 2)  # Ajusta según tu respuesta real