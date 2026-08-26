# 2. Third-party
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# 3. Local
from auth_app.models import User


class ProfileDetailTests(APITestCase):
    """Tests for GET/PATCH /api/profile/{pk}/."""

    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="pw12345", type=User.BUSINESS)
        self.other = User.objects.create_user(username="other", password="pw12345", type=User.CUSTOMER)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + Token.objects.create(user=self.owner).key)

    def test_retrieve_own_profile_returns_empty_strings_not_null(self):
        response = self.client.get(reverse("profile-detail", args=[self.owner.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field in ("first_name", "last_name", "location", "tel", "description", "working_hours"):
            self.assertEqual(response.data[field], "")

    def test_retrieve_unauthenticated_returns_401(self):
        self.client.credentials()
        response = self.client.get(reverse("profile-detail", args=[self.owner.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_unknown_user_returns_404(self):
        response = self.client.get(reverse("profile-detail", args=[9999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_own_profile_updates_fields(self):
        response = self.client.patch(reverse("profile-detail", args=[self.owner.id]), {"location": "Berlin"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["location"], "Berlin")

    def test_patch_other_users_profile_returns_403(self):
        response = self.client.patch(reverse("profile-detail", args=[self.other.id]), {"location": "Berlin"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
