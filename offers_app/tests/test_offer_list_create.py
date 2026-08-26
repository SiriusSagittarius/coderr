# 2. Third-party
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# 3. Local
from auth_app.models import User
from offers_app.models import Offer, OfferDetail


def detail_payload(offer_type, price, days):
    return {
        "title": f"{offer_type} design", "revisions": 2, "delivery_time_in_days": days,
        "price": price, "features": ["Logo"], "offer_type": offer_type,
    }


class OfferListCreateTests(APITestCase):
    """Tests for GET/POST /api/offers/."""

    def setUp(self):
        self.business = User.objects.create_user(
            username="biz", password="pw12345", type=User.BUSINESS,
        )
        self.customer = User.objects.create_user(
            username="cust", password="pw12345", type=User.CUSTOMER,
        )
        self._auth_as(self.business)
        self.url = reverse("offer-list")
        self.payload = {
            "title": "Graphic design package", "description": "Full package", "image": None,
            "details": [
                detail_payload("basic", 100, 5),
                detail_payload("standard", 200, 7),
                detail_payload("premium", 500, 10),
            ],
        }

    def _auth_as(self, user):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + Token.objects.create(user=user).key)

    def test_create_offer_as_business_succeeds(self):
        response = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Offer.objects.count(), 1)
        self.assertEqual(OfferDetail.objects.count(), 3)

    def test_create_offer_as_customer_returns_403(self):
        self._auth_as(self.customer)
        response = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_offer_unauthenticated_returns_401(self):
        self.client.credentials()
        response = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_offer_with_wrong_number_of_details_returns_400(self):
        self.payload["details"] = self.payload["details"][:2]
        response = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_offers_returns_paginated_results_with_aggregates(self):
        self.client.post(self.url, self.payload, format="json")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        offer = response.data["results"][0]
        self.assertEqual(str(offer["min_price"]), "100.00")
        self.assertEqual(offer["min_delivery_time"], 5)
        self.assertEqual(len(offer["details"]), 3)

    def test_list_offers_filter_by_creator_id(self):
        self.client.post(self.url, self.payload, format="json")
        response = self.client.get(self.url, {"creator_id": self.business.id})
        self.assertEqual(response.data["count"], 1)
        response = self.client.get(self.url, {"creator_id": self.customer.id})
        self.assertEqual(response.data["count"], 0)

    def test_list_offers_filter_by_max_delivery_time(self):
        self.client.post(self.url, self.payload, format="json")
        response = self.client.get(self.url, {"max_delivery_time": 5})
        self.assertEqual(response.data["count"], 1)
        response = self.client.get(self.url, {"max_delivery_time": 1})
        self.assertEqual(response.data["count"], 0)

    def test_list_offers_search_by_title(self):
        self.client.post(self.url, self.payload, format="json")
        response = self.client.get(self.url, {"search": "Graphic"})
        self.assertEqual(response.data["count"], 1)
        response = self.client.get(self.url, {"search": "Nonexistent"})
        self.assertEqual(response.data["count"], 0)

    def test_list_offers_ordering_by_updated_at(self):
        self.client.post(self.url, self.payload, format="json")
        response = self.client.get(self.url, {"ordering": "-updated_at"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_offers_page_size(self):
        self.client.post(self.url, self.payload, format="json")
        response = self.client.get(self.url, {"page_size": 1})
        self.assertEqual(len(response.data["results"]), 1)
