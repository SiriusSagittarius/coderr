"""Project-wide DRF field overrides."""
# 2. Third-party
from django.utils import timezone
from rest_framework import serializers


class LocalDateTimeField(serializers.DateTimeField):
    """Serialises datetimes as local-time ISO-8601 with a real UTC offset.

    The API contract expects timestamps like ``2026-09-10T12:02:00.260003+02:00``
    (with a ``T`` separator, microseconds and a numeric offset, not a ``Z``).
    DRF's default renders UTC with a ``Z``, so we convert to the active timezone
    and emit ``datetime.isoformat()``.
    """

    def to_representation(self, value):
        if value is None:
            return None
        if timezone.is_aware(value):
            value = timezone.localtime(value)
        return value.isoformat()
