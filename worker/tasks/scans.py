from __future__ import annotations

from celery import shared_task


@shared_task(name="tasks.scans.run_scan")
def run_scan(scan_id: int, target: str, tools: list[str]) -> dict:
    # Placeholder: invoke real scanners or plugins
    return {"scan_id": scan_id, "status": "completed"}
