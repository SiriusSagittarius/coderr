# 2. Third-party
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

# 3. Local
from offers_app.models import Offer, OfferDetail

from .filters import OfferFilter
from .permissions import IsBusiness, IsOwnerOrReadOnly
from .serializers import OfferDetailSerializer, OfferListSerializer, OfferWriteSerializer


class OfferPagination(PageNumberPagination):
    """Default page size for the offer list, overridable via ?page_size=."""

    page_size = 6
    page_size_query_param = "page_size"


class OfferViewSet(viewsets.ModelViewSet):
    """CRUD endpoint for offers, with filtering/search/ordering on the list."""

    queryset = Offer.objects.select_related("user").prefetch_related("details")
    pagination_class = OfferPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = OfferFilter
    search_fields = ["title", "description"]

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return OfferListSerializer
        return OfferWriteSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsBusiness()]
        if self.request.method in ("PATCH", "PUT", "DELETE"):
            return [permissions.IsAuthenticated(), IsOwnerOrReadOnly()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        queryset = super().get_queryset()
        ordering = self.request.query_params.get("ordering")
        if ordering in ("updated_at", "-updated_at"):
            queryset = queryset.order_by(ordering)
        return queryset.distinct()


class OfferDetailRetrieveView(generics.RetrieveAPIView):
    """Read-only access to a single offer detail (pricing tier)."""

    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
