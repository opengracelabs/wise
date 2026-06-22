# Docker Guide

| Field | Value |
|-------|-------|
| **Status** | Operational documentation (non-governance) |
| **Date** | 2026-06-22 |
| **Scope** | Run the full WISE stack with Docker Compose |
| **Authority** | Companion to `docker-compose.yml`, `infrastructure/`. Does not modify Architecture v1.0, governance, ADRs, or the Agent Registry. |

## 1. What the stack contains

Defined in `docker-compose.yml` (project name `wise`):

### Data plane
| Service | Image | Ports | Notes |
|---------|-------|-------|-------|
| `postgres` | `wise-postgres:16-postgis-pgvector` (built from `infrastructure/docker/postgres/Dockerfile`) | 5432 | PostGIS + pgvector; runs `init/01-extensions.sql` on first boot |
| `redis` | `redis:7-alpine` | 6379 | cache/queue |
| `minio` (+ `minio-init`) | `minio/minio` | 9000, 9001 | object storage; `minio-init` creates the `wise-preservation` bucket |
| `opensearch` | `opensearchproject/opensearch:2.18.0` | 9200 | search (Phase 6 scaffold) |

### Platform services (FastAPI; `/health` on each)
| Service | Port | Depends on |
|---------|-----:|------------|
| `api-service` | 8000 | discovery, metadata, preservation, knowledge-graph, orchestrator |
| `discovery-service` | 8001 | postgres, redis |
| `metadata-service` | 8002 | postgres |
| `preservation-service` | 8003 | postgres, minio |
| `knowledge-graph-service` | 8004 | postgres, opensearch |
| `orchestrator-service` | 8005 | postgres |
| `n8n` | 5678 | orchestrator (profile `orchestration` only) |

Each service Dockerfile is multi-stage `python:3.12-slim`, installs the shared packages + the service, exposes its port, and defines a `curl /health` HEALTHCHECK. The `api-service` image also bundles `apps/demonstration-surface` and `data/` (`WISE_DEMONSTRATION_SURFACE_PATH=/app/demonstration-surface`).

## 2. Start

```bash
cp .env.example .env          # configure environment (defaults work for local)
docker compose up --build     # build images and start the stack
# optional workflow automation:
docker compose --profile orchestration up n8n
```

Health checks:

```bash
curl http://localhost:8000/health   # api-service
curl http://localhost:8001/health   # discovery-service
curl http://localhost:8002/health   # metadata-service
curl http://localhost:8003/health   # preservation-service
curl http://localhost:8004/health   # knowledge-graph-service
curl http://localhost:8005/health   # orchestrator-service
```

## 3. Migrations & seed data (important)

Compose starts the services but **does not auto-apply Alembic migrations**. The `postgres` container runs `01-extensions.sql` (extensions + schemas) on first boot, but the read API returns 404s until the reference data is seeded. From the host (with deps installed, see the Local Development Guide) or `docker compose exec`:

```bash
export WISE_DATABASE_URL=postgresql+psycopg://wise:wise@localhost:5432/wise
infrastructure/scripts/migrate.sh    # registry -> reference -> metadata -> discovery
```

## 4. Common operations

```bash
docker compose ps                       # status
docker compose logs -f api-service      # follow logs
docker compose build api-service        # rebuild one service
docker compose config --quiet           # validate compose syntax
docker compose down                      # stop (keep volumes)
docker compose down -v                   # stop and DELETE data volumes
```

Named volumes: `postgres_data`, `redis_data`, `minio_data`, `opensearch_data`, `n8n_data`.

## 5. CI parity

`.github/workflows/ci.yml` builds the service images and validates the compose config:

```bash
docker compose build api-service discovery-service metadata-service preservation-service knowledge-graph-service
docker compose config --quiet
```

## 6. Environment note (headless / Cloud Agent)

Docker is **not installed** in the Cursor Cloud VM used for this repository; local development there uses **native PostgreSQL** instead (see the Local Development Guide and `AGENTS.md`). To run Docker-in-Docker in that environment, install Docker plus `fuse-overlayfs` and switch `iptables` to legacy mode (the storage driver must be `fuse-overlayfs`). On a normal developer machine with Docker Desktop / Engine, `docker compose up --build` works directly.

---

*Operational documentation. Does not modify Architecture v1.0, governance, ADRs, or the Agent Registry.*
