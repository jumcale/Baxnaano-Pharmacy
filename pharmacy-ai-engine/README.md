# Pharmacy AI Engine

FastAPI-based AI microservice for Baxnaano Pharmacy. Provides endpoints for demand forecasting and expiry risk evaluation. Includes Celery workers for asynchronous processing.

## Quick Start

```bash
docker compose up --build
```

API available at `http://localhost:8001/api/ai/forecast/`.

## Endpoints

- `POST /api/ai/forecast/`
- `POST /api/ai/expiry/`

## Testing

```bash
pip install -r requirements.txt
pytest
```
