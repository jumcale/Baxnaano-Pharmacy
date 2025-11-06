from __future__ import annotations

from datetime import timedelta

from django.db import models
from django.db.models import Sum
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from alerts.models import Alert
from inventory.models import Medicine
from sales.models import Sale, SaleItem


class DashboardReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.now()
        start_of_week = today - timedelta(days=today.weekday())
        start_of_month = today.replace(day=1)

        total_sales = Sale.objects.count()
        total_revenue = Sale.objects.aggregate(total=Sum("total"))["total"] or 0
        weekly_sales = Sale.objects.filter(created_at__gte=start_of_week).aggregate(total=Sum("total"))["total"] or 0
        monthly_sales = Sale.objects.filter(created_at__gte=start_of_month).aggregate(total=Sum("total"))["total"] or 0

        low_stock_count = Medicine.objects.filter(reorder_level__gte=0).annotate(
            total_stock=Sum("batches__quantity")
        ).filter(total_stock__lte=models.F("reorder_level")).count()

        recent_alerts = Alert.objects.order_by("-created_at")[:5].values(
            "id", "title", "alert_type", "status", "created_at"
        )

        top_medicines = (
            SaleItem.objects.values("medicine__name")
            .annotate(total_quantity=Sum("quantity"))
            .order_by("-total_quantity")[:5]
        )

        data = {
            "total_sales": total_sales,
            "total_revenue": float(total_revenue),
            "weekly_sales": float(weekly_sales),
            "monthly_sales": float(monthly_sales),
            "low_stock_count": low_stock_count,
            "recent_alerts": list(recent_alerts),
            "top_medicines": list(top_medicines),
        }

        return Response(data)