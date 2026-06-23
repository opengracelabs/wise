# RC10 Public Beta Checklist

**Status:** Public beta readiness checklist  
**Authority:** architecture-v1.0 (`architecture-v1.0`, ADR-011)  
**Scope:** Experience Plane beta readiness only — no governance changes, no Architecture v1.0 changes, no agents, no ADRs

---

## 1. Accessibility

- [ ] Every page has a single meaningful `<h1>`.
- [ ] Skip link is present and keyboard reachable.
- [ ] Navigation links are keyboard accessible.
- [ ] Product and collection cards expose readable labels.
- [ ] Product mockups and future images include descriptive `alt` text.
- [ ] Color contrast meets WCAG AA for text and controls.
- [ ] Focus states are visible on links and buttons.
- [ ] Dynamic status text uses `aria-live` where actions are recorded.

---

## 2. SEO

- [ ] Homepage title is final: `Nature & Culture`.
- [ ] Route titles are descriptive for shop, maps, education, gifts, products, and admin.
- [ ] Add meta descriptions before public promotion.
- [ ] Add canonical URLs after production domain is assigned.
- [ ] Add structured data for collections/products only after rights and pricing posture is approved.
- [ ] Ensure no payment or availability structured data is emitted for read-only products.

---

## 3. Analytics

- [ ] Implement RC10 event taxonomy before external traffic.
- [ ] Normalize prototype aliases:
  - `add_to_wishlist` -> `wishlist`
  - `buy_interest` -> `buy_intent`
  - `checkout_intent` -> `buy_intent` metadata
- [ ] Track:
  - `page_view`
  - `collection_view`
  - `series_view`
  - `product_view`
  - `wishlist`
  - `buy_intent`
  - `outbound_click`
  - `search`
  - `session_duration`
- [ ] Confirm landing experiment variant assignment is anonymous.
- [ ] Confirm analytics avoids names, emails, payment data, and precise location.
- [ ] Confirm dashboard copy states prototype/local status when production analytics is not connected.

---

## 4. Performance

- [ ] Keep homepage and shop routes static.
- [ ] Keep JavaScript bundle minimal and dependency-free for beta.
- [ ] Optimize future imagery before launch.
- [ ] Avoid blocking third-party scripts.
- [ ] Confirm Vercel preview loads homepage and shop routes within acceptable latency.
- [ ] Confirm product-grid rendering remains responsive for the Top 50 product candidate set.

---

## 5. Privacy

- [ ] Use anonymous session IDs only.
- [ ] Store referrer and outbound data as domains, not full URLs, unless explicitly approved.
- [ ] Do not collect payment, order, account, or contact data.
- [ ] Add privacy notice before production analytics collection.
- [ ] Respect consent requirements for analytics tools in target launch jurisdictions.
- [ ] Keep `/admin/commercial` out of public promotion.

---

## 6. Broken links

- [ ] Verify `/`.
- [ ] Verify `/shop`.
- [ ] Verify `/shop/maps`.
- [ ] Verify `/shop/education`.
- [ ] Verify `/shop/gifts`.
- [ ] Verify representative product detail routes.
- [ ] Verify `/objects/stonehenge`.
- [ ] Verify `/objects/panthera-leo`.
- [ ] Verify `/areas/everglades-national-park`.
- [ ] Verify `/admin/commercial`.
- [ ] Verify all `/static/*` assets resolve through Vercel rewrites.

---

## 7. Route validation

Required public beta route set:

| Route | Purpose | Beta status |
|-------|---------|-------------|
| `/` | Nature & Culture homepage | Required |
| `/shop` | Product validation index | Required |
| `/shop/maps` | Historic maps route | Required |
| `/shop/education` | Education route | Required |
| `/shop/gifts` | Gift route | Required |
| `/shop/products/{slug}` | Product detail route | Required |
| `/admin/commercial` | Local/steward dashboard | Prototype only |

Validation commands:

```bash
python3 -m pytest tests/e2e/test_reference_capability_6.py -q
python3 -m json.tool data/portfolio/top_100_collections.json >/dev/null
python3 -m json.tool data/portfolio/top_100_series.json >/dev/null
python3 -m json.tool data/portfolio/top_50_products.json >/dev/null
python3 -m json.tool data/portfolio/landing_page_experiments.json >/dev/null
python3 -m json.tool vercel.json >/dev/null
node --check apps/demonstration-surface/commercial.js
```

---

## 8. Vercel readiness

- [ ] `vercel.json` parses as valid JSON.
- [ ] Rewrites preserve:
  - `/`
  - `/shop`
  - `/shop/maps`
  - `/shop/education`
  - `/shop/gifts`
  - `/shop/products/:slug`
  - `/admin/commercial`
  - `/static/:path*`
- [ ] Preview deploy confirms no framework build step is required for static routes.
- [ ] No `package.json` requirement is assumed for this repository unless a future frontend app is added.
- [ ] Production promotion is labeled public beta/prototype.

---

## 9. Content gates

- [ ] Confirm Top 100 Collections are balanced by geography, domain, theme, and diversity role.
- [ ] Confirm Top 100 Series reference valid collections and assets.
- [ ] Confirm Top 50 Products include asset source, collection, demand rationale, and commercial rationale.
- [ ] Review source and rights status before using launch imagery.
- [ ] Replace placeholder product visuals before public promotion beyond beta.

---

## 10. ADR-011 compliance

RC10 follows ADR-011:

- No Architecture v1.0 documents modified.
- No governance files modified.
- No agents added.
- No ADRs added.
- No payment, order, preservation, or platform write path introduced.
