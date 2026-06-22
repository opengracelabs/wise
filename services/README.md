# services/

Platform-plane microservices implementing architecture-v1.0 capabilities (03 §4).

| Service | Phase | Port | Health |
|---------|-------|------|--------|
| [api-service](api-service/) | Gateway | 8000 | `/health` |
| [discovery-service](discovery-service/) | 1 — Discovery | 8001 | `/health` |
| [preservation-service](preservation-service/) | 2–3 — Ingestion & Preservation | 8003 | `/health` |
| [metadata-service](metadata-service/) | 4 — Knowledge Modeling | 8002 | `/health` |
| [knowledge-graph-service](knowledge-graph-service/) | 5 — Knowledge Graph | 8004 | `/health` |
| [orchestrator-service](orchestrator-service/) | Orchestration — LangGraph | 8005 | `/health` |
| [analytics-service](analytics-service/) | RC6 — Demand telemetry | 8006 | `/health` |

Each service is a FastAPI application with structured logging via `packages/wise-common`.
Business logic is added in Reference Capability 1 implementation phases.

Build all services from repository root:

```bash
docker compose build
```
