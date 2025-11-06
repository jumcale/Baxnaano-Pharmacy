from __future__ import annotations

import pytest
from rest_framework.test import APIClient

from alerts.models import Alert
from alerts.tasks import generate_expiry_alerts
from inventory.models import Batch, Medicine, Supplier
from users.models import User


@pytest.mark.django_db
def test_generate_expiry_alert_creates_alert():
    supplier = Supplier.objects.create(name="Supplier")
    medicine = Medicine.objects.create(name="Ibuprofen", sku="IBU-200", supplier=supplier, reorder_level=10)
    Batch.objects.create(
        medicine=medicine,
        batch_number="IBU001",
        expiry_date="2025-01-01",
        quantity=50,
        initial_quantity=50,
    )
    generate_expiry_alerts()
    assert Alert.objects.filter(alert_type=Alert.AlertType.EXPIRY).exists()


@pytest.mark.django_db
def test_alert_acknowledge_endpoint():
    supplier = Supplier.objects.create(name="Supplier")
    medicine = Medicine.objects.create(name="Vitamin C", sku="VITC-100", supplier=supplier, reorder_level=5)
    alert = Alert.objects.create(
        title="Low stock",
        alert_type=Alert.AlertType.LOW_STOCK,
        message="Low stock on Vitamin C",
        medicine=medicine,
    )
    user = User.objects.create_user(email="staff@example.com", password="password", role=User.Role.PHARMACIST)
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.post(f"/api/alerts/{alert.id}/acknowledge/")

    assert response.status_code == 200
    alert.refresh_from_db()
    assert alert.status == Alert.AlertStatus.ACKNOWLEDGED