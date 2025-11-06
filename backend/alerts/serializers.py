from __future__ import annotations

from rest_framework import serializers

from .models import Alert


class AlertSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source="medicine.name", read_only=True)
    batch_number = serializers.CharField(source="batch.batch_number", read_only=True)

    class Meta:
        model = Alert
        fields = [
            "id",
            "title",
            "alert_type",
            "message",
            "status",
            "medicine",
            "medicine_name",
            "batch",
            "batch_number",
            "created_at",
            "acknowledged_at",
        ]
        read_only_fields = [
            "id",
            "medicine_name",
            "batch_number",
            "created_at",
            "acknowledged_at",
        ]