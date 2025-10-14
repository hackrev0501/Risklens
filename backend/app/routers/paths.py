from __future__ import annotations

from fastapi import APIRouter

from ..services.graph_builder import get_graph
from ..services.pathfinder import enumerate_paths
from ..services.ranker import rank_paths

router = APIRouter()


@router.get("/deterministic")
def deterministic_paths(limit: int = 10):
    nodes, edges = get_graph()
    raw_paths = enumerate_paths(nodes, edges, limit=limit)
    return {"paths": raw_paths}


@router.get("/ranked")
def ranked_paths(limit: int = 10):
    nodes, edges = get_graph()
    raw_paths = enumerate_paths(nodes, edges, limit=limit)
    node_lookup = {n["id"]: n for n in nodes}
    ranked = rank_paths(raw_paths, node_lookup)
    return {"paths": [{"nodes": p, "score": s} for p, s in ranked]}


@router.get("/simulate")
def simulate_patch(remove_node: str, limit: int = 10):
    nodes, edges = get_graph()
    # baseline
    base_paths = enumerate_paths(nodes, edges, limit=limit)
    node_lookup = {n["id"]: n for n in nodes}
    base_ranked = rank_paths(base_paths, node_lookup)
    base_top = base_ranked[0][1] if base_ranked else 0.0

    # remove node and incident edges
    filtered_nodes = [n for n in nodes if n["id"] != remove_node]
    filtered_edges = [e for e in edges if e["source"] != remove_node and e["target"] != remove_node]

    sim_paths = enumerate_paths(filtered_nodes, filtered_edges, limit=limit)
    sim_lookup = {n["id"]: n for n in filtered_nodes}
    sim_ranked = rank_paths(sim_paths, sim_lookup)
    sim_top = sim_ranked[0][1] if sim_ranked else 0.0

    reduction = base_top - sim_top
    percent = (reduction / base_top * 100.0) if base_top > 0 else 0.0
    return {
        "before": {"top_score": base_top},
        "after": {"top_score": sim_top},
        "reduction": reduction,
        "percent": percent,
        "removed": remove_node,
    }
