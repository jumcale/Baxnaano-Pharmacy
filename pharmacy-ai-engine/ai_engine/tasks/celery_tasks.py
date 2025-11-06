from __future__ import annotations

import os

from celery import Celery

from ai_engine.services.expiry_predictor import ExpiryPredictionService
from ai_engine.services.forecast_service import ForecastService

celery_app = Celery("ai_engine")
celery_app.conf.broker_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
celery_app.conf.result_backend = celery_app.conf.broker_url

forecast_service = ForecastService()
expiry_service = ExpiryPredictionService()


@celery_app.task
def generate_forecast_task(medicine: str, historical_sales: list[int], lookback_days: int = 30) -> dict:
    return forecast_service.predict_demand(medicine, historical_sales, lookback_days)


@celery_app.task
def evaluate_expiry_task(medicine: str, batches: list[dict]) -> dict:
    return expiry_service.evaluate_batches(medicine, batches)
