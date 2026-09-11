from rest_framework.permissions import BasePermission


class IsCustomer(BasePermission):
    """Only customer users may create reviews."""

    def has_permission(self, request, view):
        """Return whether the request is allowed at the view level."""
        return bool(request.user.is_authenticated and request.user.type == "customer")


class IsReviewOwner(BasePermission):
    """Only the reviewer who wrote a review may update or delete it."""

    def has_object_permission(self, request, view, obj):
        """Return whether the request is allowed on this object."""
        return bool(obj.reviewer == request.user)
