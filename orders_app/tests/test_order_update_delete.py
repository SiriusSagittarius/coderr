from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from auth_app.models import User
from core.test_utils import (
    auth_header, make_business, make_customer, make_offer, make_offer_detail, make_order,
)


class OrderUpdateDeleteTests(APITestCase):
    """Tests for PATCH/DELETE /api/orders/{id}/."""

    def setUp(self):
        """Set up the objects shared by the tests in this case."""
        self.business = make_business()
        self.other_business = make_business(username="biz2")
        self.customer = make_customer()
        self.staff = User.objects.create_user(username="admin", password="pw12345", is_staff=True)
        detail = make_offer_detail(make_offer(self.business))
        self.order = make_order(self.customer, self.business, detail)
        self.url = reverse("order-detail", args=[self.order.id])

    def _auth_as(self, user):
        """Authenticate the test client as the given user."""
        self.client.credentials(HTTP_AUTHORIZATION=auth_header(user))

    def test_patch_status_as_business_owner_succeeds(self):
        """Patch status as business owner succeeds."""
        self._auth_as(self.business)
        response = self.client.patch(self.url, {"status": "completed"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "completed")

    def test_patch_status_as_other_business_returns_403(self):
        """Patch status as other business returns 403."""
        self._auth_as(self.other_business)
        response = self.client.patch(self.url, {"status": "completed"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_extra_field_returns_400(self):
        """Patch extra field returns 400."""
        self._auth_as(self.business)
        response = self.client.patch(self.url, {"status": "completed", "price": 1})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_unauthenticated_returns_401(self):
        """Patch unauthenticated returns 401."""
        response = self.client.patch(self.url, {"status": "completed"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_as_staff_returns_204(self):
        """Delete as staff returns 204."""
        self._auth_as(self.staff)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_as_non_staff_returns_403(self):
        """Delete as non staff returns 403."""
        self._auth_as(self.business)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_unknown_order_returns_404(self):
        """Patch unknown order returns 404."""
        self._auth_as(self.business)
        response = self.client.patch(reverse("order-detail", args=[9999]), {"status": "completed"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
