import uuid

from src.models import Todo
from src.tests.base import BaseTestCase


class TodoCRUDTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.todo = Todo.objects.create(
            title='Test Todo', description='Test Desc', user=self.user
        )

    def test_get_all_todos(self):
        resp = self.client.get('/api/v1/todos', **self.auth_header())
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()['data']['todos']), 1)

    def test_get_todo_by_id(self):
        resp = self.client.get(
            f'/api/v1/todos/{self.todo.id}', **self.auth_header()
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['data']['todo']['title'], 'Test Todo')

    def test_get_todo_not_found(self):
        resp = self.client.get(
            f'/api/v1/todos/{uuid.uuid4()}', **self.auth_header()
        )
        self.assertEqual(resp.status_code, 404)

    def test_create_todo(self):
        resp = self.client.post(
            '/api/v1/todos',
            {'title': 'New Todo', 'description': 'New Desc'},
            content_type='application/json',
            **self.auth_header(),
        )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json()['data']['todo']['title'], 'New Todo')

    def test_create_todo_missing_title(self):
        resp = self.client.post(
            '/api/v1/todos',
            {'description': 'No title'},
            content_type='application/json',
            **self.auth_header(),
        )
        self.assertEqual(resp.status_code, 400)

    def test_update_own_todo(self):
        resp = self.client.patch(
            f'/api/v1/todos/{self.todo.id}',
            {'title': 'Updated'},
            content_type='application/json',
            **self.auth_header(),
        )
        self.assertEqual(resp.status_code, 200)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Updated')

    def test_cannot_update_others_todo(self):
        other_todo = Todo.objects.create(
            title='Admin Todo', user=self.admin_user
        )
        resp = self.client.patch(
            f'/api/v1/todos/{other_todo.id}',
            {'title': 'Hacked'},
            content_type='application/json',
            **self.auth_header(),
        )
        self.assertEqual(resp.status_code, 403)

    def test_delete_own_todo(self):
        resp = self.client.delete(
            f'/api/v1/todos/{self.todo.id}', **self.auth_header()
        )
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(Todo.objects.filter(id=self.todo.id).exists())

    def test_toggle_todo(self):
        self.assertFalse(self.todo.is_completed)
        resp = self.client.patch(
            f'/api/v1/todos/{self.todo.id}/toggle', **self.auth_header()
        )
        self.assertEqual(resp.status_code, 200)
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.is_completed)
        # toggle back
        self.client.patch(
            f'/api/v1/todos/{self.todo.id}/toggle', **self.auth_header()
        )
        self.todo.refresh_from_db()
        self.assertFalse(self.todo.is_completed)

    def test_get_current_user_todos(self):
        resp = self.client.get(
            '/api/v1/todos/current-user', **self.auth_header())
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()['data']['todos']), 1)

    def test_no_auth(self):
        resp = self.client.get('/api/v1/todos')
        self.assertEqual(resp.status_code, 401)
