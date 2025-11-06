from __future__ import annotations

import statistics
from pathlib import Path
from typing import List, Optional

import joblib
import numpy as np

MODEL: Optional[any] = None


def load_model(path: Path) -> None:
    global MODEL
    if path.exists():
        MODEL = joblib.load(path)
    else:
        MODEL = None


class ForecastService:
    forecast_horizon: int = 30

    def predict_demand(self, medicine: str, historical_sales: List[int], lookback_days: int):
        history = historical_sales[-lookback_days:] if lookback_days else historical_sales
        if not history:
            raise ValueError("Historical sales data is required.")

        if MODEL is not None:
            forecast_array = MODEL.predict(np.array(history).reshape(1, -1))[0]
            predicted_demand = int(float(np.sum(forecast_array)))
            daily_forecast = [max(int(value), 0) for value in forecast_array]
            confidence = 0.9
        else:
            moving_average = statistics.mean(history[-7:]) if len(history) >= 7 else statistics.mean(history)
            daily_forecast = [int(round(moving_average)) for _ in range(self.forecast_horizon)]
            predicted_demand = sum(daily_forecast)
            confidence = 0.6

        return {
            "medicine": medicine,
            "predicted_demand": predicted_demand,
            "confidence": confidence,
            "daily_forecast": daily_forecast,
        }
