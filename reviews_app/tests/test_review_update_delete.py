# 2. Third-party
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# 3. Local
from auth_app.models import User
from reviews_app.models import Review


class ReviewUpdateDeleteTests(APITestCase):
    """Tests for PATCH/DELETE /api/reviews/{id}/."""

    def setUp(self):
        self.business = User.objects.create_user(
            username="biz", password="pw12345", type=User.BUSINESS,
        )
        self.reviewer = User.objects.create_user(
            username="cust", password="pw12345", type=User.CUSTOMER,
        )
        self.other_customer = User.objects.create_user(
            username="cust2", password="pw12345", type=User.CUSTOMER,
        )
        self.review = Review.objects.create(
            business_user=self.business, reviewer=self.reviewer, rating=3, description="Ok",
        )
        self.url = reverse("review-detail", args=[self.review.id])
        self._auth_as(self.reviewer)

    def _auth_as(self, user):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + Token.objects.create(user=user).key)

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
