# Open Grace Registry Portal

Read-only Next.js portal for browsing Open Grace governance registries: agents, capability classes, benchmarks, audits, and model council assignments.

## Prerequisites

- Node.js 20+
- npm

No Python runtime is required for local development — registry data is bundled as static JSON under `data/`.

## Setup

```bash
cd apps/open-grace-registry
npm install
```

To refresh bundled data from Open Grace package seeds:

```bash
npm run sync-data
```

This reads YAML seeds from `packages/open-grace-*` and the canonical WISE agents manifest, then writes JSON into `data/`.

## Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Tests

```bash
npm test
```

Vitest covers the static data loader and search/filter utilities.

## Pages

| Route | Description |
|-------|-------------|
| `/` | Portal overview |
| `/agents` | Agent fleet list |
| `/agents/[id]` | Agent detail with benchmarks and audits |
| `/capabilities` | Capability class list |
| `/capabilities/[id]` | Capability detail with risks, standards, benchmark gate |
| `/benchmarks` | Benchmark definitions and scores |
| `/benchmarks/[id]` | Benchmark threshold and observed score |
| `/audits` | Audit evidence trail |
| `/audits/[id]` | Audit record detail |
| `/models` | Model council registry |
| `/models/[id]` | Model governance metadata |

## Data sources

Static JSON is generated from:

- `packages/open-grace-governance/data/seed/` — capabilities, risks, standards
- `packages/open-grace-benchmarking/data/seed/` — benchmarks
- `packages/open-grace-agent-registry/data/seed/` — models
- `data/registry/agents/manifest.yaml` — canonical agent fleet

Reference models displayed in the UI include **Wikidata**, **GBIF**, and **UNESCO World Heritage List**.

## Constraints

- Read-only — no mutations or authentication
- No external API calls at runtime
- Data loaded from bundled JSON via `src/lib/data.ts`
