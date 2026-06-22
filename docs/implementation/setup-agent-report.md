# Setup Agent v1 — Report

| Field | Value |
|-------|-------|
| **Status** | Implementation report (non-governance) |
| **Date** | 2026-06-22 |
| **Scope** | Environment setup, deployment prep, CI/CD validation, infrastructure verification, release runbooks, operational documentation |
| **Constraints** | Does **not** modify Architecture, Governance, ADRs, the Agent Registry, or the canonical Open Grace architecture. No new agent is registered. |

## Interpretation & scope

"Setup Agent v1" is implemented here as an **operational capability expressed in documentation + validation**, not as a registered software agent. The task explicitly forbids modifying the Agent Registry, canonical architecture, ADRs, or adding agents — so no entry was added to `data/registry/agents/`, no spec was added under `docs/architecture/canonical/`, and no service was created. The deliverables are the runnable/operable knowledge a Setup Agent would own: setup guides, deployment/runbooks, and verified procedures.

## Deliverables

| Area | Path |
|------|------|
| Local development guide | `docs/setup/local-development-guide.md` |
| Docker guide | `docs/setup/docker-guide.md` |
| Deployment guide | `docs/setup/deployment-guide.md` |
| Monitoring guide | `docs/setup/monitoring-guide.md` |
| Backup guide | `docs/setup/backup-guide.md` |
| Recovery guide | `docs/setup/recovery-guide.md` |
| Release runbook | `docs/runbooks/release-runbook.md` |
| Rollback runbook | `docs/runbooks/rollback-runbook.md` |
| This report | `docs/implementation/setup-agent-report.md` |

---

## Validation results

### 1. Repository bootstrap — ✅ PASS
The startup update script (editable install of all `packages/*` + `services/*` + `pytest httpx geoalchemy2`) is idempotent; re-running re-installs cleanly (`Successfully installed api-service-0.1.0 wise-common-0.1.0 …`). Console scripts land in `~/.local/bin`. Bootstrap is documented in the Local Development Guide and registered as the VM update script.

### 2. Docker startup — ⚠️ NOT RUNNABLE IN THIS ENVIRONMENT
Docker is **not installed** in the Cursor Cloud VM (`docker: command not found`), so `docker compose up` / `docker compose config` could not be executed here. The compose stack was **reviewed statically** and documented (6 services + Postgres/Redis/MinIO/OpenSearch, healthchecks, volumes, the `orchestration` profile for n8n). On a Docker-capable host the Docker Guide path applies; in this VM the equivalent **native PostgreSQL** path is used and verified instead. CI (`.github/workflows/ci.yml` → `docker-build` job) builds the service images and runs `docker compose config --quiet` on GitHub-hosted runners.

### 3. Test execution — ✅ PASS
On a fresh `wise_test` (PostGIS + pgvector), psycopg3 driver:
- `pytest tests/ -m smoke` → **10 passed**.
- `pytest tests/reference tests/e2e/test_reference_capability_{1,2,3}.py tests/test_contracts.py tests/test_species_contracts.py` (from `packages/wise-discovery`) → **37 passed**.

(Integration suites `tests/registry|metadata|discovery` pass on fresh per-suite databases; remaining single failures are pre-existing and tracked — see Gaps.)

### 4. Infrastructure verification — ✅ PASS (native)
- PostgreSQL 16 cluster online (`pg_lsclusters`), role `wise`, DBs `wise` + `wise_test`, extensions PostGIS + pgvector + schemas applied.
- `wise` seeded: `registry.sources = 9`, `discovery.records = 3`.
- `api-service` healthy (`GET /health` → 200); RC1/RC2/RC3 read aggregates return 200.
- Migration order verified in `infrastructure/scripts/migrate.sh`: registry → reference → metadata → discovery; `scripts/validate_alembic_heads.py` enforces a single head.

### 5. Documentation completeness — ✅ PASS
All eight requested guides/runbooks are present under `docs/setup/` (6) and `docs/runbooks/` (2), cross-linked, each carrying the non-modification banner and a rights/ADR-aware footer where relevant.

---

## Findings

1. **Environment is healthy and reproducible.** Native bootstrap + Postgres path works end-to-end; the update script is the single source of truth for dependency refresh.
2. **RC0 stabilization holds.** Registry/metadata migrations now commit with plain `alembic upgrade head`; the documented flow no longer needs the old autocommit workaround.
3. **Two durable footguns are now documented:** the psycopg3 driver requirement (`postgresql+psycopg://`) and the discovery package's relative `script_location` (run from its dir). Both appear in the guides and `AGENTS.md`.
4. **Observability is health-checks + structlog only.** The OTel/Prometheus/Grafana/Loki stack is scaffolded but not deployed (`architecture-overview.md` §7); the Monitoring Guide documents the gap and the plug-in points.
5. **Experience plane & commerce are pre-implementation.** Deployment of `apps/nature-culture-web` (Vercel) and the Phase 12 storefront are documented as forward steps, not current capability (see RC9 docs).

## Gaps

| Gap | Severity | Where covered |
|-----|----------|---------------|
| Docker not runnable in the Cloud VM | Medium | Docker Guide §6 (install steps); CI runs Docker on GH runners |
| No automated backup jobs (only documented procedures) | Medium | Backup Guide §4 (schedule recommendation) |
| Observability stack not deployed | Medium | Monitoring Guide §5 |
| Some Alembic **downgrades** are incomplete | Medium | Recovery/Rollback runbooks (prefer roll-forward / restore) |
| Cross-schema ORM `NoReferencedTableError` in 2 integration tests | Low | rc0 report (out of scope; not setup-caused) |
| No deploy-time smoke automation | Low | Release Runbook §5 (manual checklist) |
| Secrets management not formalized | Medium | Deployment Guide §3 (server-only env; no values committed) |

## Recommended next actions

1. **Automate the deploy smoke checks** (Release Runbook §5) as a script/CI step: `/health` ×6 + RC1 aggregate + map bbox.
2. **Schedule backups** (cron or an n8n workflow): daily `pg_dump` + MinIO mirror with retention; add a quarterly restore-drill (Recovery Guide §6).
3. **Stand up observability** when a phase requires it: enable `OTEL_EXPORTER_OTLP_ENDPOINT`, add Prometheus scrape + Grafana golden-signal dashboards, ship structlog to Loki.
4. **Prefer additive migrations** and add a CI guard that flags non-additive/irreversible downgrades, closing the rollback gap.
5. **Formalize secrets** (a secrets manager + documented rotation); keep DB/MinIO creds out of any `NEXT_PUBLIC_` scope.
6. **When the experience plane lands**, extend the Deployment Guide + Release Runbook with the Vercel promote/rollback path (already sketched from `rc9-public-launch-plan.md`).

---

*Implementation report. Does not modify Architecture, Governance, ADRs, the Agent Registry, or the canonical Open Grace architecture. Companion docs: `docs/setup/`, `docs/runbooks/`.*
