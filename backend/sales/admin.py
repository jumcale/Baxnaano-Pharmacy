from __future__ import annotations

from django.contrib import admin

from .models import Sale, SaleItem


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0
    readonly_fields = ("medicine", "batch", "quantity", "unit_price", "line_total")


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("invoice_number", "customer_name", "payment_method", "total", "created_at")
    list_filter = ("payment_method", "created_at")
    search_fields = ("invoice_number", "customer_name", "customer_phone")
    inlines = [SaleItemInline]
    readonly_fields = ("invoice_number", "subtotal", "discount", "tax", "total", "created_at")