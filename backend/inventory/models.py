from __future__ import annotations

from decimal import Decimal

from django.db import models
from django.utils import timezone


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Medicine(models.Model):
    class Category(models.TextChoices):
        TABLET = "tablet", "Tablet"
        CAPSULE = "capsule", "Capsule"
        SYRUP = "syrup", "Syrup"
        INJECTION = "injection", "Injection"
        OINTMENT = "ointment", "Ointment"
        OTHER = "other", "Other"

    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=50, unique=True)
    barcode = models.CharField(max_length=64, blank=True)
    category = models.CharField(max_length=32, choices=Category.choices, default=Category.OTHER)
    strength = models.CharField(max_length=128, blank=True)
    description = models.TextField(blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    reorder_level = models.PositiveIntegerField(default=0)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, related_name="medicines", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["sku"]),
            models.Index(fields=["barcode"]),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.strength})" if self.strength else self.name

    @property
    def total_stock(self) -> int:
        return sum(batch.quantity for batch in self.batches.all())

    @property
    def near_expiry_batches(self):
        threshold = timezone.now().date() + timezone.timedelta(days=30)
        return self.batches.filter(expiry_date__lte=threshold, quantity__gt=0)


class Batch(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name="batches")
    batch_number = models.CharField(max_length=100)
    expiry_date = models.DateField()
    manufactured_date = models.DateField(null=True, blank=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    quantity = models.PositiveIntegerField(default=0)
    initial_quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["expiry_date"]
        unique_together = ("medicine", "batch_number")

    def __str__(self) -> str:
        return f"{self.medicine.name} - {self.batch_number}"

    @property
    def is_expired(self) -> bool:
        return self.expiry_date < timezone.now().date()

    @property
    def remaining_percentage(self) -> float:
        if self.initial_quantity == 0:
            return 0.0
        return round(self.quantity / self.initial_quantity * 100, 2)

    def save(self, *args, **kwargs):
        if not self.pk and self.initial_quantity == 0:
            self.initial_quantity = self.quantity
        super().save(*args, **kwargs)