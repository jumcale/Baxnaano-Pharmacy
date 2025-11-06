# Baxnaano Pharmacy Platform

AI-powered pharmacy management system for Baxnaano Pharmacy in Arabsiyo, Somaliland. The platform includes:

- **Backend**: Django REST Framework, PostgreSQL, Celery, Redis
- **Frontend**: React (Vite) with Tailwind CSS and Zustand
- **AI Microservice**: FastAPI service delivering demand forecasting and expiry risk predictions
- **Infrastructure**: Docker Compose with Nginx reverse proxy, Celery workers, and Redis

## Project Structure

```
backend/                 # Django backend
frontend/                # React frontend
pharmacy-ai-engine/      # FastAPI AI microservice
docker-compose.yml       # Full-stack orchestration
nginx/nginx.conf         # Reverse proxy configuration
```

## Getting Started

### Prerequisites
- Docker & Docker Compose

### Run the full stack

```bash
docker compose up --build
```

Services:
- API: `http://localhost/api/`
- Frontend: `http://localhost/`
- AI Engine: `http://localhost:8001/api/ai/`

Default credentials can be created via Django admin or management commands.

## Testing

- Backend: `pytest --cov=pharmacy`
- Frontend: `npm run test` (inside `frontend/`)
- AI Engine: `pytest` (inside `pharmacy-ai-engine/`)

## Environment

Set environment variables in `backend/.env.example` (copy to `.env`) and adjust credentials as needed. Timezone is configured for `Africa/Mogadishu`.

## Deployment

Recommended targets: Render, Railway, or AWS ECS. Configure CI/CD pipelines to build Docker images for each service and deploy using the provided Dockerfiles.