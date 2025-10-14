from __future__ import annotations

from pydantic import BaseModel
from typing import Optional


class FindingRead(BaseModel):
    id: int
    asset_id: int
    asset_identifier: str
    vuln_id: int
    vuln_title: str
    cvss: Optional[float] = None
    port: Optional[int] = None
    service: Optional[str] = None

    class Config:
        from_attributes = True
