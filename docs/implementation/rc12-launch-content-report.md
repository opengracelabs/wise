# RC12 Launch Content Factory

**Status:** Implementation content artifact  
**Authority:** Architecture v1.0, frozen by ADR-011  
**Scope:** Launch content generation only  

RC12 turns the RC11 Showcase Portfolio into validation-ready launch content for
products, Pinterest, YouTube, SEO, and email. It does not modify governance,
architecture, agents, ADRs, registries, schemas, or canonical data stores.

## Frozen-architecture boundary

- Architecture v1.0 remains frozen.
- No governance changes are proposed or made.
- No architecture changes are proposed or made.
- No agents are proposed or added.
- No ADRs are proposed or added.
- RC12 outputs are implementation data/report artifacts only.

## Source inputs

RC12 uses:

- `data/portfolio/top_25_showcase_assets.json`
- `data/portfolio/top_25_showcase_collections.json`
- `data/portfolio/top_25_showcase_series.json`
- `data/portfolio/top_25_showcase_products.json`

## Content inventory

| Artifact | Count | Purpose |
|----------|------:|---------|
| `data/marketing/product_catalog.json` | 25 products | Product-ready titles, subtitles, descriptions, educational value, audiences, and keywords |
| `data/marketing/pinterest_campaigns.json` | 75 campaigns | Pinterest content for assets, collections, and products |
| `data/marketing/youtube_campaigns.json` | 4 campaigns | YouTube campaign outlines for Heritage, Species, Collections, and Series |
| `data/marketing/seo_pages.json` | 100 pages | SEO metadata for assets, collections, series, and products |
| `data/marketing/email_campaigns.json` | 4 sequences / 12 emails | Welcome, Collections, Species, and Products launch sequences |

## Product content inventory

The product catalog covers all top 25 showcase products and includes:

- `title`
- `subtitle`
- `short_description`
- `long_description`
- `educational_value`
- `target_audience`
- `keywords`

Primary product families:

| Product family | Role |
|----------------|------|
| Posters | Fast launch validation for heritage, species, science, and map topics |
| Framed Prints | Premium but accessible public-domain art, maps, and heritage imagery |
| Canvas Prints | Higher-margin decor validation for landmarks, wildlife, reefs, and art |
| Puzzles | Family and classroom learning through monuments, biodiversity, maps, and art |
| Calendars | Seasonal collection validation across heritage, art, and wildlife |
| Coffee Table Books | Editorial packaging for collection depth after demand validation |

## Marketing inventory

### Pinterest

Pinterest content is split into three boards:

1. **Assets** — top showcase assets as visual learning pins.
2. **Collections** — balanced collection boards across heritage, biodiversity,
   geography, culture, climate, and education.
3. **Products** — giftable validation products with product-specific CTAs.

Each campaign includes:

- `title`
- `description`
- `keywords`
- `CTA`

### YouTube

YouTube content covers four launch storylines:

| Segment | Campaign role |
|---------|---------------|
| Heritage | Explains global heritage assets as learning objects, not only travel imagery |
| Species | Connects flagship species to conservation, climate, and family learning |
| Collections | Shows how balanced collections combine heritage, biodiversity, geography, culture, and climate |
| Series | Explains how narrative strength, educational strength, and product potential become repeatable product lines |

Each YouTube campaign includes:

- `title`
- `hook`
- `outline`
- `CTA`

### Email

Email content includes four launch sequences:

| Sequence | Emails | Role |
|----------|-------:|------|
| Welcome | 3 | Introduce RC12 and the showcase selection method |
| Collections | 3 | Explain heritage, biodiversity, maps, science, and public-domain art collections |
| Species | 3 | Convert flagship species recognition into conservation learning |
| Products | 3 | Promote the top launch products and product-category roles |

## SEO inventory

`data/marketing/seo_pages.json` contains exactly 100 SEO pages:

- 25 showcase asset pages,
- 25 showcase collection pages,
- 25 showcase series pages,
- 25 showcase product pages.

Each SEO page includes:

- `title`
- `slug`
- `meta_description`
- `keywords`

The SEO inventory is designed for future validation pages and does not imply a
new frontend architecture or production deployment.

## Launch recommendations

### Top 10 first-launch products

| Rank | Product | Launch reason |
|-----:|---------|---------------|
| 1 | Machu Picchu Travel Poster | Highest combined recognition, visual appeal, and poster validation simplicity |
| 2 | Great Pyramid Educational Puzzle | Strong family learning, global recognition, and puzzle-market fit |
| 3 | Sunflowers Framed Print | Public-domain readiness and high consumer art recognition |
| 4 | World Heritage Icons Calendar | Seasonal bundle with broad global coverage |
| 5 | African Lion Conservation Poster | Strong biodiversity story and accessible wildlife demand |
| 6 | Waldseemuller World Map Framed Print | Differentiated historic-map product with high education value |
| 7 | Taj Mahal Framed Print | High visual clarity and global gift appeal |
| 8 | Van Gogh Color Puzzle | Public-domain art plus puzzle-friendly color and texture |
| 9 | Great Wall Canvas Print | Premium decor format for a global heritage icon |
| 10 | Great Barrier Reef Canvas Print | Climate, biodiversity, and visual appeal in one showcase product |

### Recommended launch order

1. Publish validation pages for the top 10 products.
2. Pair each product with one Pinterest asset pin and one product pin.
3. Launch the Welcome email sequence.
4. Release the Heritage and Species YouTube storylines first.
5. Add collection and series SEO pages after product pages are validated.
6. Use wishlist, view, and buy-intent signals only; no payment processing.

### Rights and production cautions

- Public-domain/open-access sources remain the lowest-risk launch inputs.
- UNESCO recognition does not equal image-rights clearance.
- Wildlife photography subjects require rights-cleared imagery before production.
- RC12 content is launch validation copy only, not payment, checkout, fulfillment,
  or production enablement.

## RC12 conclusion

RC12 creates a complete launch content inventory for the RC11 Showcase Portfolio:
product catalog copy, Pinterest campaigns, YouTube outlines, SEO metadata, and
email sequences. It is ready for validation-only use while preserving the
Architecture v1.0 freeze under ADR-011.
