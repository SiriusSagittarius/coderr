# 2. Third-party
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# 3. Local
from auth_app.models import User
from offers_app.models import Offer, OfferDetail
from orders_app.models import Order


class OrderListCreateTests(APITestCase):
    """Tests for GET/POST /api/orders/."""

    def setUp(self):
        self.business = User.objects.create_user(
            username="biz", password="pw12345", type=User.BUSINESS,
        )
        self.customer = User.objects.create_user(
            username="cust", password="pw12345", type=User.CUSTOMER,
        )
        self.other_customer = User.objects.create_user(
            username="cust2", password="pw12345", type=User.CUSTOMER,
        )
        offer = Offer.objects.create(user=self.business, title="Logo Design", description="desc")
        self.detail = OfferDetail.objects.create(
            offer=offer, title="basic", revisions=3, delivery_time_in_days=5,
            price=150, features=["Logo Design"], offer_type="basic",
        )
        self._auth_as(self.customer)
        self.url = reverse("order-list")

    def _auth_as(self, user):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + Token.objects.create(user=user).key)

    def test_create_order_as_customer_succeeds(self):
        response = self.client.post(self.url, {"offer_detail_id": self.detail.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["business_user"], self.business.id)
        self.assertEqual(response.data["status"], Order.IN_PROGRESS)

    def test_create_order_as_business_returns_403(self):
        self._auth_as(self.business)
        response = self.client.post(self.url, {"offer_detail_id": self.detail.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_order_unauthenticated_returns_401(self):
        self.client.credentials()
        response = self.client.post(self.url, {"offer_detail_id": self.detail.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_order_with_invalid_offer_detail_returns_400(self):
        response = self.client.post(self.url, {"offer_detail_id": 9999})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_orders_only_returns_own_orders(self):
        self.client.post(self.url, {"offer_detail_id": self.detail.id})
        self._auth_as(self.other_customer)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_orders_includes_orders_as_business(self):
        self.client.post(self.url, {"offer_detail_id": self.detail.id})
        self._auth_as(self.business)
        response = self.client.get(self.url)
        self.assertEqual(len(response.data), 1)
