# 2. Third-party
from django.urls import path

# 3. Local
from .views import CompletedOrderCountView, OrderCountView, OrderListCreateView, OrderUpdateDeleteView

urlpatterns = [
    path("orders/", OrderListCreateView.as_view(), name="order-list"),
    path("orders/<int:pk>/", OrderUpdateDeleteView.as_view(), name="order-detail"),
    path("order-count/<int:business_user_id>/", OrderCountView.as_view(), name="order-count"),
    path("completed-order-count/<int:business_user_id>/", CompletedOrderCountView.as_view(), name="completed-order-count"),
]
