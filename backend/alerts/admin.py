from __future__ import annotations

from django.contrib import admin

from .models import Alert


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ("title", "alert_type", "status", "created_at")
    list_filter = ("alert_type", "status", "created_at")
    search_fields = ("title", "message", "medicine__name", "batch__batch_number")