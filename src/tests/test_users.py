from src.models import User
from src.tests.base import BaseTestCase


class UserCurrentTest(BaseTestCase):
    def test_get_current_user(self):
        resp = self.client.get('/api/v1/users/current', **self.auth_header())
        self.assertEqual(resp.status_code, 200)
        data = resp.json()['data']
        self.assertEqual(data['username'], 'testuser')
        self.assertEqual(data['email'], 'test@test.com')

    def test_get_current_user_no_auth(self):
        resp = self.client.get('/api/v1/users/current')
        self.assertEqual(resp.status_code, 401)

    def test_update_current_user(self):
        resp = self.client.patch(
            '/api/v1/users/current',
            {'first_name': 'Updated'},
            content_type='application/json',
            **self.auth_header(),
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['data']['first_name'], 'Updated')

    def test_delete_current_user(self):
        resp = self.client.delete(
            '/api/v1/users/current', **self.auth_header())
        self.assertEqual(resp.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_deleted)


class UserByUsernameTest(BaseTestCase):
    def test_get_by_username(self):
        resp = self.client.get(
            '/api/v1/users/username/testuser', **self.auth_header()
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['data']['username'], 'testuser')

    def test_get_by_username_not_found(self):
        resp = self.client.get(
            '/api/v1/users/username/nobody', **self.auth_header()
        )
        self.assertEqual(resp.status_code, 404)


class UserByIdTest(BaseTestCase):
    def test_get_by_id(self):
        resp = self.client.get(
            f'/api/v1/users/{self.user.id}', **self.auth_header()
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['data']['username'], 'testuser')


class UserAdminTest(BaseTestCase):
    def test_get_all_users_as_admin(self):
        resp = self.client.get('/api/v1/users/', **self.admin_auth_header())
        self.assertEqual(resp.status_code, 200)
        self.assertGreaterEqual(len(resp.json()['data']), 2)

    def test_get_all_users_as_regular_user(self):
        resp = self.client.get('/api/v1/users/', **self.auth_header())
        self.assertEqual(resp.status_code, 403)

    def test_admin_update_user(self):
        resp = self.client.patch(
            f'/api/v1/users/{self.user.id}/update',
            {'first_name': 'AdminUpdated'},
            content_type='application/json',
            **self.admin_auth_header(),
        )
        self.assertEqual(resp.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'AdminUpdated')

    def test_admin_delete_user(self):
        resp = self.client.delete(
            f'/api/v1/users/{self.user.id}/delete', **self.admin_auth_header()
        )
        self.assertEqual(resp.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_deleted)
