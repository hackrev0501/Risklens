from __future__ import annotations

from typing import Any, Dict
from sqlalchemy.orm import Session

from ..models.asset import Asset
from ..models.scan import Scan
from ..models.vuln import Vulnerability, Finding


# Simple normalization with dedup and confidence boost when multiple tools report same CVE/title

def normalize_results(db: Session, scan: Scan) -> None:
    if not scan.raw_results:
        return

    # Ensure asset exists
    asset = db.query(Asset).filter(Asset.identifier == scan.target).first()
    if not asset:
        asset = Asset(identifier=scan.target, type="host")  # type: ignore[arg-type]
        db.add(asset)
        db.flush()

    merged: dict[str, dict[str, Any]] = {}

    for tool, result in scan.raw_results.items():
        if tool == "nuclei":
            for m in result.get("matches", []):
                key = m.get("id") or m.get("title")
                merged.setdefault(key, {"count": 0, "title": m.get("title", key), "source": set(), "port": m.get("port"), "service": m.get("service"), "cvss": float(m.get("severity", 0)), "exploit": bool(m.get("exploit", False))})
                merged[key]["count"] += 1
                merged[key]["source"].add("nuclei")
        if tool == "nikto":
            for i in result.get("issues", []):
                key = i.get("title")
                merged.setdefault(key, {"count": 0, "title": key, "source": set(), "port": i.get("port"), "service": "http", "cvss": float(i.get("severity", 0)), "exploit": False})
                merged[key]["count"] += 1
                merged[key]["source"].add("nikto")
        if tool == "openvas":
            for f in result.get("findings", []):
                key = f.get("cve") or f.get("title")
                merged.setdefault(key, {"count": 0, "title": f.get("title", key), "cve": f.get("cve"), "source": set(), "port": f.get("port"), "service": f.get("service"), "cvss": float(f.get("cvss", 0)), "exploit": False})
                merged[key]["count"] += 1
                merged[key]["source"].add("openvas")

    # False positive suppression: drop items seen only once with low cvss
    for key, item in list(merged.items()):
        if item["count"] == 1 and item.get("cvss", 0) < 4.0:
            merged.pop(key)

    for key, item in merged.items():
        vuln = db.query(Vulnerability).filter(Vulnerability.title == item["title"]).first()
        if not vuln:
            vuln = Vulnerability(
                cve_id=item.get("cve"),
                title=item["title"],
                description=f"Normalized from sources: {', '.join(sorted(item['source']))}",
                cvss=item.get("cvss"),
                exploit_available=item.get("exploit", False),
                source=",".join(sorted(item["source"])),
            )
            db.add(vuln)
            db.flush()

        finding = Finding(
            scan_id=scan.id,
            asset_id=asset.id,
            vuln_id=vuln.id,
            port=item.get("port"),
            service=item.get("service"),
        )
        db.add(finding)

    db.flush()
