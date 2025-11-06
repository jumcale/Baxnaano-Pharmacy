from __future__ import annotations

import logging

from pharmacy.celery import app

logger = logging.getLogger(__name__)


@app.task
def refresh_dashboard_cache() -> None:
    logger.info("Refreshing dashboard cache (placeholder)")