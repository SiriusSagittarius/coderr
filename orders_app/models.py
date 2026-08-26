# 2. Third-party
from django.conf import settings
from django.db import models


class Order(models.Model):
    """A snapshot of an offer detail, created when a customer books it."""

    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    STATUSES = [(IN_PROGRESS, "In progress"), (COMPLETED, "Completed"), (CANCELLED, "Cancelled")]

    customer_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="customer_orders",
    )
    business_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="business_orders",
    )
    offer_detail = models.ForeignKey(
        "offers_app.OfferDetail", on_delete=models.PROTECT, related_name="orders",
    )
    title = models.CharField(max_length=255)
    revisions = models.PositiveIntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=10)
    status = models.CharField(max_length=20, choices=STATUSES, default=IN_PROGRESS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id} - {self.title}"
