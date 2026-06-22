# preservation-service

WISE platform service scaffold for **Preservation (03 §4.3)**.

| Field | Value |
|-------|-------|
| **Architecture** | architecture-v1.0 |
| **Build phase** | 3 — Preservation |
| **Agent spec** | `11-preservation-agent` |
| **Port** | `8003` |

## Endpoints (scaffold)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Liveness and readiness probe |

Business logic is implemented in Reference Capability 1 phases. See repository root `architecture-overview.md`.

## Local development

```bash
export WISE_SERVICE_NAME=preservation-service
export WISE_LOG_LEVEL=INFO
uvicorn wise_preservation.main:app --reload --port 8003
```

## Docker

Built from repository root:

```bash
docker compose build preservation-service
docker compose up preservation-service
```
