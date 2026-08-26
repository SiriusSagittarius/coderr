# 2. Third-party
from django.db.models import Avg, Count
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

# 3. Local
from auth_app.models import User
from offers_app.models import Offer
from reviews_app.models import Review


class BaseInfoView(APIView):
    """Returns platform-wide statistics: reviews, average rating, businesses, offers."""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        stats = Review.objects.aggregate(review_count=Count("id"), average_rating=Avg("rating"))
        data = {
            "review_count": stats["review_count"],
            "average_rating": round(stats["average_rating"] or 0, 1),
            "business_profile_count": User.objects.filter(type=User.BUSINESS).count(),
            "offer_count": Offer.objects.count(),
        }
        return Response(data)
