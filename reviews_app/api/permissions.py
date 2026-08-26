from rest_framework.permissions import BasePermission


class IsCustomer(BasePermission):
    """Only customer users may create reviews."""

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.type == "customer")


class IsReviewOwner(BasePermission):
    """Only the reviewer who wrote a review may update or delete it."""

    def has_object_permission(self, request, view, obj):
        return bool(obj.reviewer == request.user)
