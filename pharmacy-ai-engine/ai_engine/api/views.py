from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from ai_engine.services.expiry_predictor import ExpiryPredictionService
from ai_engine.services.forecast_service import ForecastService


router = APIRouter()


class ForecastRequest(BaseModel):
    medicine: str = Field(..., description="Medicine name")
    historical_sales: List[int] = Field(..., description="Historical daily sales quantities")
    lookback_days: int = Field(default=30, description="Number of days to analyse")


class ForecastResponse(BaseModel):
    medicine: str
    predicted_demand: int
    confidence: float
    daily_forecast: List[int]


class ExpiryBatch(BaseModel):
    batch_number: str
    expiry_date: str
    quantity: int
    days_to_expiry: int


class ExpiryPredictionRequest(BaseModel):
    medicine: str
    batches: List[ExpiryBatch]


class ExpiryPredictionResponse(BaseModel):
    medicine: str
    expiry_risk: str
    confidence: float
    batches: List[ExpiryBatch]


def get_forecast_service() -> ForecastService:
    return ForecastService()


def get_expiry_service() -> ExpiryPredictionService:
    return ExpiryPredictionService()


@router.post("/forecast/", response_model=ForecastResponse)
async def predict_forecast(
    request: ForecastRequest,
    service: ForecastService = Depends(get_forecast_service),
) -> ForecastResponse:
    prediction = service.predict_demand(request.medicine, request.historical_sales, request.lookback_days)
    return ForecastResponse(**prediction)


@router.post("/expiry/", response_model=ExpiryPredictionResponse)
async def predict_expiry(
    request: ExpiryPredictionRequest,
    service: ExpiryPredictionService = Depends(get_expiry_service),
) -> ExpiryPredictionResponse:
    result = service.evaluate_batches(request.medicine, [batch.model_dump() for batch in request.batches])
    return ExpiryPredictionResponse(**result)
