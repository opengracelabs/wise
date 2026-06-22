# api-service

WISE platform service scaffold for **Platform API gateway and Founder Demonstration Surface backend**.

| Field | Value |
|-------|-------|
| **Architecture** | architecture-v1.0 |
| **Build phase** | Gateway |
| **Agent spec** | `—` |
| **Port** | `8000` |

## Endpoints (scaffold)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Liveness and readiness probe |

Business logic is implemented in Reference Capability 1 phases. See repository root `architecture-overview.md`.

## Local development

```bash
export WISE_SERVICE_NAME=api-service
export WISE_LOG_LEVEL=INFO
uvicorn wise_api.main:app --reload --port 8000
```

## Docker

Built from repository root:

```bash
docker compose build api-service
docker compose up api-service
```
