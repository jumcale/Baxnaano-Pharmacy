from __future__ import annotations

from django.contrib import admin

from .models import Batch, Medicine, Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_person", "email", "phone_number")
    search_fields = ("name", "email", "phone_number")


class BatchInline(admin.TabularInline):
    model = Batch
    extra = 0


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "category", "unit_price", "reorder_level", "total_stock")
    list_filter = ("category",)
    search_fields = ("name", "sku", "barcode")
    inlines = [BatchInline]


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ("medicine", "batch_number", "expiry_date", "quantity", "is_expired")
    list_filter = ("expiry_date",)
    search_fields = ("batch_number", "medicine__name")