from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.reports import generate_csv_report

router = APIRouter()


@router.post("/generate")
def generate(db: Session = Depends(get_db)):
    path = generate_csv_report(db)
    return {"path": path}
