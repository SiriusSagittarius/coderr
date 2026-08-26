# 2. Third-party
from rest_framework import generics, permissions

# 3. Local
from reviews_app.models import Review

from .permissions import IsCustomer, IsReviewOwner
from .serializers import ReviewSerializer, ReviewUpdateSerializer


class ReviewListCreateView(generics.ListCreateAPIView):
    """Lists reviews (filterable/orderable) or creates a new one."""

    serializer_class = ReviewSerializer

    def get_queryset(self):
        queryset = Review.objects.all()
        queryset = self._filter_by_query_params(queryset)
        ordering = self.request.query_params.get("ordering")
        return queryset.order_by(ordering if ordering in ("rating", "updated_at") else "-updated_at")

    def _filter_by_query_params(self, queryset):
        params = self.request.query_params
        if params.get("business_user_id"):
            queryset = queryset.filter(business_user_id=params["business_user_id"])
        if params.get("reviewer_id"):
            queryset = queryset.filter(reviewer_id=params["reviewer_id"])
        return queryset

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsCustomer()]
        return [permissions.IsAuthenticated()]


class ReviewUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieves, updates or deletes a single review (owner only for writes)."""

    queryset = Review.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsReviewOwner]

    def get_serializer_class(self):
        return ReviewUpdateSerializer if self.request.method == "PATCH" else ReviewSerializer
