from __future__ import annotations

from decimal import Decimal

from rest_framework import serializers

from inventory.models import Batch, Medicine

from .models import Sale, SaleItem


class SaleItemSerializer(serializers.ModelSerializer):
    medicine_detail = serializers.StringRelatedField(source="medicine", read_only=True)
    batch_number = serializers.CharField(source="batch.batch_number", read_only=True)

    class Meta:
        model = SaleItem
        fields = [
            "id",
            "medicine",
            "medicine_detail",
            "batch",
            "batch_number",
            "quantity",
            "unit_price",
            "line_total",
        ]
        read_only_fields = ["id", "medicine_detail", "batch_number", "line_total"]


class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Sale
        fields = [
            "id",
            "invoice_number",
            "customer_name",
            "customer_phone",
            "customer_email",
            "payment_method",
            "subtotal",
            "discount",
            "tax",
            "total",
            "notes",
            "items",
            "created_at",
            "created_by",
        ]
        read_only_fields = [
            "id",
            "invoice_number",
            "subtotal",
            "tax",
            "total",
            "created_at",
            "created_by",
        ]

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Sale must contain at least one item.")
        for item in value:
            medicine = item.get("medicine")
            batch = item.get("batch")
            quantity = item.get("quantity")
            if not all([medicine, batch, quantity]):
                raise serializers.ValidationError("Medicine, batch, and quantity are required for each item.")
            if quantity <= 0:
                raise serializers.ValidationError("Quantity must be greater than zero.")
            if not Batch.objects.filter(pk=batch.pk, medicine_id=medicine.id).exists():
                raise serializers.ValidationError("Batch does not belong to the selected medicine.")
        return value

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        discount = Decimal(validated_data.get("discount", 0))
        tax_rate = Decimal(self.context["request"].data.get("tax_rate", 0))
        sale, _ = Sale.create_with_items(
            items=[
                {
                    "medicine": item["medicine"].id if isinstance(item["medicine"], Medicine) else item["medicine"],
                    "batch": item["batch"].id if isinstance(item["batch"], Batch) else item["batch"],
                    "quantity": item["quantity"],
                    "price": item.get("unit_price"),
                }
                for item in items_data
            ],
            created_by=self.context["request"].user,
            payment_method=validated_data["payment_method"],
            customer_name=validated_data.get("customer_name", ""),
            customer_phone=validated_data.get("customer_phone", ""),
            customer_email=validated_data.get("customer_email", ""),
            discount=discount,
            tax_rate=tax_rate,
            notes=validated_data.get("notes", ""),
        )
        return sale