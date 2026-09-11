from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.test_utils import (
    auth_header, make_business, make_customer, make_offer, make_offer_detail, make_order,
)
from orders_app.models import Order


class OrderCountTests(APITestCase):
    """Tests for GET /api/order-count/ and /api/completed-order-count/."""

    def setUp(self):
        """Set up the objects shared by the tests in this case."""
        self.business = make_business()
        self.customer = make_customer()
        detail = make_offer_detail(make_offer(self.business))
        make_order(self.customer, self.business, detail, status=Order.IN_PROGRESS)
        make_order(self.customer, self.business, detail, status=Order.COMPLETED)
        self.client.credentials(HTTP_AUTHORIZATION=auth_header(self.customer))

    def test_order_count_returns_in_progress_count(self):
        """Order count returns in progress count."""
        response = self.client.get(reverse("order-count", args=[self.business.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["order_count"], 1)

    def test_completed_order_count_returns_completed_count(self):
        """Completed order count returns completed count."""
        response = self.client.get(reverse("completed-order-count", args=[self.business.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["completed_order_count"], 1)

    def test_order_count_unknown_business_user_returns_404(self):
        """Order count unknown business user returns 404."""
        response = self.client.get(reverse("order-count", args=[9999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_completed_order_count_unauthenticated_returns_401(self):
        """Completed order count unauthenticated returns 401."""
        self.client.credentials()
        response = self.client.get(reverse("completed-order-count", args=[self.business.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
