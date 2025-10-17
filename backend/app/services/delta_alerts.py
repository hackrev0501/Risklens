from __future__ import annotations

from sqlalchemy.orm import Session

from ..models.vuln import Finding
from ..models.alert import DeltaAlert


# Basic delta: if a finding appears for an asset that did not exist previously with same vuln

def compute_delta_alerts(db: Session) -> int:
    # For demo: if any finding exists, create a generic alert per asset
    count = 0
    existing_assets = set()
    for f in db.query(Finding).all():
        if f.asset_id in existing_assets:
            continue
        existing_assets.add(f.asset_id)
        alert = DeltaAlert(asset_id=f.asset_id, message="New findings detected for asset")
        db.add(alert)
        count += 1
    db.commit()
    return count
