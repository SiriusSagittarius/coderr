# 2. Third-party
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# 3. Local
from auth_app.models import User
from offers_app.models import Offer, OfferDetail
from orders_app.models import Order


class OrderUpdateDeleteTests(APITestCase):
    """Tests for PATCH/DELETE /api/orders/{id}/."""

    def setUp(self):
        self.business = User.objects.create_user(username="biz", password="pw12345", type=User.BUSINESS)
        self.other_business = User.objects.create_user(username="biz2", password="pw12345", type=User.BUSINESS)
        self.customer = User.objects.create_user(username="cust", password="pw12345", type=User.CUSTOMER)
        self.staff = User.objects.create_user(username="admin", password="pw12345", is_staff=True)
        offer = Offer.objects.create(user=self.business, title="Logo Design", description="desc")
        detail = OfferDetail.objects.create(
            offer=offer, title="basic", revisions=3, delivery_time_in_days=5,
            price=150, features=[], offer_type="basic",
        )
        self.order = Order.objects.create(
            customer_user=self.customer, business_user=self.business, offer_detail=detail,
            title="basic", revisions=3, delivery_time_in_days=5, price=150, features=[], offer_type="basic",
        )
        self.url = reverse("order-detail", args=[self.order.id])

    def _auth_as(self, user):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + Token.objects.create(user=user).key)

    def test_patch_status_as_business_owner_succeeds(self):
        self._auth_as(self.business)
        response = self.client.patch(self.url, {"status": "completed"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "completed")

    def test_patch_status_as_other_business_returns_403(self):
        self._auth_as(self.other_business)
        response = self.client.patch(self.url, {"status": "completed"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_extra_field_returns_400(self):
        self._auth_as(self.business)
        response = self.client.patch(self.url, {"status": "completed", "price": 1})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_unauthenticated_returns_401(self):
        response = self.client.patch(self.url, {"status": "completed"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_as_staff_returns_204(self):
        self._auth_as(self.staff)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_as_non_staff_returns_403(self):
        self._auth_as(self.business)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_unknown_order_returns_404(self):
        self._auth_as(self.business)
        response = self.client.patch(reverse("order-detail", args=[9999]), {"status": "completed"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
