from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from ..models.asset import Asset
from ..models.scan import Scan
from ..models.vuln import Vulnerability, Finding
from ..models.ticket import Ticket, TicketStatus

router = APIRouter()


@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    total_assets = db.query(func.count(Asset.id)).scalar() or 0
    total_scans = db.query(func.count(Scan.id)).scalar() or 0
    total_vulns = db.query(func.count(Vulnerability.id)).scalar() or 0
    critical_vulns = db.query(func.count(Vulnerability.id)).filter((Vulnerability.cvss != None) & (Vulnerability.cvss >= 9.0)).scalar() or 0
    open_tickets = db.query(func.count(Ticket.id)).filter(Ticket.status.in_([TicketStatus.open, TicketStatus.in_progress])).scalar() or 0
    return {
        "total_assets": total_assets,
        "total_scans": total_scans,
        "total_vulns": total_vulns,
        "critical_vulns": critical_vulns,
        "open_tickets": open_tickets,
    }


@router.get("/heatmap")
def heatmap(db: Session = Depends(get_db)):
    # Aggregate approximate risk per asset: sum(cvss) * (business_criticality / 5)
    q = (
        db.query(Asset.id, Asset.identifier, Asset.business_criticality, func.sum(Vulnerability.cvss))
        .join(Finding, Finding.asset_id == Asset.id)
        .join(Vulnerability, Finding.vuln_id == Vulnerability.id)
        .group_by(Asset.id)
        .all()
    )
    result = []
    for aid, ident, crit, sum_cvss in q:
        risk = (sum_cvss or 0.0) * (float(crit or 1) / 5.0)
        result.append({"asset_id": aid, "asset": ident, "risk": risk})
    result.sort(key=lambda x: x["risk"], reverse=True)
    return {"assets": result}
