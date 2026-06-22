# Deployment Validation Runbook

| Field | Value |
|-------|-------|
| **Status** | Operational runbook (non-governance) |
| **Date** | 2026-06-22 |
| **Scope** | Run the deploy-time smoke tests (`scripts/smoke/`) to gate a release |
| **Authority** | Companion to `docs/runbooks/release-runbook.md`, `docs/setup/monitoring-guide.md`. Does not modify Architecture v1.0, governance, ADRs, or the Agent Registry. |

These checks automate the manual verification in the Release Runbook §5. Run them after every deploy and as the final gate before sign-off.

## Quick run

```bash
# from the repo root, with the target DSN and (optionally) the service list:
WISE_DATABASE_URL=postgresql+psycopg://wise:wise@<db-host>:5432/wise \
SMOKE_HOST=<gateway-host> \
SMOKE_SERVICES="api-service:8000 discovery-service:8001 metadata-service:8002 \
  preservation-service:8003 knowledge-graph-service:8004 orchestrator-service:8005" \
  scripts/smoke/run_smoke.sh
```

Exit code `0` = all PASS (gate open); non-zero = at least one FAIL (do not proceed; see Release/Rollback runbooks).

## Checks

### 1. Health endpoints — `smoke_health.sh`
Probes `GET /health` on each declared service and requires `200` + `"status":"ok"`.
- **Env:** `SMOKE_HOST` (default `localhost`), `SMOKE_SERVICES` (default `api-service:8000`).
- Set `SMOKE_SERVICES` to the full six-service list in a full-stack deploy; keep it narrow when only the gateway is deployed.

### 2. Database connectivity — `smoke_db.py`
Connects with the psycopg3 DSN, runs `SELECT 1`, and asserts required tables exist (`registry.sources`, `discovery.records`).
- **Env:** `WISE_DATABASE_URL`/`DATABASE_URL`. A bare `postgresql://` is auto-normalized to `postgresql+psycopg://`.

### 3. Migration verification — `smoke_migrations.py`
For each package (`wise-registry`, `wise-reference`, `wise-metadata`, `wise-discovery`): asserts a **single Alembic head** and that the DB version table is **at head**.
- **Env:** `SMOKE_REQUIRE_MIGRATED=1` to FAIL (instead of WARN) when a package's version table is absent — set this when the DB is expected to be fully migrated.

## Expected output (healthy)

```
== health ==
PASS  api-service (http://localhost:8000/health) -> 200 ok
== database ==
PASS  database connectivity + required tables present: ['registry.sources', 'discovery.records']
== migrations ==
PASS  wise-registry: at head 006_merge_rc3_and_v1_1
PASS  wise-reference: at head 006_seed_everglades
PASS  wise-metadata: at head 002_seed_schema_mappings
PASS  wise-discovery: at head 001_discovery_v1_agent

SMOKE: PASS
```

## Interpreting failures

| Failure | Likely cause | Action |
|---------|--------------|--------|
| health FAIL (000) | service down / wrong host/port | check process & logs; do not promote |
| db FAIL (connection error) | wrong DSN / DB unreachable / bad creds | verify secret + network |
| db FAIL (missing tables) | migrations not applied | run `infrastructure/scripts/migrate.sh` |
| migrations FAIL (multiple heads) | un-merged Alembic branch | add a merge revision before release |
| migrations FAIL (db not at head) | migration step skipped | re-run migrations; re-validate |

## Wiring into CI/CD

Add a post-deploy job that runs `scripts/smoke/run_smoke.sh` against the freshly deployed environment and **blocks promotion** on non-zero exit. Pair with the Release Runbook gate.

## Validation status

Run locally against the dev stack (api-service + seeded `wise`): **SMOKE: PASS** (health, database, all four migration heads). See `docs/implementation/setup-agent-v2-report.md`.

---

*Operational runbook. Does not modify Architecture v1.0, governance, ADRs, or the Agent Registry.*
