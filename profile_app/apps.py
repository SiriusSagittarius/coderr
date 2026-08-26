from django.apps import AppConfig


class ProfileAppConfig(AppConfig):
    """Configuration for the profile app. Registers the auto-create signal."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "profile_app"
    verbose_name = "Profiles"

    def ready(self):
        from . import signals  # noqa: F401
