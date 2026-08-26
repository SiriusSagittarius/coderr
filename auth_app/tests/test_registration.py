# 2. Third-party
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# 3. Local
from auth_app.models import User


class RegistrationTests(APITestCase):
    """Tests for POST /api/registration/."""

    def setUp(self):
        self.url = reverse("registration")
        self.payload = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "customer",
        }

    def test_registration_success_returns_token_and_user_data(self):
        response = self.client.post(self.url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["username"], "exampleUsername")
        self.assertEqual(response.data["email"], "example@mail.de")
        self.assertTrue(User.objects.filter(username="exampleUsername").exists())

    def test_registration_business_type_is_persisted(self):
        self.payload["type"] = "business"
        response = self.client.post(self.url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username="exampleUsername")
        self.assertEqual(user.type, User.BUSINESS)

    def test_registration_password_mismatch_returns_400(self):
        self.payload["repeated_password"] = "somethingElse"
        response = self.client.post(self.url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("repeated_password", response.data)

    def test_registration_duplicate_username_returns_400(self):
        self.client.post(self.url, self.payload)
        response = self.client.post(self.url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_missing_field_returns_400(self):
        del self.payload["password"]
        response = self.client.post(self.url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
