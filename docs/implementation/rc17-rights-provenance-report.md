# RC17 Rights & Provenance Infrastructure Report

**Status:** Implementation rights/provenance artifact  
**Scope:** Convert RC14 content assets into publication-governed assets  
**Boundary:** Does not modify architecture, governance, ADRs, or the Open Grace canonical model.

## Objective

RC17 creates a rights and provenance infrastructure layer for the RC14 flagship content drafts. It registers collection assets, sources, licenses, attributions, provenance events, publication approval states, and jurisdiction rules.

## Created registries

| Registry | Path | Purpose |
|----------|------|---------|
| Asset registry | `rights/asset-registry.json` | Registers every unique RC14 collection asset with source, license, rights status, and publication status |
| Source registry | `rights/source-registry.json` | Defines source classes used by collection assets |
| License registry | `rights/license-registry.json` | Defines allowed non-unknown license categories |
| Attribution registry | `rights/attribution-registry.json` | Provides displayable attribution records for each asset |
| Provenance registry | `rights/provenance-registry.json` | Records registration provenance from RC14 collection drafts |
| Publication approvals | `rights/publication-approvals.json` | Tracks publication status, blockers, and next action |
| Jurisdiction rules | `rights/jurisdiction-rules.json` | Records publication risk rules by jurisdiction/source context |

## Created policy docs

| Document | Path |
|----------|------|
| Rights policy | `docs/rights/rights-policy.md` |
| Provenance policy | `docs/rights/provenance-policy.md` |
| Attribution policy | `docs/rights/attribution-policy.md` |
| Publication approval process | `docs/rights/publication-approval-process.md` |
| Jurisdiction guidelines | `docs/rights/jurisdiction-guidelines.md` |

## Asset coverage

RC17 extracts assets from all RC14 collection drafts under `content/collections/`.

- Unique collection assets registered: **42**
- Collections covered: **10**
- Provenance events created: **42**
- Attribution records created: **42**
- Publication approval records created: **42**

## Summary metrics

| Metric | Count |
|--------|------:|
| Assets approved | 6 |
| Assets blocked | 4 |
| Assets requiring review | 32 |
| Total registered assets | 42 |

## Validation rules implemented

Validation fails when:

1. source is missing,
2. license is unknown or missing,
3. rights status is unknown or missing,
4. an asset referenced in RC14 collection drafts is absent from the asset registry,
5. asset, attribution, provenance, and publication approval records diverge.

## Rights posture

Most assets remain in `Review Required` because RC14 content relies on heritage references, species concepts, wildlife subjects, and culturally sensitive assets whose publication requires image, partner, source, or sensitivity review. Approved assets are limited to source classes with stronger public-domain/open-access readiness, such as public-domain maps and Smithsonian/Open Access style references.

## Publication posture

No asset is marked `Published`. Approved assets may proceed to editorial review. Review-required and restricted assets remain blocked from publication until clearance is complete.

## Architecture and governance boundary

RC17 is an implementation-level rights registry for content drafts. It does not alter architecture, governance, ADRs, canonical registries, or the Open Grace canonical model.

## Implementation conclusion

RC17 converts RC14 content assets into publication-governed assets by adding registry coverage, policy documentation, validation tests, and summary metrics. It makes rights and provenance risk visible before publication while preserving all frozen architecture and governance boundaries.
