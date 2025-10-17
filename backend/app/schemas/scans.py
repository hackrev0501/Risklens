from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class ScanCreate(BaseModel):
    target: str
    tools: List[str] = ["nmap", "nuclei", "nikto"]


class ScanRead(BaseModel):
    id: int
    target: str
    tools: Optional[str]
    status: str
    error: Optional[str] = None

    class Config:
        from_attributes = True


class ScanDetail(ScanRead):
    raw_results: Optional[Dict[str, Any]] = None
