# 2. Third-party
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

# 3. Local
from .serializers import LoginSerializer, RegistrationSerializer


def build_auth_response(user, status_code=status.HTTP_200_OK):
    """Return the token + basic user info shared by registration and login."""
    token, _ = Token.objects.get_or_create(user=user)
    data = {"token": token.key, "username": user.username, "email": user.email, "user_id": user.id}
    return Response(data, status=status_code)


class RegistrationView(APIView):
    """Creates a new customer or business user and returns an auth token."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return build_auth_response(user, status.HTTP_201_CREATED)


class LoginView(APIView):
    """Authenticates a user and returns an auth token."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return build_auth_response(serializer.validated_data["user"])
