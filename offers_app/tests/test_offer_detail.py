from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.test_utils import (
    auth_header, make_business, make_offer, make_offer_detail, make_offer_with_tiers,
)
from offers_app.models import Offer


class OfferDetailTests(APITestCase):
    """Tests for GET/PATCH/DELETE /api/offers/{id}/."""

    def setUp(self):
        """Set up the objects shared by the tests in this case."""
        self.owner = make_business(username="owner")
        self.other_business = make_business(username="other")
        self.offer = make_offer_with_tiers(self.owner)
        self._auth_as(self.owner)
        self.url = reverse("offer-detail", args=[self.offer.id])

    def _auth_as(self, user):
        """Authenticate the test client as the given user."""
        self.client.credentials(HTTP_AUTHORIZATION=auth_header(user))

    def test_retrieve_offer_returns_full_data(self):
        """Retrieve offer returns full data."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Logo Design")

    def test_retrieve_unknown_offer_returns_404(self):
        """Retrieve unknown offer returns 404."""
        response = self.client.get(reverse("offer-detail", args=[9999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_offer_as_owner_updates_title(self):
        """Patch offer as owner updates title."""
        response = self.client.patch(self.url, {"title": "Updated title"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated title")

    def test_patch_single_detail_by_offer_type(self):
        """Patch single detail by offer type."""
        payload = {"details": [{"offer_type": "basic", "price": 120}]}
        response = self.client.patch(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        basic = self.offer.details.get(offer_type="basic")
        self.assertEqual(str(basic.price), "120.00")

    def test_patch_offer_as_non_owner_returns_403(self):
        """Patch offer as non owner returns 403."""
        self._auth_as(self.other_business)
        response = self.client.patch(self.url, {"title": "Hacked"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_offer_as_owner_returns_204(self):
        """Delete offer as owner returns 204."""
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Offer.objects.filter(id=self.offer.id).exists())

    def test_delete_offer_as_non_owner_returns_403(self):
        """Delete offer as non owner returns 403."""
        self._auth_as(self.other_business)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_offer_as_non_owner_is_allowed(self):
        """Retrieve offer as non owner is allowed."""
        self._auth_as(self.other_business)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OfferDetailRetrieveTests(APITestCase):
    """Tests for GET /api/offerdetails/{id}/."""

    def setUp(self):
        """Set up the objects shared by the tests in this case."""
        user = make_business(username="owner")
        self.detail = make_offer_detail(
            make_offer(user), price=100, revisions=2, features=["Logo"],
        )
        self.client.credentials(HTTP_AUTHORIZATION=auth_header(user))

    def test_retrieve_offer_detail_returns_data(self):
        """Retrieve offer detail returns data."""
        response = self.client.get(reverse("offerdetail-detail", args=[self.detail.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["offer_type"], "basic")

    def test_retrieve_unauthenticated_returns_401(self):
        """Retrieve unauthenticated returns 401."""
        self.client.credentials()
        response = self.client.get(reverse("offerdetail-detail", args=[self.detail.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
