from django.contrib.auth import authenticate
from rest_framework import serializers

from auth_app.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """Validates and creates a new user (customer or business)."""

    repeated_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "repeated_password", "type"]

    def validate(self, attrs):
        """Validate the incoming data across multiple fields."""
        if attrs["password"] != attrs.pop("repeated_password"):
            raise serializers.ValidationError({"repeated_password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        """Create and return a new instance from the validated data."""
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """Authenticates a user by username and password."""

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """Validate the incoming data across multiple fields."""
        user = authenticate(username=attrs["username"], password=attrs["password"])
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        attrs["user"] = user
        return attrs
