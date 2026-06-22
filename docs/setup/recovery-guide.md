# Recovery Guide

| Field | Value |
|-------|-------|
| **Status** | Operational documentation (non-governance) |
| **Date** | 2026-06-22 |
| **Scope** | Restoring WISE from backups after data loss, corruption, or environment loss |
| **Authority** | Companion to `backup-guide.md`, `rollback-runbook.md`. Does not modify Architecture v1.0, governance, ADRs, or the Agent Registry. |

## 1. Decision tree

| Situation | Procedure |
|-----------|-----------|
| Bad release / code regression | **Rollback runbook** (redeploy previous image) — not this guide |
| Bad migration | §4 (downgrade or restore) |
| DB corruption / loss | §2 (PostgreSQL restore) |
| Object store loss | §3 (MinIO restore) |
| Whole environment lost | §5 (full rebuild) |

## 2. PostgreSQL restore

1. Provision/clean target and ensure extensions exist:
   ```bash
   sudo -u postgres psql -c "DROP DATABASE IF EXISTS wise;" -c "CREATE DATABASE wise OWNER wise;"
   sudo -u postgres psql -q -d wise -f infrastructure/docker/postgres/init/01-extensions.sql
   ```
2. Restore the latest good dump (custom format):
   ```bash
   PGPASSWORD=wise pg_restore -h localhost -U wise -d wise --no-owner --clean --if-exists \
     backups/wise_<timestamp>.dump
   ```
3. Verify:
   ```bash
   PGPASSWORD=wise psql -h localhost -U wise -d wise -tAc \
     "SELECT count(*) FROM registry.sources; SELECT count(*) FROM discovery.records;"
   ```
   Then restart `api-service` and confirm `GET /v1/objects/stonehenge` returns 200.

**PITR variant:** restore the base backup, then replay WAL to the target time (`recovery_target_time`).

## 3. MinIO restore

```bash
mc alias set wise http://localhost:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD"
mc mb --ignore-existing wise/wise-preservation
mc mirror --overwrite backups/minio/wise-preservation wise/wise-preservation
```
Cross-check object counts/fixity against PREMIS records in PostgreSQL (`preservation.premis_events`).

## 4. Migration recovery

- **Roll forward (preferred):** fix and apply a new migration.
- **Downgrade:** `cd packages/<pkg> && alembic downgrade -1` (set `WISE_DATABASE_URL`). ⚠️ Some downgrades are known-incomplete (e.g. the registry v1.1 provenance downgrade leaves `previous_event_id` — see `docs/implementation/rc0-stabilization-report.md` and `rc13-portfolio-rescore.md`). For schema corruption, prefer a **restore from dump** (§2) over downgrade.
- After any migration recovery, run `python scripts/validate_alembic_heads.py` (single head) and the smoke tests.

## 5. Full environment rebuild

1. **Dependencies:** run the bootstrap (Local Development Guide §2) or `docker compose up --build`.
2. **Data plane:** start PostgreSQL (PostGIS + pgvector), Redis, MinIO, OpenSearch.
3. **Schema:** apply `01-extensions.sql`.
4. **Data:** restore PostgreSQL (§2) and MinIO (§3) from backups. If no backup exists (dev), re-seed via `infrastructure/scripts/migrate.sh`.
5. **Services:** start upstream services, then `api-service`; wait for `/health`.
6. **Validate:** run the post-recovery checklist (§6).

## 6. Post-recovery validation checklist

- [ ] All six `/health` endpoints return 200
- [ ] `registry.sources` and `discovery.records` row counts match expectation
- [ ] `GET /v1/objects/stonehenge` → 200 (RC1 aggregate intact)
- [ ] `GET /v1/map/search?bbox=-82,25,-80,26` → 200 (PostGIS intact)
- [ ] MinIO object count / fixity reconciles with PREMIS events
- [ ] `scripts/validate_alembic_heads.py` → single head
- [ ] `pytest tests/ -m smoke` → green

## 7. Targets

| Metric | Target |
|--------|--------|
| RPO | ≤ 24h (daily dump) · minutes (PITR) |
| RTO | ≤ 1h (single DB restore) · ≤ 4h (full rebuild) |

Record actuals from each restore drill and update these targets.

---

*Operational documentation. Does not modify Architecture v1.0, governance, ADRs, or the Agent Registry.*
