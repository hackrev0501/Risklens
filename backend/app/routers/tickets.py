from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.ticketing import create_ticket
from ..models.ticket import Ticket

router = APIRouter()


@router.post("/")
def create(
    finding_id: int | None = None, external_system: str = "github", summary: str = "Fix vuln", description: str | None = None, db: Session = Depends(get_db)
):
    t = create_ticket(db, finding_id=finding_id, external_system=external_system, summary=summary, description=description)
    return {"id": t.id, "status": t.status}


@router.get("/")
def list_tickets(db: Session = Depends(get_db)):
    ts = db.query(Ticket).all()
    return [
        {
            "id": t.id,
            "status": t.status,
            "external_system": t.external_system,
            "external_id": t.external_id,
            "summary": t.summary,
        }
        for t in ts
    ]
