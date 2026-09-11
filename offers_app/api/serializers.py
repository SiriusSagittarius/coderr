from django.db import transaction
from rest_framework import serializers
from rest_framework.reverse import reverse

from offers_app.models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    """Serializes a single pricing tier of an offer."""

    class Meta:
        model = OfferDetail
        exclude = ["offer"]


class OfferDetailLinkSerializer(serializers.ModelSerializer):
    """Compact {id, url} representation used inside the offer list/detail."""

    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ["id", "url"]

    def get_url(self, obj):
        """Return the url for the serialized object."""
        request = self.context.get("request")
        return reverse("offerdetail-detail", args=[obj.id], request=request)


class UserDetailsSerializer(serializers.Serializer):
    """Minimal creator info embedded in the offer list response."""

    first_name = serializers.CharField(source="user.first_name", default="")
    last_name = serializers.CharField(source="user.last_name", default="")
    username = serializers.CharField(source="user.username")


class OfferListSerializer(serializers.ModelSerializer):
    """Read-only representation used for list/retrieve, including aggregates."""

    details = OfferDetailLinkSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            "id", "user", "title", "image", "description", "created_at",
            "updated_at", "details", "min_price", "min_delivery_time", "user_details",
        ]

    def get_min_price(self, obj):
        """Return the min price for the serialized object."""
        return obj.details.order_by("price").values_list("price", flat=True).first()

    def get_min_delivery_time(self, obj):
        """Return the min delivery time for the serialized object."""
        days = obj.details.order_by("delivery_time_in_days")
        return days.values_list("delivery_time_in_days", flat=True).first()

    def get_user_details(self, obj):
        """Return the user details for the serialized object."""
        user = obj.user
        return {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
        }


class OfferWriteSerializer(serializers.ModelSerializer):
    """Validates and persists an offer together with its 3 pricing details."""

    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ["id", "title", "image", "description", "details"]

    def validate_details(self, value):
        # On update (PATCH) a partial set of details is allowed; each one must
        # still carry an offer_type so we know which tier to update.
        """Validate the 'details' field."""
        if self.instance is not None:
            for item in value:
                if "offer_type" not in item:
                    raise serializers.ValidationError(
                        "Each detail must include an 'offer_type'."
                    )
            return value
        offer_types = {item.get("offer_type") for item in value}
        if len(value) != 3 or offer_types != {"basic", "standard", "premium"}:
            raise serializers.ValidationError(
                "An offer requires exactly one basic, standard and premium detail."
            )
        return value

    def create(self, validated_data):
        """Create and return a new instance from the validated data."""
        details = validated_data.pop("details")
        with transaction.atomic():
            offer = Offer.objects.create(user=self.context["request"].user, **validated_data)
            new_details = [OfferDetail(offer=offer, **detail) for detail in details]
            OfferDetail.objects.bulk_create(new_details)
        return offer

    def update(self, instance, validated_data):
        """Apply the validated data to the existing instance and return it."""
        details = validated_data.pop("details", None)
        with transaction.atomic():
            instance = super().update(instance, validated_data)
            self._update_details(instance, details)
        return instance

    def _update_details(self, instance, details):
        """Helper: update details."""
        if details is None:
            return
        for detail_data in details:
            detail_type = detail_data.pop("offer_type")
            OfferDetail.objects.update_or_create(
                offer=instance, offer_type=detail_type, defaults=detail_data,
            )

    def to_representation(self, instance):
        """POST/PATCH return the full detail objects (id, title, price, ...),
        unlike the list/retrieve view which only embeds {id, url} links."""
        data = {
            "id": instance.id,
            "title": instance.title,
            "image": instance.image.url if instance.image else None,
            "description": instance.description,
            "details": OfferDetailSerializer(
                instance.details.all(), many=True, context=self.context,
            ).data,
        }
        return data
