#!/usr/bin/env bash
# Run all deploy-time smoke checks (health + database + migrations).
# Aggregates exit codes: 0 = all PASS, non-zero = at least one FAIL.
#
# Usage:
#   scripts/smoke/run_smoke.sh
# Env: see smoke_health.sh, smoke_db.py, smoke_migrations.py
set -uo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
rc=0

echo "== health =="
bash "$here/smoke_health.sh" || rc=1
echo
echo "== database =="
python3 "$here/smoke_db.py" || rc=1
echo
echo "== migrations =="
python3 "$here/smoke_migrations.py" || rc=1

echo
if [ "$rc" -eq 0 ]; then
  echo "SMOKE: PASS"
else
  echo "SMOKE: FAIL"
fi
exit "$rc"
