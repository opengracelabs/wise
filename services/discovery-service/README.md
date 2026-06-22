# discovery-service

WISE platform service scaffold for **Discovery (03 §4.1)**.

| Field | Value |
|-------|-------|
| **Architecture** | architecture-v1.0 |
| **Build phase** | 1 — Discovery |
| **Agent spec** | `09-source-discovery-agent` |
| **Port** | `8001` |

## Endpoints (scaffold)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Liveness and readiness probe |

Business logic is implemented in Reference Capability 1 phases. See repository root `architecture-overview.md`.

## Local development

```bash
export WISE_SERVICE_NAME=discovery-service
export WISE_LOG_LEVEL=INFO
uvicorn discovery_service.main:app --reload --port 8001
```

## Docker

Built from repository root:

```bash
docker compose build discovery-service
docker compose up discovery-service
```
