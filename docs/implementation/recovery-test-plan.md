# Recovery Test Plan

| Field | Value |
|-------|-------|
| **Status** | Implementation plan (non-governance) |
| **Date** | 2026-06-22 |
| **Scope** | Backup-restore tests, disaster-recovery drills, and RPO/RTO targets for WISE |
| **Authority** | Companion to `docs/setup/backup-guide.md`, `docs/setup/backup-automation.md`, `docs/setup/recovery-guide.md`. Does not modify Architecture v1.0, governance, ADRs, or the Agent Registry. |

A backup is only real if a restore is tested. This plan defines the tests, their cadence, and the targets they must meet.

## 1. Objectives

| Target | Definition | Goal |
|--------|------------|------|
| **RPO** (Recovery Point Objective) | Max acceptable data loss | ≤ 24h (daily logical dump); minutes with PITR |
| **RTO** (Recovery Time Objective) | Max acceptable downtime | ≤ 1h (single-DB restore); ≤ 4h (full rebuild) |

Record actuals from every drill and revise targets as the system grows.

## 2. Backup-restore tests

### T1 — PostgreSQL logical restore (monthly)
1. Produce a backup: `scripts/backups/backup_postgres.sh` (`BACKUP_DIR`, `WISE_DATABASE_URL` set).
2. Restore into a scratch DB:
   ```bash
   sudo -u postgres psql -c "DROP DATABASE IF EXISTS wise_restore;" -c "CREATE DATABASE wise_restore OWNER wise;"
   sudo -u postgres psql -q -d wise_restore -f infrastructure/docker/postgres/init/01-extensions.sql
   PGPASSWORD=wise pg_restore -h localhost -U wise -d wise_restore --no-owner --clean --if-exists "$BACKUP_DIR"/wise_<ts>.dump
   ```
3. Validate with the smoke suite pointed at the restored DB:
   ```bash
   WISE_DATABASE_URL=postgresql+psycopg://wise:wise@localhost:5432/wise_restore SMOKE_REQUIRE_MIGRATED=1 \
     python3 scripts/smoke/smoke_db.py && \
   WISE_DATABASE_URL=postgresql+psycopg://wise:wise@localhost:5432/wise_restore SMOKE_REQUIRE_MIGRATED=1 \
     python3 scripts/smoke/smoke_migrations.py
   ```
   **Pass:** required tables present, all four packages at head, row counts match the source.
4. Record restore duration (contributes to RTO).

### T2 — MinIO restore (monthly, where MinIO is deployed)
1. `scripts/backups/backup_minio.sh` to snapshot the bucket.
2. Restore into a scratch bucket (`mc mirror <snapshot> wisebak/wise-preservation-restore`).
3. Reconcile object count + fixity against `preservation.premis_events`.

### T3 — PITR replay (quarterly, production)
With WAL archiving + base backup, restore to a target time (`recovery_target_time`) and confirm the chosen RPO is achievable.

## 3. Disaster-recovery drills

### D1 — Single database loss (quarterly)
Simulate DB loss; execute `recovery-guide.md` §2; validate via smoke. Measure RTO.

### D2 — Object store loss (quarterly, where deployed)
Simulate bucket loss; execute `recovery-guide.md` §3; reconcile fixity.

### D3 — Full environment rebuild (semi-annual)
From nothing: bootstrap deps → data plane → `01-extensions.sql` → restore Postgres + MinIO → start services → run `scripts/smoke/run_smoke.sh`. This is the end-to-end RTO test.

### D4 — Bad migration (quarterly)
Apply a deliberately broken migration on a scratch DB; practice the Rollback Runbook §3 decision (roll-forward vs downgrade vs restore). Confirms the documented handling of incomplete downgrades.

## 4. Acceptance criteria (every drill)

- [ ] `scripts/smoke/run_smoke.sh` (or its DB/migration parts) → PASS on the recovered system
- [ ] `GET /v1/objects/stonehenge` → 200; `GET /v1/map/search?bbox=-82,25,-80,26` → 200
- [ ] Row counts / object fixity reconcile with the source
- [ ] Measured RPO ≤ target and RTO ≤ target
- [ ] Result logged (date, scenario, durations, issues, follow-ups)

## 5. Schedule & ownership

| Test | Cadence | Owner |
|------|---------|-------|
| T1 Postgres restore | monthly | Platform on-call |
| T2 MinIO restore | monthly (when deployed) | Platform on-call |
| T3 PITR | quarterly (prod) | Platform lead |
| D1/D2/D4 drills | quarterly | Platform on-call |
| D3 full rebuild | semi-annual | Platform lead + reviewer |

Track drills against `scripts/backups/retention.example.cron` (which includes a quarterly drill reminder).

## 6. Current status

- **Backup scripts:** implemented and validated (`backup_postgres.sh` produced a verified dump; `backup_minio.sh` degrades cleanly without `mc`).
- **Restore validation tooling:** reuses `scripts/smoke/` (DB + migration checks), which currently PASSes against the live dev DB.
- **Not yet automated:** scheduled drills and PITR (require a deployed environment with WAL archiving) — tracked as next actions in `setup-agent-v2-report.md`.

---

*Implementation plan. Does not modify Architecture v1.0, governance, ADRs, or the Agent Registry.*
