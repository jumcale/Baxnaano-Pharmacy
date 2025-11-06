from __future__ import annotations

import logging

import requests
from django.conf import settings

from pharmacy.celery import app

from .models import Medicine

logger = logging.getLogger(__name__)


@app.task
def notify_ai_engine_for_medicine(medicine_id: int) -> None:
    try:
        medicine = Medicine.objects.get(pk=medicine_id)
    except Medicine.DoesNotExist:
        logger.warning("Medicine with id %s does not exist", medicine_id)
        return

    payload = {
        "medicine": medicine.name,
        "sku": medicine.sku,
        "barcode": medicine.barcode,
        "category": medicine.category,
        "strength": medicine.strength,
        "unit_price": str(medicine.unit_price),
        "reorder_level": medicine.reorder_level,
        "total_stock": medicine.total_stock,
    }

    ai_endpoint = settings.AI_ENGINE_BASE_URL.rstrip("/") + "/api/ai/forecast/"
    try:
        response = requests.post(ai_endpoint, json=payload, timeout=5)
        response.raise_for_status()
        logger.info("Synced medicine %s with AI engine", medicine.sku)
    except requests.RequestException as exc:
        logger.error("Failed to sync medicine %s with AI engine: %s", medicine.sku, exc)