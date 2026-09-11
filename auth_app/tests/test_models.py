from django.test import TestCase

from auth_app.models import User


class UserModelTests(TestCase):
    """Tests for the User model."""

    def test_str_returns_username_and_type(self):
        """Str returns username and type."""
        user = User.objects.create_user(username="max", password="pw12345", type=User.BUSINESS)
        self.assertEqual(str(user), "max (business)")
