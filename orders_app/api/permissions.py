from rest_framework.permissions import BasePermission


class IsCustomer(BasePermission):
    """Only customer users may create orders."""

    def has_permission(self, request, view):
        """Return whether the request is allowed at the view level."""
        return bool(request.user.is_authenticated and request.user.type == "customer")


class IsBusinessOwner(BasePermission):
    """Only the business user attached to the order may update its status."""

    def has_object_permission(self, request, view, obj):
        """Return whether the request is allowed on this object."""
        return bool(request.user.is_authenticated and obj.business_user == request.user)
