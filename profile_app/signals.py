# 2. Third-party
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# 3. Local
from .models import Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    """Automatically create an empty profile whenever a new user registers."""
    if created:
        Profile.objects.create(user=instance)
