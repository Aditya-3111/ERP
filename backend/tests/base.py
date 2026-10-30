"""Shared helpers for the API tests."""
from rest_framework.test import APITestCase

from apps.core.models import User


class BaseAPITest(APITestCase):
    """Creates a staff user, logs in through the real login endpoint and sets the token."""

    def setUp(self):
        self.user = User.objects.create_user('tester', password='secret123', is_staff=True, is_superuser=True)
        resp = self.client.post('/api/auth/login/', {'username': 'tester', 'password': 'secret123'}, format='json')
        self.assertEqual(resp.status_code, 200, resp.content)
        self.access, self.refresh = resp.json()['access'], resp.json()['refresh']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access)
