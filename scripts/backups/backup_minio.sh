#!/usr/bin/env bash
# WISE MinIO backup — mirror the preservation bucket + retention pruning.
#
# Env:
#   MINIO_ENDPOINT     endpoint URL (default: http://localhost:9000)
#   MINIO_ACCESS_KEY / MINIO_ROOT_USER       access key (default: wise)
#   MINIO_SECRET_KEY / MINIO_ROOT_PASSWORD   secret key (default: wise-minio-secret)
#   MINIO_BUCKET       bucket (default: wise-preservation)
#   BACKUP_DIR         output dir (default: backups/minio)
#   RETENTION_DAYS     prune snapshots older than N days (default: 30)
#
# Requires the MinIO client `mc`. In production prefer bucket VERSIONING and
# cross-region replication in addition to (or instead of) local mirroring.
set -euo pipefail

ENDPOINT="${MINIO_ENDPOINT:-http://localhost:9000}"
case "$ENDPOINT" in http*://*) ;; *) ENDPOINT="http://${ENDPOINT}" ;; esac
ACCESS="${MINIO_ACCESS_KEY:-${MINIO_ROOT_USER:-wise}}"
SECRET="${MINIO_SECRET_KEY:-${MINIO_ROOT_PASSWORD:-wise-minio-secret}}"
BUCKET="${MINIO_BUCKET:-wise-preservation}"
BACKUP_DIR="${BACKUP_DIR:-backups/minio}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"

if ! command -v mc >/dev/null 2>&1; then
  echo "[backup_minio] ERROR: MinIO client 'mc' not found." >&2
  echo "[backup_minio] install: https://min.io/docs/minio/linux/reference/minio-mc.html" >&2
  exit 3
fi

mkdir -p "$BACKUP_DIR"
mc alias set wisebak "$ENDPOINT" "$ACCESS" "$SECRET" >/dev/null
ts="$(date +%Y%m%dT%H%M%S)"
dest="$BACKUP_DIR/$ts"

echo "[backup_minio] mirroring ${ENDPOINT}/${BUCKET} -> $dest"
mc mirror --overwrite "wisebak/${BUCKET}" "$dest"
echo "[backup_minio] snapshot complete: $dest"

# Retention: remove timestamped snapshot dirs older than N days.
find "$BACKUP_DIR" -mindepth 1 -maxdepth 1 -type d -mtime +"$RETENTION_DAYS" -print -exec rm -rf {} +
echo "[backup_minio] pruned snapshots older than ${RETENTION_DAYS} days"
