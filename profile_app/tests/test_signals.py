# 2. Third-party
from django.test import TestCase

# 3. Local
from auth_app.models import User
from profile_app.models import Profile


class ProfileSignalTests(TestCase):
    """Tests the post_save signal that auto-creates a profile for new users."""

    def test_creating_a_user_creates_a_profile(self):
        user = User.objects.create_user(username="newbie", password="pw12345")
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_saving_existing_user_does_not_duplicate_profile(self):
        user = User.objects.create_user(username="newbie", password="pw12345")
        user.email = "changed@mail.de"
        user.save()
        self.assertEqual(Profile.objects.filter(user=user).count(), 1)
