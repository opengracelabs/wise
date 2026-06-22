# RC18 Demonstration Surface Hardening Report

**Status:** Demonstration surface hardening implemented  
**Scope:** Accessibility, SEO, structured data, OpenGraph, sitemap validation, Lighthouse scoring, security headers, and performance hardening only  
**Constraints:** No payment processing, no checkout, no customer data collection

---

## 1. Summary

RC18 hardens the static Nature & Culture demonstration/public beta surface in `apps/web` and repository-root Vercel routing. The work focuses on low-risk production-readiness improvements for a read-only public demonstration.

Implemented:

- route-level SEO metadata
- canonical links
- OpenGraph metadata
- Twitter card metadata
- JSON-LD structured data
- sitemap and robots validation
- security headers
- static cache headers
- accessibility improvements for keyboard focus and live search status
- privacy improvement: raw search queries are no longer stored in analytics events
- performance improvement: analytics route no longer fetches showcase data unnecessarily; static assets are preload hinted and cacheable

---

## 2. Accessibility

Implemented:

- Preserved skip link and semantic header/main/footer structure.
- Added `aria-busy` to the dynamic app region.
- Added `role="status"` and `aria-live="polite"` to search result status text.
- Made generated cards keyboard-focusable.
- Added visible focus styling for generated cards.
- Added keyboard-focus analytics parity for collection and series views.
- Added descriptive `aria-label` values to product interest buttons.
- Added reduced-motion safety CSS.

Validation:

- Focused test suite validates hardened route shells and accessibility markers.
- Lighthouse accessibility score on local homepage: **98**.

---

## 3. SEO

Implemented:

- Route-specific `<title>` and meta description values.
- Route-specific canonical links.
- `robots` meta tags, including `noindex,nofollow` for `/admin/analytics`.
- Existing sitemap retained and XML-validated.
- Existing robots.txt retained and sitemap-linked.

Validation:

- Sitemap XML parsed successfully.
- Lighthouse SEO score on local homepage: **100**.

---

## 4. Structured Data

Implemented:

- Embedded JSON-LD on all `apps/web` routes.
- Homepage uses `WebSite` structured data with a `SearchAction`.
- Public routes use `CollectionPage`, `EducationalOrganization`, or `WebPage` as appropriate.
- Structured data includes publisher, URL, name, description, and free-access marker.

Validation:

- Focused tests verify every route includes JSON-LD and route URLs.

---

## 5. OpenGraph

Implemented:

- `og:title`
- `og:description`
- `og:type`
- `og:site_name`
- `og:url`
- `og:image`
- Twitter summary-large-image card metadata

Notes:

- `og:image` points to the existing placeholder production-domain pattern. Final image generation and rights clearance remain future work.

---

## 6. Sitemap validation

Validated:

```bash
python3 - <<'PY'
from pathlib import Path
import xml.etree.ElementTree as ET
ET.parse(Path('apps/web/sitemap.xml'))
PY
```

Result:

- `apps/web/sitemap.xml` parsed successfully.

---

## 7. Lighthouse scoring

Command run against local static server:

```bash
python3 -m http.server 4173 --directory apps/web
npx --yes lighthouse@latest http://127.0.0.1:4173/ \
  --output=json \
  --output-path=/tmp/rc18-lighthouse-home.json \
  --chrome-flags='--headless --no-sandbox' \
  --quiet
```

Environment note:

- `lighthouse@13.4.0` emitted an `EBADENGINE` warning because it expects Node `>=22.19` and the environment has Node `22.14.0`.
- The Lighthouse run completed successfully despite the warning.

Homepage scores:

| Category | Score |
|----------|-------|
| Performance | 91 |
| Accessibility | 98 |
| Best Practices | 96 |
| SEO | 100 |

---

## 8. Security headers

Implemented in:

- `apps/web/vercel.json`
- repository-root `vercel.json`

Headers:

- `Content-Security-Policy`
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=(), browsing-topics=()`

Notes:

- CSP permits inline scripts only to support static JSON-LD. No inline executable application JavaScript is used in `apps/web`.
- `payment=()` explicitly denies browser payment APIs.

---

## 9. Performance optimization

Implemented:

- Preload hints for CSS and JavaScript.
- Cache headers for `/static/*`.
- Short cache/stale-while-revalidate headers for `/data/*`.
- `content-visibility: auto` for generated cards.
- Analytics page no longer fetches collection/series/product JSON before rendering the local dashboard.

Validation:

- JavaScript syntax checks passed.
- Lighthouse performance score on local homepage: **91**.

---

## 10. Privacy / customer data

Implemented:

- Raw search queries are no longer stored in analytics events.
- Search event metadata keeps only result count, query length, zero-result flag, and `query_redacted: true`.
- No customer name, email, address, payment details, account creation, checkout, or customer data collection was added.

---

## 11. Validation commands

Run:

```bash
python3 -m pytest tests/e2e/test_reference_capability_6.py -q
python3 -m json.tool apps/web/vercel.json >/dev/null
python3 -m json.tool vercel.json >/dev/null
node --check apps/web/static/analytics.js
node --check apps/web/static/app.js
python3 -m json.tool apps/web/lighthouse.config.json >/dev/null
```

---

## 12. Remaining actions

1. Replace placeholder `nature-and-culture.example` URLs with the final production domain.
2. Add final rights-cleared OpenGraph image.
3. Move JSON-LD to a nonce/hash CSP model if stricter CSP is required later.
4. Run Lighthouse against the deployed Vercel preview/production URL after credentials are fixed.
5. Add automated link crawling once the final domain and deployment route are available.
