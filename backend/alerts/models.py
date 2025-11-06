from __future__ import annotations

from django.conf import settings
from django.db import models

from inventory.models import Batch, Medicine


class Alert(models.Model):
    class AlertType(models.TextChoices):
        EXPIRY = "expiry", "Expiry"
        LOW_STOCK = "low_stock", "Low Stock"
        SALES = "sales", "Sales"
        AI = "ai", "AI Prediction"

    class AlertStatus(models.TextChoices):
        NEW = "new", "New"
        ACKNOWLEDGED = "acknowledged", "Acknowledged"
        RESOLVED = "resolved", "Resolved"

    title = models.CharField(max_length=255)
    alert_type = models.CharField(max_length=32, choices=AlertType.choices)
    message = models.TextField()
    medicine = models.ForeignKey(Medicine, null=True, blank=True, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, null=True, blank=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=32, choices=AlertStatus.choices, default=AlertStatus.NEW)
    created_at = models.DateTimeField(auto_now_add=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="resolved_alerts"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.alert_type}: {self.title}"