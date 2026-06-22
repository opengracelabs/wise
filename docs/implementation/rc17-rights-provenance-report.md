# RC17 Rights & Provenance Report

**Status:** Rights and provenance infrastructure implemented
**Authority:** architecture-v1.0 (`architecture-v1.0`, ADR-011)
**Scope:** Rights, provenance, attribution, and publication approval infrastructure only — no governance changes, no Architecture v1.0 changes, no agents, no ADRs, no payment processing, no checkout, no customer data collection

---

## 1. Assets reviewed

Assets reviewed: **25**

Every asset in `data/publishing/top_25_showcase_assets.json` is represented in `rights/asset-registry.json` with:

- unique asset ID
- source reference
- rights status
- license ID
- approval status
- collection reference when available

## 2. Sources reviewed

Sources reviewed: **7**

| Source authority | Source URL | Verification method |
|------------------|------------|---------------------|
| UNESCO World Heritage Centre | https://whc.unesco.org/ | Authority homepage and public World Heritage listing review |
| Global Biodiversity Information Facility | https://www.gbif.org/ | GBIF public species/taxonomy source review |
| The National Gallery, London | https://www.nationalgallery.org.uk/ | Public-domain/open-access collection policy review |
| Rijksmuseum | https://www.rijksmuseum.nl/ | Rijksmuseum public-domain collection policy review |
| Library of Congress | https://www.loc.gov/ | Library of Congress public collection rights advisory review |
| Smithsonian Open Access | https://www.si.edu/openaccess | Smithsonian Open Access policy review |
| National Geographic subject taxonomy / editorial inspiration | https://www.nationalgeographic.com/ | Subject-level editorial reference only; no image license assumed |

## 3. Rights classifications

| Rights status | Count |
|---------------|-------|
| CC-BY | 5 |
| CC0 | 1 |
| Public Domain | 2 |
| Rights Restricted | 17 |

License classes are defined in `rights/license-registry.json`: Public Domain, CC0, CC-BY, CC-BY-SA, Rights Restricted, Unknown.

## 4. Unknown rights blockers

Unknown rights blockers: **0**

No approved showcase asset uses `rights_status: "Unknown"`. Validation is configured to fail if Unknown appears on a registered publishable asset.

## 5. Publication approval readiness

Publication approval records: **25**
Approved for public demo metadata/text use: **25**
Blocked for commercial image/final product use without item license: **22**

Approval scope for RC17 is intentionally limited to:

- public demo metadata
- editorial text reference
- placeholder product copy

This does not approve final product imagery, print production, paid distribution, or commercial image use unless item-level rights are separately cleared.

## 6. Validation summary

RC17 validation verifies:

- all existing showcase assets are represented
- all existing showcase collections reference approved assets
- validation fails if an asset rights status is Unknown
- all source, license, provenance, attribution, approval, and jurisdiction registries parse
- summary statistics are present

## 7. Recommended next actions

1. Add item-level source URLs for every production visual.
2. Capture creator/photographer/object credit lines per asset.
3. Convert category-level rights assumptions into asset-level evidence records.
4. Resolve Rights Restricted assets before product imagery, YouTube visuals, Pinterest images, or paid campaigns.
5. Add a production publication status only after attribution and jurisdiction review are complete.
6. Keep all commerce surfaces read-only until a separate approved commerce path exists.

## 8. ADR-011 compliance

RC17 follows ADR-011:

- No Architecture v1.0 documents modified.
- No governance files modified.
- No agents added.
- No ADRs added.
- No payment, checkout, order, fulfillment, customer-data, preservation, or platform write path introduced.
