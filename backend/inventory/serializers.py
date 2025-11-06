from __future__ import annotations

from rest_framework import serializers

from .models import Batch, Medicine, Supplier


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"


class BatchSerializer(serializers.ModelSerializer):
    is_expired = serializers.BooleanField(read_only=True)
    remaining_percentage = serializers.FloatField(read_only=True)

    class Meta:
        model = Batch
        fields = [
            "id",
            "medicine",
            "batch_number",
            "expiry_date",
            "manufactured_date",
            "cost_price",
            "selling_price",
            "quantity",
            "initial_quantity",
            "is_expired",
            "remaining_percentage",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "is_expired", "remaining_percentage"]


class MedicineSerializer(serializers.ModelSerializer):
    total_stock = serializers.IntegerField(read_only=True)
    near_expiry_batches = BatchSerializer(many=True, read_only=True)
    batches = BatchSerializer(many=True, read_only=True)

    class Meta:
        model = Medicine
        fields = [
            "id",
            "name",
            "sku",
            "barcode",
            "category",
            "strength",
            "description",
            "unit_price",
            "reorder_level",
            "supplier",
            "total_stock",
            "near_expiry_batches",
            "batches",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "total_stock", "near_expiry_batches", "batches", "created_at", "updated_at"]