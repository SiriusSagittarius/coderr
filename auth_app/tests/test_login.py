from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from auth_app.models import User


class LoginTests(APITestCase):
    """Tests for POST /api/login/."""

    def setUp(self):
        """Set up the objects shared by the tests in this case."""
        self.url = reverse("login")
        self.user = User.objects.create_user(
            username="max", password="secret123", email="max@mail.de",
        )

    def test_login_success_returns_token_and_user_data(self):
        """Login success returns token and user data."""
        response = self.client.post(self.url, {"username": "max", "password": "secret123"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["user_id"], self.user.id)

    def test_login_wrong_password_returns_400(self):
        """Login wrong password returns 400."""
        response = self.client.post(self.url, {"username": "max", "password": "wrong"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_unknown_username_returns_400(self):
        """Login unknown username returns 400."""
        response = self.client.post(self.url, {"username": "ghost", "password": "secret123"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_missing_field_returns_400(self):
        """Login missing field returns 400."""
        response = self.client.post(self.url, {"username": "max"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_ignores_invalid_leftover_token(self):
        """Login ignores invalid leftover token."""
        self.client.credentials(HTTP_AUTHORIZATION="Token this-token-does-not-exist")
        response = self.client.post(self.url, {"username": "max", "password": "secret123"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
