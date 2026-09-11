from django.test import TestCase

from auth_app.models import User
from reviews_app.models import Review


class ReviewModelTests(TestCase):
    """Tests for the Review model."""

    def test_str_returns_reviewer_business_and_rating(self):
        """Str returns reviewer business and rating."""
        business = User.objects.create_user(
            username="biz", password="pw12345", type=User.BUSINESS,
        )
        reviewer = User.objects.create_user(
            username="cust", password="pw12345", type=User.CUSTOMER,
        )
        review = Review.objects.create(
            business_user=business, reviewer=reviewer, rating=4, description="Good",
        )
        self.assertEqual(str(review), "cust -> biz: 4")
