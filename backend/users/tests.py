from __future__ import annotations

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from .models import User


@pytest.mark.django_db
def test_login_flow():
    user = User.objects.create_user(email="admin@example.com", password="password", role=User.Role.ADMIN)
    client = APIClient()
    response = client.post(reverse("api:login"), {"email": user.email, "password": "password"}, format="json")

    assert response.status_code == 200
    data = response.json()
    assert "access" in data and "refresh" in data
    assert data["user"]["email"] == user.email