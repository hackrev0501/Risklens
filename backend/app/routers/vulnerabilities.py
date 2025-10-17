from __future__ import annotations

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.vuln import Vulnerability
from ..schemas.vulns import VulnerabilityRead

router = APIRouter()


@router.get("/", response_model=List[VulnerabilityRead])
def list_vulns(db: Session = Depends(get_db)):
    return db.query(Vulnerability).order_by(Vulnerability.cvss.desc().nullslast()).all()
