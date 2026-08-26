# 2. Third-party
from rest_framework import serializers

# 3. Local
from profile_app.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """Serializes a profile together with read-only fields from the related user.

    Text fields must never be null in the response; blank=True on the model
    combined with allow_blank here guarantees an empty string instead of null.
    """

    user = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    type = serializers.CharField(source="user.type", read_only=True)
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = Profile
        fields = [
            "user", "username", "first_name", "last_name", "file", "location",
            "tel", "description", "working_hours", "type", "email", "created_at",
        ]
        read_only_fields = ["created_at"]

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        self._update_user_email(instance, user_data)
        return super().update(instance, validated_data)

    def _update_user_email(self, instance, user_data):
        if "email" in user_data:
            instance.user.email = user_data["email"]
            instance.user.save(update_fields=["email"])


class BusinessProfileSerializer(serializers.ModelSerializer):
    """Read-only list representation of a business profile."""

    user = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    type = serializers.CharField(source="user.type", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "user", "username", "first_name", "last_name", "file",
            "location", "tel", "description", "working_hours", "type",
        ]


class CustomerProfileSerializer(serializers.ModelSerializer):
    """Read-only list representation of a customer profile."""

    user = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    type = serializers.CharField(source="user.type", read_only=True)

    class Meta:
        model = Profile
        fields = ["user", "username", "first_name", "last_name", "file", "created_at", "type"]
