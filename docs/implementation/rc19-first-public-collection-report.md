# RC19 First Public Collection Report

**Status:** First rights-gated public collection prepared  
**Collection:** Big Cats of the World  
**Scope:** Public collection release only — no architecture changes, no governance changes, no ADR changes, no agents, no payment processing, no checkout, no customer data collection

---

## 1. Assets used

Only RC17-approved, non-restricted assets are displayed:

| Asset | Asset ID | Rights status | License | Approval status | Use |
|-------|----------|---------------|---------|-----------------|-----|
| Lion | `asset-lion` | CC-BY | `cc-by` | Approved | Public demo metadata/text display |
| Tiger | `asset-tiger` | CC-BY | `cc-by` | Approved | Public demo metadata/text display |

Excluded:

- `asset-tiger-in-mangrove-forest`
- `asset-bengal-tiger-cub-portrait`

Reason:

- Both are Rights Restricted National Geographic subject records and cannot appear in the public collection.

---

## 2. Rights status

Displayed assets:

- have source records
- have license records
- have attribution records
- have publication approval records
- are not Rights Restricted
- are not Unknown

The release is text-first. Final wildlife images are not displayed until item-level media rights are cleared.

---

## 3. Attribution status

Attribution appears in:

- `content/public-collections/big-cats-of-the-world/image-attribution.md`
- `apps/web/data/big_cats_public_collection.json`
- `/collections/big-cats-of-the-world` route rendering

Attribution status:

- template-ready attribution with source authority and source URL
- individual asset URL still required before production publication

---

## 4. Routes added

Added:

- `/collections/big-cats-of-the-world`

Files:

- `apps/web/collections/big-cats-of-the-world/index.html`
- `apps/web/data/big_cats_public_collection.json`

Updated:

- `apps/web/static/app.js`
- `apps/web/vercel.json`
- root `vercel.json`
- `apps/web/sitemap.xml`

---

## 5. Content package

Created:

- `content/public-collections/big-cats-of-the-world/collection-page.md`
- `content/public-collections/big-cats-of-the-world/species-pages/lion.md`
- `content/public-collections/big-cats-of-the-world/species-pages/tiger.md`
- `content/public-collections/big-cats-of-the-world/education-guide.md`
- `content/public-collections/big-cats-of-the-world/image-attribution.md`
- `content/public-collections/big-cats-of-the-world/rights-summary.md`
- `content/public-collections/big-cats-of-the-world/publication-readiness-checklist.md`

---

## 6. Tests run

Run:

- focused e2e tests
- JSON validation
- JavaScript syntax checks
- build/typecheck attempts
- Lighthouse check if available

Results:

- `python3 -m pytest tests/e2e/test_reference_capability_6.py -q` — **48 passed**.
- `python3 -m json.tool apps/web/data/big_cats_public_collection.json >/dev/null` — passed.
- `python3 -m json.tool apps/web/vercel.json >/dev/null` — passed.
- `python3 -m json.tool vercel.json >/dev/null` — passed.
- `node --check apps/web/static/app.js` — passed.
- `node --check apps/web/static/analytics.js` — passed.
- `npm run build` — unavailable: repository root has no `package.json`.
- `npm run typecheck` — unavailable: repository root has no `package.json`.
- Lighthouse route check for `/collections/big-cats-of-the-world` completed:
  - Performance: 91
  - Accessibility: 100
  - Best Practices: 96
  - SEO: 100

---

## 7. Known gaps

1. Final species images are not displayed.
2. Individual GBIF media/occurrence records need item-level license review before image use.
3. Final source URLs for exact species records should be attached before production publication.
4. Route is public-demo ready, not commerce ready.
5. Product CTAs remain demo only / not for sale.

---

## 8. Publication recommendation

Recommended for public demonstration release as a text-first, rights-gated Big Cats collection using Lion and Tiger metadata/assets only.

Not recommended for production image publication until item-level media rights, source URLs, and credit lines are complete.
