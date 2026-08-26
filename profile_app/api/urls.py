# 2. Third-party
from django.urls import path

# 3. Local
from .views import BusinessProfileListView, CustomerProfileListView, ProfileDetailView

urlpatterns = [
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name="profile-detail"),
    path("profiles/business/", BusinessProfileListView.as_view(), name="profile-business-list"),
    path("profiles/customer/", CustomerProfileListView.as_view(), name="profile-customer-list"),
]
