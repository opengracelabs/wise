# metadata-service

WISE platform service scaffold for **Knowledge Modeling (03 §4.4)**.

| Field | Value |
|-------|-------|
| **Architecture** | architecture-v1.0 |
| **Build phase** | 4 — Knowledge Modeling |
| **Agent spec** | `10-metadata-agent` |
| **Port** | `8002` |

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Liveness and readiness probe |
| GET | `/modeling/assertions` | List entity assertion proposals (read-only) |
| GET | `/modeling/records/{record_id}` | Read normalized metadata record |

Business logic lives in `packages/wise-metadata`. This service exposes read endpoints only; no Knowledge Graph placement.

## Local development

```bash
pip install -e packages/wise-common -e packages/wise-contracts -e packages/wise-registry -e packages/wise-metadata -e services/metadata-service
export WISE_DATABASE_URL=postgresql+psycopg://wise:wise@localhost:5432/wise
export WISE_SERVICE_NAME=metadata-service
export WISE_LOG_LEVEL=INFO
uvicorn metadata_service.main:app --reload --port 8002
```

## Docker

Built from repository root:

```bash
docker compose build metadata-service
docker compose up metadata-service
```
