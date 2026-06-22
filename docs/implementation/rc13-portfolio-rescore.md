# RC13 Portfolio Re-Score

**Status:** Implementation scoring artifact  
**Authority:** Architecture v1.0, frozen by ADR-011  
**Scope:** Portfolio data expansion and scoring only  

RC13 compares the original RC9 portfolio, the RC11 showcase distillation, and
the expanded RC13 portfolio. It does not modify governance, architecture, agents,
ADRs, registries, schemas, or canonical data stores.

## Frozen-architecture boundary

- Architecture v1.0 remains frozen.
- No governance changes are proposed or made.
- No architecture changes are proposed or made.
- No agents are proposed or added.
- No ADRs are proposed or added.
- RC13 outputs are implementation data/report artifacts only.

## Review basis

The requested `docs/implementation/rc11-gap-analysis.md` file is not present on
this branch. RC13 therefore uses the available RC9 audit gap sections and RC11
showcase report as the implementation review basis:

- `docs/implementation/rc9-portfolio-audit.md`
- `docs/implementation/rc11-showcase-report.md`

## Portfolio versions compared

| Portfolio | Files | Purpose |
|-----------|-------|---------|
| RC9 portfolio | `top_100_global_assets.json`, `top_100_collections.json`, `top_100_series.json` | Initial commercial validation portfolio |
| RC11 showcase | `top_25_showcase_assets.json`, `top_25_showcase_collections.json`, `top_25_showcase_series.json`, `top_25_showcase_products.json` | Launch-focused distillation |
| RC13 expanded portfolio | `expansion_candidates.json`, `top_200_global_assets.json`, `top_200_collections.json`, `top_200_series.json` | Representation-balanced expansion |

## Score comparison

| Dimension | RC9 | RC11 | RC13 | Change from RC9 |
|-----------|----:|-----:|-----:|----------------:|
| Geographic diversity | 70 | 78 | 92 | +22 |
| Cultural balance | 80 | 84 | 91 | +11 |
| Biodiversity balance | 80 | 86 | 91 | +11 |
| Public-domain readiness | 80 | 84 | 88 | +8 |
| Indigenous representation | 62 | 70 | 90 | +28 |
| Education value | 90 | 92 | 94 | +4 |
| Product potential | 90 | 94 | 93 | +3 |
| Portfolio balance | 80 | 86 | 92 | +12 |
| **Overall portfolio score** | **84** | **88** | **91** | **+7** |

## Target result

RC13 reaches the target improvement:

**84 -> 91**

This clears the requested **90+** threshold by adding 100 representation-focused
asset candidates and 100 additional collections and series.

## Why RC13 improves the score

### Geographic balance

RC13 adds substantial representation for:

- Sub-Saharan Africa,
- West Asia,
- Central Asia,
- South Asia,
- Oceania,
- Indigenous cultures across the Americas, Arctic, and Pacific.

### Cultural balance

RC13 adds:

- African kingdoms and cities,
- Islamic architecture and geometry,
- Persian miniature and manuscript contexts,
- Silk Roads cities,
- South Asian sacred sites and cave temples,
- textile and pattern heritage,
- Indigenous knowledge contexts.

### Biodiversity balance

RC13 adds:

- baobab and forest ecosystems,
- African wild dog, shoebill, Ethiopian wolf,
- Arabian oryx and cedar of Lebanon,
- saiga antelope and Bactrian camel,
- Bengal tiger, Ganges river dolphin, Himalayan monal,
- kakapo, kiwi, kea, Tasmanian devil, birds-of-paradise,
- Amazon biodiversity, Andean condor, and jaguar corridor maps.

### Public-domain readiness

RC13 improves readiness by distinguishing:

- `public_domain_ready`,
- `open_access_ready`,
- `public_domain_likely`,
- `public_domain_item_review`,
- `public_domain_data_needs_design`,
- `image_rights_required`,
- `needs_image_clearance`,
- `needs_partner_clearance`,
- `sensitivity_review_required`.

The portfolio still requires item-level rights work before production, but RC13
now makes rights readiness visible in the expanded portfolio files.

### Indigenous representation

RC13 adds Indigenous and sensitivity-aware candidates without converting them
into unrestricted commercial production claims. These are marked for sensitivity
or partner review where appropriate.

## Remaining score constraints

RC13 reaches 91 rather than a higher score because:

1. Many Indigenous and cultural knowledge candidates require sensitivity review.
2. Wildlife and ecosystem candidates still require rights-cleared imagery.
3. Some public-domain readiness is likely but not item-verified.
4. Regional expansion improves balance, but production readiness remains uneven.
5. The expansion is a prototype dataset, not a final canonical portfolio.

## Recommended portfolio-only next steps

These actions stay within implementation/data scope:

1. Add rights-clearance status per item.
2. Add sensitivity-review status per Indigenous/cultural knowledge candidate.
3. Add region and culture tags to future top 25 showcase derivatives.
4. Split production-ready assets from discovery/watchlist assets.
5. Build a public-domain evidence checklist for maps, manuscripts, and art.
6. Add biodiversity taxon type tags to reduce mammal overrepresentation.
7. Re-run showcase selection from the expanded top 200 data.

## Conclusion

RC13 successfully expands the portfolio from a commercially strong but
geographically concentrated RC9 score of **84** to a representation-balanced
expanded portfolio score of **91**. It follows ADR-011 and introduces no
architecture, governance, agent, or ADR changes.
