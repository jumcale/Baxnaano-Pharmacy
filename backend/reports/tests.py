from __future__ import annotations

import pytest
from rest_framework.test import APIClient

from alerts.models import Alert
from inventory.models import Medicine, Supplier
from sales.models import Sale
from users.models import User


@pytest.mark.django_db
def test_dashboard_report_endpoint():
    supplier = Supplier.objects.create(name="Supplier")
    medicine = Medicine.objects.create(name="Zinc", sku="ZINC-50", supplier=supplier, reorder_level=10)
    user = User.objects.create_user(email="admin@baxnaano.com", password="password", role=User.Role.ADMIN)
    Sale.objects.create(
        invoice_number="20250101-001",
        customer_name="Test",
        payment_method="cash",
        total="100.00",
        subtotal="100.00",
        discount="0.00",
        tax="0.00",
    )
    Alert.objects.create(
        title="Test Alert",
        alert_type=Alert.AlertType.LOW_STOCK,
        message="Low stock on Zinc",
        medicine=medicine,
    )

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get("/api/reports/dashboard/")
    assert response.status_code == 200
    payload = response.json()
    assert "total_sales" in payload