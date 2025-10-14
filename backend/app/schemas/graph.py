from typing import List, Optional
from pydantic import BaseModel


class GraphNode(BaseModel):
    id: str
    label: str
    type: str  # host, service, vuln
    risk: Optional[float] = None


class GraphEdge(BaseModel):
    source: str
    target: str
    relation: str


class AttackPath(BaseModel):
    nodes: List[str]
    score: Optional[float] = None
