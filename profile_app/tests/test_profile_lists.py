# 2. Third-party
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# 3. Local
from auth_app.models import User


class ProfileListTests(APITestCase):
    """Tests for GET /api/profiles/business/ and /api/profiles/customer/."""

    def setUp(self):
        self.business = User.objects.create_user(
            username="biz", password="pw12345", type=User.BUSINESS,
        )
        self.customer = User.objects.create_user(
            username="cust", password="pw12345", type=User.CUSTOMER,
        )
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + Token.objects.create(user=self.business).key,
        )

    def test_business_list_contains_only_business_profiles(self):
        response = self.client.get(reverse("profile-business-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        usernames = [entry["username"] for entry in response.data]
        self.assertIn("biz", usernames)
        self.assertNotIn("cust", usernames)

    def test_customer_list_contains_only_customer_profiles(self):
        response = self.client.get(reverse("profile-customer-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        usernames = [entry["username"] for entry in response.data]
        self.assertIn("cust", usernames)
        self.assertNotIn("biz", usernames)

    def test_lists_require_authentication(self):
        self.client.credentials()
        response = self.client.get(reverse("profile-business-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
