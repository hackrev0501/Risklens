# Unified Vulnerability Management Platform (Demo)

This is a demo implementation scaffolding the architecture described: backend (FastAPI), worker (Celery), frontend (Next.js), Neo4j graph, Postgres, Redis. Many features are stubbed for local exploration.

## Quick start (Docker Compose)

```bash
cd infra
docker compose up --build
```

Then initialize and seed the DB in another shell:

```bash
docker compose exec backend python scripts/init_db.py
docker compose exec backend python scripts/seed.py
```

Open UI at http://localhost:3000 and API at http://localhost:8000/docs

## Notes
- Scans are simulated; replace with real worker tasks.
- Graph uses Neo4j; click Build Graph then view nodes.
- Assistant is a keyword-search stub.
- Reports generates a CSV at /data/reports in the backend container.
- Plugin example at `plugins/example_scanner`.
```
