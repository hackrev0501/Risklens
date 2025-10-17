from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.vuln import Finding, Vulnerability
from ..models.asset import Asset

router = APIRouter()


@router.get("/")
def list_findings(db: Session = Depends(get_db)):
    q = (
        db.query(Finding, Vulnerability, Asset)
        .join(Vulnerability, Finding.vuln_id == Vulnerability.id)
        .join(Asset, Finding.asset_id == Asset.id)
        .all()
    )
    out = []
    for f, v, a in q:
        out.append(
            {
                "id": f.id,
                "asset_id": a.id,
                "asset_identifier": a.identifier,
                "vuln_id": v.id,
                "vuln_title": v.title,
                "cvss": v.cvss,
                "port": f.port,
                "service": f.service,
            }
        )
    return out
