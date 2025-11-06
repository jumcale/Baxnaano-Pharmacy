from __future__ import annotations

import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ai_engine.api.urls import api_router
from ai_engine.services.forecast_service import load_model

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Pharmacy AI Engine",
    version="0.1.0",
    description="AI microservice providing demand forecast and expiry risk predictions.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    model_path = Path(__file__).resolve().parent / "ai_engine" / "models" / "ai_model.pkl"
    try:
        load_model(model_path)
        logger.info("AI model loaded from %s", model_path)
    except FileNotFoundError:
        logger.warning("AI model file not found at %s. Using fallback predictors.", model_path)


@app.get("/healthz", tags=["Health"])
async def health_check():
    return {"status": "ok"}


app.include_router(api_router, prefix="/api/ai")
