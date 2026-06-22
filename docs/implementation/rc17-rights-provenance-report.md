# RC17 Rights & Provenance Infrastructure Report

**Scope:** Publication-grade rights and provenance controls for RC17.

**Architecture boundary:** Architecture v1.0, governance, ADRs, and agent
specifications were not modified. This report documents implementation-level
rights registry artifacts and validation results only.

## Registry artifacts

The RC17 rights infrastructure is stored under `rights/`:

- `asset-registry.json`
- `source-registry.json`
- `license-registry.json`
- `provenance-registry.json`
- `attribution-registry.json`
- `publication-approvals.json`
- `jurisdiction-rules.json`
- `summary-metrics.json`

## Asset lifecycle validation

Assets are validated through the publication lifecycle:

```text
Asset
-> Source Verified
-> License Verified
-> Provenance Verified
-> Rights Approved
-> Publication Approved
-> Publishable
```

Validation blocks publication when rights are unknown, a source is missing, a
license is missing, provenance is missing or mismatched, rights are not approved,
publication approval is missing or blocked, or an asset is restricted.

## Summary metrics

| Metric | Value |
|--------|-------|
| Registered assets | 5 |
| Publishable assets | 4 |
| Blocked assets | 1 |
| Publishable share | 80% |
| Restricted asset count | 1 |
| Referenced source coverage | 100% |
| Referenced license coverage | 100% |

Publishable assets:

- `stonehenge`
- `everglades-national-park`
- `panthera-leo`
- `wikidata-q140-lion`

Blocked assets:

- `sensitive-oral-history-example`

## Source coverage

All referenced sources are present and verified.

| Source | Coverage status |
|--------|-----------------|
| UNESCO World Heritage Centre (`unesco-whc`) | Covered |
| Ramsar Sites Information Service (`ramsar`) | Covered |
| Global Biodiversity Information Facility (`gbif`) | Covered |
| Wikidata (`wikidata`) | Covered |
| Community Archive Restricted Collection (`community-archive`) | Covered |

## License coverage

All referenced licenses are present and verified.

| License | Publication status |
|---------|--------------------|
| `noc-oklr` | Publication allowed with attribution |
| `cc0-1.0` | Publication allowed |
| `cc-by-4.0` | Publication allowed with attribution |
| `restricted-cultural` | Publication blocked |

## Rights blockers

Current blockers are limited to the restricted sample asset:

| Blocker | Count |
|---------|-------|
| `license_publication_blocked` | 1 |
| `publication_not_approved` | 1 |
| `restricted_asset` | 1 |
| `rights_not_approved` | 1 |

## Publication readiness

Four assets complete every lifecycle stage and are publishable. The restricted
oral history example intentionally completes source, license, and provenance
verification but fails rights approval and publication approval, demonstrating
that restricted assets cannot become publishable.

## Known gaps

- Registries are static JSON artifacts; database persistence is not introduced.
- Jurisdiction rules are initial publication baselines for `GLOBAL`, `GB`, and
  `US` only.
- The restricted cultural protocol is represented as a publication-blocking
  license category; more granular steward protocols can be added later without
  changing the lifecycle contract.
- Rights review actors are represented as stable strings, not identity records.

## Recommended next actions

1. Add more jurisdiction rules before expanding publication beyond the current
   reference regions.
2. Add additional license records as new source types enter publication review.
3. Require each new asset to include source, license, provenance, attribution,
   jurisdiction, and publication approval references before publication.
4. Keep restricted cultural and community assets blocked until steward approval
   and protocol-specific publication rules are explicitly recorded.
5. Re-run the RC17 lifecycle tests whenever registry JSON changes.
