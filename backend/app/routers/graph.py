from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.graph_builder import build_graph, get_graph
from ..schemas.graph import GraphNode, GraphEdge

router = APIRouter()


@router.post("/build")
def build(db: Session = Depends(get_db)):
    build_graph(db)
    return {"ok": True}


@router.get("/", response_model=dict)
def graph():
    nodes, edges = get_graph()
    return {"nodes": nodes, "edges": edges}
