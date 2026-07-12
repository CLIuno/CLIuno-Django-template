from src.models import Role
from src.tests.base import BaseTestCase


class RoleAdminTest(BaseTestCase):
    def test_get_all_roles(self):
        resp = self.client.get('/api/v1/roles/', **self.admin_auth_header())
        self.assertEqual(resp.status_code, 200)
        self.assertGreaterEqual(len(resp.json()['data']['roles']), 2)

    def test_get_all_roles_forbidden(self):
        resp = self.client.get('/api/v1/roles/', **self.auth_header())
        self.assertEqual(resp.status_code, 403)

    def test_get_role_by_id(self):
        resp = self.client.get(
            f'/api/v1/roles/{self.role.id}', **self.admin_auth_header()
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['data']['role']['name'], 'user')

    def test_create_role(self):
        resp = self.client.post(
            '/api/v1/roles/create',
            {'name': 'moderator'},
            content_type='application/json',
            **self.admin_auth_header(),
        )
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(Role.objects.filter(name='moderator').exists())

    def test_create_duplicate_role(self):
        resp = self.client.post(
            '/api/v1/roles/create',
            {'name': 'user'},
            content_type='application/json',
            **self.admin_auth_header(),
        )
        self.assertEqual(resp.status_code, 400)

    def test_update_role(self):
        resp = self.client.patch(
            f'/api/v1/roles/{self.role.id}/update',
            {'name': 'member'},
            content_type='application/json',
            **self.admin_auth_header(),
        )
        self.assertEqual(resp.status_code, 200)
        self.role.refresh_from_db()
        self.assertEqual(self.role.name, 'member')

    def test_delete_role(self):
        new_role = Role.objects.create(name='temp')
        resp = self.client.delete(
            f'/api/v1/roles/{new_role.id}/delete', **self.admin_auth_header()
        )
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(Role.objects.filter(id=new_role.id).exists())

    def test_get_users_by_role(self):
        resp = self.client.get(
            f'/api/v1/roles/{self.role.id}/users', **self.admin_auth_header()
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()['data']['users']), 1)
