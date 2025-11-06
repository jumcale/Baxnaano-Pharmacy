from __future__ import annotations

from datetime import timedelta

from django.db.models import F, Sum
from django.db.models.functions import Coalesce
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.permissions import IsAdminOrPharmacist

from .models import Batch, Medicine, Supplier
from .serializers import BatchSerializer, MedicineSerializer, SupplierSerializer


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAdminOrPharmacist]
    filterset_fields = ["name"]
    search_fields = ["name", "email", "phone_number"]


class MedicineViewSet(viewsets.ModelViewSet):
    serializer_class = MedicineSerializer
    permission_classes = [IsAdminOrPharmacist]
    filterset_fields = ["category", "supplier"]
    search_fields = ["name", "sku", "barcode"]
    ordering_fields = ["name", "unit_price", "reorder_level"]

    def get_queryset(self):
        return (
            Medicine.objects.select_related("supplier")
            .prefetch_related("batches")
            .annotate(total_stock=Coalesce(Sum("batches__quantity"), 0))
        )

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def low_stock(self, request):
        queryset = self.filter_queryset(self.get_queryset().filter(total_stock__lte=F("reorder_level")))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def near_expiry(self, request):
        threshold_days = int(request.query_params.get("days", 30))
        threshold = timezone.now().date() + timedelta(days=threshold_days)
        batches = Batch.objects.filter(expiry_date__lte=threshold, quantity__gt=0).select_related("medicine")
        serializer = BatchSerializer(batches, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def scan(self, request):
        barcode = request.query_params.get("barcode")
        if not barcode:
            return Response({"detail": "Barcode parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            medicine = self.get_queryset().get(barcode=barcode)
        except Medicine.DoesNotExist:
            return Response({"detail": "Medicine not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(medicine)
        return Response(serializer.data)


class BatchViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.select_related("medicine")
    serializer_class = BatchSerializer
    permission_classes = [IsAdminOrPharmacist]
    filterset_fields = ["medicine", "expiry_date"]
    search_fields = ["batch_number"]
    ordering_fields = ["expiry_date", "quantity"]

    @action(detail=True, methods=["post"], permission_classes=[IsAdminOrPharmacist])
    def adjust_stock(self, request, pk=None):
        batch = self.get_object()
        adjustment = int(request.data.get("adjustment", 0))
        if adjustment == 0:
            return Response({"detail": "Adjustment must be non-zero."}, status=status.HTTP_400_BAD_REQUEST)
        batch.quantity = max(batch.quantity + adjustment, 0)
        batch.save()
        serializer = self.get_serializer(batch)
        return Response(serializer.data)