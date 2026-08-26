# 2. Third-party
from rest_framework import serializers

# 3. Local
from offers_app.models import OfferDetail
from orders_app.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """Read representation of an order; only 'status' is writable via PATCH."""

    class Meta:
        model = Order
        fields = [
            "id", "customer_user", "business_user", "title", "revisions",
            "delivery_time_in_days", "price", "features", "offer_type",
            "status", "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "customer_user", "business_user", "title", "revisions",
            "delivery_time_in_days", "price", "features", "offer_type", "created_at", "updated_at",
        ]


class OrderCreateSerializer(serializers.Serializer):
    """Creates an order from an existing offer detail."""

    offer_detail_id = serializers.PrimaryKeyRelatedField(queryset=OfferDetail.objects.all())

    def create(self, validated_data):
        detail = validated_data["offer_detail_id"]
        return Order.objects.create(
            customer_user=self.context["request"].user,
            business_user=detail.offer.user,
            offer_detail=detail,
            title=detail.title,
            revisions=detail.revisions,
            delivery_time_in_days=detail.delivery_time_in_days,
            price=detail.price,
            features=detail.features,
            offer_type=detail.offer_type,
        )

    def to_representation(self, instance):
        return OrderSerializer(instance).data
