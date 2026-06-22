# RC9 Public Launch Plan

**Status:** Prototype launch plan  
**Authority:** architecture-v1.0 (`architecture-v1.0`, ADR-011)  
**Scope:** Experience Plane launch readiness only — no governance changes, no Architecture v1.0 changes, no agents, no ADRs

---

## 1. Deployment readiness review

### Reviewed surfaces

| Surface | Path | Current readiness | Launch notes |
|---------|------|-------------------|--------------|
| Nature & Culture homepage | `/` | Prototype-ready | Contains mission, featured collections, featured series, featured products, explore-by-place/species/theme, education, research, and shop sections. |
| Demonstration records | `/objects/stonehenge`, `/objects/panthera-leo`, `/areas/everglades-national-park` | Prototype-ready | Read-only records remain useful proof points for heritage, species, and protected-area coverage. |
| Commerce index | `/shop` | Prototype-ready | Static product cards render from local product intelligence data. No checkout or payment path exists. |
| Commerce maps | `/shop/maps` | Prototype-ready | Historic map route validates place-led commerce demand. |
| Commerce education | `/shop/education` | Prototype-ready | Educational products validate classroom and family learning demand. |
| Commerce gifts | `/shop/gifts` | Prototype-ready | Gift products validate high-giftability categories. |
| Product details | `/shop/products/{slug}` | Prototype-ready | Generic static detail page renders product metadata and records local demand events. |
| Commercial dashboard | `/admin/commercial` | Prototype-ready, steward-only convention | Local dashboard summarizes this browser's demand events and RC7 product intelligence scores. |

### Readiness conclusion

RC9 is ready for a **public launch prototype** when framed as a read-only static public experience. The surface can validate positioning, route integrity, product interest, and early audience response without requiring payment processing, user accounts, server writes, or new platform capabilities.

### Known launch constraints

1. Analytics are browser-local only; aggregate production analytics requires a future approved event collection path.
2. Product imagery is placeholder/editorial; launch-quality images and rights metadata are still required.
3. `/admin/commercial` is a local prototype dashboard, not authenticated production administration.
4. Top 100 Global Assets are a prototype portfolio dataset for merchandising and editorial prioritization, not canonical records.

---

## 2. Deployment architecture

RC9 remains inside the existing Experience Plane.

```text
User browser
  |
  | HTTPS
  v
Vercel static routing
  |
  +-- /                         -> apps/demonstration-surface/index.html
  +-- /shop                     -> apps/demonstration-surface/shop/index.html
  +-- /shop/maps                -> apps/demonstration-surface/shop/maps/index.html
  +-- /shop/education           -> apps/demonstration-surface/shop/education/index.html
  +-- /shop/gifts               -> apps/demonstration-surface/shop/gifts/index.html
  +-- /shop/products/:slug      -> apps/demonstration-surface/shop/product-detail/index.html
  +-- /admin/commercial         -> apps/demonstration-surface/admin/commercial/index.html
  +-- /static/*                 -> apps/demonstration-surface/*
```

Runtime behavior:

- HTML, CSS, and JavaScript are static assets.
- Product intelligence is embedded in `apps/demonstration-surface/commercial.js`.
- Demand events are written to `localStorage` under the commercial validation key.
- No payment processor, order API, user account API, or server write path is present.
- `vercel.json` preserves static route compatibility.

---

## 3. Vercel deployment steps

1. Confirm branch contents:
   - `apps/demonstration-surface/index.html`
   - `apps/demonstration-surface/shop/**`
   - `apps/demonstration-surface/admin/commercial/index.html`
   - `apps/demonstration-surface/commercial.js`
   - `vercel.json`
2. Run validation:
   - `python3 -m pytest tests/e2e/test_reference_capability_6.py -q`
   - `node --check apps/demonstration-surface/commercial.js`
   - `python3 -m json.tool vercel.json`
   - `python3 -m json.tool data/portfolio/top_100_global_assets.json`
3. Deploy branch preview on Vercel.
4. Verify preview routes:
   - `/`
   - `/shop`
   - `/shop/maps`
   - `/shop/education`
   - `/shop/gifts`
   - `/shop/products/big-cats-poster`
   - `/shop/products/world-heritage-historic-map`
   - `/admin/commercial`
5. Confirm no checkout or payment route exists.
6. Promote to production only as a public launch prototype.

---

## 4. Analytics events

Current local event names:

| Event | Trigger | Purpose |
|-------|---------|---------|
| `product_view` | Product detail page load or card detail link | Measures product attention. |
| `add_to_wishlist` | Add to Wishlist button | Measures softer demand and gift save behavior. |
| `buy_interest` | Buy Interest button | Measures purchase intent without checkout. |
| `checkout_intent` | Buy Interest button companion event | Simulates funnel intent without payment processing. |

Recommended RC9 launch analysis:

- Top products by `product_view`
- Highest buy intent by `buy_interest`
- Highest wishlist rate: `add_to_wishlist / product_view`
- Highest product fit score from RC7
- Top category score from RC7
- Product demand delta by route group: shop, maps, education, gifts

---

## 5. Traffic goals

Prototype launch traffic goals should validate directional demand, not scale operations.

| Goal | Target |
|------|--------|
| Homepage visits | 1,000 prototype visits |
| Shop visits | 400 prototype visits |
| Product detail views | 250 product views |
| Wishlist actions | 75 wishlist events |
| Buy interest actions | 40 buy interest events |
| Route coverage | At least one validated visit to every public route |
| Product coverage | At least one view for every featured product candidate |

Success signal:

- At least three products show both wishlist and buy-interest activity.
- At least two categories show repeat interest across multiple products.
- Homepage-to-shop navigation is observable in review sessions.

---

## 6. Content requirements

### Homepage

- Final Nature & Culture mission copy.
- Editorial hero treatment.
- Featured collection descriptions for Big Cats of the World and World Heritage.
- Featured series titles and editorial blurbs.
- Explore-by-place, species, and theme navigation.
- Education and research copy.
- Shop explanation that clearly states read-only/no payment.

### Asset portfolio

- Top 100 Global Assets prototype dataset.
- Source family assignment for each asset.
- Recognition, demand, and commercial scores.
- Product recommendation arrays.
- Rights/clearance review before using launch imagery.

### Product pages

- Launch-quality product names.
- Price placeholders until pricing is approved.
- Product fit, category, giftability, and repeat-purchase scores.
- Product copy that avoids implying fulfillment or availability.
- Clear "No payment processing" statement.

---

## 7. Product requirements

### Required launch product categories

- Posters
- Framed Prints
- Canvas Prints
- Puzzles
- Calendars
- Coffee Table Books

### Required launch product blocks

| Collection | Products |
|------------|----------|
| Big Cats Collection | Poster, Framed Print, Canvas, Puzzle, Calendar |
| World Heritage Collection | Museum Print, Historic Map, Coffee Table Book |

### Required safeguards

- No checkout route.
- No payment processor dependency.
- No order persistence.
- No user account requirement.
- Demand events remain explicitly validation-only.

---

## 8. ADR-011 compliance

RC9 follows ADR-011 by treating launch work as Experience Plane implementation:

- No Architecture v1.0 documents modified.
- No governance files modified.
- No agents added.
- No ADRs added.
- No Platform Plane or Preservation Plane write path introduced.

---

## 9. Launch recommendation

Proceed with RC9 as a public launch prototype after visual QA and preview-route verification. Keep messaging explicit: Nature & Culture is presenting a read-only prototype for public experience and commercial validation, not a live commerce operation.
