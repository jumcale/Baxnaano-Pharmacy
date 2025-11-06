from __future__ import annotations

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from inventory.models import Batch, Medicine, Supplier
from users.models import User


@pytest.mark.django_db
def test_sale_creation_decrements_stock():
    supplier = Supplier.objects.create(name="Supplier")
    medicine = Medicine.objects.create(name="Amoxicillin", sku="AMOX-250", supplier=supplier, unit_price="5.00")
    batch = Batch.objects.create(
        medicine=medicine,
        batch_number="B001",
        expiry_date="2030-01-01",
        quantity=100,
        initial_quantity=100,
        selling_price="5.00",
    )
    user = User.objects.create_user(email="cashier@example.com", password="password", role=User.Role.PHARMACIST)
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post(
        reverse("sale-list"),
        {
            "customer_name": "John Doe",
            "customer_email": "john@example.com",
            "payment_method": "cash",
            "items": [
                {"medicine": medicine.id, "batch": batch.id, "quantity": 2, "unit_price": "5.00"},
            ],
        },
        format="json",
    )

    assert response.status_code == 201, response.json()
    batch.refresh_from_db()
    assert batch.quantity == 98