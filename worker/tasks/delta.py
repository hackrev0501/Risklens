from __future__ import annotations

from celery import shared_task
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from backend.app.services.delta_alerts import compute_delta_alerts

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://uivmp:uivmp@postgres:5432/uivmp")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)


@shared_task(name="tasks.delta.run_delta_alerts")
def run_delta_alerts() -> int:
    db: Session = SessionLocal()
    try:
        return compute_delta_alerts(db)
    finally:
        db.close()
