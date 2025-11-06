from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_forecast_endpoint():
    response = client.post(
        "/api/ai/forecast/",
        json={"medicine": "Paracetamol 500mg", "historical_sales": [10, 12, 11, 15, 14, 13, 12], "lookback_days": 7},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["medicine"] == "Paracetamol 500mg"
    assert "predicted_demand" in data
    assert len(data["daily_forecast"]) == 30


def test_expiry_endpoint():
    response = client.post(
        "/api/ai/expiry/",
        json={
            "medicine": "Amoxicillin",
            "batches": [
                {"batch_number": "B1", "expiry_date": "2025-01-01", "quantity": 50, "days_to_expiry": 90},
                {"batch_number": "B2", "expiry_date": "2024-12-01", "quantity": 30, "days_to_expiry": 20},
            ],
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["medicine"] == "Amoxicillin"
    assert "expiry_risk" in data
