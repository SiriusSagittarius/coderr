# 2. Third-party
from django.test import TestCase

# 3. Local
from auth_app.models import User
from offers_app.models import Offer, OfferDetail
from orders_app.models import Order


class OrderModelTests(TestCase):
    """Tests for the Order model."""

    def test_str_returns_id_and_title(self):
        business = User.objects.create_user(
            username="biz", password="pw12345", type=User.BUSINESS,
        )
        customer = User.objects.create_user(
            username="cust", password="pw12345", type=User.CUSTOMER,
        )
        offer = Offer.objects.create(user=business, title="Logo Design", description="desc")
        detail = OfferDetail.objects.create(
            offer=offer, title="basic", revisions=2, delivery_time_in_days=5,
            price=100, features=[], offer_type="basic",
        )
        order = Order.objects.create(
            customer_user=customer, business_user=business, offer_detail=detail,
            title="basic", revisions=2, delivery_time_in_days=5, price=100,
            features=[], offer_type="basic",
        )
        self.assertEqual(str(order), f"Order #{order.id} - basic")
