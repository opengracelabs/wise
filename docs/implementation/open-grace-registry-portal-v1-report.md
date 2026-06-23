# Open Grace Registry Portal v1 — Implementation Report

**Date:** 2026-06-23  
**Location:** `apps/open-grace-registry/`  
**Status:** Complete

## Summary

Delivered a read-only Next.js (App Router) registry portal that surfaces Open Grace governance data from bundled static JSON. The portal requires no Python runtime, no authentication, and no external APIs at dev or runtime.

## Scope delivered

### Pages

| Route | Records (seed sync) |
|-------|---------------------|
| `/` | Overview with counts |
| `/agents`, `/agents/[id]` | 15 agents |
| `/capabilities`, `/capabilities/[id]` | 8 capability classes |
| `/benchmarks`, `/benchmarks/[id]` | 13 benchmarks |
| `/audits`, `/audits/[id]` | 5 audit records |
| `/models`, `/models/[id]` | 5 models |

### Features

- **Search** — client-side query across id, display name, and related fields via URL params (`?q=`)
- **Filtering** — lifecycle stage, plane (agents), outcome (audits), reference model
- **Benchmark scores** — observed values with pass/fail against thresholds; capability-level gate evaluation
- **Risk ratings** — severity badges and mitigation on capability detail pages
- **Audit history** — timeline on agent and capability detail pages; full audit browser
- **Standards compliance** — required standards with binding URIs and conformance level on capability pages
- **Reference models** — Wikidata, GBIF, UNESCO World Heritage List (plus NIST AI RMF, ISO 42001, etc.) shown as metadata tags

### Data strategy

`scripts/sync-seed-data.mjs` aggregates YAML seeds at build/sync time:

| Output JSON | Source |
|-------------|--------|
| `agents.json` | `data/registry/agents/manifest.yaml` |
| `capabilities.json`, `agent-bindings.json` | `packages/open-grace-governance/.../capability_framework.yaml` |
| `benchmarks.json` | `packages/open-grace-benchmarking/.../benchmark_registry.yaml` |
| `benchmark-scores.json` | Generated passing observed values |
| `risks.json`, `standards.json` | `packages/open-grace-governance/.../risk_registry.yaml`, `standards_registry.yaml` |
| `models.json` | `packages/open-grace-agent-registry/.../model_registry.yaml` |
| `audits.json` | Generated lifecycle audit records for constitutional agents and sample capabilities |
| `reference-models.json` | Portal reference model profiles |

Committed JSON under `data/` allows `npm install && npm test` without running sync first.

## Architecture

```
apps/open-grace-registry/
├── data/                    # Static JSON (synced from package seeds)
├── scripts/sync-seed-data.mjs
├── src/
│   ├── app/                 # Next.js App Router pages
│   ├── components/          # UI primitives (badges, filters, timelines)
│   └── lib/
│       ├── data.ts          # Static loader + cross-registry joins
│       ├── search.ts        # Filter utilities
│       └── types.ts         # TypeScript contracts
└── package.json
```

- **Read-only:** no write endpoints or forms
- **No auth:** public static/SSG pages
- **No external APIs:** all data from `import ... from "../../data/*.json"`

## Tests

Vitest suite (`npm test`):

- `src/lib/data.test.ts` — loader, lookups, benchmark evaluation, capability gate
- `src/lib/search.test.ts` — search/filter utilities

**Result:** 15 tests passed (2 files).

## Build verification

- `npm run build` — succeeds; 55 static pages generated via `generateStaticParams`
- `npm run dev` — development server on port 3000

## How to run

```bash
cd apps/open-grace-registry
npm install
npm run dev      # http://localhost:3000
npm test
npm run sync-data   # refresh data/ from package seeds
```

## Out of scope (v1)

- Knowledge registry pages (`open-grace-knowledge` seeds not surfaced — portal focuses on governance registries per requirements)
- Observability package integration (not present in repo at implementation time)
- Write operations, steward approval workflows, live benchmark ingestion
- Authentication and deployment configuration

## Files created

- `apps/open-grace-registry/` — full Next.js application (package.json, pages, components, lib, tests, README)
- `apps/open-grace-registry/data/*.json` — 10 bundled registry files
- `docs/implementation/open-grace-registry-portal-v1-report.md` — this report

## Constraints observed

- Canonical WISE architecture and package seeds were read only; no modifications to `packages/open-grace-*` or `data/registry/`
- No git push performed
