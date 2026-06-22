# RC14 First Publishable Launch Artifacts Report

**Status:** First publishable launch artifact draft set  
**Authority:** architecture-v1.0 (`architecture-v1.0`, ADR-011)  
**Scope:** Content artifact drafting only — no governance changes, no Architecture v1.0 changes, no agents, no ADRs, no payment processing

---

## 1. Artifacts created

### First ebook

Path:

- `content/ebooks/big-cats-of-the-world/`

Files:

- `manuscript.md`
- `outline.md`
- `product-description.md`
- `rights-checklist.md`

Readiness level:

- Draft sample with 3 manuscript chapters.
- Editorial, species expert, rights, and image review required before publication.

### First audiobook script

Path:

- `content/audiobooks/big-cats-of-the-world/`

Files:

- `narration-script.md`
- `chapter-outline.md`
- `production-notes.md`

Readiness level:

- Draft narration script and production notes.
- Voice review, pronunciation review, transcript QA, and audio production planning required.

### First YouTube scripts

Path:

- `content/youtube/`

Files:

- `big-cats-of-the-world.md`
- `the-story-of-stonehenge.md`
- `endangered-earth.md`

Each includes:

- Hook
- Narration
- Visual direction
- CTA
- Rights/source notes

Readiness level:

- Draft-complete scripts ready for editorial review and production planning.

### First Pinterest pins

Path:

- `content/pinterest/`

Files:

- `pin-brief-01.md`
- `pin-brief-02.md`
- `pin-brief-03.md`
- `pin-brief-04.md`
- `pin-brief-05.md`

Each includes:

- Title
- Description
- Image requirements
- Keywords
- CTA
- Linked product or collection

Readiness level:

- Draft-ready design briefs.

### First product page copy

Path:

- `content/products/`

Files:

- 10 product copy Markdown files generated from `data/portfolio/top_25_showcase_products.json`.

Each includes:

- Title
- Subtitle
- Short description
- Long description
- Educational value
- Target audience
- Suggested product type
- Rights/source notes

Readiness level:

- Draft-ready copy for product validation pages.
- No checkout, payment, order creation, or fulfillment enabled.

---

## 2. Source dependencies

Required source files used:

- `data/publishing/ebooks.json`
- `data/publishing/audiobooks.json`
- `data/publishing/youtube_production.json`
- `data/publishing/pinterest_production.json`
- `data/publishing/print_products.json`
- `data/portfolio/top_25_showcase_products.json`

Additional contextual source files:

- `data/publishing/top_25_showcase_assets.json`
- `data/portfolio/top_25_showcase_collections.json`

---

## 3. Rights risks

Primary risks:

1. Big-cat imagery may require explicit license review and source attribution.
2. Wildlife imagery must avoid exploitative or misleading framing.
3. Stonehenge and heritage visuals need source, license, and jurisdiction review.
4. Product mockups require rights-cleared base images.
5. YouTube scripts require rights-cleared visuals, music, captions, and thumbnail assets.
6. Pinterest pins require vertical imagery and source-safe captions.

Current mitigation:

- All RC14 artifacts are text drafts.
- Every artifact includes source or rights notes.
- No artifact grants image rights.
- No payment processing is enabled.

---

## 4. Readiness level

| Artifact group | Readiness | Blockers |
|----------------|-----------|----------|
| Ebook | Draft sample | Editorial review, expert review, rights-cleared images |
| Audiobook | Draft script | Voice production, pronunciation, transcript QA |
| YouTube scripts | Draft complete | Visual rights, production edit, captions |
| Pinterest briefs | Draft complete | Design production, image rights |
| Product copy | Draft complete | Product imagery, final pricing policy, rights/source review |

---

## 5. Next production actions

1. Assign editorial owner for Big Cats of the World ebook.
2. Create final image list and rights table.
3. Request species expert review for big-cat copy.
4. Produce one YouTube pilot from `content/youtube/big-cats-of-the-world.md`.
5. Design five Pinterest pin mockups from `content/pinterest/`.
6. Add product mockup images only after rights clearance.
7. Review all copy for accessibility, reading level, and source attribution.
8. Keep products read-only until commerce requirements are separately approved.

---

## 6. Validation status

Required validation:

- Markdown files present.
- JSON/source references valid.
- No Architecture v1.0 changes.
- No governance changes.
- No agents added.
- No ADRs added.
- No payment processing enabled.

---

## 7. ADR-011 compliance

RC14 follows ADR-011:

- No Architecture v1.0 documents modified.
- No governance files modified.
- No agents added.
- No ADRs added.
- No payment, order, fulfillment, preservation, or platform write path introduced.
