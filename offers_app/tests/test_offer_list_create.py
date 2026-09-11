from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.test_utils import auth_header, make_business, make_customer
from offers_app.models import Offer, OfferDetail


def detail_payload(offer_type, price, days):
    """Detail payload."""
    return {
        "title": f"{offer_type} design", "revisions": 2, "delivery_time_in_days": days,
        "price": price, "features": ["Logo"], "offer_type": offer_type,
    }


class OfferListCreateTests(APITestCase):
    """Tests for GET/POST /api/offers/."""

    def setUp(self):
        """Set up the objects shared by the tests in this case."""
        self.business = make_business()
        self.customer = make_customer()
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
        """Authenticate the test client as the given user."""
        self.client.credentials(HTTP_AUTHORIZATION=auth_header(user))

    def test_create_offer_as_business_succeeds(self):
        """Create offer as business succeeds."""
        response = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Offer.objects.count(), 1)
        self.assertEqual(OfferDetail.objects.count(), 3)

    def test_create_offer_as_customer_returns_403(self):
        """Create offer as customer returns 403."""
        self._auth_as(self.customer)
        response = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_offer_unauthenticated_returns_401(self):
        """Create offer unauthenticated returns 401."""
        self.client.credentials()
        response = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_offer_with_wrong_number_of_details_returns_400(self):
        """Create offer with wrong number of details returns 400."""
        self.payload["details"] = self.payload["details"][:2]
        response = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_offers_returns_paginated_results_with_aggregates(self):
        """List offers returns paginated results with aggregates."""
        self.client.post(self.url, self.payload, format="json")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        offer = response.data["results"][0]
        self.assertEqual(str(offer["min_price"]), "100.00")
        self.assertEqual(offer["min_delivery_time"], 5)
        self.assertEqual(len(offer["details"]), 3)

    def test_list_offers_filter_by_creator_id(self):
        """List offers filter by creator id."""
        self.client.post(self.url, self.payload, format="json")
        response = self.client.get(self.url, {"creator_id": self.business.id})
        self.assertEqual(response.data["count"], 1)
        response = self.client.get(self.url, {"creator_id": self.customer.id})
        self.assertEqual(response.data["count"], 0)

    def test_list_offers_filter_by_max_delivery_time(self):
        """List offers filter by max delivery time."""
        self.client.post(self.url, self.payload, format="json")
        response = self.client.get(self.url, {"max_delivery_time": 5})
        self.assertEqual(response.data["count"], 1)
        response = self.client.get(self.url, {"max_delivery_time": 1})
        self.assertEqual(response.data["count"], 0)

    def test_list_offers_search_by_title(self):
        """List offers search by title."""
        self.client.post(self.url, self.payload, format="json")
        response = self.client.get(self.url, {"search": "Graphic"})
        self.assertEqual(response.data["count"], 1)
        response = self.client.get(self.url, {"search": "Nonexistent"})
        self.assertEqual(response.data["count"], 0)

    def test_list_offers_ordering_by_updated_at(self):
        """List offers ordering by updated at."""
        self.client.post(self.url, self.payload, format="json")
        response = self.client.get(self.url, {"ordering": "-updated_at"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_offers_page_size(self):
        """List offers page size."""
        self.client.post(self.url, self.payload, format="json")
        response = self.client.get(self.url, {"page_size": 1})
        self.assertEqual(len(response.data["results"]), 1)
