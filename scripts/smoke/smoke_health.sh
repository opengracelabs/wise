#!/usr/bin/env bash
# Deploy-time smoke test: verify service /health endpoints.
#
# Config (env):
#   SMOKE_HOST       host to probe (default: localhost)
#   SMOKE_SERVICES   space-separated name:port pairs to require
#                    (default: "api-service:8000")
#                    Full stack example:
#                    SMOKE_SERVICES="api-service:8000 discovery-service:8001 \
#                      metadata-service:8002 preservation-service:8003 \
#                      knowledge-graph-service:8004 orchestrator-service:8005"
set -uo pipefail

HOST="${SMOKE_HOST:-localhost}"
SERVICES="${SMOKE_SERVICES:-api-service:8000}"
body="$(mktemp)"
trap 'rm -f "$body"' EXIT
fail=0

for svc in $SERVICES; do
  name="${svc%%:*}"; port="${svc##*:}"
  url="http://${HOST}:${port}/health"
  code="$(curl -s -m 5 -o "$body" -w '%{http_code}' "$url" 2>/dev/null || echo 000)"
  if [ "$code" = "200" ] && grep -q '"status":"ok"' "$body"; then
    echo "PASS  ${name} (${url}) -> 200 ok"
  else
    echo "FAIL  ${name} (${url}) -> ${code}"
    fail=1
  fi
done

exit "$fail"
