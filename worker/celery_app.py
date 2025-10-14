from __future__ import annotations

import os
from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery_app = Celery("uivmp", broker=REDIS_URL, backend=REDIS_URL)
celery_app.conf.task_routes = {"tasks.*": {"queue": "default"}}
celery_app.conf.beat_schedule = {
    "delta-alerts": {
        "task": "tasks.delta.run_delta_alerts",
        "schedule": 3600.0,  # hourly
    }
}
