# Release Runbook

| Field | Value |
|-------|-------|
| **Status** | Operational runbook (non-governance) |
| **Date** | 2026-06-22 |
| **Scope** | Cutting and deploying a WISE platform release |
| **Authority** | Companion to `docs/setup/deployment-guide.md`, `.github/workflows/ci.yml`. Does not modify Architecture v1.0, governance, ADRs, or the Agent Registry. |

> A runbook is a checklist to execute under change-control or incident pressure. Work top to bottom; do not skip the pre-flight gate.

## Roles
- **Release driver** — executes the steps.
- **Reviewer / on-call** — verifies the gate and stands by for rollback.

## 1. Pre-flight gate (must all be true)
- [ ] CI green on the release commit (`lint-and-test` **and** `docker-build` jobs in `.github/workflows/ci.yml`).
- [ ] `python scripts/validate_alembic_heads.py` → single head.
- [ ] Backups current (see `docs/setup/backup-guide.md`): a fresh PostgreSQL dump and MinIO mirror exist.
- [ ] Release notes / changelog prepared; migration list identified (any new Alembic revisions?).
- [ ] Rollback target identified: the previous known-good image tag(s) and DB state.
- [ ] Maintenance window agreed (if a migration is non-additive).

## 2. Build & tag
```bash
docker compose build api-service discovery-service metadata-service \
                     preservation-service knowledge-graph-service orchestrator-service
# tag images with the release version, e.g. v0.x.y, and push to the registry
```

## 3. Database migration (if any)
```bash
export WISE_DATABASE_URL=postgresql+psycopg://<user>:<pass>@<host>:5432/wise
infrastructure/scripts/migrate.sh      # registry -> reference -> metadata -> discovery
python scripts/validate_alembic_heads.py
```
- Take a **pre-migration dump** immediately before this step.
- Additive migrations (new tables/columns) are safe online. For non-additive changes, use the maintenance window.

## 4. Deploy (rolling)
1. Deploy upstream services first: `discovery`, `metadata`, `preservation`, `knowledge-graph`, `orchestrator`.
2. Wait for each `/health` = 200.
3. Deploy `api-service` last (it depends on the others).
4. If an experience-plane app exists (`apps/nature-culture-web`), promote the Vercel build after the gateway is healthy.

## 5. Post-deploy verification
```bash
for p in 8000 8001 8002 8003 8004 8005; do curl -fs http://<host>:$p/health && echo " ok:$p"; done
curl -fs http://<host>:8000/v1/objects/stonehenge      | head -c 80    # RC1 aggregate 200
curl -fs "http://<host>:8000/v1/map/search?bbox=-82,25,-80,26"          # PostGIS 200
```
- [ ] All six services healthy.
- [ ] RC1/RC2/RC3 read aggregates return 200 with expected fields.
- [ ] Error rate and latency normal (see `docs/setup/monitoring-guide.md`).
- [ ] No migration drift.

## 6. Sign-off
- [ ] Reviewer confirms verification passed.
- [ ] Release tagged and recorded; changelog published.
- [ ] Monitor for one observation window; keep the rollback target ready.

## 7. If verification fails
Go directly to `docs/runbooks/rollback-runbook.md`. Do not attempt forward fixes under pressure unless the fix is trivial and reviewed.

---

*Operational runbook. Does not modify Architecture v1.0, governance, ADRs, or the Agent Registry.*
