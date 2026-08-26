# 2. Third-party
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

# 3. Local
from auth_app.models import User
from orders_app.models import Order

from .permissions import IsBusinessOwner, IsCustomer
from .serializers import OrderCreateSerializer, OrderSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    """Lists the authenticated user's orders, or creates a new one."""

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(Q(customer_user=user) | Q(business_user=user))

    def get_serializer_class(self):
        return OrderCreateSerializer if self.request.method == "POST" else OrderSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsCustomer()]
        return [permissions.IsAuthenticated()]


class OrderUpdateDeleteView(generics.UpdateAPIView, generics.DestroyAPIView):
    """Updates an order's status (business owner) or deletes it (staff only)."""

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticated(), IsBusinessOwner()]

    def partial_update(self, request, *args, **kwargs):
        if set(request.data) != {"status"}:
            return Response({"detail": "Only the status field may be updated."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class OrderCountView(APIView):
    """Returns the number of in-progress orders for a business user."""

    def get(self, request, business_user_id):
        get_object_or_404(User, pk=business_user_id, type=User.BUSINESS)
        count = Order.objects.filter(business_user_id=business_user_id, status=Order.IN_PROGRESS).count()
        return Response({"order_count": count})


class CompletedOrderCountView(APIView):
    """Returns the number of completed orders for a business user."""

    def get(self, request, business_user_id):
        get_object_or_404(User, pk=business_user_id, type=User.BUSINESS)
        count = Order.objects.filter(business_user_id=business_user_id, status=Order.COMPLETED).count()
        return Response({"completed_order_count": count})
