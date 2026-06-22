# RC14 Content Readiness Report

| Field | Value |
|-------|-------|
| **Status** | Implementation report (non-governance) |
| **Date** | 2026-06-22 |
| **Scope** | First publishable content drafts (collections, products, SEO, newsletter, ebook) built from the RC11 showcase + RC13 portfolio |
| **Constraints** | Does not modify Architecture v1.0, governance, ADRs, or agents (ADR-011) |

## Summary

RC14 produces the **first publishable content set** under `content/` — 38 draft files grounded in the portfolio data (`data/portfolio/*`). Every factual claim is drawn from each asset's `historical_significance`; every product references real catalogue entries and their `source_asset_ids`. All drafts are marked *draft for review — not yet published* and carry a rights gate.

---

## 1. Content completed

| Area | Path | Count | Notes |
|------|------|------:|-------|
| Collection drafts | `content/collections/` | 10 | intro · key assets · educational narrative · product opportunities |
| Product pages | `content/products/` | 10 | posters (2), framed prints (2), calendars (2), puzzles (2), coffee-table books (2) |
| SEO landing pages | `content/seo/` | 10 | meta · H1/hero · body · internal links · FAQ · JSON-LD |
| Newsletter issues | `content/newsletter/` | 4 | welcome · collections · species · products |
| Ebook (Big Cats) | `content/ebooks/big-cats-of-the-world/` | 4 | outline · chapters · product page · marketing copy |
| **Total** | `content/` | **38** | |

### Collections (10)
Big Cats of the World · Great Civilizations · World Heritage Icons · Endangered Earth · Sacred Mountains · Ancient Maps · Oceans of the World · African Kingdoms · Cities of the Silk Road · Wonders of Australia.

Each draft links its real key assets (e.g. African Kingdoms → Great Zimbabwe, Benin Bronzes, Timbuktu, Meroë, Lalibela, Nok) with the verified significance text, an educational narrative, and mapped product opportunities.

### Products (10)
Across all five requested categories, each referencing catalogue products and their source assets, with specs, audience, fulfilment provider and SEO metadata. Public-domain artwork SKUs (Starry Night, Vermeer) lead because they are reproduction-ready.

### SEO (10)
One landing page per collection with URL, meta title/description, primary + secondary keywords, hero, body, internal-link plan, FAQ, and draft schema.org JSON-LD (`CollectionPage` / `CreativeWorkSeries`).

### Newsletter (4) & Ebook
Four issues with subject lines, preview text and CTAs; the *Big Cats of the World* ebook with a 10-chapter structure (6 species chapters + culture + conservation), product page (ebook + print editions) and marketing copy.

---

## 2. Content gaps

| Gap | Impact | Action |
|-----|--------|--------|
| **Imagery** | Drafts are text-only; no hero/plate images are attached | Source public-domain masters (artworks/maps) and license/commission photography (sites/species) |
| Localization | English only | Route through Translation Fabric (Phase 9) at publish time; do not hard-code translations |
| Long-form depth | Ebook ships chapter *summaries*, not full prose | Commission/expand full chapters before sale |
| Remaining collections | 10 of 200 collections drafted | Extend with the same generator pattern as demand dictates |
| Pricing | Product pages omit prices | Add per-region pricing once POD quotes are confirmed |
| Cross-linking | Internal links are described, not wired | Implement when `nature-culture-web` exists (see `rc9-public-launch-plan.md`) |
| Fact review | Auto-composed from significance strings | Editorial + subject-matter review before publication |

---

## 3. Publication readiness

| Channel | Readiness | Blockers |
|---------|-----------|----------|
| Collection pages | **Draft-complete** | imagery, editorial review, web app to host |
| Product pages | **Draft-complete** | imagery, pricing, POD contracts, storefront (Phase 12) |
| SEO pages | **Draft-complete** | imagery (OG), live URLs, sitemap/robots (per `rc9-public-launch-plan.md`) |
| Newsletter | **Draft-complete** | ESP setup, consent list, imagery |
| Ebook | **Outline-complete** | full chapter prose, plates, ISBN/edition setup |

**Overall:** content is **draft-ready, not publish-ready.** The text scaffolding is in place; the gating dependencies are imagery + rights clearance, editorial review, and the publishing/commerce surfaces (Phases 10-12), which are not yet built.

---

## 4. Rights considerations

- **Tiered readiness.** Public-domain artworks, maps and manuscripts (Smithsonian Open Access, Rijksmuseum, NGA, Library of Congress, Europeana, Public Domain Review) are reproduction-ready. Heritage sites, landscapes and species are public *subjects* but require own/commissioned or CC-licensed photography before any page or product goes live.
- **Hard gate.** No asset is published or sold until it passes discovery → preservation → metadata → rights/quality and carries machine-readable rights (Europeana Rights Statements / Creative Commons). Each draft repeats this gate in its footer.
- **Indigenous & cultural sensitivity.** African Kingdoms, Cities of the Silk Road, Wonders of Australia (Kakadu, Uluru) and Indigenous material require provenance, community attribution, and exclusion of restricted/sacred content until cleared.
- **ADR-010.** All products are derived goods; canonical public memory remains free and un-paywalled. Marketing must not imply that access to heritage is gated.
- **Conservation claims.** "A share of proceeds supports conservation" appears in Endangered Earth and the Big Cats ebook; it must be backed by a real, disclosed partner agreement before publication.

---

*Implementation report. Does not modify Architecture v1.0, governance, ADRs, or agents (ADR-011). Content: `content/`. Data: `data/portfolio/top_25_showcase_*.json`, `top_200_*.json`.*
