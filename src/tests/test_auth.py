from src.tests.base import BaseTestCase


class AuthLoginTest(BaseTestCase):
    def test_login_success(self):
        resp = self.client.post(
            '/api/v1/auth/login',
            {'usernameOrEmail': 'testuser', 'password': 'password123'},
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('token', data['data'])
        self.assertIn('refreshToken', data['data'])

    def test_login_with_email(self):
        resp = self.client.post(
            '/api/v1/auth/login',
            {'usernameOrEmail': 'test@test.com', 'password': 'password123'},
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['status'], 'success')

    def test_login_wrong_password(self):
        resp = self.client.post(
            '/api/v1/auth/login',
            {'usernameOrEmail': 'testuser', 'password': 'wrongpassword'},
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 401)

    def test_login_nonexistent_user(self):
        resp = self.client.post(
            '/api/v1/auth/login',
            {'usernameOrEmail': 'nobody', 'password': 'password123'},
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 401)

    def test_login_missing_fields(self):
        resp = self.client.post(
            '/api/v1/auth/login',
            {'usernameOrEmail': 'testuser'},
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 400)

    def test_login_unverified_user(self):
        self.user.is_verified = False
        self.user.save()
        resp = self.client.post(
            '/api/v1/auth/login',
            {'usernameOrEmail': 'testuser', 'password': 'password123'},
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 401)
        self.assertIn('verify', resp.json()['message'].lower())

    def test_login_deleted_user(self):
        self.user.is_deleted = True
        self.user.save()
        resp = self.client.post(
            '/api/v1/auth/login',
            {'usernameOrEmail': 'testuser', 'password': 'password123'},
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 401)


class AuthRegisterTest(BaseTestCase):
    def test_register_success(self):
        resp = self.client.post(
            '/api/v1/auth/register',
            {
                'username': 'newuser',
                'first_name': 'New',
                'last_name': 'User',
                'email': 'new@test.com',
                'phone': '5551234567',
                'password': 'password123',
                'password_confirmation': 'password123',
            },
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json()['status'], 'success')

    def test_register_duplicate_username(self):
        resp = self.client.post(
            '/api/v1/auth/register',
            {
                'username': 'testuser',
                'first_name': 'New',
                'last_name': 'User',
                'email': 'unique@test.com',
                'phone': '5559999999',
                'password': 'password123',
                'password_confirmation': 'password123',
            },
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 400)

    def test_register_password_mismatch(self):
        resp = self.client.post(
            '/api/v1/auth/register',
            {
                'username': 'newuser2',
                'first_name': 'New',
                'last_name': 'User',
                'email': 'new2@test.com',
                'phone': '5552222222',
                'password': 'password123',
                'password_confirmation': 'different',
            },
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 400)

    def test_register_missing_fields(self):
        resp = self.client.post(
            '/api/v1/auth/register',
            {'username': 'incomplete'},
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 400)


class AuthLogoutTest(BaseTestCase):
    def test_logout_success(self):
        token = self.get_token()
        resp = self.client.post('/api/v1/auth/logout',
                                **self.auth_header(token))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['status'], 'success')

    def test_logout_double(self):
        token = self.get_token()
        self.client.post('/api/v1/auth/logout', **self.auth_header(token))
        resp = self.client.post('/api/v1/auth/logout',
                                **self.auth_header(token))
        self.assertEqual(resp.status_code, 401)


class AuthCheckTokenTest(BaseTestCase):
    def test_check_valid_token(self):
        resp = self.client.post(
            '/api/v1/auth/check-token', **self.auth_header())
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['message'], 'Token is valid')

    def test_check_no_token(self):
        resp = self.client.post('/api/v1/auth/check-token')
        self.assertEqual(resp.status_code, 401)


class AuthPasswordTest(BaseTestCase):
    def test_change_password(self):
        resp = self.client.post(
            '/api/v1/auth/change-password',
            {'oldPassword': 'password123', 'newPassword': 'newpassword123'},
            content_type='application/json',
            **self.auth_header(),
        )
        self.assertEqual(resp.status_code, 200)
        # login with new password
        resp2 = self.client.post(
            '/api/v1/auth/login',
            {'usernameOrEmail': 'testuser', 'password': 'newpassword123'},
            content_type='application/json',
        )
        self.assertEqual(resp2.status_code, 200)

    def test_change_password_wrong_old(self):
        resp = self.client.post(
            '/api/v1/auth/change-password',
            {'oldPassword': 'wrongpassword', 'newPassword': 'newpassword123'},
            content_type='application/json',
            **self.auth_header(),
        )
        self.assertEqual(resp.status_code, 400)

    def test_reset_password_with_token(self):
        self.client.post(
            '/api/v1/auth/forgot-password',
            {'email': 'test@test.com'},
            content_type='application/json',
        )
        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.reset_token)

        resp = self.client.post(
            '/api/v1/auth/reset-password',
            {'password': 'resetpass123', 'token': self.user.reset_token},
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 200)

        resp2 = self.client.post(
            '/api/v1/auth/login',
            {'usernameOrEmail': 'testuser', 'password': 'resetpass123'},
            content_type='application/json',
        )
        self.assertEqual(resp2.status_code, 200)

    def test_forgot_password(self):
        resp = self.client.post(
            '/api/v1/auth/forgot-password',
            {'usernameOrEmail': 'test@test.com'},
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 200)

    def test_forgot_password_nonexistent(self):
        resp = self.client.post(
            '/api/v1/auth/forgot-password',
            {'usernameOrEmail': 'nobody@test.com'},
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 401)
