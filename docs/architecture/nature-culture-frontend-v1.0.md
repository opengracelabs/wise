# Nature & Culture Frontend Architecture v1.0

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Status** | Design — implementation companion (non-governance) |
| **Authority** | Aligns with architecture-v1.0 (`docs/architecture/canonical/`, tag `architecture-v1.0`) |
| **Date** | 2026-06-22 |
| **Scope** | Phase 11 Public Experience + early Experience Plane surfaces (Learning, Research entry points) |
| **Supersedes** | — |
| **Does not modify** | Constitutional Plane, Platform Plane contracts, founder build order, ADRs |

---

## Executive Summary

Nature & Culture's public portal is an **Experience Plane** application that consumes **Platform Plane FastAPI endpoints only** — never preservation storage, graph databases, or search indexes directly. This document defines the frontend architecture for that portal using **Next.js 15**, **TypeScript**, **Tailwind CSS**, **shadcn/ui**, and **Vercel**, aligned with frozen architecture-v1.0.

The design treats the frontend as a **replaceable presentation layer** (ADR-002): it may be rebuilt or redeployed without affecting canonical memory. All factual content, rights metadata, translations, and published narratives flow through defined interface contracts (03 §7): Search index documents, Knowledge Graph views, Localized Content Bundles, and Published Collection Manifests — exposed to the browser via a **public API gateway** (`api-service` today; dedicated experience-gateway at scale).

Key decisions:

1. **Monorepo placement** — New app at `apps/nature-culture-web/` alongside the existing Founder Demonstration Surface; shared TypeScript contracts generated from FastAPI OpenAPI schemas that mirror `wise-contracts`.
2. **SEO-first App Router** — Server Components by default; static/ISR generation for entity pages; JSON-LD (`schema.org`) and `hreflang` on every public URL.
3. **Locale-first routing** — `[locale]` segment on all user-facing routes; UI strings and entity labels resolved from Translation Fabric bundles (Phase 9), not hard-coded English copy.
4. **Domain-oriented composition** — Feature modules for Objects, Places, Species, Collections, Maps, Learning, and Research map to canonical entity types and experience subgraphs (03 §5).
5. **Strict read boundary** — No mutations to canonical stores from the frontend; Community (Phase 14) submissions route through authenticated Platform APIs that enter Ingestion — not around it.
6. **Vercel as CDN edge for Experience** — Matches 05-physical-architecture §4.3 (Global CDN / Public Experience delivery); Node runtime for SSR/API-backed pages; Edge for locale middleware and security headers only.

---

## Alignment with architecture-v1.0

This design implements — without amending — the following frozen concepts.

### Experience Plane boundary (03 §5, ADR-002)

> *"The experience plane is the public face of the institution. All experiences consume platform plane APIs; no experience plane component writes directly to preservation storage."* — [03-canonical-architecture.md](canonical/03-canonical-architecture.md) §5

> *"Nature & Culture operates exclusively through the Experience Plane, consuming Platform Plane APIs."* — [08-decision-record.md](canonical/08-decision-record.md) ADR-002

The Next.js application is a **read-only consumer** of REST/GraphQL gateway endpoints. Any future write paths (Community contributions, translation participation) call Platform Plane authenticated APIs that enqueue Ingestion workflows — never MinIO, PostgreSQL, or graph stores.

### Public Experience definition (03 §5.1)

> *"The primary public portal: search, explore, entity pages, maps, timelines, and visual narratives."*  
> *"Consumes: Search, Knowledge Graph, Translation Fabric, Publishing"*  
> *"Serves: Web, mobile, low-bandwidth, accessibility-compliant interfaces"*

Route groups and feature modules below map directly to these capabilities.

### Founder build order (06-build-roadmap.md §3, ADR-003)

Public Experience is **Phase 11**, depending on Search (6), Publishing (10), and Translation Fabric (9). The frontend must:

- **Gracefully degrade** when upstream phases are incomplete (current repository state).
- **Not bypass** phase dependencies — e.g., do not embed raw database queries because Search is not ready.
- **Remain distinct** from the Founder Demonstration Surface (06 §3.1), which is Phases 1–3 only and explicitly *not* Public Experience.

### Interface contracts (03 §7)

| Contract | Frontend consumption |
|----------|---------------------|
| Knowledge Graph → All Experience | Entity page aggregates (`HeritageObjectView`, `SpeciesObjectView`, `ProtectedAreaObjectView`; future graph entity views) |
| Search → Public Experience | Search results, facets, entity panels |
| Translation Fabric → All Experience | `LocalizedContentBundle` per locale (labels, descriptions, UI strings) |
| Publishing → Public Experience | `PublishedCollectionManifest`, IIIF Presentation manifests, visual narratives |
| Research Fabric → External | Research portal pages, dataset metadata, citation blocks |

### Identity and access (03 §6.1)

Public users receive **anonymous read access** to canonical public memory. Research and Community authenticated flows use OAuth 2.1 / OIDC (07 §8) via Platform gateways — not frontend-managed sessions against data stores.

### Rights and quality gates (03 §6.3, 13-quality-review-agent)

No object enters the public experience without machine-readable rights (Europeana Rights Statements, Creative Commons). The frontend **must not render** entities where `rights_verified === false` or publishing clearance is absent — surface a governance-safe empty state instead.

### Physical deployment (05-physical-architecture.md §4.3, §6.1)

Public Experience deploys at **Global CDN / Edge**. Vercel fulfills the Experience Plane delivery tier; Platform Plane remains in Zone Alpha/Beta. Image-rich content uses **IIIF Image API** endpoints from Publishing/Preservation — not Vercel blob storage for masters.

### Standards (07-reference-standards.md §7, §11)

| Requirement | Frontend implementation |
|-------------|---------------------------|
| HTML5 | Semantic App Router pages |
| WCAG 2.1 AA (canonical) / **2.2 AA (this design target)** | shadcn/ui primitives, axe CI, manual audit |
| IIIF Presentation + Image API | `@iiif/presentation-3` client for collections and field guides |
| hreflang + BCP 47 | Locale routing, `<link rel="alternate" hreflang="…">` |
| schema.org JSON-LD | `@graph` scripts on entity and collection pages |
| Content Security Policy | Strict CSP via Next.js headers |
| GraphQL (Required for Experience) | Consumed via gateway when exposed; REST-first until GraphQL gateway ships |

### Translation as platform capability (ADR-008)

> *"Translation Fabric is a Platform Plane capability (Phase 9), not an Experience Plane afterthought."*

The frontend **does not own translation logic**. It requests locale bundles from the Platform Plane and renders `fallbackChain` when a locale tier is incomplete. Source-language content is always available; translations are additive with provenance attribution in UI.

### Documented gaps (repository state vs. Phase 11)

| Phase 11 dependency | Current repository state |
|---------------------|--------------------------|
| Search (6) | OpenSearch scaffold only; no `/v1/search` routes |
| Translation Fabric (9) | Agent spec only; no `/v1/locales` or bundle API |
| Publishing (10) | Agent spec only; no `/v1/collections` or IIIF manifest routes |
| Research Fabric (8) | Not implemented |
| GraphQL API | Specified (03 §4.5) but not exposed |
| **Available today** | `GET /v1/objects/{id}`, `/v1/species/{id}`, `/v1/areas/{id}`, `/v1/map/*` via `api-service` |

The architecture below includes **contract-first stubs** for missing endpoints so implementation can proceed incrementally without redesign when Platform phases complete.

---

## Repository Structure

The frontend lives in the WISE monorepo under `apps/`, consistent with [architecture-overview.md](../../architecture-overview.md) §1.1.

```
wise/
├── apps/
│   ├── demonstration-surface/          # Founder Demonstration Surface (Phases 1–3) — UNCHANGED
│   └── nature-culture-web/               # Phase 11 Public Experience (this document)
│       ├── app/                          # Next.js 15 App Router
│       │   ├── [locale]/                 # Locale-first route group
│       │   │   ├── layout.tsx            # Shell: nav, footer, skip links, locale provider
│       │   │   ├── page.tsx              # Home / explore hub
│       │   │   ├── explore/              # Search & discovery
│       │   │   ├── objects/[stableId]/   # Heritage objects (CIDOC-CRM)
│       │   │   ├── species/[stableId]/   # Taxa (Darwin Core)
│       │   │   ├── places/[stableId]/      # Places & protected areas (GeoNames / schema:Place)
│       │   │   ├── collections/[slug]/   # Published Collection Manifests
│       │   │   ├── map/                    # Interactive map explorer
│       │   │   ├── learn/                  # Education portal (Phase 13 entry)
│       │   │   └── research/               # Research Fabric portal (Phase 8 entry)
│       │   ├── api/                        # Route handlers (optional BFF — see §API)
│       │   │   └── revalidate/             # On-demand ISR webhook (Platform → Vercel)
│       │   ├── sitemap.ts
│       │   ├── robots.ts
│       │   └── manifest.ts                 # Web app manifest (mobile-first PWA-lite)
│       ├── components/
│       │   ├── ui/                         # shadcn/ui generated primitives
│       │   ├── layout/                     # Header, Footer, Nav, SkipLink, LocaleSwitcher
│       │   ├── domain/                     # Domain-specific composites (see §Components)
│       │   ├── media/                      # IIIF viewer, image zoom, AV player
│       │   ├── map/                        # MapLibre/Mapbox wrapper, bbox search UI
│       │   └── seo/                        # JsonLd, Hreflang, OpenGraph
│       ├── lib/
│       │   ├── api/                        # Typed FastAPI client (server-only)
│       │   ├── i18n/                       # Locale config, routing, formatters (CLDR)
│       │   ├── seo/                        # Metadata builders, schema.org mappers
│       │   ├── a11y/                       # Focus management, live region helpers
│       │   └── constants/                  # Public config, feature flags
│       ├── hooks/                          # Client hooks (map interaction, media UI)
│       ├── styles/
│       │   └── globals.css                 # Tailwind v4 + design tokens
│       ├── messages/                       # Fallback UI strings (until Translation Fabric)
│       │   └── en.json                     # Seed locale only — not authoritative content
│       ├── public/
│       │   ├── icons/
│       │   └── fonts/                      # Self-hosted variable fonts (performance)
│       ├── tests/
│       │   ├── a11y/                       # axe-playwright
│       │   ├── e2e/                        # Playwright critical paths
│       │   └── unit/                       # Vitest component tests
│       ├── next.config.ts
│       ├── tailwind.config.ts
│       ├── components.json                 # shadcn/ui config
│       ├── package.json
│       └── tsconfig.json
│
├── packages/
│   └── wise-api-client/                    # NEW: generated + hand-written API client
│       ├── src/
│       │   ├── client.ts                   # fetch wrapper, error types, auth injection
│       │   ├── schemas/                    # OpenAPI-generated types (from api-service)
│       │   └── endpoints/                  # objects, species, places, map, search, …
│       ├── openapi/                        # Committed OpenAPI snapshot from FastAPI
│       └── package.json
│
└── docs/
    └── architecture/
        └── nature-culture-frontend-v1.0.md   # This document
```

### Directory rationale

| Path | Purpose |
|------|---------|
| `apps/nature-culture-web/` | Isolated deployable Experience Plane app; Vercel project root |
| `packages/wise-api-client/` | Single typed client shared if Phase 12 Products adds embeddable widgets |
| `components/ui/` | shadcn/ui only — unstyled primitives, never domain logic |
| `components/domain/` | Business-meaningful UI tied to canonical entity types |
| `lib/api/` | Server-only fetch layer — secrets and upstream URLs never imported in Client Components |
| `messages/` | Bootstrap UI copy; replaced/incremented by Translation Fabric bundles at runtime |

### Relationship to `demonstration-surface`

| Attribute | `demonstration-surface` | `nature-culture-web` |
|-----------|-------------------------|----------------------|
| Phase | 1–3 Founder preview | 11 Public Experience |
| WCAG | 2.1 A minimum | 2.2 AA target |
| API scope | RC1–RC3 object views | Full Search, Publishing, Translation |
| Deployment | Served by api-service static mount | Independent Vercel project |
| Governance | Steward-gated demo | Public launch criteria (06 §Phase 11) |

Do not extend `demonstration-surface` for Public Experience — maintain separation per 06 §3.1.

---

## Routing Structure

Next.js 15 **App Router** with locale-first segments. All public URLs include a BCP 47 locale prefix except default-locale redirect.

### Locale routing

```
Middleware (Edge)
  ├── Detect Accept-Language + cookie `nc_locale`
  ├── Redirect / → /{preferred-locale}/
  ├── Validate locale against supported set from Platform `/v1/locales`
  └── Set Content-Language response header
```

**Supported locale source of truth:** Translation Fabric (Phase 9). Until available, config file `lib/i18n/locales.ts` mirrors roadmap target (≥ 20 languages at launch per 06 §Phase 11).

**Default locale:** Institution primary (likely `en` at launch). **hreflang** alternates generated for every indexed page.

### Route map

| Route | Purpose | Primary API | Rendering |
|-------|---------|-------------|-----------|
| `/[locale]` | Home, featured collections, global search entry | Search, Publishing | ISR (60s) |
| `/[locale]/explore` | Full search + facets | `GET /v1/search` | SSR (dynamic) |
| `/[locale]/explore?q=&facets=` | Query state in URL (SEO-shareable) | Search | SSR |
| `/[locale]/objects/[stableId]` | Heritage object entity page | `GET /v1/objects/{id}?locale=` | SSG/ISR |
| `/[locale]/species/[stableId]` | Species / taxon page | `GET /v1/species/{id}?locale=` | SSG/ISR |
| `/[locale]/places/[stableId]` | Place / protected area page | `GET /v1/areas/{id}?locale=` | SSG/ISR |
| `/[locale]/collections/[slug]` | Published exhibit / collection | `GET /v1/collections/{slug}?locale=` | ISR |
| `/[locale]/collections/[slug]/manifest.json` | IIIF Presentation manifest proxy | Publishing IIIF URI | Static proxy |
| `/[locale]/map` | Full-screen map explorer | `GET /v1/map/search?bbox=` | SSR + client hydration |
| `/[locale]/map/places/[stableId]` | Map-anchored place detail panel | Map + area APIs | SSR |
| `/[locale]/learn` | Education hub (Phase 13) | `GET /v1/education/resources` | ISR |
| `/[locale]/learn/[resourceId]` | Lesson / module | Education bundle API | ISR |
| `/[locale]/research` | Research portal landing | Research Fabric catalog | ISR |
| `/[locale]/research/datasets/[doi]` | Dataset citation page | `GET /v1/research/datasets/{doi}` | ISR |
| `/[locale]/timeline/[entityId]` | Temporal narrative (Publishing) | Graph + Publishing | ISR |

### URL identity rules

- **Stable IDs** in paths match Platform Plane identifiers (`stable_id` in `wise-contracts`) — not slugs alone — for durable linking. Optional slug suffix for readability: `/objects/stonehenge--whs-373` where `stonehenge` is cosmetic and `whs-373` is authoritative.
- **ARK identifiers** appear in metadata and JSON-LD `identifier` — canonical ARK URIs resolve via Platform resolver, not frontend routing.
- **Trailing slashes:** Consistent policy via `trailingSlash: false` in `next.config.ts`.

### Parallel routes and intercepting (optional)

- `@modal/(..)objects/[stableId]` — Accessible quick-view drawer on map/search without losing context.
- `@panel` on map route — Side panel for selected feature (mobile: full-screen sheet via shadcn `Sheet`).

### Route groups (non-segment)

```
app/[locale]/(public)/     # Marketing + explore — full chrome
app/[locale]/(immersive)/  # Map, visual narratives — minimal chrome
app/[locale]/(learn)/      # Education — age-appropriate chrome variant
```

---

## Component Architecture

Four layers, bottom-up. **Domain components** never import from `app/`; **pages** compose domain + layout only.

```
┌─────────────────────────────────────────────────────────┐
│  Pages (app/[locale]/…/page.tsx)                        │
│  — data fetching, generateMetadata, JSON-LD injection   │
├─────────────────────────────────────────────────────────┤
│  Domain components (components/domain/)                  │
│  — ObjectHero, SpeciesTaxonomyTree, PlaceBoundaryMap, …   │
├─────────────────────────────────────────────────────────┤
│  Feature / pattern components (components/layout|media) │
│  — EntityPageLayout, ProvenanceTimeline, IIIFViewer     │
├─────────────────────────────────────────────────────────┤
│  shadcn/ui primitives (components/ui/)                  │
│  — Button, Dialog, Tabs, NavigationMenu, Sheet, …       │
└─────────────────────────────────────────────────────────┘
```

### Server vs. Client Components

| Default | Server Component | Client Component (`"use client"`) |
|---------|------------------|-----------------------------------|
| Entity page body | ✓ | |
| Search facets (URL-driven) | ✓ initial | Hydrate interactive controls |
| MapLibre map | | ✓ |
| IIIF OpenSeadragon viewer | | ✓ |
| Locale switcher | | ✓ (cookie write) |
| Provenance timeline (static) | ✓ | |
| Low-bandwidth toggle | | ✓ (localStorage) |

**Rule:** Push `"use client"` boundaries as deep as possible — leaf interactive widgets only.

### shadcn/ui usage

- Initialize with **New York** style, **neutral** base, **CSS variables** for theming.
- Extend tokens in `globals.css` for institution brand (Nature & Culture) without forking primitives.
- Components to install at scaffold: `button`, `navigation-menu`, `dialog`, `sheet`, `tabs`, `breadcrumb`, `card`, `badge`, `skeleton`, `select`, `command` (search palette), `toast`, `tooltip`, `dropdown-menu`, `separator`, `aspect-ratio`.
- **Do not** use shadcn for map canvas, IIIF viewer, or data tables with 1000+ rows — dedicated accessible libraries.

### Core layout components

| Component | Responsibility |
|-----------|----------------|
| `SiteHeader` | Global nav, search trigger (Cmd+K), locale switcher, low-bandwidth toggle |
| `SiteFooter` | Institutional links, language list, rights/attribution |
| `SkipLink` | WCAG bypass block |
| `EntityPageLayout` | Two-column responsive: media + narrative / metadata sidebar |
| `ProvenanceTimeline` | Ordered provenance chain from view model |
| `RightsBadge` | Europeana/CC rights display with link |
| `TranslationAttribution` | Human/machine/community tier per ADR-008 |
| `EvidencePanel` | Evidence Output Profile fields (03 §6.6) for observatory content |

### Domain component modules

```
components/domain/
├── objects/
│   ├── ObjectHero.tsx
│   ├── ObjectMetadata.tsx
│   └── ObjectRelatedEntities.tsx
├── species/
│   ├── SpeciesSummary.tsx
│   ├── TaxonomyBreadcrumb.tsx
│   └── OccurrenceMapPreview.tsx
├── places/
│   ├── PlaceBoundaryMap.tsx
│   ├── PlaceHeritageStatus.tsx
│   └── PlaceSpeciesRollup.tsx
├── collections/
│   ├── CollectionGrid.tsx
│   ├── VisualNarrative.tsx
│   └── ExhibitTableOfContents.tsx
├── maps/
│   ├── MapExplorer.tsx
│   ├── MapFeaturePopup.tsx
│   └── BboxSearchController.tsx
├── learning/
│   ├── LessonCard.tsx
│   ├── CurriculumBadge.tsx
│   └── TeacherGuideDownload.tsx
└── research/
    ├── DatasetCitation.tsx
    ├── ApiEndpointDoc.tsx
    └── ResearchSearchForm.tsx
```

### Design tokens (mobile-first)

Tailwind breakpoints:

- **Default (0–639px):** Single column, bottom nav, map full-bleed, touch targets ≥ 44×44px.
- **`sm`/`md`:** Sidebar collapses to sheet.
- **`lg`+:** Two-column entity layout, persistent map + panel.

Low-bandwidth mode (06 §Phase 11): Client flag suppresses autoplay, replaces IIIF deep zoom with static surrogates, reduces map tile resolution.

---

## API Integration Strategy

### Principle: FastAPI only

All data access flows:

```
Browser → Next.js Server Component / Route Handler → api-service (FastAPI) → Platform services
```

No direct PostgreSQL, OpenSearch, MinIO, or SPARQL from the frontend. GraphQL — when available — is consumed **through the same gateway**, not embedded in Client Components.

### Typed client (`packages/wise-api-client`)

1. Export OpenAPI schema from FastAPI: `GET /openapi.json`.
2. Generate TypeScript types via `openapi-typescript`.
3. Wrap with thin `createWiseClient({ baseUrl, locale, fetch })` adding:
   - `Accept-Language` header from locale segment
   - Structured error type (`WiseApiError` with `status`, `code`, `detail`)
   - Timeout (default 10s server, 5s client-side prefetch)
   - Optional `Authorization: Bearer` for Research/Community routes

```typescript
// Server-only usage pattern
import { getObject } from "@wise/api-client";

export default async function ObjectPage({ params }) {
  const object = await getObject(params.stableId, {
    locale: params.locale,
    revalidate: 3600,
  });
  if (!object.rights_verified) notFound();
  return <ObjectHero object={object} />;
}
```

Types align with Python `wise-contracts` Pydantic models (`HeritageObjectView`, `SpeciesObjectView`, `ProtectedAreaObjectView`, `MapSearchResult`, future search/publishing types).

### Endpoint map (current + planned)

| Domain | Status | Method | Path |
|--------|--------|--------|------|
| Objects | **Implemented** | GET | `/v1/objects/{stable_id}` |
| Species | **Implemented** | GET | `/v1/species/{stable_id}` |
| Places (areas) | **Implemented** | GET | `/v1/areas/{stable_id}` |
| Maps | **Implemented** | GET | `/v1/map/areas/{stable_id}`, `/v1/map/search?bbox=` |
| Search | Planned (Phase 6) | GET | `/v1/search?q=&facet=&locale=` |
| Collections | Planned (Phase 10) | GET | `/v1/collections/{slug}?locale=` |
| IIIF manifest | Planned (Phase 10) | GET | `/v1/iiif/{manifest_id}` |
| Locales | Planned (Phase 9) | GET | `/v1/locales`, `/v1/locales/{locale}/bundle` |
| Graph entity | Planned (Phase 5) | GET | `/v1/entities/{uri}?locale=` |
| Education | Planned (Phase 13) | GET | `/v1/education/resources`, `/v1/education/resources/{id}` |
| Research | Planned (Phase 8) | GET | `/v1/research/datasets`, `/v1/research/datasets/{doi}` |

Query parameter **`locale`** (BCP 47) on all experience endpoints — Platform returns localized fields per Translation Fabric; source language always included in `_source` namespace.

### Caching and rendering strategy

| Content type | Strategy | Revalidation |
|--------------|----------|--------------|
| Entity pages (objects, species, places) | SSG + ISR | 3600s default; on-demand via `/api/revalidate` webhook from Publishing |
| Home, collections | ISR | 60–300s |
| Search results | SSR dynamic | `cache: 'no-store'` — always fresh |
| Map bbox queries | SSR + short cache | 60s `revalidate` |
| Static assets (fonts, icons) | Vercel CDN | Immutable |
| IIIF images | Platform CDN / IIIF server | Respect `Cache-Control` from image service |

Use Next.js 15 `fetch(url, { next: { revalidate, tags } })` with cache tags per entity: `object:stonehenge`, `locale:fr`.

**On-demand revalidation:** Publishing Agent emits webhook post-approval → Platform calls Vercel `revalidateTag` for affected entities.

### Optional BFF route handlers

Route handlers under `app/api/` are permitted **only** for:

- Revalidation webhooks (HMAC-verified)
- OAuth callback proxy (Research/Community — future)
- IIIF manifest CORS proxy if image servers lack CORS (minimize use)

BFF must not become a shadow Platform Plane — no business logic duplication.

### Error handling

| HTTP status | User experience |
|-------------|-----------------|
| 404 | Localized `not-found.tsx` with search suggestion |
| 403 / rights withheld | Explain public access constraint; no entity leak |
| 422 | Validation message (map bbox) inline |
| 429 | Retry-after banner; backoff |
| 5xx | Static fallback page; no stack traces; report correlation ID |

Log upstream errors server-side with `x-request-id` propagation from api-service.

### Feature flags

`lib/constants/features.ts` gates routes for incomplete Platform phases:

```typescript
export const features = {
  search: process.env.NC_FEATURE_SEARCH === "true",
  publishing: process.env.NC_FEATURE_PUBLISHING === "true",
  education: process.env.NC_FEATURE_EDUCATION === "true",
  research: process.env.NC_FEATURE_RESEARCH === "true",
};
```

Unready features show roadmap-safe placeholders — not broken routes.

---

## Vercel Deployment Strategy

### Project configuration

| Setting | Value |
|---------|-------|
| Root directory | `apps/nature-culture-web` |
| Framework | Next.js 15 |
| Node.js | 20 LTS |
| Install command | `pnpm install` (from monorepo root with filter) |
| Build command | `pnpm --filter nature-culture-web build` |
| Output | Default Next.js |

### Environments

| Environment | Branch | API upstream |
|-------------|--------|--------------|
| Production | `main` | `https://api.natureandculture.org` (Zone Alpha + CDN) |
| Preview | PR branches | `https://api-staging.natureandculture.org` or per-PR ephemeral |
| Development | local | `http://localhost:8000` |

### Environment variables

| Variable | Scope | Purpose |
|----------|-------|---------|
| `WISE_API_BASE_URL` | Server | FastAPI gateway base URL |
| `WISE_API_TIMEOUT_MS` | Server | Upstream timeout |
| `NEXT_PUBLIC_SITE_URL` | Public | Canonical URL for SEO |
| `NEXT_PUBLIC_DEFAULT_LOCALE` | Public | Fallback locale (`en`) |
| `NC_FEATURE_*` | Server | Phase gating flags |
| `REVALIDATION_SECRET` | Server | HMAC for on-demand ISR webhook |
| `VERCEL_ENV` | System | Environment detection |

**Never expose** database URLs, MinIO credentials, or internal service tokens to the frontend.

### Edge vs. Node runtime

| Workload | Runtime |
|----------|---------|
| Middleware (locale, security headers, bot detection) | **Edge** |
| Entity pages, search SSR, API client fetch | **Node** (default) |
| Static generation / ISR | **Node** build |
| Image optimization (`next/image`) | Vercel Image Optimization → IIIF allowed domains |

Do not run heavy IIIF processing on Edge. Map tile requests go directly from client to tile server (domain allowlist in CSP).

### Preview deployments

- Every PR generates a preview URL.
- Previews call staging API; **no production canonical writes** (ADR-002).
- Optional: Vercel Comments for design review.
- Preview robots: `X-Robots-Tag: noindex` via middleware when `VERCEL_ENV === 'preview'`.

### Security headers (next.config.ts)

- Strict CSP (default-src 'self'; img-src IIIF + CDN; connect-src API gateway)
- HSTS, X-Frame-Options, Referrer-Policy
- Permissions-Policy (disable unused APIs)

### Performance targets (06 §Phase 11)

- **LCP p95 < 2.5s** on 4G (mobile-first)
- **Page load p95 < 3s** institutional target
- Core Web Vitals monitored via Vercel Analytics + optional OpenTelemetry export

### Monorepo CI

GitHub Actions:

1. `pnpm lint && pnpm typecheck`
2. `pnpm test:a11y && pnpm test:e2e`
3. `pnpm build` (nature-culture-web)
4. Vercel deployment on success

OpenAPI drift check: regenerate `wise-api-client` types in CI; fail if schema changed without client update.

---

## SEO Strategy

SEO is structural — not a post-launch overlay.

### Metadata API

Every `page.tsx` exports `generateMetadata` using Platform-provided SEO fields (title, description, og:image from Publishing). Fallback to entity label + institutional template.

### JSON-LD (schema.org)

Per 22-standards-agent and 07 §11:

| Page type | schema.org type |
|-----------|-----------------|
| Heritage object | `MuseumObject`, `CreativeWork` |
| Species | `Taxon` |
| Place | `Place`, `LandmarksOrHistoricalBuildings` where applicable |
| Collection | `Collection`, `CreativeWorkSeries` |
| Article / exhibit | `Article`, `LearningResource` |

Inject via `<JsonLd data={…} />` server component. Identifiers (`sameAs`, ARK, Wikidata, GBIF) from graph view models.

### Sitemaps

Dynamic `sitemap.ts`:

- Paginated entity sitemaps per locale (`/sitemap/objects/1.xml`, …)
- `lastmod` from Platform `updated_at`
- Submit to search consoles per environment

### hreflang

Alternate links for every indexed page across supported locales. `x-default` points to default locale URL.

### Crawl policy

- `robots.ts`: Allow public entities; disallow `/api/`, preview auth routes.
- Canonical URL always includes locale prefix matching content language.

### Performance as SEO

ISR + image optimization + font subsetting. Avoid client-only rendering for primary content.

---

## Accessibility Approach (WCAG 2.2 AA)

Canonical baseline is **WCAG 2.1 AA** (07 §7, 06 §Phase 11). This design **targets WCAG 2.2 AA** as a superset — satisfying 2.1 AA plus 2.2 criteria (focus appearance, dragging movements, target size).

### Implementation checklist

| Area | Approach |
|------|----------|
| Semantics | Native HTML5 landmarks; one `<h1>` per page; logical heading order |
| Keyboard | All actions keyboard-operable; visible focus rings (shadcn defaults enhanced) |
| Screen readers | ARIA only where necessary; live regions for search results updates |
| Color | Contrast ≥ 4.5:1 text; high-contrast theme toggle |
| Motion | `prefers-reduced-motion` disables map fly animations, carousels |
| Media | IIIF alt text from Quality Platform; transcripts for AV |
| Map | Keyboard pan/zoom alternatives; feature list duplicate of map points |
| Forms | Labelled inputs; error identification (WCAG 3.3.1) |
| Target size | Touch targets ≥ 44×44px (WCAG 2.5.8) |

### Testing

- **Automated:** axe-core in CI on key templates; eslint-plugin-jsx-a11y
- **Manual:** Screen reader smoke (NVDA/VoiceOver) per release
- **Quality gate:** Honor `accessibility_compliant` flag on view models (13-quality-review-agent)

---

## Mobile-First & i18n Approach

### Mobile-first

- CSS mobile defaults first; progressive enhancement at `md`/`lg`
- Bottom navigation on mobile (`SiteMobileNav`); top nav on desktop
- Map and media viewers: full-viewport on small screens
- Low-bandwidth mode persisted in cookie/localStorage
- `viewport` meta: device-width, interactive-widget support

### Internationalization

**Architecture (ADR-008):**

```
Translation Fabric (Platform)
  └── Localized Content Bundle
        ├── entity.labels[locale]
        ├── entity.descriptions[locale]
        ├── ui.strings[locale]        # replaces messages/*.json over time
        └── provenance.tier           # human | machine | community
```

**Implementation:**

- Library: `next-intl` with `[locale]` segment
- Formatting: `@formatjs/intl` or native `Intl` for dates/numbers (CLDR via Unicode CLDR — 07 §9)
- RTL: `dir={localeDir}` on `<html>` for Arabic, Hebrew, etc.
- Language negotiation: Middleware + cookie persistence
- **Never** hard-code entity factual content in frontend — only chrome fallbacks in `messages/` until bundles arrive
- Search: locale-aware ranking from Platform (Phase 6 + 9)

---

## Domain-Specific Notes

### Objects (Heritage)

- **Contract:** `HeritageObjectView` (`GET /v1/objects/{stable_id}`)
- **Standards:** CIDOC-CRM entity mapping, ARK in JSON-LD, Europeana EDM parallels
- **UI:** Provenance timeline, source registry badge, related graph entities, IIIF media when publishing clearance exists
- **Gate:** Require `rights_verified && quality_approved` before full public render

### Places

- **Contract:** `ProtectedAreaObjectView` + `MapAreaSummary`
- **Standards:** schema.org `Place`, GeoJSON boundaries (07 §5)
- **UI:** Boundary map (MapLibre), heritage status from graph, species/site rollups
- **Note:** "Places" is the public UX term; API path `/v1/areas/` reflects protected-area Reference Capability 3 — generalize to `/v1/places/` when graph entity type expands

### Species

- **Contract:** `SpeciesObjectView`
- **Standards:** Darwin Core, GBIF Taxon identifiers, schema.org `Taxon`
- **UI:** Taxonomy breadcrumb, occurrence map preview, threatened status from Biodiversity Observatory (Phase 15 — read-only approved signals)
- **Field guides:** Publishing manifest integration (Phase 10)

### Collections

- **Contract:** `PublishedCollectionManifest` (Phase 10)
- **Standards:** IIIF Presentation API 3.0, EDM
- **UI:** Visual narrative layouts (Publishing Agent patterns), grid/list toggle, downloadable open datasets where licensed
- **Multilingual:** Edition switcher per Translation Fabric bundles

### Maps

- **Contract:** `GET /v1/map/search?bbox=`, `GET /v1/map/areas/{id}`
- **Stack:** MapLibre GL JS + vector/raster tiles from Platform tile service
- **Accessibility:** List-based browse of features in bbox; table sort/filter
- **Performance:** Debounced bbox queries; cluster markers at low zoom
- **Future:** Observatory layers (climate, biodiversity, tourism) as toggled overlays — approved observations only (17–20 agent specs)

### Learning

- **Phase:** 13 (depends on Publishing + Public Experience)
- **Contract:** Learning Resource bundles from Education Agent (16-education-agent)
- **UI:** Age-appropriate layouts, curriculum standard badges (NGSS, UNESCO frameworks), teacher guide downloads
- **Safety:** Student-facing routes honor restriction flags; no observatory alerts without classroom clearance
- **Standards:** HTML5, WCAG 2.1 AA minimum, optional SCORM export links

### Research

- **Phase:** 8 (Research Fabric)
- **Contract:** REST/OpenAPI documented datasets, DOI metadata, citation blocks
- **UI:** Dataset catalog, API documentation mirror, download links to bulk exports (never direct MinIO)
- **Auth:** OAuth 2.1 for elevated quotas — token exchange via Platform, not frontend secrets
- **Constitutional:** Open access emphasis; no gating canonical public memory (03 §5.2)

---

## Implementation Phases (Suggested)

Aligned with founder build order — frontend work **tracks** Platform readiness, does not precede it.

| Milestone | Platform dependency | Frontend deliverable |
|-----------|--------------------|--------------------|
| M0 Scaffold | api-service RC endpoints | App shell, object/species/place pages, map MVP |
| M1 Search | Phase 6 | `/explore` with facets, entity panels |
| M2 i18n | Phase 9 | Locale bundles, hreflang, 20+ locales |
| M3 Publishing | Phase 10 | Collections, IIIF viewer, visual narratives |
| M4 Launch | Phase 11 gate | WCAG audit, performance budget, production Vercel |
| M5 Learning | Phase 13 | `/learn` portal |
| M6 Research | Phase 8 (parallel) | `/research` portal |
| M7 Observatories | Phase 15 | Map overlays, dashboard embeds |

---

## Governance and Change Control

This document is an **implementation design companion**. It does not amend architecture-v1.0, ADRs, or the Architecture Registry.

Changes to Experience Plane **behavior** that affect Platform contracts require Architecture Office review. Changes to frontend framework choices (Next.js, Vercel) are Engineering Council decisions within ADR-002's read-only boundary.

---

## References

| Document | Relevance |
|----------|-----------|
| [03-canonical-architecture.md](canonical/03-canonical-architecture.md) | Experience Plane §5, contracts §7 |
| [06-build-roadmap.md](canonical/06-build-roadmap.md) | Phase 11 success criteria |
| [05-physical-architecture.md](canonical/05-physical-architecture.md) | CDN, T0 Hot delivery |
| [07-reference-standards.md](canonical/07-reference-standards.md) | HTML, WCAG, IIIF, hreflang |
| [08-decision-record.md](canonical/08-decision-record.md) | ADR-001, ADR-002, ADR-003, ADR-008 |
| [15-publishing-agent.md](canonical/15-publishing-agent.md) | Collection manifests, IIIF |
| [16-education-agent.md](canonical/16-education-agent.md) | Learning resources |
| [architecture-registry.md](../governance/architecture-registry.md) | v1.0 freeze authority |
| [architecture-overview.md](../../architecture-overview.md) | Current implementation map |

---

*Document version: 1.0 · Aligns with architecture-v1.0 (`architecture-v1.0` tag) · Does not modify governance.*
