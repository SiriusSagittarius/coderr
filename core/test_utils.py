# 1. Standard library
# (none)

# 2. Third-party
from rest_framework.authtoken.models import Token

# 3. Local
from auth_app.models import User
from offers_app.models import Offer, OfferDetail
from orders_app.models import Order
from reviews_app.models import Review


def make_business(username="biz", **kwargs):
    """Create a business-type user for tests."""
    return User.objects.create_user(username=username, password="pw12345", type=User.BUSINESS, **kwargs)


def make_customer(username="cust", **kwargs):
    """Create a customer-type user for tests."""
    return User.objects.create_user(username=username, password="pw12345", type=User.CUSTOMER, **kwargs)


def make_offer(user, title="Logo Design", description="desc"):
    """Create a bare Offer (no details) owned by the given user."""
    return Offer.objects.create(user=user, title=title, description=description)


def make_offer_detail(offer, offer_type="basic", price=150, days=5, revisions=3, features=None):
    """Create a single OfferDetail tier for the given offer."""
    return OfferDetail.objects.create(
        offer=offer, title=offer_type, revisions=revisions, delivery_time_in_days=days,
        price=price, features=features or [], offer_type=offer_type,
    )


def make_offer_with_tiers(user, title="Logo Design", description="desc"):
    """Create an Offer plus its basic/standard/premium OfferDetails."""
    offer = make_offer(user, title=title, description=description)
    tiers = (("basic", 100, 5), ("standard", 200, 7), ("premium", 500, 10))
    for offer_type, price, days in tiers:
        make_offer_detail(offer, offer_type=offer_type, price=price, days=days, revisions=2)
    return offer


def make_order(customer, business, detail, status=Order.IN_PROGRESS):
    """Create an Order snapshotting the given OfferDetail."""
    return Order.objects.create(
        customer_user=customer, business_user=business, offer_detail=detail,
        title=detail.title, revisions=detail.revisions,
        delivery_time_in_days=detail.delivery_time_in_days, price=detail.price,
        features=detail.features, offer_type=detail.offer_type, status=status,
    )


def make_review(business, reviewer, rating=3, description="Ok"):
    """Create a Review from reviewer for business."""
    return Review.objects.create(
        business_user=business, reviewer=reviewer, rating=rating, description=description,
    )


def auth_header(user):
    """Return an Authorization header value with a fresh token for user."""
    return "Token " + Token.objects.create(user=user).key
