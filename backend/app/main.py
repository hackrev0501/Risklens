from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, assets, scans, vulnerabilities, graph, paths, assistant, reports, tickets, plugins, admin, findings, alerts, metrics

app = FastAPI(title="Unified Vulnerability Management Platform", version="0.1.0", docs_url="/docs", redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(assets.router, prefix="/api/assets", tags=["assets"])
app.include_router(scans.router, prefix="/api/scans", tags=["scans"])
app.include_router(vulnerabilities.router, prefix="/api/vulns", tags=["vulnerabilities"])
app.include_router(graph.router, prefix="/api/graph", tags=["graph"])
app.include_router(paths.router, prefix="/api/paths", tags=["paths"])
app.include_router(assistant.router, prefix="/api/assistant", tags=["assistant"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])
app.include_router(tickets.router, prefix="/api/tickets", tags=["tickets"])
app.include_router(plugins.router, prefix="/api/plugins", tags=["plugins"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(findings.router, prefix="/api/findings", tags=["findings"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["alerts"])
app.include_router(metrics.router, prefix="/api/metrics", tags=["metrics"])


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
