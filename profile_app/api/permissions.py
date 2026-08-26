from rest_framework.permissions import BasePermission


class IsProfileOwner(BasePermission):
    """Allows write access only to the profile's own user; read access to anyone authenticated."""

    def has_object_permission(self, request, view, obj):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        return bool(obj.user == request.user)
