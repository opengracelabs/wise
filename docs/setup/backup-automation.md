# Backup Automation

| Field | Value |
|-------|-------|
| **Status** | Operational documentation (non-governance) |
| **Date** | 2026-06-22 |
| **Scope** | Automated backups via `scripts/backups/` (PostgreSQL + MinIO) with retention |
| **Authority** | Companion to `docs/setup/backup-guide.md` (concepts), `docs/setup/recovery-guide.md`, `docs/implementation/recovery-test-plan.md`. Does not modify Architecture v1.0, governance, ADRs, or the Agent Registry. |

This automates the procedures described in `backup-guide.md`.

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/backups/backup_postgres.sh` | `pg_dump` (custom format) + verify + retention prune |
| `scripts/backups/backup_minio.sh` | `mc mirror` of the preservation bucket + retention prune |
| `scripts/backups/retention.example.cron` | Example crontab wiring both with retention windows |

All scripts are executable (`chmod +x`) and configured entirely by environment variables.

## PostgreSQL — `backup_postgres.sh`

```bash
WISE_DATABASE_URL=postgresql://wise:wise@localhost:5432/wise \
BACKUP_DIR=/var/backups/wise/postgres \
RETENTION_DAYS=30 \
  scripts/backups/backup_postgres.sh
```

- Writes `wise_<UTC-timestamp>.dump` (custom format, `-Fc`, `--no-owner`).
- **Verifies** the dump is readable (`pg_restore --list`) before trusting it; exits non-zero on failure.
- Strips a `+psycopg` driver suffix so the SQLAlchemy DSN works with libpq/`pg_dump`.
- Prunes dumps older than `RETENTION_DAYS`.

**Env:** `WISE_DATABASE_URL`/`DATABASE_URL` (default `postgresql://wise:wise@localhost:5432/wise`), `BACKUP_DIR` (default `backups/postgres`), `RETENTION_DAYS` (default 30).

## MinIO — `backup_minio.sh`

```bash
MINIO_ENDPOINT=http://minio-host:9000 \
MINIO_ACCESS_KEY=... MINIO_SECRET_KEY=... MINIO_BUCKET=wise-preservation \
BACKUP_DIR=/var/backups/wise/minio RETENTION_DAYS=30 \
  scripts/backups/backup_minio.sh
```

- Mirrors the bucket into a timestamped snapshot directory (`mc mirror --overwrite`).
- Requires the MinIO client `mc`; if absent it exits `3` with install instructions (verified behavior).
- Normalizes a scheme-less `MINIO_ENDPOINT` to `http://`.
- Prunes snapshot dirs older than `RETENTION_DAYS`.

> Production: also enable **bucket versioning** and **cross-region replication** (05-physical-architecture §3). Local mirroring is the floor, not the ceiling, for preservation data.

## Scheduling

Install `scripts/backups/retention.example.cron` (adjust paths/secrets):

```cron
0 2 * * *   cd /opt/wise && RETENTION_DAYS=30 BACKUP_DIR=/var/backups/wise/postgres scripts/backups/backup_postgres.sh >> /var/log/wise-backup.log 2>&1
30 2 * * *  cd /opt/wise && RETENTION_DAYS=30 BACKUP_DIR=/var/backups/wise/minio    scripts/backups/backup_minio.sh    >> /var/log/wise-backup.log 2>&1
0 3 * * 0   cd /opt/wise && RETENTION_DAYS=365 BACKUP_DIR=/var/backups/wise/postgres-weekly scripts/backups/backup_postgres.sh >> /var/log/wise-backup.log 2>&1
```

Alternatives: a systemd timer, a Kubernetes `CronJob`, or an n8n scheduled workflow (`infrastructure/n8n/`). Secrets come from the environment/secrets manager, never the crontab itself.

## Retention policy (recommended)

| Backup | Frequency | Retention |
|--------|-----------|-----------|
| Postgres logical dump | daily | 30 days |
| Postgres weekly dump | weekly | 365 days |
| Postgres base backup + WAL (PITR, prod) | continuous + weekly base | 90 days |
| MinIO mirror / versioning | daily / continuous | per preservation policy |

## Validation

- Both scripts are executable and run from the repo root.
- `backup_postgres.sh` validated locally: produced a verified ~128K dump of the `wise` database and pruned correctly.
- `backup_minio.sh` validated to fail clean (exit 3) when `mc` is not installed.
- Restore is exercised separately by `docs/implementation/recovery-test-plan.md`.

## Monitoring backups

- Alert if no successful dump in 24h (check newest file mtime in `BACKUP_DIR`).
- Alert on non-zero exit (the cron `>> log` captures stderr).
- Track backup size trend; a sudden drop may signal a partial dump.

---

*Operational documentation. Does not modify Architecture v1.0, governance, ADRs, or the Agent Registry.*
