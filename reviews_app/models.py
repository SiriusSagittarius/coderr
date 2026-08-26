# 2. Third-party
from django.conf import settings
from django.db import models


class Review(models.Model):
    """A customer's rating and comment about a business user. One per pair."""

    business_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_reviews",
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="written_reviews",
    )
    rating = models.PositiveSmallIntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ["-updated_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["business_user", "reviewer"], name="one_review_per_business",
            ),
        ]

    def __str__(self):
        return f"{self.reviewer.username} -> {self.business_user.username}: {self.rating}"
