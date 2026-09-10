"""Project-wide DRF field overrides."""
# 1. Standard library
from datetime import timezone as dt_timezone

# 2. Third-party
from django.utils import timezone
from rest_framework import serializers


class LocalDateTimeField(serializers.DateTimeField):
    """Serialises datetimes as ISO-8601 UTC with a trailing ``Z``.

    The API contract (verified against the official Postman test runner)
    expects timestamps like ``2026-09-10T13:55:48.148617Z`` — a ``T``
    separator, microseconds and a ``Z`` suffix for UTC, *not* a numeric
    ``+02:00`` offset in local time. DRF's default (with USE_TZ=True and a
    non-UTC TIME_ZONE) renders the active timezone with an offset, so we
    normalise to UTC and emit ``...Z``.
    """

    def to_representation(self, value):
        if value is None:
            return None
        if timezone.is_aware(value):
            value = value.astimezone(dt_timezone.utc)
        return value.isoformat().replace("+00:00", "Z")
