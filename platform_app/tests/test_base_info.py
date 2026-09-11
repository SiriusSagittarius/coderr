from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.test_utils import make_business, make_customer, make_offer, make_review


class BaseInfoTests(APITestCase):
    """Tests for GET /api/base-info/."""

    def setUp(self):
        """Set up the objects shared by the tests in this case."""
        self.url = reverse("base-info")

    def test_base_info_with_no_data_returns_zeros(self):
        """Base info with no data returns zeros."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["review_count"], 0)
        self.assertEqual(response.data["average_rating"], 0)

    def test_base_info_aggregates_correctly(self):
        """Base info aggregates correctly."""
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
        """Base info does not require authentication."""
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_base_info_ignores_invalid_leftover_token(self):
        """Base info ignores invalid leftover token."""
        self.client.credentials(HTTP_AUTHORIZATION="Token this-token-does-not-exist")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
