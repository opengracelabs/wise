# Secrets Management

| Field | Value |
|-------|-------|
| **Status** | Operational documentation (non-governance) |
| **Date** | 2026-06-22 |
| **Scope** | How WISE secrets are stored, injected, rotated and recovered across local, CI and deployment |
| **Authority** | Companion to `docs/setup/deployment-guide.md`, `.env.example`. Does not modify Architecture v1.0, governance, ADRs, or the Agent Registry. |

## Principles

1. **No secret in git.** `.gitignore` excludes `.env`; only `.env.example` (placeholder values) is committed.
2. **Least privilege & scoping.** Each environment gets its own credentials; never share prod secrets with dev/CI.
3. **Server-side only.** Database, MinIO, and internal tokens are server-scoped. Never expose them to the browser/experience plane (no `NEXT_PUBLIC_*`).
4. **Rotatable.** Every secret has an owner, a store, and a rotation procedure (below).

## Inventory

| Secret | Used by | Notes |
|--------|---------|-------|
| `POSTGRES_PASSWORD` / DSN in `WISE_DATABASE_URL` | all services | psycopg3 DSN (`postgresql+psycopg://`) |
| `MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD` (`MINIO_ACCESS_KEY`/`MINIO_SECRET_KEY`) | preservation-service, backups | object storage |
| `OPENSEARCH_INITIAL_ADMIN_PASSWORD` | knowledge-graph-service | search |
| `REDIS_URL` (if auth) | discovery-service | cache/queue |
| `REVALIDATION_SECRET` | experience plane (future) | HMAC for ISR webhook |
| Provider keys (`STRIPE_SECRET_KEY`, POD keys) | commerce (Phase 12, future) | payments/fulfilment |
| Registry/deploy tokens | CI/CD | image push, deploy |

See `.env.example` for the full variable list and defaults.

## 1. Local secrets

- Copy the template and edit locally: `cp .env.example .env`. `.env` is git-ignored.
- Dev defaults (`wise`/`wise`, `wise-minio-secret`) are **non-secret placeholders** for local only — never reuse them beyond a developer machine.
- Do not commit `.env`; do not paste secrets into code, notebooks, or chat.
- For the Cursor Cloud VM, real secrets are injected as environment variables from the **Secrets** panel (personal/team/repo scoped), not stored in the repo.

## 2. CI secrets

- Store in **GitHub Actions encrypted secrets** (repo or org/environment scope); reference as `${{ secrets.NAME }}`.
- `.github/workflows/ci.yml` uses an ephemeral PostgreSQL with throwaway credentials — no production secret is needed for tests.
- Add deployment/registry secrets (image push, deploy token) as **Environment secrets** with required reviewers on the `production` environment.
- Never `echo` a secret in a workflow; mask with `::add-mask::` if a value must transit a step.

## 3. Deployment secrets

- Use a managed **secrets manager** (e.g. cloud KMS/Secrets Manager, Vault) as the source of truth; inject at runtime as env vars into containers.
- Per-environment separation: distinct credentials for `production`, `preview/staging`, `development`.
- The platform plane holds DB/MinIO/search secrets; the experience plane (Vercel) holds only its own server-scoped vars (`WISE_API_BASE_URL`, `REVALIDATION_SECRET`, …) — **never** the database URL.
- Restrict who can read prod secrets; log access.

## 4. Rotation process

Rotate on a schedule (≥ every 90 days) and immediately on suspected exposure.

1. **Generate** a new credential in the managing store (DB role password, MinIO key pair, token).
2. **Add alongside the old** (dual-credential window) where the system supports it:
   - PostgreSQL: `ALTER ROLE wise WITH PASSWORD '<new>';` then update the DSN in the secrets manager.
   - MinIO: create a new service account/key, deploy it, then disable the old key.
3. **Roll out** the new value to each environment (update secrets manager → restart/redeploy services to pick up new env).
4. **Verify** with the smoke suite: `scripts/smoke/run_smoke.sh` (health + DB connectivity confirms the new DSN works).
5. **Revoke** the old credential.
6. **Record** the rotation (date, secret, operator) in the ops log.

> Prefer credentials the app reads from env at startup so rotation is "update secret + restart", not a code change.

## 5. Recovery process (lost/compromised secret)

1. **Contain:** revoke the compromised credential immediately at the source (DB role, MinIO key, token).
2. **Reissue:** generate a replacement (Rotation §1–3).
3. **Restore access:** redeploy services with the new value; run `scripts/smoke/run_smoke.sh` to confirm connectivity.
4. **Assess blast radius:** review access logs; if data exposure is possible, follow the incident process and (for preservation data) verify fixity against PREMIS records.
5. **Backups:** if backup credentials were affected, rotate them and re-validate a restore drill (`docs/implementation/recovery-test-plan.md`).
6. **Post-mortem:** document cause and add a guard (e.g. secret scanning, tighter scoping).

## Guardrails

- Enable **secret scanning** / push protection on the repository.
- CI must fail if a secret-shaped string is committed.
- Never store secrets in `data/`, `content/`, or any committed file; keep them in the manager/`.env`.

---

*Operational documentation. Does not modify Architecture v1.0, governance, ADRs, or the Agent Registry.*
