# 2. Third-party
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# 3. Local
from auth_app.models import User


class LoginTests(APITestCase):
    """Tests for POST /api/login/."""

    def setUp(self):
        self.url = reverse("login")
        self.user = User.objects.create_user(username="max", password="secret123", email="max@mail.de")

    def test_login_success_returns_token_and_user_data(self):
        response = self.client.post(self.url, {"username": "max", "password": "secret123"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["user_id"], self.user.id)

    def test_login_wrong_password_returns_400(self):
        response = self.client.post(self.url, {"username": "max", "password": "wrong"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_unknown_username_returns_400(self):
        response = self.client.post(self.url, {"username": "ghost", "password": "secret123"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_missing_field_returns_400(self):
        response = self.client.post(self.url, {"username": "max"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
