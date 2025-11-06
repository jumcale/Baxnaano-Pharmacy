from __future__ import annotations

from datetime import timedelta

from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.permissions import IsAdminOrPharmacist

from .models import Sale
from .tasks import email_sale_receipt
from .serializers import SaleSerializer


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.prefetch_related("items__medicine", "items__batch")
    serializer_class = SaleSerializer
    permission_classes = [IsAdminOrPharmacist]
    filterset_fields = ["payment_method", "created_at"]
    search_fields = ["invoice_number", "customer_name", "customer_phone"]
    ordering_fields = ["created_at", "total"]

    def perform_create(self, serializer):
        sale = serializer.save()
        if sale.customer_email:
            email_sale_receipt.delay(sale.id)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def summary(self, request):
        days = int(request.query_params.get("days", 7))
        start_date = timezone.now() - timedelta(days=days)
        queryset = self.get_queryset().filter(created_at__gte=start_date)
        total_sales = queryset.count()
        total_revenue = sum(sale.total for sale in queryset[:1000])  # limit to prevent heavy queries
        return Response({"total_sales": total_sales, "total_revenue": str(total_revenue), "days": days})

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def invoice(self, request, pk=None):
        sale = self.get_object()
        serializer = self.get_serializer(sale)
        return Response(serializer.data)