from __future__ import annotations

import logging
from datetime import timedelta

from django.utils import timezone

from pharmacy.celery import app

from inventory.models import Batch, Medicine

from .models import Alert

logger = logging.getLogger(__name__)


@app.task
def generate_expiry_alerts() -> None:
    today = timezone.now().date()
    horizon = today + timedelta(days=30)
    batches = Batch.objects.filter(expiry_date__lte=horizon, quantity__gt=0)
    for batch in batches:
        alert, created = Alert.objects.get_or_create(
            alert_type=Alert.AlertType.EXPIRY,
            batch=batch,
            defaults={
                "title": f"Batch {batch.batch_number} nearing expiry",
                "medicine": batch.medicine,
                "message": f"{batch.medicine.name} batch {batch.batch_number} expires on {batch.expiry_date}.",
            },
        )
        if not created and alert.status == Alert.AlertStatus.RESOLVED:
            alert.status = Alert.AlertStatus.NEW
            alert.save(update_fields=["status"])


@app.task
def generate_low_stock_alerts() -> None:
    medicines = Medicine.objects.all()
    for medicine in medicines:
        if medicine.total_stock <= medicine.reorder_level:
            Alert.objects.get_or_create(
                alert_type=Alert.AlertType.LOW_STOCK,
                medicine=medicine,
                defaults={
                    "title": f"Low stock: {medicine.name}",
                    "message": f"Stock for {medicine.name} is {medicine.total_stock}, reorder level is {medicine.reorder_level}.",
                },
            )