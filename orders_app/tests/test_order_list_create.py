from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.test_utils import (
    auth_header, make_business, make_customer, make_offer, make_offer_detail,
)
from orders_app.models import Order


class OrderListCreateTests(APITestCase):
    """Tests for GET/POST /api/orders/."""

    def setUp(self):
        """Set up the objects shared by the tests in this case."""
        self.business = make_business()
        self.customer = make_customer()
        self.other_customer = make_customer(username="cust2")
        self.detail = make_offer_detail(make_offer(self.business), features=["Logo Design"])
        self._auth_as(self.customer)
        self.url = reverse("order-list")

    def _auth_as(self, user):
        """Authenticate the test client as the given user."""
        self.client.credentials(HTTP_AUTHORIZATION=auth_header(user))

    def test_create_order_as_customer_succeeds(self):
        """Create order as customer succeeds."""
        response = self.client.post(self.url, {"offer_detail_id": self.detail.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["business_user"], self.business.id)
        self.assertEqual(response.data["status"], Order.IN_PROGRESS)

    def test_create_order_as_business_returns_403(self):
        """Create order as business returns 403."""
        self._auth_as(self.business)
        response = self.client.post(self.url, {"offer_detail_id": self.detail.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_order_unauthenticated_returns_401(self):
        """Create order unauthenticated returns 401."""
        self.client.credentials()
        response = self.client.post(self.url, {"offer_detail_id": self.detail.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_order_with_invalid_offer_detail_returns_400(self):
        """Create order with invalid offer detail returns 400."""
        response = self.client.post(self.url, {"offer_detail_id": 9999})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_orders_only_returns_own_orders(self):
        """List orders only returns own orders."""
        self.client.post(self.url, {"offer_detail_id": self.detail.id})
        self._auth_as(self.other_customer)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_orders_includes_orders_as_business(self):
        """List orders includes orders as business."""
        self.client.post(self.url, {"offer_detail_id": self.detail.id})
        self._auth_as(self.business)
        response = self.client.get(self.url)
        self.assertEqual(len(response.data), 1)
