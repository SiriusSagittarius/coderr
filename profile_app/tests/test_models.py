# 2. Third-party
from django.test import TestCase

# 3. Local
from auth_app.models import User
from profile_app.models import Profile


class ProfileModelTests(TestCase):
    """Tests for the Profile model."""

    def test_str_returns_owner_username(self):
        user = User.objects.create_user(username="max", password="pw12345")
        profile = Profile.objects.get(user=user)
        self.assertEqual(str(profile), "Profile of max")
