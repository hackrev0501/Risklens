from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List
from sqlalchemy.orm import Session

from ..models.scan import Scan, ScanStatus
from ..services.normalization import normalize_results

# In production this would enqueue Celery tasks


SUPPORTED_TOOLS = {"nmap", "nuclei", "nikto", "openvas"}


def start_scan(db: Session, target: str, tools: List[str]) -> Scan:
    tools = [t for t in tools if t in SUPPORTED_TOOLS]
    scan = Scan(target=target, tools=",".join(tools), status=ScanStatus.running, started_at=datetime.utcnow())
    db.add(scan)
    db.commit()
    db.refresh(scan)

    # Simulate tool execution; replace with Celery tasks in worker
    raw_results: Dict[str, Any] = {}
    for tool in tools:
        raw_results[tool] = _fake_tool_output(tool, target)

    scan.raw_results = raw_results
    scan.status = ScanStatus.completed
    scan.completed_at = datetime.utcnow()

    # Normalize and persist findings/vulns
    normalize_results(db, scan)

    db.add(scan)
    db.commit()
    db.refresh(scan)
    return scan


def _fake_tool_output(tool: str, target: str) -> Dict[str, Any]:
    # Deterministic fake output for demo
    if tool == "nmap":
        return {"ports": [{"port": 80, "service": "http"}, {"port": 5432, "service": "postgres"}]}
    if tool == "nuclei":
        return {
            "matches": [
                {
                    "id": "CVE-2023-0001",
                    "title": "Example RCE",
                    "severity": 9.8,
                    "service": "http",
                    "port": 80,
                    "exploit": True,
                }
            ]
        }
    if tool == "nikto":
        return {"issues": [{"title": "Outdated Server", "severity": 5.0, "port": 80}]}
    if tool == "openvas":
        return {
            "findings": [
                {"cve": "CVE-2022-9999", "title": "SQL Injection", "cvss": 7.5, "service": "http", "port": 80}
            ]
        }
    return {}
