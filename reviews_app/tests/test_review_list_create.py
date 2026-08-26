# 2. Third-party
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# 3. Local
from auth_app.models import User
from reviews_app.models import Review


class ReviewListCreateTests(APITestCase):
    """Tests for GET/POST /api/reviews/."""

    def setUp(self):
        self.business = User.objects.create_user(
            username="biz", password="pw12345", type=User.BUSINESS,
        )
        self.other_business = User.objects.create_user(
            username="biz2", password="pw12345", type=User.BUSINESS,
        )
        self.customer = User.objects.create_user(
            username="cust", password="pw12345", type=User.CUSTOMER,
        )
        self._auth_as(self.customer)
        self.url = reverse("review-list")

    def _auth_as(self, user):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + Token.objects.create(user=user).key)

    def test_create_review_as_customer_succeeds(self):
        payload = {"business_user": self.business.id, "rating": 4, "description": "Great!"}
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["reviewer"], self.customer.id)

    def test_create_review_as_business_returns_403(self):
        self._auth_as(self.business)
        payload = {"business_user": self.other_business.id, "rating": 4, "description": "Great!"}
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_duplicate_review_returns_400(self):
        payload = {"business_user": self.business.id, "rating": 4, "description": "Great!"}
        self.client.post(self.url, payload)
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_review_invalid_rating_returns_400(self):
        payload = {"business_user": self.business.id, "rating": 9, "description": "Great!"}
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_reviews_requires_authentication(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_reviews_filter_by_business_user_id(self):
        Review.objects.create(
            business_user=self.business, reviewer=self.customer, rating=5, description="A",
        )
        response = self.client.get(self.url, {"business_user_id": self.business.id})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.url, {"business_user_id": self.other_business.id})
        self.assertEqual(len(response.data), 0)

    def test_list_reviews_ordering_by_rating(self):
        Review.objects.create(
            business_user=self.business, reviewer=self.customer, rating=2, description="A",
        )
        response = self.client.get(self.url, {"ordering": "rating"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_reviews_filter_by_reviewer_id(self):
        Review.objects.create(
            business_user=self.business, reviewer=self.customer, rating=5, description="A",
        )
        response = self.client.get(self.url, {"reviewer_id": self.customer.id})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.url, {"reviewer_id": self.other_business.id})
        self.assertEqual(len(response.data), 0)
