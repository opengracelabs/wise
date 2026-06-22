# Local Development Guide

| Field | Value |
|-------|-------|
| **Status** | Operational documentation (non-governance) |
| **Date** | 2026-06-22 |
| **Scope** | Run WISE locally without Docker (native Python + PostgreSQL) |
| **Authority** | Companion to `README.md`, `AGENTS.md`, `architecture-overview.md`. Does not modify Architecture v1.0, governance, ADRs, or the Agent Registry. |

> Authoritative quick-reference for day-to-day commands lives in `AGENTS.md` (`## Cursor Cloud specific instructions`). This guide is the longer-form walkthrough.

## 1. Prerequisites

- **Python 3.12** (the monorepo targets `>=3.12`).
- **PostgreSQL 16** with **PostGIS** and **pgvector** extensions.
- Build/runtime Python deps are installed editable from the monorepo; no Node toolchain is required for the platform services.

## 2. Bootstrap (dependencies)

From the repository root:

```bash
pip install -e packages/wise-common -e packages/wise-contracts -e packages/wise-registry \
            -e packages/wise-metadata -e packages/wise-discovery -e packages/wise-reference \
            -e packages/wise-orchestration
pip install -e services/discovery-service -e services/metadata-service \
            -e services/preservation-service -e services/knowledge-graph-service \
            -e services/api-service -e services/orchestrator-service
pip install pytest httpx geoalchemy2
```

This is exactly the startup update script (idempotent). Console scripts (`alembic`, `uvicorn`, `pytest`) install to `~/.local/bin`; ensure it is on `PATH`.

## 3. Database

PostgreSQL is **not** auto-started in headless environments. Start it and create the dev + test databases:

```bash
sudo pg_ctlcluster 16 main start                      # start the cluster

sudo -u postgres psql -c "CREATE ROLE wise WITH LOGIN PASSWORD 'wise' SUPERUSER;"
sudo -u postgres psql -c "CREATE DATABASE wise OWNER wise;"
sudo -u postgres psql -c "CREATE DATABASE wise_test OWNER wise;"

for db in wise wise_test; do
  sudo -u postgres psql -q -d "$db" -f infrastructure/docker/postgres/init/01-extensions.sql
done
```

`01-extensions.sql` enables PostGIS + pgvector and creates the application schemas.

**Connection string — use the psycopg3 driver:**

```
postgresql+psycopg://wise:wise@localhost:5432/wise
```

A bare `postgresql://...` selects the psycopg2 dialect, which is **not installed** and will fail at import.

## 4. Migrations

Apply in order: **registry → reference → metadata → discovery**. As of RC0 stabilization, all packages commit correctly with plain `alembic upgrade head` (see `docs/implementation/rc0-stabilization-report.md`).

```bash
export WISE_DATABASE_URL=postgresql+psycopg://wise:wise@localhost:5432/wise
(cd packages/wise-registry  && alembic upgrade head)
(cd packages/wise-reference && alembic upgrade head)
(cd packages/wise-metadata  && alembic upgrade head)   # requires registry.sources (FKs)
(cd packages/wise-discovery && alembic upgrade head)   # adds discovery.records.source_id + FK
```

`packages/wise-discovery/alembic.ini` uses a **relative** `script_location`, so run discovery migrations from its package directory (as above). Helper: `infrastructure/scripts/migrate.sh`.

## 5. Run the API service

The public read surface (RC1–RC3 + the demonstration surface):

```bash
DATABASE_URL=postgresql+psycopg://wise:wise@localhost:5432/wise \
  uvicorn wise_api.main:app --host 0.0.0.0 --port 8000 --reload   # run from services/api-service
```

Verify:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/v1/objects/stonehenge
curl http://localhost:8000/v1/species/panthera-leo
curl http://localhost:8000/v1/areas/everglades-national-park
curl "http://localhost:8000/v1/map/search?bbox=-82.0,25.0,-80.0,26.0"
```

HTML demonstration pages: `/objects/stonehenge`, `/objects/panthera-leo`, `/areas/everglades-national-park`.

### Other services (optional)
All are FastAPI apps run with `uvicorn <module>:app --port <port>` (modules + ports from each `services/*/Dockerfile`):

| Service | Module | Port |
|---------|--------|-----:|
| api-service | `wise_api.main:app` | 8000 |
| discovery-service | `discovery_service.main:app` | 8001 |
| metadata-service | `metadata_service.main:app` | 8002 |
| preservation-service | `wise_preservation.main:app` | 8003 |
| knowledge-graph-service | `wise_knowledge_graph.main:app` | 8004 |
| orchestrator-service | `wise_orchestrator.main:app` | 8005 |

## 6. Tests

```bash
export WISE_TEST_DATABASE_URL=postgresql+psycopg://wise:wise@localhost:5432/wise_test
export WISE_DATABASE_URL=$WISE_TEST_DATABASE_URL DATABASE_URL=$WISE_TEST_DATABASE_URL

pytest tests/ -m smoke                       # 10 tests, no live DB needed for most
# reference + e2e fixtures re-run migrations and rely on the relative discovery path:
cd packages/wise-discovery && pytest /workspace/tests/reference /workspace/tests/e2e
```

Run integration suites (`tests/registry|metadata|discovery`) against a **fresh** database: the conftests drop their schemas but not the `alembic_version_*` tables, so a reused DB can skip re-migration. Drop/recreate + re-apply `01-extensions.sql` between suites.

## 7. Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `No module named 'psycopg2'` | bare `postgresql://` URL | use `postgresql+psycopg://` |
| `relation registry.* does not exist` in tests | stale `alembic_version_*` on reused DB | recreate the test DB |
| `Path doesn't exist: migrations` | discovery relative `script_location` | run from `packages/wise-discovery` |
| `command not found: alembic/uvicorn` | `~/.local/bin` not on `PATH` | add it to `PATH` |

---

*Operational documentation. Does not modify Architecture v1.0, governance, ADRs, or the Agent Registry.*
