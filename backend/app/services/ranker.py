from __future__ import annotations

from typing import List


# Simple heuristic ranker as an ML stub
# score = mean(cvss along path) + 1.5 * (exploit flag present) - 0.1 * hops + 0.2 * business criticality

def rank_paths(paths: List[List[str]], node_lookup: dict[str, dict]) -> list[tuple[List[str], float]]:
    ranked: list[tuple[list[str], float]] = []
    for p in paths:
        cvss_values: list[float] = []
        exploit_present = False
        criticality: float = 0.0
        for nid in p:
            meta = node_lookup.get(nid)
            if not meta:
                continue
            if meta["type"] == "vuln":
                cvss_values.append(float(meta.get("risk") or 0.0))
                if meta.get("exploit"):
                    exploit_present = True
            if meta["type"] == "host":
                criticality += float(meta.get("risk") or 0.0)
        avg_cvss = sum(cvss_values) / len(cvss_values) if cvss_values else 0.0
        hops = max(0, len(p) - 1)
        score = avg_cvss + (1.5 if exploit_present else 0.0) - 0.1 * hops + 0.2 * criticality
        ranked.append((p, score))
    ranked.sort(key=lambda x: x[1], reverse=True)
    return ranked
