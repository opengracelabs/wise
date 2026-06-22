#!/usr/bin/env bash
# WISE PostgreSQL backup — logical dump (custom format) + retention pruning.
#
# Env:
#   WISE_DATABASE_URL / DATABASE_URL  connection DSN
#                                     (default: postgresql://wise:wise@localhost:5432/wise)
#   BACKUP_DIR                        output dir (default: backups/postgres)
#   RETENTION_DAYS                    prune dumps older than N days (default: 30)
#
# Notes:
#   - pg_dump uses libpq URIs, so any "+psycopg" driver suffix is stripped.
#   - Custom format (-Fc) supports selective/parallel restore (see recovery-guide.md).
set -euo pipefail

DSN="${WISE_DATABASE_URL:-${DATABASE_URL:-postgresql://wise:wise@localhost:5432/wise}}"
DSN="${DSN/+psycopg/}"                       # libpq does not understand the SQLAlchemy driver suffix
BACKUP_DIR="${BACKUP_DIR:-backups/postgres}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"

mkdir -p "$BACKUP_DIR"
ts="$(date +%Y%m%dT%H%M%S)"
out="$BACKUP_DIR/wise_${ts}.dump"

echo "[backup_postgres] dumping -> $out"
pg_dump -Fc --no-owner "$DSN" -f "$out"
echo "[backup_postgres] wrote $out ($(du -h "$out" | cut -f1))"

# Validate the dump is readable before trusting it.
if pg_restore --list "$out" >/dev/null 2>&1; then
  echo "[backup_postgres] verified: dump is readable"
else
  echo "[backup_postgres] ERROR: dump failed verification" >&2
  exit 1
fi

# Retention.
pruned="$(find "$BACKUP_DIR" -name 'wise_*.dump' -type f -mtime +"$RETENTION_DAYS" -print -delete | wc -l)"
echo "[backup_postgres] pruned $pruned dump(s) older than ${RETENTION_DAYS} days"
