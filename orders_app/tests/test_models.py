# 2. Third-party
from django.test import TestCase

# 3. Local
from core.test_utils import make_customer, make_offer, make_offer_detail, make_order


class OrderModelTests(TestCase):
    """Tests for the Order model."""

    def test_str_returns_id_and_title(self):
        business = make_offer(make_customer(username="biz")).user
        customer = make_customer()
        detail = make_offer_detail(make_offer(business), price=100, revisions=2)
        order = make_order(customer, business, detail)
        self.assertEqual(str(order), f"Order #{order.id} - basic")
