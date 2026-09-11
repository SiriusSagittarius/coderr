from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from auth_app.models import User


class RegistrationTests(APITestCase):
    """Tests for POST /api/registration/."""

    def setUp(self):
        """Set up the objects shared by the tests in this case."""
        self.url = reverse("registration")
        self.payload = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "customer",
        }

    def test_registration_success_returns_token_and_user_data(self):
        """Registration success returns token and user data."""
        response = self.client.post(self.url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["username"], "exampleUsername")
        self.assertEqual(response.data["email"], "example@mail.de")
        self.assertTrue(User.objects.filter(username="exampleUsername").exists())

    def test_registration_business_type_is_persisted(self):
        """Registration business type is persisted."""
        self.payload["type"] = "business"
        response = self.client.post(self.url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username="exampleUsername")
        self.assertEqual(user.type, User.BUSINESS)

    def test_registration_password_mismatch_returns_400(self):
        """Registration password mismatch returns 400."""
        self.payload["repeated_password"] = "somethingElse"
        response = self.client.post(self.url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("repeated_password", response.data)

    def test_registration_duplicate_username_returns_400(self):
        """Registration duplicate username returns 400."""
        self.client.post(self.url, self.payload)
        response = self.client.post(self.url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_missing_field_returns_400(self):
        """Registration missing field returns 400."""
        del self.payload["password"]
        response = self.client.post(self.url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_ignores_invalid_leftover_token(self):
        """Registration ignores invalid leftover token."""
        self.client.credentials(HTTP_AUTHORIZATION="Token this-token-does-not-exist")
        response = self.client.post(self.url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
