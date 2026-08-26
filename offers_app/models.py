# 2. Third-party
from django.conf import settings
from django.db import models


class Offer(models.Model):
    """A service offer created by a business user, consisting of 3 details."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="offers",
    )
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="offers/", blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Offer"
        verbose_name_plural = "Offers"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class OfferDetail(models.Model):
    """One pricing tier (basic/standard/premium) belonging to an offer."""

    BASIC = "basic"
    STANDARD = "standard"
    PREMIUM = "premium"
    OFFER_TYPES = [(BASIC, "Basic"), (STANDARD, "Standard"), (PREMIUM, "Premium")]

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="details")
    title = models.CharField(max_length=255)
    revisions = models.PositiveIntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=10, choices=OFFER_TYPES)

    class Meta:
        verbose_name = "Offer detail"
        verbose_name_plural = "Offer details"
        ordering = ["price"]

    def __str__(self):
        return f"{self.offer.title} - {self.offer_type}"
