# 2. Third-party
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# 3. Local
from auth_app.models import User
from offers_app.models import Offer, OfferDetail
from orders_app.models import Order


class OrderCountTests(APITestCase):
    """Tests for GET /api/order-count/ and /api/completed-order-count/."""

    def setUp(self):
        self.business = User.objects.create_user(
            username="biz", password="pw12345", type=User.BUSINESS,
        )
        self.customer = User.objects.create_user(
            username="cust", password="pw12345", type=User.CUSTOMER,
        )
        offer = Offer.objects.create(user=self.business, title="Logo Design", description="desc")
        detail = OfferDetail.objects.create(
            offer=offer, title="basic", revisions=3, delivery_time_in_days=5,
            price=150, features=[], offer_type="basic",
        )
        Order.objects.create(
            customer_user=self.customer, business_user=self.business, offer_detail=detail,
            title="basic", revisions=3, delivery_time_in_days=5, price=150,
            features=[], offer_type="basic", status=Order.IN_PROGRESS,
        )
        Order.objects.create(
            customer_user=self.customer, business_user=self.business, offer_detail=detail,
            title="basic", revisions=3, delivery_time_in_days=5, price=150,
            features=[], offer_type="basic", status=Order.COMPLETED,
        )
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + Token.objects.create(user=self.customer).key,
        )

    def test_order_count_returns_in_progress_count(self):
        response = self.client.get(reverse("order-count", args=[self.business.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["order_count"], 1)

    def test_completed_order_count_returns_completed_count(self):
        response = self.client.get(reverse("completed-order-count", args=[self.business.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["completed_order_count"], 1)

    def test_order_count_unknown_business_user_returns_404(self):
        response = self.client.get(reverse("order-count", args=[9999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_completed_order_count_unauthenticated_returns_401(self):
        self.client.credentials()
        response = self.client.get(reverse("completed-order-count", args=[self.business.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
