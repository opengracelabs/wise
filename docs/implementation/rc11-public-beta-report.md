# RC11 Public Beta Report

**Status:** Public beta implementation prepared; Vercel deployment blocked by environment credentials  
**Authority:** architecture-v1.0 (`architecture-v1.0`, ADR-011)  
**Scope:** Experience Plane public beta deployment only — no governance changes, no Architecture v1.0 changes, no agents, no ADRs

---

## 1. Deployment status

### Target

- Application: `apps/web`
- Target platform: Vercel
- Deployment mode: static app with Vercel rewrites

### Result

The RC11 public beta app is prepared for Vercel deployment, but deployment from this cloud environment did not complete because Vercel credentials are invalid.

Evidence:

```bash
$ vercel --cwd apps/web --yes
vercel: command not found
```

Fallback attempt:

```bash
$ npx --yes vercel@latest --cwd apps/web --yes
Vercel CLI 54.14.5
Directory /workspace/apps/web
Loading teams...
Error: The specified token is not valid. Use `vercel login` to generate a new token.
```

Vercel MCP fallback:

- Vercel MCP server discovery failed with server status `error`.
- No MCP deployment tools were available.

Deployment conclusion:

- **Prepared:** Yes
- **Vercel-compatible static app:** Yes
- **Production/preview URL created from this environment:** No, blocked by invalid Vercel token

---

## 2. Route status

| Route | File | Status |
|-------|------|--------|
| `/` | `apps/web/index.html` | Ready |
| `/collections` | `apps/web/collections/index.html` | Ready |
| `/series` | `apps/web/series/index.html` | Ready |
| `/species` | `apps/web/species/index.html` | Ready |
| `/places` | `apps/web/places/index.html` | Ready |
| `/shop` | `apps/web/shop/index.html` | Ready |
| `/education` | `apps/web/education/index.html` | Ready |
| `/research` | `apps/web/research/index.html` | Ready |
| `/admin/analytics` | `apps/web/admin/analytics/index.html` | Ready |

Repository-root `vercel.json` also rewrites these routes into `apps/web` for root preview deployments.

---

## 3. Analytics status

Implemented in `apps/web/static/analytics.js`.

Tracked RC10 event names:

- `page_view`
- `collection_view`
- `series_view`
- `product_view`
- `wishlist`
- `buy_intent`
- `outbound_click`
- `search`
- `session_duration`

Implementation notes:

- Analytics are browser-local for public beta validation.
- Anonymous session IDs are generated client-side.
- Events are stored in `localStorage`.
- Existing aliases are normalized:
  - `add_to_wishlist` -> `wishlist`
  - `buy_interest` -> `buy_intent`
  - `checkout_intent` -> `buy_intent` with simulated checkout metadata
- `/admin/analytics` reads local events and displays event counts and product-interest summaries.

---

## 4. Showcase content status

### Top 25 Showcase Collections

Output:

- `data/portfolio/top_25_showcase_collections.json`
- `apps/web/data/top_25_showcase_collections.json`

Selection criteria:

- Visual appeal
- Educational value
- Global representation
- Product potential

Status:

- 25 selected
- Global representation includes Africa, Asia, Europe, Global, Latin America, North America, and Oceania

### Top 25 Showcase Series

Output:

- `data/portfolio/top_25_showcase_series.json`
- `apps/web/data/top_25_showcase_series.json`

Status:

- 25 selected
- Each references collections and assets
- Each contains educational narrative copy

### Top 25 Showcase Products

Output:

- `data/portfolio/top_25_showcase_products.json`
- `apps/web/data/top_25_showcase_products.json`

Required categories represented:

- Posters
- Framed Prints
- Canvas Prints
- Puzzles
- Calendars
- Coffee Table Books

Status:

- 25 selected
- Each includes asset source, collection, demand rationale, and commercial rationale

---

## 5. SEO status

Generated under `apps/web`:

- `sitemap.xml`
- `robots.txt`
- `metadata-templates.json`
- `opengraph-templates.json`

Status:

- Route sitemap covers homepage, collections, series, species, places, shop, education, research, and analytics.
- Robots file allows public crawling and references sitemap.
- Metadata templates cover core public beta routes.
- OpenGraph templates define site-level image and route-specific title/description patterns.

Production follow-up:

- Replace `https://nature-and-culture.example` placeholder with the final Vercel/production domain after deployment.

---

## 6. Content readiness

Ready for public beta:

- Homepage route shell
- Collections route
- Series route
- Species route
- Places route
- Shop route
- Education route
- Research route
- Top 25 showcase datasets

Needs future production refinement:

- Launch-quality images
- Final source URLs per asset
- Rights review for all visual assets
- Final domain metadata
- More detailed collection/series detail routes if moving beyond beta

---

## 7. Product readiness

Ready for read-only beta validation:

- Top 25 showcase product dataset
- Product card rendering
- Product view event
- Wishlist event
- Buy intent event

Not present by design:

- Payment processing
- Checkout
- Order creation
- Fulfillment
- User accounts

---

## 8. Validation status

Validation commands run:

```bash
python3 -m pytest tests/e2e/test_reference_capability_6.py -q
python3 -m json.tool apps/web/vercel.json >/dev/null
python3 -m json.tool vercel.json >/dev/null
node --check apps/web/static/analytics.js
node --check apps/web/static/app.js
```

Results:

- Focused beta test suite: 30 passed.
- Showcase JSON files: parsed successfully.
- SEO JSON templates: parsed successfully.
- `apps/web/vercel.json`: parsed successfully.
- repository-root `vercel.json`: parsed successfully.
- `apps/web/static/analytics.js`: syntax check passed.
- `apps/web/static/app.js`: syntax check passed.
- `apps/web/sitemap.xml`: XML parse passed.

Deployment validation status:

- Local/static readiness validation: passed
- Vercel deploy validation: blocked by invalid token

---

## 9. ADR-011 compliance

RC11 follows ADR-011:

- No Architecture v1.0 documents modified.
- No governance files modified.
- No agents added.
- No ADRs added.
- No payment, order, preservation, or platform write path introduced.
