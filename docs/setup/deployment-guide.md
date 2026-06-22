# Deployment Guide

| Field | Value |
|-------|-------|
| **Status** | Operational documentation (non-governance) |
| **Date** | 2026-06-22 |
| **Scope** | Build, configure and deploy the WISE platform services and the public experience surface |
| **Authority** | Companion to `docker-compose.yml`, `.github/workflows/ci.yml`, `05-physical-architecture.md`, `docs/architecture/nature-culture-frontend-v1.0.md`. Does not modify Architecture v1.0, governance, ADRs, or the Agent Registry. |

## 1. Topology

Two planes deploy separately (ADR-002 boundary):

- **Platform plane** (`services/*`, data plane) — container hosts in Zone Alpha/Beta. The `api-service` is the only public gateway; the others are internal.
- **Experience plane** (the planned `apps/nature-culture-web` Next.js app) — Vercel CDN/edge, read-only consumer of `api-service`. See `docs/implementation/rc9-public-launch-plan.md` and `rc9-deployment-readiness-report.md` (currently pre-implementation).

```
Users → [Experience: Vercel/Next.js]* → api-service (FastAPI) → discovery/metadata/preservation/kg/orchestrator
                                                              → PostgreSQL+PostGIS+pgvector · MinIO · Redis · OpenSearch
  (* not yet built; today api-service serves the demonstration surface directly)
```

## 2. Build artifacts

Each service ships as a `python:3.12-slim` image (see `services/*/Dockerfile`). Build via Compose:

```bash
docker compose build api-service discovery-service metadata-service \
                     preservation-service knowledge-graph-service orchestrator-service
```

Images install the shared `wise-*` packages then the service. The `api-service` image bundles `apps/demonstration-surface` and `data/`.

## 3. Configuration (environment variables)

Service env (see `.env.example` and the compose `x-service-env` anchor):

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` / `WISE_DATABASE_URL` | Postgres DSN — **must** use `postgresql+psycopg://` |
| `REDIS_URL` | Redis DSN |
| `MINIO_ENDPOINT` / `MINIO_ACCESS_KEY` / `MINIO_SECRET_KEY` / `MINIO_BUCKET` | object storage |
| `OPENSEARCH_URL` | search endpoint |
| `WISE_ENVIRONMENT`, `WISE_LOG_LEVEL`, `WISE_SERVICE_NAME` | runtime/log/identity |
| `WISE_DEMONSTRATION_SURFACE_PATH` | static surface path (api-service) |
| `WISE_MANIFEST_ROOT` | agent/capability manifest root (orchestrator) |
| `WISE_ARK_NAAN` | ARK namespace |

**Never** expose database/MinIO credentials or internal tokens to the browser/experience plane.

Per-environment upstreams (frontend, when built): `WISE_API_BASE_URL`, `NEXT_PUBLIC_SITE_URL`, `NEXT_PUBLIC_DEFAULT_LOCALE`, `REVALIDATION_SECRET`, `NC_FEATURE_*`.

## 4. Deploy sequence

1. **Provision data plane:** PostgreSQL 16 (PostGIS + pgvector), Redis, MinIO (+ `wise-preservation` bucket), OpenSearch.
2. **Initialize DB:** apply `infrastructure/docker/postgres/init/01-extensions.sql` (the postgres image does this on first boot).
3. **Migrate:** `infrastructure/scripts/migrate.sh` (registry → reference → metadata → discovery) with `WISE_DATABASE_URL` set. Run discovery from its package dir (relative `script_location`).
4. **Deploy services:** start `discovery/metadata/preservation/knowledge-graph/orchestrator`, then `api-service`. Wait for each `/health` to return 200.
5. **(Experience plane)** deploy `apps/nature-culture-web` to Vercel (root `apps/nature-culture-web`, `pnpm build`) once it exists — see RC9 docs.
6. **Smoke test:** the gateway endpoints in §6.

## 5. CI/CD

`.github/workflows/ci.yml` (push/PR to `main`) runs two jobs:

- **`lint-and-test`** — starts PostgreSQL, installs packages, validates the Alembic graph (`scripts/validate_alembic_heads.py`), runs migrations, then `tests/registry`, `tests/reference` + RC3 e2e + contracts, `tests/metadata`, `tests/discovery`, and smoke tests.
- **`docker-build`** — builds the five service images and runs `docker compose config --quiet`.

A green pipeline is the precondition for the Release Runbook (`docs/runbooks/release-runbook.md`).

## 6. Post-deploy verification

```bash
for p in 8000 8001 8002 8003 8004 8005; do curl -fs http://<host>:$p/health; done
curl http://<host>:8000/v1/objects/stonehenge        # seeded RC1 aggregate (HTTP 200)
curl "http://<host>:8000/v1/map/search?bbox=-82,25,-80,26"
```

## 7. Rollback

See `docs/runbooks/rollback-runbook.md`. In short: redeploy the previous image tag; if a migration must be undone, `alembic downgrade` per package (note: some downgrades are incomplete — see the rescore/stabilization reports). Prefer roll-forward for schema changes.

---

*Operational documentation. Does not modify Architecture v1.0, governance, ADRs, or the Agent Registry.*
