from __future__ import annotations

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.scan import Scan
from ..schemas.scans import ScanCreate, ScanRead, ScanDetail
from ..services.scan_orchestrator import start_scan

router = APIRouter()


@router.get("/", response_model=List[ScanRead])
def list_scans(db: Session = Depends(get_db)):
    return db.query(Scan).order_by(Scan.id.desc()).all()


@router.post("/", response_model=ScanDetail)
def create_scan(data: ScanCreate, db: Session = Depends(get_db)):
    scan = start_scan(db, data.target, data.tools)
    return scan


@router.get("/{scan_id}", response_model=ScanDetail)
def get_scan(scan_id: int, db: Session = Depends(get_db)):
    obj = db.query(Scan).get(scan_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Scan not found")
    return obj
