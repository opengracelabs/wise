# RC19 Rights-Aware Public Collection Validation

| Field | Value |
|-------|-------|
| **Reference Capability** | RC19 |
| **Collection** | Big Cats of the World |
| **Status** | Complete |
| **Report** | [collection-validation-report.json](../../collection-validation-report.json) |
| **Pipeline** | [validate_public_collection.py](../../scripts/validate_public_collection.py) |
| **Scope** | Validation only; architecture, governance, ADRs, and agent registry unchanged |

## 1. Objective

Validate that a public collection can only be built from rights-approved assets with approved source, attribution, provenance, and publication approval records.

## 2. Validation Pipeline

```
Asset
  ->
Source Check
  ->
License Check
  ->
Attribution Check
  ->
Provenance Check
  ->
Publication Approval Check
  ->
Collection Eligibility
```

## 3. Enforcement Rules

| Rule | Enforcement |
|------|-------------|
| Unknown rights fail | Any `rights_record.status == "unknown"` or `rights_category == "unknown"` blocks eligibility. |
| Missing source fails | Any missing `source_record` blocks eligibility. |
| Missing attribution fails | Any missing `attribution_record` blocks eligibility. |
| Restricted assets fail | Any restricted rights record or non-open rights category blocks eligibility. |
| Unapproved assets fail | Any asset whose `asset_status != "approved"` blocks eligibility. |

All required records must be present and `approved`: asset, source, rights, attribution, provenance, and publication approval.

## 4. Assets Reviewed

| Asset ID | Title | Species | Result |
|----------|-------|---------|--------|
| `bigcats-lion-gbif-profile` | Lion species profile | *Panthera leo* | Approved |
| `bigcats-tiger-commons-photo` | Tiger open-license photograph | *Panthera tigris* | Approved |
| `bigcats-snow-leopard-eol-summary` | Snow leopard education summary | *Panthera uncia* | Approved |
| `bigcats-jaguar-museum-scan` | Jaguar historical museum scan | *Panthera onca* | Blocked |
| `bigcats-leopard-field-audio` | Leopard field audio | *Panthera pardus* | Blocked |
| `bigcats-cheetah-range-map` | Cheetah range map | *Acinonyx jubatus* | Blocked |
| `bigcats-cougar-education-card` | Cougar education card | *Puma concolor* | Blocked |
| `bigcats-clouded-leopard-archive-photo` | Clouded leopard archive photograph | *Neofelis nebulosa* | Blocked |
| `bigcats-lynx-draft-profile` | Lynx draft profile | *Lynx lynx* | Blocked |

## 5. Approved Assets

| Asset ID | Rights Basis | Required Records |
|----------|--------------|------------------|
| `bigcats-lion-gbif-profile` | Public domain / CC0 | Asset, source, rights, attribution, provenance, publication approval all approved |
| `bigcats-tiger-commons-photo` | Open license / CC BY-SA 4.0 | Asset, source, rights, attribution, provenance, publication approval all approved |
| `bigcats-snow-leopard-eol-summary` | Open license / CC BY 4.0 | Asset, source, rights, attribution, provenance, publication approval all approved |

## 6. Blocked Assets

| Asset ID | Blocking Reason | Failed Gate |
|----------|-----------------|-------------|
| `bigcats-jaguar-museum-scan` | `restricted_asset` | License Check |
| `bigcats-leopard-field-audio` | `unknown_rights` | License Check |
| `bigcats-cheetah-range-map` | `missing_source` | Source Check |
| `bigcats-cougar-education-card` | `missing_attribution` | Attribution Check |
| `bigcats-clouded-leopard-archive-photo` | `missing_provenance` | Provenance Check |
| `bigcats-lynx-draft-profile` | `unapproved_asset` | Asset |

## 7. Missing Provenance

| Asset ID | Status |
|----------|--------|
| `bigcats-clouded-leopard-archive-photo` | Missing provenance record; blocked from public collection eligibility |

## 8. Missing Attribution

| Asset ID | Status |
|----------|--------|
| `bigcats-cougar-education-card` | Missing attribution record; blocked from public collection eligibility |

## 9. Publication Readiness Score

| Metric | Value |
|--------|-------|
| Assets reviewed | 9 |
| Approved assets | 3 |
| Blocked assets | 6 |
| Missing provenance | 1 |
| Missing attribution | 1 |
| Publication readiness score | 33.33 |

Readiness is calculated as `approved_assets / assets_reviewed * 100`.

## 10. Final Report

The generated final report is [collection-validation-report.json](../../collection-validation-report.json). It contains the full per-asset validation trace, including source, rights, attribution, provenance, publication approval, gate results, collection eligibility, and blocked reasons.

**Conclusion:** Big Cats of the World is not ready for public publication as a complete collection. Only 3 of 9 reviewed assets are eligible. The collection may publish only the approved assets until blocked records are corrected and revalidated.
