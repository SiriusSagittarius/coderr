# 2. Third-party
from django.urls import path

# 3. Local
from .views import ReviewListCreateView, ReviewUpdateDeleteView

urlpatterns = [
    path("reviews/", ReviewListCreateView.as_view(), name="review-list"),
    path("reviews/<int:pk>/", ReviewUpdateDeleteView.as_view(), name="review-detail"),
]
