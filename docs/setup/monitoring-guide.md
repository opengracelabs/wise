# Monitoring Guide

| Field | Value |
|-------|-------|
| **Status** | Operational documentation (non-governance) |
| **Date** | 2026-06-22 |
| **Scope** | Health, logs, and observability for the WISE platform |
| **Authority** | Companion to `architecture-overview.md` §7, `04-system-diagram.md` §2.1. Does not modify Architecture v1.0, governance, ADRs, or the Agent Registry. |

## 1. Current state

Per `architecture-overview.md` §7, the full observability stack (OpenTelemetry, Prometheus, Grafana, Loki) is **listed in the engineering stack but not yet deployed**. What exists today:

- **Health endpoints** on every service (`GET /health`).
- **Structured logs** via `structlog` (`packages/wise-common/src/wise_common/logging.py`), configured at startup in each service `main.py`. Log level is set by `WISE_LOG_LEVEL`.
- **Container HEALTHCHECKs** (`curl /health`) in every service Dockerfile.
- **Database/infra healthchecks** in `docker-compose.yml` (`pg_isready`, `redis-cli ping`, MinIO `/minio/health/live`, OpenSearch `_cluster/health`).

This guide documents how to monitor with what exists and where the planned stack plugs in.

## 2. Health checks

```bash
for p in 8000 8001 8002 8003 8004 8005; do
  printf "port %s: " "$p"; curl -fs "http://localhost:$p/health" && echo
done
```

A healthy response is `{"status":"ok","service":"<name>","environment":"<env>"}`. Compose surfaces health via `docker compose ps` (the `STATUS` column shows `healthy`).

### Data plane
```bash
pg_isready -h localhost -U wise -d wise
redis-cli -u redis://localhost:6379/0 ping
curl -fs http://localhost:9000/minio/health/live
curl -fs http://localhost:9200/_cluster/health
```

## 3. Logs

- **Native:** services log to stdout/stderr; capture via your process manager. The PostgreSQL log is at `/var/log/postgresql/postgresql-16-main.log`.
- **Docker:** `docker compose logs -f <service>`.
- **Format:** `structlog` key-value events (e.g. `service_starting`, `service_stopping`). Set `WISE_LOG_LEVEL=DEBUG` for verbose output.
- **Correlation:** propagate `x-request-id` from `api-service` to upstream services for tracing (see the frontend doc error-handling section).

## 4. Key signals to watch

| Signal | Source | Healthy |
|--------|--------|---------|
| Service liveness | `/health` | 200 on all six |
| Gateway errors | api-service logs / 5xx rate | near zero |
| DB connectivity | `pg_isready`, connection-pool errors | reachable; no pool exhaustion |
| Migration drift | `scripts/validate_alembic_heads.py` | single head per package |
| Read aggregate | `GET /v1/objects/stonehenge` | 200 with full payload |
| Geospatial | `GET /v1/map/search?bbox=...` | 200, expected `count` |
| Disk (data volumes) | host / `postgres_data`, `minio_data` | below threshold |

## 5. Planned observability (scaffold → production)

When the stack is deployed (Phase-aligned, not yet present):

- **OpenTelemetry**: set `OTEL_EXPORTER_OTLP_ENDPOINT` (already in `.env.example`); instrument FastAPI + SQLAlchemy.
- **Prometheus** (`PROMETHEUS_PORT=9090`): scrape per-service metrics (request rate, latency, error rate, DB pool).
- **Grafana** (`GRAFANA_PORT=3000`): dashboards for the four golden signals per service + data-plane saturation.
- **Loki**: ship `structlog` JSON for centralized log search.
- **Frontend (Vercel)**: Web Vitals via Vercel Analytics (see `rc9-public-launch-plan.md`).

Until then, alerting is manual: a failing `/health`, a non-200 on the RC1 aggregate, or `pg_isready` failure are the primary pager conditions.

---

*Operational documentation. Does not modify Architecture v1.0, governance, ADRs, or the Agent Registry.*
