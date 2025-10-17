from __future__ import annotations

from collections import deque
from typing import List


# Deterministic BFS from any Internet node to Vuln nodes via Host/Service

def enumerate_paths(nodes: list[dict], edges: list[dict], limit: int = 20) -> List[List[str]]:
    # Build adjacency
    adj: dict[str, list[str]] = {}
    for e in edges:
        adj.setdefault(e["source"], []).append(e["target"])

    # Treat all hosts as reachable from a virtual Internet node
    internet = "internet"
    adj[internet] = [n["id"] for n in nodes if n["type"] == "host"]

    target_nodes = set([n["id"] for n in nodes if n["type"] == "vuln"])

    paths: list[list[str]] = []
    q = deque([(internet, [internet])])
    visited: set[tuple[str, str]] = set()

    while q and len(paths) < limit:
        node, path = q.popleft()
        for nxt in adj.get(node, []):
            step = (node, nxt)
            if step in visited:
                continue
            visited.add(step)
            new_path = path + [nxt]
            if nxt in target_nodes:
                paths.append(new_path)
            q.append((nxt, new_path))

    return paths
