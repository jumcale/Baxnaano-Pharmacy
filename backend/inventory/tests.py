from __future__ import annotations

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from users.models import User

from .models import Medicine, Supplier


@pytest.mark.django_db
def test_medicine_creation_flow():
    supplier = Supplier.objects.create(name="Health Supplies")
    user = User.objects.create_user(email="pharmacist@example.com", password="password", role=User.Role.PHARMACIST)
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post(
        reverse("medicine-list"),
        {
            "name": "Paracetamol",
            "sku": "PARA-500",
            "barcode": "1234567890123",
            "category": "tablet",
            "strength": "500mg",
            "unit_price": "1.50",
            "reorder_level": 20,
            "supplier": supplier.id,
        },
        format="json",
    )

    assert response.status_code == 201
    assert Medicine.objects.filter(name="Paracetamol").exists()