from typing import Optional
from pydantic import BaseModel


class VulnerabilityRead(BaseModel):
    id: int
    cve_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    cvss: Optional[float] = None
    exploit_available: bool = False
    source: Optional[str] = None

    class Config:
        from_attributes = True
