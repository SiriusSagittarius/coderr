# 2. Third-party
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# 3. Local
from auth_app.models import User
from offers_app.models import Offer
from reviews_app.models import Review


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
        business = User.objects.create_user(username="biz", password="pw12345", type=User.BUSINESS)
        customer = User.objects.create_user(username="cust", password="pw12345", type=User.CUSTOMER)
        Offer.objects.create(user=business, title="Logo", description="desc")
        Review.objects.create(business_user=business, reviewer=customer, rating=4, description="Good")
        response = self.client.get(self.url)
        self.assertEqual(response.data["review_count"], 1)
        self.assertEqual(response.data["average_rating"], 4.0)
        self.assertEqual(response.data["business_profile_count"], 1)
        self.assertEqual(response.data["offer_count"], 1)

    def test_base_info_does_not_require_authentication(self):
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
