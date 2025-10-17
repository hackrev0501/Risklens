from __future__ import annotations

import os
import pandas as pd
from sqlalchemy.orm import Session

from ..models.vuln import Finding, Vulnerability
from ..models.asset import Asset


def generate_csv_report(db: Session, out_dir: str = "/data/reports") -> str:
    os.makedirs(out_dir, exist_ok=True)
    rows: list[dict] = []
    q = (
        db.query(Finding, Vulnerability, Asset)
        .join(Vulnerability, Finding.vuln_id == Vulnerability.id)
        .join(Asset, Finding.asset_id == Asset.id)
        .all()
    )
    for f, v, a in q:
        rows.append(
            {
                "asset": a.identifier,
                "service": f.service,
                "port": f.port,
                "cve": v.cve_id,
                "title": v.title,
                "cvss": v.cvss,
                "exploit": v.exploit_available,
                "source": v.source,
            }
        )
    df = pd.DataFrame(rows)
    path = os.path.join(out_dir, "report.csv")
    df.to_csv(path, index=False)
    return path
