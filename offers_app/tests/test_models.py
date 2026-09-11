from django.test import TestCase

from auth_app.models import User
from offers_app.models import Offer, OfferDetail


class OfferModelTests(TestCase):
    """Tests for the Offer and OfferDetail models."""

    def setUp(self):
        """Set up the objects shared by the tests in this case."""
        self.user = User.objects.create_user(
            username="biz", password="pw12345", type=User.BUSINESS,
        )
        self.offer = Offer.objects.create(user=self.user, title="Logo Design", description="desc")

    def test_offer_str_returns_title(self):
        """Offer str returns title."""
        self.assertEqual(str(self.offer), "Logo Design")

    def test_offer_detail_str_returns_offer_title_and_type(self):
        """Offer detail str returns offer title and type."""
        detail = OfferDetail.objects.create(
            offer=self.offer, title="Basic", revisions=2, delivery_time_in_days=5,
            price=100, features=[], offer_type="basic",
        )
        self.assertEqual(str(detail), "Logo Design - basic")
