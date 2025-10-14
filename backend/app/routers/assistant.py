from __future__ import annotations

from fastapi import APIRouter

from ..services.assistant import assistant_index

router = APIRouter()


@router.post("/index")
def index_doc(doc_id: str, text: str, url: str | None = None):
    assistant_index.upsert(doc_id, text, url)
    return {"ok": True}


@router.get("/query")
def query(q: str):
    hits = assistant_index.query(q)
    return {"results": hits}
