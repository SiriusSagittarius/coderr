from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from auth_app.models import User


class ProfileDetailTests(APITestCase):
    """Tests for GET/PATCH /api/profile/{pk}/."""

    def setUp(self):
        """Set up the objects shared by the tests in this case."""
        self.owner = User.objects.create_user(
            username="owner", password="pw12345", type=User.BUSINESS,
        )
        self.other = User.objects.create_user(
            username="other", password="pw12345", type=User.CUSTOMER,
        )
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + Token.objects.create(user=self.owner).key,
        )

    def test_retrieve_own_profile_returns_empty_strings_not_null(self):
        """Retrieve own profile returns empty strings not null."""
        response = self.client.get(reverse("profile-detail", args=[self.owner.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        text_fields = (
            "first_name", "last_name", "location", "tel", "description", "working_hours",
        )
        for field in text_fields:
            self.assertEqual(response.data[field], "")

    def test_retrieve_unauthenticated_returns_401(self):
        """Retrieve unauthenticated returns 401."""
        self.client.credentials()
        response = self.client.get(reverse("profile-detail", args=[self.owner.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_unknown_user_returns_404(self):
        """Retrieve unknown user returns 404."""
        response = self.client.get(reverse("profile-detail", args=[9999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_own_profile_updates_fields(self):
        """Patch own profile updates fields."""
        url = reverse("profile-detail", args=[self.owner.id])
        response = self.client.patch(url, {"location": "Berlin"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["location"], "Berlin")

    def test_patch_other_users_profile_returns_403(self):
        """Patch other users profile returns 403."""
        url = reverse("profile-detail", args=[self.other.id])
        response = self.client.patch(url, {"location": "Berlin"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_own_email_updates_user_record(self):
        """Patch own email updates user record."""
        url = reverse("profile-detail", args=[self.owner.id])
        response = self.client.patch(url, {"email": "new@mail.de"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.owner.refresh_from_db()
        self.assertEqual(self.owner.email, "new@mail.de")
