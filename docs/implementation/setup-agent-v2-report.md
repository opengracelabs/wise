# Setup Agent v2 — Report

| Field | Value |
|-------|-------|
| **Status** | Implementation report (non-governance) |
| **Date** | 2026-06-22 |
| **Scope** | Close the operational gaps from Setup Agent v1: secrets, backup automation, deploy-time smoke tests, observability plan, recovery testing |
| **Constraints** | Does **not** modify Architecture v1.0, Governance, ADRs, the Agent Registry, or the canonical architecture. No new agent registered. |

## What v1 left open (and how v2 closes it)

| v1 gap | v2 deliverable | Status |
|--------|----------------|--------|
| Secrets management not formalized | `docs/setup/secrets-management.md` | ✅ documented (local/CI/deploy/rotate/recover) |
| No automated backup jobs | `scripts/backups/` + `docs/setup/backup-automation.md` | ✅ implemented + validated |
| No deploy-time smoke automation | `scripts/smoke/` + `docs/runbooks/deployment-validation.md` | ✅ implemented + **passing** |
| Observability stack not deployed | `docs/setup/observability-stack.md` | ✅ deployment plan |
| Recovery not tested | `docs/implementation/recovery-test-plan.md` | ✅ plan + T1 restore validated |

## Deliverables

### Scripts (executable)
| Path | Purpose |
|------|---------|
| `scripts/smoke/smoke_health.sh` | `/health` checks (configurable services) |
| `scripts/smoke/smoke_db.py` | DB connectivity + required tables |
| `scripts/smoke/smoke_migrations.py` | single Alembic head + DB at head, per package |
| `scripts/smoke/run_smoke.sh` | aggregate runner (exit 0 = all PASS) |
| `scripts/backups/backup_postgres.sh` | `pg_dump` (custom) + verify + retention |
| `scripts/backups/backup_minio.sh` | `mc mirror` bucket + retention |
| `scripts/backups/retention.example.cron` | example schedule wiring |

### Docs
| Path | Purpose |
|------|---------|
| `docs/setup/secrets-management.md` | secrets across local/CI/deploy + rotation + recovery |
| `docs/setup/backup-automation.md` | how to run/schedule the backup scripts |
| `docs/runbooks/deployment-validation.md` | run the smoke gate |
| `docs/setup/observability-stack.md` | OTel/Prometheus/Grafana/Loki deployment plan |
| `docs/implementation/recovery-test-plan.md` | restore tests, DR drills, RPO/RTO |
| `docs/implementation/setup-agent-v2-report.md` | this report |

---

## Validation results

### 1. Documentation complete — ✅ PASS
All five requested topics plus this report are present and cross-linked. Each carries the non-modification banner.

### 2. Scripts executable — ✅ PASS
All scripts are `chmod +x` and configured purely by environment variables (no hard-coded secrets).

### 3. Smoke tests pass — ✅ PASS
`scripts/smoke/run_smoke.sh` against the live dev stack (api-service + seeded `wise`):

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
SMOKE: PASS   (exit 0)
```
(Applied the metadata migration to the dev `wise` DB so all four packages report a clean head.)

### 4. Backup automation — ✅ PASS
`backup_postgres.sh` produced a verified ~128K custom-format dump of `wise` (`pg_restore --list` check) and pruned by retention. `backup_minio.sh` exits `3` with install guidance when `mc` is absent (verified graceful degradation).

### 5. Recovery test (T1) — ✅ PASS
End-to-end: backup → restore into a scratch `wise_restore` (extensions + `pg_restore`) → validated with `smoke_db.py` + `smoke_migrations.py` (`SMOKE_REQUIRE_MIGRATED=1`):
```
PASS  database connectivity + required tables present
PASS  wise-registry/reference/metadata/discovery: at head   (exit 0)
```
Scratch DB dropped after the drill.

---

## Findings

1. **The deploy gate is now scriptable.** `run_smoke.sh` gives a single exit code suitable for blocking CI/CD promotion (Deployment Validation runbook).
2. **Backups are real and self-verifying.** The Postgres script refuses to trust an unreadable dump; restore is proven by reusing the same smoke checks.
3. **Environment honesty preserved.** MinIO backup and the observability stack can't run in this Docker-less VM; both are documented to run where `mc`/containers exist, and the scripts degrade cleanly.
4. **No protected surface touched.** Only `scripts/` and `docs/` changed; no architecture/governance/ADR/registry edits.

## Remaining gaps / next actions

| Item | Action |
|------|--------|
| Scheduled backups in a real environment | install `retention.example.cron` (or systemd/K8s CronJob/n8n) where Postgres+MinIO run |
| PITR (WAL archiving) | enable in production for minute-level RPO |
| Observability stack | execute the rollout phases in `observability-stack.md` (start with infra exporters) |
| Smoke gate in CI/CD | add a post-deploy job running `scripts/smoke/run_smoke.sh`, blocking on failure |
| Secrets manager | adopt a managed store + enable repo secret scanning/push protection |
| DR drills | begin the quarterly cadence in `recovery-test-plan.md`; record RPO/RTO actuals |
| `mc` availability | install the MinIO client on backup hosts to enable object-store backups |

---

*Implementation report. Does not modify Architecture, Governance, ADRs, the Agent Registry, or the canonical architecture. Companion: `docs/setup/`, `docs/runbooks/`, `scripts/`.*
