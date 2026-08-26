# 2. Third-party
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# 3. Local
from auth_app.models import User
from offers_app.models import Offer, OfferDetail


class OfferDetailTests(APITestCase):
    """Tests for GET/PATCH/DELETE /api/offers/{id}/."""

    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner", password="pw12345", type=User.BUSINESS,
        )
        self.other_business = User.objects.create_user(
            username="other", password="pw12345", type=User.BUSINESS,
        )
        self.offer = Offer.objects.create(user=self.owner, title="Logo Design", description="desc")
        tiers = (("basic", 100, 5), ("standard", 200, 7), ("premium", 500, 10))
        for offer_type, price, days in tiers:
            OfferDetail.objects.create(
                offer=self.offer, title=offer_type, revisions=2,
                delivery_time_in_days=days, price=price, features=[], offer_type=offer_type,
            )
        self._auth_as(self.owner)
        self.url = reverse("offer-detail", args=[self.offer.id])

    def _auth_as(self, user):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + Token.objects.create(user=user).key)

    def test_retrieve_offer_returns_full_data(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Logo Design")

    def test_retrieve_unknown_offer_returns_404(self):
        response = self.client.get(reverse("offer-detail", args=[9999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_offer_as_owner_updates_title(self):
        response = self.client.patch(self.url, {"title": "Updated title"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated title")

    def test_patch_single_detail_by_offer_type(self):
        payload = {"details": [{"offer_type": "basic", "price": 120}]}
        response = self.client.patch(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        basic = self.offer.details.get(offer_type="basic")
        self.assertEqual(str(basic.price), "120.00")

    def test_patch_offer_as_non_owner_returns_403(self):
        self._auth_as(self.other_business)
        response = self.client.patch(self.url, {"title": "Hacked"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_offer_as_owner_returns_204(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Offer.objects.filter(id=self.offer.id).exists())

    def test_delete_offer_as_non_owner_returns_403(self):
        self._auth_as(self.other_business)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_offer_as_non_owner_is_allowed(self):
        self._auth_as(self.other_business)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OfferDetailRetrieveTests(APITestCase):
    """Tests for GET /api/offerdetails/{id}/."""

    def setUp(self):
        user = User.objects.create_user(username="owner", password="pw12345", type=User.BUSINESS)
        offer = Offer.objects.create(user=user, title="Logo Design", description="desc")
        self.detail = OfferDetail.objects.create(
            offer=offer, title="basic", revisions=2, delivery_time_in_days=5,
            price=100, features=["Logo"], offer_type="basic",
        )
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + Token.objects.create(user=user).key,
        )

    def test_retrieve_offer_detail_returns_data(self):
        response = self.client.get(reverse("offerdetail-detail", args=[self.detail.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["offer_type"], "basic")

    def test_retrieve_unauthenticated_returns_401(self):
        self.client.credentials()
        response = self.client.get(reverse("offerdetail-detail", args=[self.detail.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
