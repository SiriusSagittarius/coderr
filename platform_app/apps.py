from django.apps import AppConfig


class PlatformAppConfig(AppConfig):
    """Configuration for the platform app (cross-cutting, aggregating endpoints)."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "platform_app"
    verbose_name = "Platform"
