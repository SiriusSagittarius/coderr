# 2. Third-party
from django.conf import settings
from django.db import models


class Profile(models.Model):
    """Extended, editable information about a user (customer or business)."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    file = models.ImageField(upload_to="profiles/", blank=True, null=True)
    location = models.CharField(max_length=150, blank=True)
    tel = models.CharField(max_length=40, blank=True)
    description = models.TextField(blank=True)
    working_hours = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        ordering = ["user__username"]

    def __str__(self):
        return f"Profile of {self.user.username}"
