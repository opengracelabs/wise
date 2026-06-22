# Rollback Runbook

| Field | Value |
|-------|-------|
| **Status** | Operational runbook (non-governance) |
| **Date** | 2026-06-22 |
| **Scope** | Reverting a WISE release that failed verification or caused an incident |
| **Authority** | Companion to `docs/runbooks/release-runbook.md`, `docs/setup/recovery-guide.md`. Does not modify Architecture v1.0, governance, ADRs, or the Agent Registry. |

## When to use
A release failed post-deploy verification (Release Runbook §5), or an incident is traced to the latest deploy. **Default action: roll the code/images back to the previous known-good tag.** Schema changes get special handling (§3).

## 0. Triage (≤ 5 min)
- [ ] Confirm the regression correlates with the latest deploy (timing, logs, `/health`, error rate).
- [ ] Identify whether the release included a **migration**. If yes, read §3 before reverting.
- [ ] Notify on-call / reviewer; start an incident note.

## 1. Roll back services (code/images)
```bash
# redeploy the previous known-good image tag for each affected service,
# api-service LAST is fine on rollback too; order is not critical when reverting to a known-good set
# (deploy upstream services first if the previous set changed their contracts)
```
- Roll back **all** services that changed in the bad release to the matching previous tag (avoid mixed versions).
- Wait for `/health` = 200 on each.

## 2. Verify the rollback
```bash
for p in 8000 8001 8002 8003 8004 8005; do curl -fs http://<host>:$p/health && echo " ok:$p"; done
curl -fs http://<host>:8000/v1/objects/stonehenge | head -c 80
```
- [ ] All services healthy on the previous version.
- [ ] RC1/RC2/RC3 aggregates 200; error rate back to baseline.

## 3. Database migrations (handle with care)
Schema is the hard part. Decision order:

1. **Backward-compatible migration?** (new tables/columns only) — the previous code runs fine against the new schema. **Leave the schema in place**; just roll back code. Preferred.
2. **Breaking migration + clean downgrade exists?** `cd packages/<pkg> && alembic downgrade -1` (with `WISE_DATABASE_URL` set), then `python scripts/validate_alembic_heads.py`.
3. **Breaking migration + downgrade unsafe/incomplete?** Some downgrades are known-incomplete (e.g. registry v1.1 leaves `previous_event_id` — see `docs/implementation/rc0-stabilization-report.md`). In that case **restore the pre-migration dump** per `docs/setup/recovery-guide.md` §2.

> Always prefer additive, backward-compatible migrations precisely so that code rollback never requires a schema downgrade.

## 4. Post-rollback
- [ ] Confirm data integrity (`registry.sources`, `discovery.records` counts; MinIO/PREMIS reconcile if preservation was touched).
- [ ] `pytest tests/ -m smoke` (if a test environment mirrors prod) → green.
- [ ] Close the maintenance window; resume normal monitoring.

## 5. Follow-up
- [ ] Record root cause in the incident note.
- [ ] File the fix; do **not** re-attempt the release until CI is green and the failure is understood.
- [ ] If the failure was a schema/downgrade gap, add a forward-fix migration and a restore-tested backup before retrying.

---

*Operational runbook. Does not modify Architecture v1.0, governance, ADRs, or the Agent Registry.*
