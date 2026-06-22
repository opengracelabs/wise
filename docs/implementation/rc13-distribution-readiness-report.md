# RC13 Distribution Readiness Report

**Status:** Publishing and distribution readiness review  
**Authority:** architecture-v1.0 (`architecture-v1.0`, ADR-011)  
**Scope:** Publishing/distribution readiness only — no governance changes, no Architecture v1.0 changes, no agents, no ADRs

---

## 1. Objective

RC13 prepares Nature & Culture publishing outputs for downstream distribution channels while keeping the platform read-only and prototype-safe. The work produces content factory pipelines, ebook and audiobook concepts, print product pipelines, and production-ready briefs for YouTube and Pinterest.

Generated data:

- `data/publishing/content_factory.json`
- `data/publishing/top_25_showcase_assets.json`
- `data/publishing/ebooks.json`
- `data/publishing/audiobooks.json`
- `data/publishing/print_products.json`
- `data/publishing/youtube_production.json`
- `data/publishing/pinterest_production.json`

---

## 2. Content factory readiness

The content factory defines draft pipelines for:

- Articles
- Collection Pages
- Series Pages
- Product Pages
- Educational Resources

Inputs:

- `top_25_showcase_assets`
- `top_25_showcase_collections`
- `top_25_showcase_series`
- `top_25_showcase_products`

Readiness status:

- Pipeline definitions are complete.
- Outputs are marked as draft/editorial-review artifacts.
- No automated publishing, commerce, or distribution API is wired.

---

## 3. Channel readiness review

### Shopify

Readiness: **Not production-ready; catalog-ready only**

Use case:

- Future storefront and product validation hub.

Requirements before use:

- Product pricing approval.
- Payment and tax configuration.
- Fulfillment policy.
- Rights-cleared product imagery.
- Terms, refund, privacy, and support flows.

RC13 posture:

- Do not connect Shopify yet.
- Current outputs can inform product titles, descriptions, collections, and draft catalog structure.

### Gelato

Readiness: **Prototype-ready for print-on-demand evaluation**

Use case:

- Posters, framed prints, calendars, and selected wall art.

Requirements before use:

- Image resolution and color profile validation.
- Rights-cleared image source files.
- Test orders for quality assurance.
- Region and shipping coverage review.

RC13 posture:

- Use `print_products.json` as an internal product planning input only.

### Printful

Readiness: **Prototype-ready for fulfillment comparison**

Use case:

- Posters, framed prints, canvas prints, and selected educational merchandise.

Requirements before use:

- Print file templates.
- Product mockups.
- Quality testing against Gelato.
- Fulfillment and returns comparison.

RC13 posture:

- Use for vendor comparison, not live fulfillment.

### Amazon KDP

Readiness: **Concept-ready for ebooks and coffee table books**

Use case:

- Ebooks, print books, coffee table books, and educational guides.

Requirements before use:

- Manuscript development.
- Image rights verification.
- ISBN/publishing imprint decisions.
- Interior layout and cover production.
- Metadata and category review.

RC13 posture:

- `ebooks.json`, `audiobooks.json`, and coffee table book entries in `print_products.json` are concept inputs only.

### YouTube

Readiness: **Production-brief ready**

Use case:

- Educational video distribution and audience acquisition.

Requirements before use:

- Script review.
- Rights-cleared visuals.
- Voiceover production.
- Captions and transcript generation.
- Thumbnail design.

RC13 posture:

- `youtube_production.json` is ready for editorial and production planning.

### Pinterest

Readiness: **Design-brief ready**

Use case:

- Visual discovery, collection promotion, product-interest validation.

Requirements before use:

- Rights-cleared vertical imagery.
- Pin templates.
- Destination URL mapping.
- UTM campaign conventions.

RC13 posture:

- `pinterest_production.json` is ready for design queue planning.

---

## 4. Distribution blockers

1. Rights-cleared final imagery is required before public distribution.
2. Shopify/payment flows are out of scope for the current architecture-constrained prototype.
3. Print-on-demand vendors require quality test orders before launch.
4. KDP requires manuscript/editorial completion and publishing metadata decisions.
5. YouTube and Pinterest require final creative production before scheduling.

---

## 5. Recommended sequence

1. Editorial review of content factory outputs.
2. Rights review for all source images and public-domain/open-access claims.
3. Produce one pilot collection page, one article, one video, one Pinterest set, and one print product mockup.
4. Run internal QA against accessibility, attribution, and brand voice.
5. Compare Gelato and Printful using test print files.
6. Prepare KDP layout only after ebook manuscript approval.
7. Defer Shopify until payment, tax, support, and fulfillment policies are approved.

---

## 6. ADR-011 compliance

RC13 follows ADR-011:

- No Architecture v1.0 documents modified.
- No governance files modified.
- No agents added.
- No ADRs added.
- No payment, order, preservation, or platform write path introduced.
