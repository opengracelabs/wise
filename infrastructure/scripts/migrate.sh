#!/usr/bin/env bash
# Apply all WISE database migrations (registry + reference capability 1).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

export WISE_DATABASE_URL="${WISE_DATABASE_URL:-${DATABASE_URL:-postgresql+psycopg://wise:wise@localhost:5432/wise}}"

echo "Applying Source Registry migrations..."
(cd "$ROOT/packages/wise-registry" && alembic upgrade head)

echo "Applying Reference Capability migrations (RC1–RC3)..."
(cd "$ROOT/packages/wise-reference" && alembic upgrade head)

echo "Applying Metadata Agent migrations..."
(cd "$ROOT/packages/wise-metadata" && alembic upgrade head)

echo "Applying Source Discovery Agent migrations..."
(cd "$ROOT/packages/wise-discovery" && alembic upgrade head)

echo "Migrations complete."
