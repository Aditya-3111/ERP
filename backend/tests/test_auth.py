"""Login, token refresh, logout."""

from tests.base import BaseAPITest


class AuthTests(BaseAPITest):
    def test_bad_password_rejected(self):
        self.client.credentials()
        r = self.client.post('/api/auth/login/', {'username': 'tester', 'password': 'nope'}, format='json')
        self.assertEqual(r.status_code, 401)

    def test_refresh_token_endpoint_exists_and_rotates(self):
        self.client.credentials()
        r = self.client.post('/api/auth/refresh/', {'refresh': self.refresh}, format='json')
        self.assertEqual(r.status_code, 200, r.content)
        self.assertIn('access', r.json())
        self.assertIn('refresh', r.json())  # ROTATE_REFRESH_TOKENS=True -> new refresh token
        # the old refresh token is blacklisted after rotation
        again = self.client.post('/api/auth/refresh/', {'refresh': self.refresh}, format='json')
        self.assertEqual(again.status_code, 401)

    def test_logout_blacklists_refresh_token(self):
        r = self.client.post('/api/auth/logout/', {'refresh': self.refresh}, format='json')
        self.assertEqual(r.status_code, 200)
        self.client.credentials()
        again = self.client.post('/api/auth/refresh/', {'refresh': self.refresh}, format='json')
        self.assertEqual(again.status_code, 401)

    def test_api_requires_login(self):
        self.client.credentials()
        self.assertEqual(self.client.get('/api/finance/ledgers/').status_code, 401)
