# 2. Third-party
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# 3. Local
from core.test_utils import make_business, make_customer, make_offer, make_review


class BaseInfoTests(APITestCase):
    """Tests for GET /api/base-info/."""

    def setUp(self):
        self.url = reverse("base-info")

    def test_base_info_with_no_data_returns_zeros(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["review_count"], 0)
        self.assertEqual(response.data["average_rating"], 0)

    def test_base_info_aggregates_correctly(self):
        business = make_business()
        customer = make_customer()
        make_offer(business, title="Logo")
        make_review(business, customer, rating=4, description="Good")
        response = self.client.get(self.url)
        self.assertEqual(response.data["review_count"], 1)
        self.assertEqual(response.data["average_rating"], 4.0)
        self.assertEqual(response.data["business_profile_count"], 1)
        self.assertEqual(response.data["offer_count"], 1)

    def test_base_info_does_not_require_authentication(self):
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_base_info_ignores_invalid_leftover_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token this-token-does-not-exist")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
