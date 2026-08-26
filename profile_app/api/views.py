# 2. Third-party
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

# 3. Local
from auth_app.models import User
from profile_app.models import Profile

from .permissions import IsProfileOwner
from .serializers import BusinessProfileSerializer, CustomerProfileSerializer, ProfileSerializer


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """Retrieves or partially updates a single user's profile."""

    queryset = Profile.objects.select_related("user")
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated & IsProfileOwner]

    def get_object(self):
        user = get_object_or_404(User, pk=self.kwargs["pk"])
        profile = get_object_or_404(Profile, user=user)
        self.check_object_permissions(self.request, profile)
        return profile


class BusinessProfileListView(generics.ListAPIView):
    """Lists all business profiles on the platform."""

    serializer_class = BusinessProfileSerializer

    def get_queryset(self):
        return Profile.objects.select_related("user").filter(user__type=User.BUSINESS)


class CustomerProfileListView(generics.ListAPIView):
    """Lists all customer profiles on the platform."""

    serializer_class = CustomerProfileSerializer

    def get_queryset(self):
        return Profile.objects.select_related("user").filter(user__type=User.CUSTOMER)
