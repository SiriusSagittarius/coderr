from rest_framework.permissions import BasePermission


class IsBusiness(BasePermission):
    """Only business users may create offers."""

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.type == "business")


class IsOwnerOrStaff(BasePermission):
    """Only the offer's creator (or staff) may update or delete it.

    Only used for write methods (PATCH/PUT/DELETE); read access is granted
    to any authenticated user directly in OfferViewSet.get_permissions.
    """

    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_staff or obj.user == request.user)
