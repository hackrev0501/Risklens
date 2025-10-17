from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.alert import DeltaAlert
from ..services.delta_alerts import compute_delta_alerts

router = APIRouter()


@router.get("/")
def list_alerts(db: Session = Depends(get_db)):
    alerts = db.query(DeltaAlert).order_by(DeltaAlert.created_at.desc()).all()
    return [
        {
            "id": a.id,
            "asset_id": a.asset_id,
            "message": a.message,
            "created_at": a.created_at.isoformat() if a.created_at else None,
        }
        for a in alerts
    ]


@router.post("/run")
def run_delta(db: Session = Depends(get_db)):
    count = compute_delta_alerts(db)
    return {"generated": count}
