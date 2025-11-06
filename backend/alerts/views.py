from __future__ import annotations

from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.permissions import IsAdminOrPharmacist

from .models import Alert
from .serializers import AlertSerializer


class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.select_related("medicine", "batch")
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["alert_type", "status"]
    search_fields = ["title", "message", "medicine__name"]
    ordering_fields = ["created_at"]

    def get_permissions(self):
        if self.action in {"destroy"}:
            return [IsAdminOrPharmacist()]
        return [permission() for permission in self.permission_classes]

    @action(detail=True, methods=["post"])
    def acknowledge(self, request, pk=None):
        alert = self.get_object()
        alert.status = Alert.AlertStatus.ACKNOWLEDGED
        alert.acknowledged_at = timezone.now()
        alert.resolved_by = request.user
        alert.save(update_fields=["status", "acknowledged_at", "resolved_by"])
        serializer = self.get_serializer(alert)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], permission_classes=[IsAdminOrPharmacist])
    def resolve(self, request, pk=None):
        alert = self.get_object()
        alert.status = Alert.AlertStatus.RESOLVED
        alert.resolved_by = request.user
        alert.acknowledged_at = alert.acknowledged_at or timezone.now()
        alert.save(update_fields=["status", "resolved_by", "acknowledged_at"])
        serializer = self.get_serializer(alert)
        return Response(serializer.data)