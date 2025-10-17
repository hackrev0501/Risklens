from __future__ import annotations

from typing import List, Tuple
from neo4j import GraphDatabase, Driver
import os
from sqlalchemy.orm import Session

from ..models.vuln import Finding, Vulnerability
from ..models.asset import Asset


NEO4J_URI = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "neo4jpassword")


def get_driver() -> Driver:
    return GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def build_graph(db: Session) -> None:
    driver = get_driver()
    with driver.session() as session:
        # Clear existing graph
        session.run("MATCH (n) DETACH DELETE n")

        # Create nodes and relationships
        for asset in db.query(Asset).all():
            session.run(
                "MERGE (h:Host {id: $id}) SET h.label=$label, h.risk=$risk",
                id=f"host:{asset.id}",
                label=asset.identifier,
                risk=float(asset.business_criticality),
            )

        q = db.query(Finding).join(Vulnerability, Finding.vuln_id == Vulnerability.id).all()
        for f in q:
            session.run(
                "MERGE (s:Service {id: $sid}) SET s.label=$slabel\n"
                "MERGE (v:Vuln {id: $vid}) SET v.label=$vlabel, v.cvss=$cvss, v.exploit=$exploit\n"
                "MERGE (h:Host {id: $hid})\n"
                "MERGE (h)-[:RUNS]->(s)\n"
                "MERGE (s)-[:HAS_VULN]->(v)",
                sid=f"service:{f.asset_id}:{f.port or 'na'}:{f.service or 'unknown'}",
                slabel=f"{f.service or 'svc'}:{f.port or 'na'}",
                vid=f"vuln:{f.vuln_id}",
                vlabel=f.vul.title,
                cvss=float(f.vul.cvss or 0.0),
                exploit=bool(f.vul.exploit_available),
                hid=f"host:{f.asset_id}",
            )

        # Simple reachability edges between hosts (demo: fully connected)
        hosts = [f"host:{a.id}" for a in db.query(Asset).all()]
        for i, h1 in enumerate(hosts):
            for h2 in hosts[i + 1 :]:
                session.run("MATCH (a:Host {id:$a}),(b:Host {id:$b}) MERGE (a)-[:CAN_REACH]->(b)", a=h1, b=h2)

    driver.close()


def get_graph() -> Tuple[list[dict], list[dict]]:
    driver = get_driver()
    nodes: list[dict] = []
    edges: list[dict] = []
    with driver.session() as session:
        for rec in session.run("MATCH (n) RETURN n.id as id, labels(n) as labels, n as props"):
            ntype = "unknown"
            labels = rec["labels"]
            if "Host" in labels:
                ntype = "host"
            elif "Service" in labels:
                ntype = "service"
            elif "Vuln" in labels:
                ntype = "vuln"
            nodes.append({"id": rec["id"], "type": ntype, "label": rec["props"].get("label", rec["id"]), "risk": rec["props"].get("cvss") or rec["props"].get("risk")})

        for rec in session.run("MATCH (a)-[r]->(b) RETURN a.id as s, type(r) as rel, b.id as t"):
            edges.append({"source": rec["s"], "target": rec["t"], "relation": rec["rel"]})
    driver.close()
    return nodes, edges
