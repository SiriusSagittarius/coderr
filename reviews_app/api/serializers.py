from rest_framework import serializers

from reviews_app.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Serializes a review; only rating/description are writable after creation."""

    class Meta:
        model = Review
        fields = [
            "id", "business_user", "reviewer", "rating",
            "description", "created_at", "updated_at",
        ]
        read_only_fields = ["reviewer", "created_at", "updated_at"]

    def validate_rating(self, value):
        """Validate the 'rating' field."""
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate_business_user(self, value):
        """Validate the 'business_user' field."""
        reviewer = self.context["request"].user
        if Review.objects.filter(business_user=value, reviewer=reviewer).exists():
            raise serializers.ValidationError("You have already reviewed this business user.")
        return value

    def create(self, validated_data):
        """Create and return a new instance from the validated data."""
        return Review.objects.create(reviewer=self.context["request"].user, **validated_data)


class ReviewUpdateSerializer(serializers.ModelSerializer):
    """Restricts writes to rating/description, but returns the full review."""

    class Meta:
        model = Review
        fields = ["rating", "description"]

    def validate_rating(self, value):
        """Validate the 'rating' field."""
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def to_representation(self, instance):
        # The contract expects the complete review object in the PATCH response
        # (id, business_user, reviewer, rating, description, created_at, updated_at).
        """Return the serialized output representation of the instance."""
        return ReviewSerializer(instance, context=self.context).data
