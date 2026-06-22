# knowledge-graph-service

WISE platform service scaffold for **Knowledge Graph (03 §4.5)**.

| Field | Value |
|-------|-------|
| **Architecture** | architecture-v1.0 |
| **Build phase** | 5 — Knowledge Graph |
| **Agent spec** | `12-knowledge-graph-agent` |
| **Port** | `8004` |

## Endpoints (scaffold)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Liveness and readiness probe |

Business logic is implemented in Reference Capability 1 phases. See repository root `architecture-overview.md`.

## Local development

```bash
export WISE_SERVICE_NAME=knowledge-graph-service
export WISE_LOG_LEVEL=INFO
uvicorn wise_knowledge_graph.main:app --reload --port 8004
```

## Docker

Built from repository root:

```bash
docker compose build knowledge-graph-service
docker compose up knowledge-graph-service
```
