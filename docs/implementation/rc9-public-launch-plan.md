# RC9 Public Launch Readiness Plan

| Field | Value |
|-------|-------|
| **Status** | Implementation plan (non-governance) |
| **Date** | 2026-06-22 |
| **Scope** | Public launch readiness for the Nature & Culture Experience Plane and the Phase 12 Products surface |
| **Authority** | Implementation companion to [nature-culture-frontend-v1.0.md](../architecture/nature-culture-frontend-v1.0.md); aligns with architecture-v1.0 (`architecture-v1.0` tag) |
| **Constraints** | Does **not** modify Architecture v1.0, governance, ADRs, or agent specifications (ADR-011) |

> **Reading note.** This plan separates **what ships today** (the Founder Demonstration Surface) from **what the public launch requires** (the `nature-culture-web` Experience Plane app and a Products storefront). It is a readiness map, not a claim that the public app already exists.

---

## 1. Current state (verified against the repository)

| Surface | State | Evidence |
|---------|-------|----------|
| `apps/demonstration-surface` | **Live** — static HTML/JS/CSS served by `api-service` (`/objects/{id}`, `/areas/{id}`, `/static/*`) | `apps/demonstration-surface/`, `services/api-service/src/wise_api/main.py` |
| `apps/web` / `apps/nature-culture-web` | **Absent** — design only | [nature-culture-frontend-v1.0.md](../architecture/nature-culture-frontend-v1.0.md) |
| Commerce / checkout / cart | **Absent** (Phase 12 Products, planned) | `06-build-roadmap.md` Phase 12 |
| Collections API / pages | **Absent** (Phase 10 Publishing, planned) | frontend doc §API endpoint map |
| Series | **Absent** (modeled as `schema.org/CreativeWorkSeries` for collection pages) | frontend doc SEO §JSON-LD |
| Product catalog / SKUs | **Absent**; seeded by `data/portfolio/*` (this RC) | `data/portfolio/` |
| Web analytics | **Absent**; backend uses `structlog` only | `packages/wise-common/.../logging.py` |
| SEO (sitemap/robots/OG/JSON-LD) | **Minimal** (demo `<title>` only) | demo HTML pages |
| Vercel / web CI | **Absent** | no `vercel.json`, no `package.json`, `.github/workflows/ci.yml` is Python-only |

Available Platform APIs today: `GET /v1/objects/{id}`, `/v1/species/{id}`, `/v1/areas/{id}`, `/v1/map/areas/{id}`, `/v1/map/search?bbox=`.

**Implication.** A *credible* public launch (Phase 11) depends on Search (Phase 6), Translation Fabric (Phase 9), and Publishing (Phase 10), which are not implemented. The plan below therefore defines a **staged launch**: a small, fully-clean public beta from existing contracts, then progressive enablement as Platform phases land. This respects the founder build order (ADR-003) — the frontend tracks Platform readiness and never bypasses it.

---

## 2. Deployment architecture

```
                     ┌──────────────────────────────────────────┐
   End users ─────▶  │  Vercel Edge (CDN, locale middleware,     │
   (web, mobile)     │  security headers, preview noindex)        │
                     └───────────────┬──────────────────────────┘
                                     │  (Node runtime: SSR / ISR)
                     ┌───────────────▼──────────────────────────┐
                     │  apps/nature-culture-web (Next.js 15)      │
                     │  Server Components → typed FastAPI client  │
                     └───────────────┬──────────────────────────┘
                                     │  HTTPS (read-only, ADR-002)
                     ┌───────────────▼──────────────────────────┐
                     │  api-service (FastAPI gateway, Zone Alpha) │
                     │  /v1/objects /species /areas /map …        │
                     └───────────────┬──────────────────────────┘
              ┌──────────────────────┼───────────────────────────┐
              ▼                      ▼                            ▼
     PostgreSQL + PostGIS      MinIO (T0 Hot)              IIIF image service
     + pgvector (canonical)    preservation bitstreams     (image delivery)
```

Principles (from [nature-culture-frontend-v1.0.md](../architecture/nature-culture-frontend-v1.0.md), ADR-002, 05-physical-architecture §4.3):

- The web app is a **replaceable, read-only presentation layer**. It calls Platform Plane APIs only — never PostgreSQL, MinIO, OpenSearch, or graph stores directly.
- **Experience Plane on Vercel Edge/CDN; Platform Plane in Zone Alpha/Beta.** Master images stream from IIIF/Preservation, never Vercel Blob.
- The existing `demonstration-surface` (served by `api-service`) remains the **Founder preview** and is kept distinct (06 §3.1).
- **Products / commerce** is a separate concern (Part 5 + the `data/portfolio/*` catalogue seed). Per ADR-010, products generate revenue but **must never gate canonical public memory** — entity pages stay free and un-paywalled.

### Commerce/storefront topology (Phase 12)

```
nature-culture-web  ──▶  /[locale]/shop (catalog from data/portfolio + product service)
                    ──▶  checkout  ──▶  Payment provider (Stripe)  ──▶  Print-on-demand fulfilment
                                                                       (Prodigi / Gelato / Printful)
```

Storefront reads the curated catalogue (`data/portfolio/top_100_global_assets.json`, `top_100_collections.json`, `top_100_series.json`) → product variants → POD provider. No canonical write path; orders live in a commerce datastore distinct from the canonical stores.

---

## 3. Vercel deployment

| Setting | Value |
|---------|-------|
| Root directory | `apps/nature-culture-web` |
| Framework | Next.js 15 (App Router) |
| Node.js | 20 LTS |
| Install | `pnpm install` (monorepo, filtered) |
| Build | `pnpm --filter nature-culture-web build` |
| Output | Default Next.js |

| Environment | Branch | API upstream | Indexable |
|-------------|--------|--------------|-----------|
| Production | `main` | `https://api.natureandculture.org` | yes |
| Preview | PR branches | staging API / per-PR | **no** (`X-Robots-Tag: noindex`) |
| Development | local | `http://localhost:8000` | n/a |

**Environment variables (frontend, server-scoped unless `NEXT_PUBLIC_`):** `WISE_API_BASE_URL`, `WISE_API_TIMEOUT_MS`, `NEXT_PUBLIC_SITE_URL`, `NEXT_PUBLIC_DEFAULT_LOCALE`, `NC_FEATURE_SEARCH|PUBLISHING|EDUCATION|RESEARCH`, `REVALIDATION_SECRET`, plus commerce secrets when Phase 12 lands (`STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `POD_PROVIDER_API_KEY`). **Never** expose database URLs, MinIO credentials, or internal tokens to the browser.

**Runtime split:** Edge for locale/security middleware; Node for SSR/ISR/entity pages; Vercel Image Optimization restricted to allow-listed IIIF/CDN domains. **On-demand ISR:** Publishing emits an HMAC-signed webhook → `revalidateTag('object:<id>')`.

**CI gate before deploy:** `pnpm lint && pnpm typecheck`, `pnpm test:a11y && pnpm test:e2e`, `pnpm build`, OpenAPI drift check (regenerate the typed client; fail on schema drift).

---

## 4. Analytics events

No analytics exist today. Launch with a **privacy-first, cookieless** plan (Vercel Web Analytics and/or Plausible) plus a small first-party event schema. No PII, no cross-site tracking, consent-gated where required.

| Event | Trigger | Key properties |
|-------|---------|----------------|
| `page_view` | route render | `path`, `locale`, `template` (object/species/place/collection/shop) |
| `entity_view` | entity page load | `entity_type`, `stable_id`, `rights_verified` |
| `search_performed` | `/explore` query | `query_len`, `result_count`, `facets[]` (no raw PII) |
| `map_bbox_search` | map query | `bbox`, `result_count` |
| `collection_view` | collection page | `collection_id` |
| `product_view` | shop PDP | `product_id`, `asset_id`, `category` |
| `add_to_cart` / `begin_checkout` / `purchase` | commerce funnel | `product_id`, `value`, `currency`, `qty` |
| `language_switch` | locale change | `from_locale`, `to_locale` |
| `download_open_asset` | public-domain download | `asset_id`, `format` |
| `outbound_attribution_click` | source/rights link | `source_registry_ref` |

Conventions: event names `snake_case`; emit server-side where possible for ad-blocker resilience; sample high-volume events; route to a single analytics module (`lib/analytics`) so the provider is swappable.

---

## 5. Privacy review

| Area | Position |
|------|----------|
| Lawful basis | Anonymous read access to canonical public memory (03 §6.1); no account needed to browse |
| PII | None collected for browsing; commerce collects order/shipping data under a published privacy policy |
| Cookies | None for analytics (cookieless); functional cookie `nc_locale` only; commerce session cookie at checkout |
| Consent | Cookie/consent banner only where a jurisdiction requires it; analytics respects Do-Not-Track / Global Privacy Control |
| Data residency | Canonical data in Zone Alpha/Beta; commerce/PII processed by the payment + fulfilment providers under DPAs |
| Third parties | Payment (Stripe), POD fulfilment, map tiles, IIIF image host, analytics — each listed in the privacy policy |
| Retention | Order data per legal/tax requirements; analytics aggregated, short retention |
| Rights of data subjects | Access/erasure/portability handled through the commerce processor; browsing leaves no profile |
| Security | TLS everywhere; secrets server-only; strict CSP; no secrets in `NEXT_PUBLIC_` |

**Launch blockers:** publish privacy policy + cookie notice; sign DPAs with payment/POD/analytics vendors; confirm GPC/DNT handling.

---

## 6. Performance review

Targets (06 §Phase 11, frontend doc §Performance): **LCP p95 < 2.5s (4G mobile)**, **page load p95 < 3s**, Core Web Vitals "good".

| Lever | Plan |
|-------|------|
| Rendering | Server Components by default; SSG/ISR for entity pages (3600s) and collections (60-300s); SSR only for search/map |
| Images | `next/image` + IIIF derivatives; AVIF/WebP; explicit dimensions; lazy below-fold; low-bandwidth mode swaps deep-zoom for static surrogates |
| Fonts | Self-hosted, subset variable fonts; `font-display: swap` |
| JS budget | Push `"use client"` to leaf widgets (map, IIIF viewer, locale switcher); route-level code splitting |
| Caching | Vercel CDN immutable static; cache tags per entity/locale; on-demand revalidation |
| Maps | Debounced bbox queries; marker clustering at low zoom; tiles client-direct (CSP-allowed) |
| Monitoring | Vercel Web Analytics (Web Vitals) + optional OTel; CI Lighthouse budget on key templates |

**Demonstration surface caveat:** the Everglades page loads Leaflet + OSM tiles from external CDNs — acceptable for the demo, but the production app should self-host/allow-list and budget these.

---

## 7. SEO review

SEO is structural, not an overlay (frontend doc §SEO).

| Item | Plan | Today |
|------|------|-------|
| `generateMetadata` per page | title/description/OG from Publishing + entity fallback | demo sets `document.title` only |
| JSON-LD (`schema.org`) | `MuseumObject`/`CreativeWork` (objects), `Taxon` (species), `Place` (areas), `Collection`/`CreativeWorkSeries` (collections/series) | none |
| Sitemaps | dynamic `sitemap.ts`, paginated per locale, `lastmod` from `updated_at` | none |
| `robots.ts` | allow public entities; disallow `/api/`; preview `noindex` | none |
| `hreflang` | alternates per locale; `x-default` → default locale | none |
| Canonical URLs | locale-prefixed, `trailingSlash:false`, stable-ID paths | n/a |
| Open Graph / Twitter | per-entity images from Publishing | none |

**Series note:** the Top 100 Series map naturally to `schema.org/CreativeWorkSeries`; collections to `Collection`. The `data/portfolio/*` IDs become stable URL slugs.

---

## 8. Accessibility review

Canonical baseline **WCAG 2.1 AA** (07 §7); the frontend design **targets 2.2 AA** (frontend doc §Accessibility).

| Area | Plan | Demo today |
|------|------|------------|
| Landmarks/headings | one `<h1>`, semantic regions | present (`header/main/section`, skip link) |
| Keyboard | all actions operable; visible focus | basic |
| Screen readers | ARIA only where needed; live regions for search | minimal |
| Colour contrast | ≥ 4.5:1; high-contrast toggle | needs audit |
| Motion | `prefers-reduced-motion` disables map fly/carousels | n/a |
| Media | IIIF alt text from Quality Platform; AV transcripts | n/a |
| Maps | keyboard pan/zoom + list-based feature alternative | Leaflet default only |
| Targets | ≥ 44×44px | needs audit |
| Quality gate | honour `accessibility_compliant` on view models | available in contracts |
| Testing | axe-core in CI; manual NVDA/VoiceOver per release | none |

---

## 9. Content readiness

| Content set | State | Source |
|-------------|-------|--------|
| RC1-RC3 entities (Stonehenge, Panthera leo, Everglades) | Ready, rights+quality verified | seeded; e2e green |
| Top 100 Global Assets | **Seeded this RC** | `data/portfolio/top_100_global_assets.json` |
| Top 100 Collections | **Seeded this RC** | `data/portfolio/top_100_collections.json` |
| Top 100 Series | **Seeded this RC** | `data/portfolio/top_100_series.json` |
| Product candidates | **Defined this RC** | `top_20_product_candidates.md` |
| Localized content | Not ready (Phase 9) | Translation Fabric |
| Published collections / IIIF | Not ready (Phase 10) | Publishing |

**Rights gate (non-negotiable, 03 §6.3):** no entity renders publicly unless `rights_verified === true` and publishing clearance exists. The portfolio JSON is a **prioritization seed**: each listed asset must pass discovery → preservation → metadata → rights/quality before it appears on a public page or as a sellable product. High-resolution master images must be confirmed public domain or licensed (Smithsonian Open Access, Rijksmuseum, NGA, LoC, Europeana, Public Domain Review) before commercial use.

---

## 10. Launch checklist

### A. Engineering
- [ ] Scaffold `apps/nature-culture-web` (Next.js 15) + `packages/wise-api-client` from `api-service` OpenAPI
- [ ] Object / species / place pages + map MVP from existing `/v1/*` endpoints
- [ ] Feature flags hide unbuilt routes (search/collections/learn/research) — no broken links
- [ ] Rights gate: `notFound()` when `rights_verified === false`
- [ ] CI: lint, typecheck, axe, Playwright e2e, build, OpenAPI drift

### B. SEO & content
- [ ] `sitemap.ts`, `robots.ts`, `hreflang`, canonical URLs
- [ ] JSON-LD per template; OG images
- [ ] Verify rights/quality for every launch entity drawn from `data/portfolio/*`

### C. Performance & a11y
- [ ] LCP p95 < 2.5s; Lighthouse budget in CI
- [ ] axe clean on key templates; manual screen-reader smoke
- [ ] Self-host/allow-list fonts, map tiles, IIIF domains in CSP

### D. Privacy & analytics
- [ ] Privacy policy + cookie notice published; GPC/DNT honoured
- [ ] Cookieless analytics wired to the event schema (§4)
- [ ] DPAs signed (payments, POD, analytics)

### E. Commerce (Phase 12, if launching storefront)
- [ ] Catalogue ingest from `data/portfolio/*`; product variants per `top_20_product_candidates.md`
- [ ] Stripe checkout + webhook; POD provider integration; order datastore (separate from canonical)
- [ ] Confirm ADR-010: no paywall on canonical memory; products are derived goods only

### F. Deployment & ops
- [ ] Vercel project (root `apps/nature-culture-web`), env vars set per environment
- [ ] Preview = `noindex`, staging API; production = `main`, production API
- [ ] Security headers (CSP/HSTS/Referrer-Policy/Permissions-Policy)
- [ ] Web Vitals + error monitoring; `x-request-id` propagation to `api-service`
- [ ] Rollback plan (Vercel instant rollback) and on-call runbook

### G. Go / No-Go
- [ ] All launch entities pass rights+quality gate
- [ ] No broken/placeholder links in indexed routes
- [ ] Performance + a11y budgets met; privacy artifacts live
- [ ] Architecture v1.0 unchanged; no new ADRs/agents/governance (ADR-011)

---

*Implementation companion. Does not modify Architecture v1.0, governance, ADRs, or agents (ADR-011). See [nature-culture-frontend-v1.0.md](../architecture/nature-culture-frontend-v1.0.md) and [06-build-roadmap.md](../architecture/canonical/06-build-roadmap.md).*
