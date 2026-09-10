# 2. Third-party
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# 3. Local
from core.test_utils import auth_header, make_business, make_customer, make_review
from reviews_app.models import Review


class ReviewUpdateDeleteTests(APITestCase):
    """Tests for PATCH/DELETE /api/reviews/{id}/."""

    def setUp(self):
        self.business = make_business()
        self.reviewer = make_customer()
        self.other_customer = make_customer(username="cust2")
        self.review = make_review(self.business, self.reviewer)
        self.url = reverse("review-detail", args=[self.review.id])
        self._auth_as(self.reviewer)

    def _auth_as(self, user):
        self.client.credentials(HTTP_AUTHORIZATION=auth_header(user))

    def test_patch_own_review_updates_rating_and_description(self):
        response = self.client.patch(self.url, {"rating": 5, "description": "Even better!"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["rating"], 5)

    def test_patch_invalid_rating_returns_400(self):
        response = self.client.patch(self.url, {"rating": 0})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_other_users_review_returns_403(self):
        self._auth_as(self.other_customer)
        response = self.client.patch(self.url, {"rating": 5})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_unauthenticated_returns_401(self):
        self.client.credentials()
        response = self.client.patch(self.url, {"rating": 5})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_own_review_returns_204(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())

    def test_delete_other_users_review_returns_403(self):
        self._auth_as(self.other_customer)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_unknown_review_returns_404(self):
        response = self.client.patch(reverse("review-detail", args=[9999]), {"rating": 5})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
