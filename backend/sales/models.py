from __future__ import annotations

from decimal import Decimal
from typing import Iterable

from django.conf import settings
from django.db import models, transaction
from django.utils import timezone

from inventory.models import Batch, Medicine


class Sale(models.Model):
    class PaymentMethod(models.TextChoices):
        CASH = "cash", "Cash"
        MPESA = "mpesa", "Mobile Money"
        CARD = "card", "Card"
        TRANSFER = "transfer", "Bank Transfer"

    invoice_number = models.CharField(max_length=32, unique=True)
    customer_name = models.CharField(max_length=255, blank=True)
    customer_phone = models.CharField(max_length=50, blank=True)
    customer_email = models.EmailField(blank=True)
    payment_method = models.CharField(max_length=32, choices=PaymentMethod.choices, default=PaymentMethod.CASH)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="sales", on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Invoice {self.invoice_number}"

    @staticmethod
    def next_invoice_number() -> str:
        today = timezone.now().strftime("%Y%m%d")
        last_sale = Sale.objects.filter(invoice_number__startswith=today).order_by("-invoice_number").first()
        if not last_sale:
            return f"{today}-001"
        _, seq = last_sale.invoice_number.split("-")
        next_seq = int(seq) + 1
        return f"{today}-{next_seq:03d}"

    @classmethod
    def create_with_items(
        cls,
        *,
        items: Iterable[dict],
        created_by,
        payment_method: str,
        customer_name: str = "",
        customer_phone: str = "",
        customer_email: str = "",
        discount: Decimal = Decimal("0.00"),
        tax_rate: Decimal = Decimal("0.00"),
        notes: str = "",
    ):
        with transaction.atomic():
            invoice_number = cls.next_invoice_number()
            sale = cls.objects.create(
                invoice_number=invoice_number,
                customer_name=customer_name,
                customer_phone=customer_phone,
                customer_email=customer_email,
                payment_method=payment_method,
                discount=discount,
                tax=Decimal("0.00"),
                subtotal=Decimal("0.00"),
                total=Decimal("0.00"),
                created_by=created_by,
                notes=notes,
            )
            subtotal = Decimal("0.00")
            sale_items = []
            for item in items:
                medicine = Medicine.objects.get(pk=item["medicine"])
                batch = Batch.objects.get(pk=item["batch"])
                quantity = int(item["quantity"])
                price = Decimal(item.get("price", batch.selling_price))
                sale_item = SaleItem(
                    sale=sale,
                    medicine=medicine,
                    batch=batch,
                    quantity=quantity,
                    unit_price=price,
                )
                sale_item.full_clean()
                sale_item.save()
                sale_items.append(sale_item)
                subtotal += sale_item.line_total

            tax_amount = (subtotal - discount) * tax_rate / Decimal("100.00")
            total = subtotal - discount + tax_amount
            sale.subtotal = subtotal
            sale.tax = tax_amount.quantize(Decimal("0.01"))
            sale.total = total.quantize(Decimal("0.01"))
            sale.save()

        return sale, sale_items


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name="items", on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)
    batch = models.ForeignKey(Batch, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    line_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        verbose_name = "Sale Item"
        verbose_name_plural = "Sale Items"

    def __str__(self) -> str:
        return f"{self.medicine.name} x {self.quantity}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.line_total = self.unit_price * self.quantity
            if self.batch.quantity < self.quantity:
                raise ValueError("Insufficient stock in batch.")
            self.batch.quantity -= self.quantity
            self.batch.save()
        super().save(*args, **kwargs)