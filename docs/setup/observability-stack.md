# Observability Stack — Deployment Plan

| Field | Value |
|-------|-------|
| **Status** | Operational plan (non-governance) |
| **Date** | 2026-06-22 |
| **Scope** | Deploying OpenTelemetry, Prometheus, Grafana and Loki for the WISE platform |
| **Authority** | Companion to `docs/setup/monitoring-guide.md`, `architecture-overview.md` §7, `04-system-diagram.md` §2.1. Does not modify Architecture v1.0, governance, ADRs, or the Agent Registry. |

> The observability stack is listed in the engineering stack but **not yet deployed** (`architecture-overview.md` §7). Today: `/health` endpoints + `structlog` (see the Monitoring Guide). This document is the plan to close that gap. It adds infrastructure and instrumentation only — no architecture/governance change.

## 1. Target architecture

```
WISE services ──(OTLP)──▶ OpenTelemetry Collector ──▶ Prometheus (metrics)
   structlog JSON ───────────────────────────────────▶ Loki (logs)
   (traces) ─────────────────────────────────────────▶ Tempo/Jaeger (optional)
                                                         │
                                          Grafana (dashboards + alerts) ◀┘
                                                         └─▶ Alertmanager ─▶ pager/email/Slack
```

- **Instrument** each FastAPI service with the OpenTelemetry SDK (auto-instrumentation for FastAPI + SQLAlchemy + httpx).
- **Export** OTLP to a central **Collector**, which fans out to Prometheus (metrics), Loki (logs), and optionally a trace backend.
- **Visualize/alert** in Grafana + Alertmanager.

## 2. Deployment model

| Component | Deploy as | Notes |
|-----------|-----------|-------|
| OpenTelemetry Collector | container/sidecar or per-node DaemonSet | receives OTLP on 4317/4318 |
| Prometheus | container/StatefulSet | scrapes Collector + service `/metrics`; 15s interval |
| Grafana | container | dashboards as code (provisioned), SSO |
| Loki | container/StatefulSet | log store; Promtail/OTel ships `structlog` JSON |
| Alertmanager | container | routes Prometheus alerts |

- **Local/dev:** add an optional `observability` Compose profile (Collector + Prometheus + Grafana + Loki) mirroring the `orchestration` profile pattern in `docker-compose.yml`. Do not enable by default.
- **Production:** deploy to the platform plane (Zone Alpha/Beta), separate from the experience plane. Frontend Web Vitals come from Vercel Analytics (see `rc9-public-launch-plan.md`).

### Service wiring
- `.env.example` already exposes `OTEL_EXPORTER_OTLP_ENDPOINT`, `PROMETHEUS_PORT=9090`, `GRAFANA_PORT=3000`.
- Set `OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318` and `OTEL_SERVICE_NAME=<service>`; extend `wise-common` logging to emit OTel-correlated, JSON `structlog` for Loki.

## 3. Metrics

### Per-service (the four golden signals)
| Metric | Type | Meaning |
|--------|------|---------|
| `http_server_requests_total{service,method,route,status}` | counter | request rate / error rate (5xx) |
| `http_server_request_duration_seconds` | histogram | latency (p50/p95/p99) |
| `db_pool_in_use` / `db_pool_size` | gauge | saturation (SQLAlchemy pool) |
| `db_query_duration_seconds` | histogram | DB latency |
| `process_*`, `python_gc_*` | gauge | runtime health |

### Platform/data plane
PostgreSQL exporter (connections, locks, replication lag, slowest queries), Redis exporter, MinIO metrics endpoint, OpenSearch cluster health, node CPU/mem/disk (especially `postgres_data`/`minio_data`).

### Domain (WISE-specific)
- Read-aggregate success rate (`/v1/objects|species|areas`).
- Migration head drift (export `scripts/validate_alembic_heads.py` result).
- Steward approval queue depth (orchestration), discovery/ingest throughput.

## 4. Dashboards (Grafana, provisioned as code)

1. **Platform overview** — golden signals per service, up/down, error budget.
2. **API gateway** — `api-service` RPS, latency heatmap, 4xx/5xx, top routes.
3. **Database** — connections, pool saturation, slow queries, replication/WAL, disk.
4. **Data plane** — Redis, MinIO (capacity/throughput), OpenSearch cluster health.
5. **Pipeline** — discovery→…→quality throughput, steward queue depth.
6. **Backups & migrations** — last successful backup age, migration head status.

## 5. Alerts (Prometheus → Alertmanager)

| Alert | Condition | Severity |
|-------|-----------|----------|
| ServiceDown | `up == 0` or `/health` failing 2m | page |
| HighErrorRate | 5xx ratio > 2% for 5m | page |
| HighLatency | p95 > 1s (api-service) for 10m | warn→page |
| DBPoolSaturation | `db_pool_in_use/db_pool_size > 0.9` 5m | warn |
| DBUnreachable | postgres exporter down / `pg_isready` fail | page |
| DiskFilling | `postgres_data`/`minio_data` > 85% | warn; > 95% page |
| BackupStale | no successful dump in 26h | warn |
| MigrationDrift | multiple heads / DB not at head | warn |
| ReadAggregateFailing | synthetic `GET /v1/objects/stonehenge` != 200 | page |

Until the stack ships, these conditions are covered manually by `scripts/smoke/run_smoke.sh` and the Monitoring Guide checks.

## 6. Rollout phases

1. Collector + Prometheus + Grafana, scrape exporters (infra metrics first — no code change).
2. Instrument services with OTel SDK (metrics + traces); add dashboards 1–4.
3. Loki + structured-log shipping; correlate logs↔traces via `x-request-id`.
4. Alertmanager routes + on-call; add dashboards 5–6 and synthetic checks.

---

*Operational plan. Does not modify Architecture v1.0, governance, ADRs, or the Agent Registry.*
