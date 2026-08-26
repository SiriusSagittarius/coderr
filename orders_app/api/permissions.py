from rest_framework.permissions import BasePermission


class IsCustomer(BasePermission):
    """Only customer users may create orders."""

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.type == "customer")


class IsBusinessOwner(BasePermission):
    """Only the business user attached to the order may update its status."""

    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_authenticated and obj.business_user == request.user)
