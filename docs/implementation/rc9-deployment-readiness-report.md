# RC9 Deployment Readiness Report

| Field | Value |
|-------|-------|
| **Status** | Implementation review (non-governance) |
| **Date** | 2026-06-22 |
| **Scope** | Build process, environment variables, Vercel readiness, route coverage, broken links, static assets |
| **Method** | Static review of the repository at `architecture-v1.0`; live checks against the local `api-service` |
| **Constraints** | Does not modify Architecture v1.0, governance, ADRs, or agents (ADR-011) |

## Verdict

| Deployable unit | Verdict |
|-----------------|---------|
| **`api-service` + `apps/demonstration-surface`** (Founder preview) | **READY** — builds, serves, all RC1-RC3 routes return 200 (post-RC0 fixes) |
| **`apps/nature-culture-web`** (public Experience Plane) | **NOT READY** — application does not exist yet (design only) |
| **Vercel project** | **NOT READY** — no `vercel.json`, no `package.json`, no web app to deploy |
| **Commerce / storefront** | **NOT READY** — no implementation (Phase 12) |

The Founder Demonstration Surface is shippable today as part of the `api-service` container. The public web app and storefront are pre-implementation; this report lists exactly what exists and what each gap requires.

---

## 1. Build process

| Component | Build | State |
|-----------|-------|-------|
| `api-service` (FastAPI) | `services/api-service/Dockerfile`; `uvicorn wise_api.main:app`; bundles `apps/demonstration-surface` into the image | **Works** |
| Other services (discovery/metadata/preservation/knowledge-graph/orchestrator) | per-service Dockerfiles | Build (compose) |
| `apps/demonstration-surface` | None — static files copied into the API image (`WISE_DEMONSTRATION_SURFACE_PATH`) | **Works** (no build step) |
| `apps/nature-culture-web` | Planned `pnpm --filter nature-culture-web build` | **Absent** (no `package.json`) |
| CI | `.github/workflows/ci.yml` — Python lint/test, Alembic, `docker compose build` for services; **no** Node/web build or deploy. An alternate `infrastructure/github/workflows/ci.yml` also covers Python only. | Python-only |

**Notes.** There is no JavaScript/TypeScript toolchain in the repo (0 `package.json`). The API image is the only artifact that carries a public surface today. The web build pipeline and OpenAPI-client generation described in [nature-culture-frontend-v1.0.md](../architecture/nature-culture-frontend-v1.0.md) §"Monorepo CI" are not yet implemented.

---

## 2. Environment variables

### Implemented (`api-service`)
| Variable | Purpose | Notes |
|----------|---------|-------|
| `DATABASE_URL` / `WISE_DATABASE_URL` | Postgres DSN | **Must use `postgresql+psycopg://`** (psycopg2 not installed) — see `AGENTS.md` |
| `WISE_DEMONSTRATION_SURFACE_PATH` | Static surface path | Defaults to `/app/demonstration-surface`; auto-detects local `apps/demonstration-surface` |
| `WISE_ENVIRONMENT`, `WISE_LOG_LEVEL` | Runtime/log config | from `wise-common` settings |

### Required for the public web app (not yet present)
`WISE_API_BASE_URL`, `WISE_API_TIMEOUT_MS`, `NEXT_PUBLIC_SITE_URL`, `NEXT_PUBLIC_DEFAULT_LOCALE`, `NC_FEATURE_SEARCH|PUBLISHING|EDUCATION|RESEARCH`, `REVALIDATION_SECRET` — plus, for the storefront, `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `POD_PROVIDER_API_KEY`.

**Hygiene:** database/MinIO credentials and internal tokens are server-only and must never be exposed via `NEXT_PUBLIC_`. `.env.example` covers the platform stack; no web `.env.example` exists yet.

---

## 3. Vercel readiness

| Check | State |
|-------|-------|
| `vercel.json` | **Absent** |
| `.vercel/` project link | **Absent** |
| Root directory `apps/nature-culture-web` | **Absent** |
| `package.json` / `next.config.ts` / `pnpm-lock.yaml` | **Absent** |
| Image-optimization domain allow-list (IIIF/CDN) | **Absent** |
| Security headers (CSP/HSTS/Referrer-Policy/Permissions-Policy) | **Absent** |
| Preview `noindex` middleware | **Absent** |

**Conclusion:** Vercel deployment cannot proceed until `apps/nature-culture-web` is scaffolded. The target configuration is specified in the frontend doc §"Vercel Deployment Strategy" and summarized in the RC9 launch plan §3. The current public surface deploys instead via the `api-service` container (any container host / Zone Alpha), not Vercel.

---

## 4. Route coverage

### Live API routes (`api-service`) — verified 200 locally
| Route | Type | Consumer |
|-------|------|----------|
| `GET /health` | JSON | liveness |
| `GET /v1/objects/{stable_id}` | JSON | `object.js` |
| `GET /v1/species/{stable_id}` | JSON | `species.js` |
| `GET /v1/areas/{stable_id}` | JSON | `area.js` |
| `GET /v1/map/areas/{stable_id}` | JSON | `area.js` |
| `GET /v1/map/search?bbox=` | JSON | API/e2e |
| `GET /objects/{stable_id}` | HTML | demo object/species pages |
| `GET /areas/{stable_id}` | HTML | demo area page |
| `GET /static/*` | static | CSS/JS |

### Demonstration-surface page → API wiring
| Page (HTML) | Loads | Calls | Status |
|-------------|-------|-------|--------|
| `/objects/stonehenge` | `object.js` | `GET /v1/objects/stonehenge` | OK |
| `/objects/panthera-leo` | `species.js` | `GET /v1/species/panthera-leo` | OK (see note) |
| `/areas/everglades-national-park` | `area.js` | `GET /v1/areas/...` + `/v1/map/areas/...` | OK |

**Note (intentional quirk):** the species page is served under `/objects/panthera-leo` (there is no `GET /species/{id}` HTML route), while its data comes from `/v1/species/...`. The public `nature-culture-web` app should normalize this to `/[locale]/species/[id]`.

### Planned routes not yet backed by APIs (feature-flag / placeholder at launch)
`/v1/search`, `/v1/collections/{slug}`, `/v1/iiif/{id}`, `/v1/locales`, `/v1/entities/{uri}`, `/v1/education/*`, `/v1/research/*` — all **planned** (frontend doc §"Endpoint map"). The web app must hide these behind `NC_FEATURE_*` flags so no indexed route 404s.

---

## 5. Broken links

Static review of `apps/demonstration-surface` (HTML + JS):

| Reference | Kind | Resolves? | Action for production |
|-----------|------|-----------|-----------------------|
| `/static/styles.css` | internal | **Yes** (200) | keep |
| `/static/object.js`, `/static/species.js`, `/static/area.js` | internal | **Yes** (200) | keep |
| `#main` skip link | in-page anchor | **Yes** | keep |
| `https://unpkg.com/leaflet@1.9.4/...` (CSS+JS) | external CDN | reachable, but a third-party runtime dependency | **self-host** Leaflet; add to CSP allow-list |
| OpenStreetMap tiles (`area.js` attribution) | external tiles | reachable | move to an allow-listed/managed tile source; CSP `img-src` |
| `https://whc.unesco.org/en/list/373/` | outbound attribution | external | keep (source link); verify periodically |
| `https://www.gbif.org/species/5219404/` | outbound attribution | external | keep |
| `https://rsis.ramsar.org/ris/374` | outbound attribution | external | keep |

**Findings:** no broken **internal** links. Risks are (a) third-party runtime dependencies (Leaflet/unpkg, OSM tiles) that should be self-hosted/allow-listed for resilience and CSP, and (b) outbound attribution links that need periodic link-checking. The future web app should add an automated link checker to CI.

---

## 6. Static assets

| Asset | Location | Served at | Notes |
|-------|----------|-----------|-------|
| `styles.css` | `apps/demonstration-surface/styles.css` | `/static/styles.css` | design tokens, layout, badges, a11y |
| `object.js` | `apps/demonstration-surface/object.js` | `/static/object.js` | RC1 loader |
| `species.js` | `apps/demonstration-surface/species.js` | `/static/species.js` | RC2 loader |
| `area.js` | `apps/demonstration-surface/area.js` | `/static/area.js` | RC3 loader + Leaflet |
| HTML pages | `objects/*`, `areas/*` | `/objects/{id}`, `/areas/{id}` | `FileResponse` |
| Portfolio data | `data/portfolio/*.json` | not web-served | catalogue seed (this RC) |

**Gaps for production:** no `favicon`, `robots.txt`, `sitemap.xml`, web app manifest, Open Graph images, or self-hosted fonts. No fingerprinting/immutable caching (the static mount serves files as-is). These are inherent to the demo and are addressed by the Next.js app's `public/` + build pipeline.

---

## 7. Remediation checklist (ordered)

1. Scaffold `apps/nature-culture-web` (Next.js 15) + `packages/wise-api-client` (generated from `api-service` `GET /openapi.json`).
2. Add `vercel.json` / project config; set env vars per environment; enable preview `noindex`.
3. Add web CI: `pnpm lint && typecheck && test:a11y && test:e2e && build` + OpenAPI drift check; add a link checker.
4. Implement SEO assets: `sitemap.ts`, `robots.ts`, `hreflang`, JSON-LD, OG images.
5. Self-host Leaflet/fonts; move map tiles to an allow-listed source; add strict CSP + security headers.
6. Feature-flag unbuilt routes (search/collections/learn/research) to prevent indexed 404s.
7. Enforce the rights/quality gate (`rights_verified`) before any public render or sellable SKU.
8. (Phase 12) Stand up the storefront: catalogue ingest from `data/portfolio/*`, Stripe checkout + webhook, POD provider, order datastore separate from canonical stores (ADR-010).

---

## 8. Sign-off gates

- [ ] Web app builds and deploys to a Vercel preview
- [ ] No indexed route returns 404; feature flags verified
- [ ] No broken internal links; external links checked in CI
- [ ] Static assets fingerprinted + cached; SEO assets present
- [ ] Secrets server-only; CSP/security headers active
- [ ] Architecture v1.0, governance, ADRs, agents unchanged (ADR-011)

---

*Implementation review. Does not modify Architecture v1.0, governance, ADRs, or agents (ADR-011). Companion to [rc9-public-launch-plan.md](rc9-public-launch-plan.md) and [nature-culture-frontend-v1.0.md](../architecture/nature-culture-frontend-v1.0.md).*
