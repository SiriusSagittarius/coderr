from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsBusiness(BasePermission):
    """Only business users may create offers."""

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.type == "business")


class IsOwnerOrReadOnly(BasePermission):
    """Only the offer's creator may update or delete it."""

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user.is_staff or obj.user == request.user)
