from django.test import TestCase

from src.models import Role, User


class BaseTestCase(TestCase):
    def setUp(self):
        self.role = Role.objects.create(name='user')
        self.admin_role = Role.objects.create(name='admin')

        self.user = User.objects.create_user(
            email='test@test.com',
            username='testuser',
            password='password123',
            first_name='Test',
            last_name='User',
            phone='1234567890',
            role=self.role,
            is_verified=True,
        )

        self.admin_user = User.objects.create_user(
            email='admin@test.com',
            username='adminuser',
            password='password123',
            first_name='Admin',
            last_name='User',
            phone='0987654321',
            role=self.admin_role,
            is_verified=True,
        )

    def get_token(self, username_or_email='testuser', password='password123'):
        response = self.client.post(
            '/api/v1/auth/login',
            {'usernameOrEmail': username_or_email, 'password': password},
            content_type='application/json',
        )
        return response.json()['data']['token']

    def auth_header(self, token=None):
        if token is None:
            token = self.get_token()
        return {'HTTP_AUTHORIZATION': f'Bearer {token}'}

    def admin_auth_header(self):
        token = self.get_token('adminuser', 'password123')
        return {'HTTP_AUTHORIZATION': f'Bearer {token}'}
