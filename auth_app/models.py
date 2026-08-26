from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model distinguishing customer and business accounts."""

    CUSTOMER = "customer"
    BUSINESS = "business"
    USER_TYPES = [(CUSTOMER, "Customer"), (BUSINESS, "Business")]

    type = models.CharField(max_length=10, choices=USER_TYPES, default=CUSTOMER)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["username"]

    def __str__(self):
        return f"{self.username} ({self.type})"
