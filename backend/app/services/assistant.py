from __future__ import annotations

from typing import List


# Minimal RAG-like stub with keyword filtering over a small in-memory store

class AssistantIndex:
    def __init__(self) -> None:
        self.docs: list[dict] = []

    def upsert(self, doc_id: str, text: str, url: str | None = None) -> None:
        self.docs = [d for d in self.docs if d["id"] != doc_id]
        self.docs.append({"id": doc_id, "text": text, "url": url})

    def query(self, q: str, top_k: int = 5) -> list[dict]:
        terms = set(t.lower() for t in q.split())
        scored: list[tuple[dict, int]] = []
        for d in self.docs:
            score = sum(1 for t in terms if t in d["text"].lower())
            if score > 0:
                scored.append((d, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [s[0] for s in scored[:top_k]]


assistant_index = AssistantIndex()
