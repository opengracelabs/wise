# RC9 Commercial Launch Report

**Status:** Prototype commercial launch report  
**Authority:** architecture-v1.0 (`architecture-v1.0`, ADR-011)  
**Scope:** Commercial validation and product prioritization only — no governance changes, no Architecture v1.0 changes, no agents, no ADRs

---

## 1. Executive summary

RC9 can launch as a read-only public prototype for Nature & Culture with a focused commercial validation layer. The strongest early product candidates are globally recognizable heritage sites, flagship wildlife subjects, and iconic public-domain artworks that map cleanly to museum-store and editorial merchandising patterns.

Primary product categories for RC9:

- Posters
- Framed Prints
- Canvas Prints
- Puzzles
- Calendars
- Coffee Table Books

Primary source families:

- UNESCO World Heritage
- GBIF flagship species
- Smithsonian Open Access
- National Gallery public domain
- Rijksmuseum public domain
- Library of Congress
- National Geographic award-winning subjects

---

## 2. Commercial readiness review

| Area | Status | Notes |
|------|--------|-------|
| `/shop` | Ready for prototype | Product cards render from static product intelligence data. |
| `/shop/maps` | Ready for prototype | Validates place-led and historic-map interest. |
| `/shop/education` | Ready for prototype | Validates classroom and repeat-use product categories. |
| `/shop/gifts` | Ready for prototype | Validates high-giftability categories. |
| `/shop/products/{slug}` | Ready for prototype | Generic detail page supports all product slugs currently embedded in `commercial.js`. |
| `/admin/commercial` | Ready as local dashboard | Local-only event view; not production-authenticated. |
| Product intelligence | Ready for prototype | RC7 scores are deterministic estimates, not automated merchandising decisions. |
| Payment processing | Not present by design | No checkout, order creation, fulfillment, or payment API. |

---

## 3. Scoring method

Top product candidates combine:

1. **Recognition:** how likely the public is to recognize the subject.
2. **Demand:** likely attention, gift interest, and shareability.
3. **Commercial fit:** suitability for one or more physical product formats.
4. **Rights and source posture:** preference for public-domain/open-access/prototype-safe source families.
5. **Merchandising pattern:** fit with Smithsonian, National Geographic, Europeana, British Museum, and Google Arts & Culture patterns.

The portfolio dataset at `data/portfolio/top_100_global_assets.json` stores asset-level:

- `recognition_score`
- `demand_score`
- `commercial_score`
- `product_recommendations`

---

## 4. Top 20 product candidates likely to sell

| Rank | Product candidate | Asset | Category | Why it should lead |
|------|-------------------|-------|----------|--------------------|
| 1 | Pyramids of Giza Poster | Pyramids of Giza | Posters | Highest global recognition, strong classroom and gift appeal, strong visual silhouette. |
| 2 | Sunflowers Framed Print | Sunflowers | Framed Prints | Iconic public-domain artwork with proven home decor demand. |
| 3 | Tiger Canvas Print | Tiger | Canvas Prints | Flagship species with high emotional demand and strong visual merchandising fit. |
| 4 | Taj Mahal Framed Print | Taj Mahal | Framed Prints | Globally recognized heritage subject with strong giftability. |
| 5 | Northern Lights Calendar | Northern Lights over Arctic Landscape | Calendars | Recurring seasonal appeal and broad landscape demand. |
| 6 | Great Wall Puzzle | Great Wall of China | Puzzles | Recognizable structure with map/route complexity suitable for puzzle format. |
| 7 | Machu Picchu Coffee Table Book | Machu Picchu | Coffee Table Books | Premium travel, history, and heritage storytelling fit. |
| 8 | The Night Watch Puzzle | The Night Watch | Puzzles | Dense visual detail supports repeat engagement. |
| 9 | Lion Poster | Lion | Posters | Big Cats collection anchor with broad recognition and education fit. |
| 10 | Venice Historic Map Print | Venice and its Lagoon | Framed Prints | Strong place identity and map-led gift appeal. |
| 11 | Great Barrier Reef Canvas Print | Great Barrier Reef | Canvas Prints | High conservation relevance and color-rich visual demand. |
| 12 | The Milkmaid Framed Print | The Milkmaid | Framed Prints | Public-domain masterpiece with strong museum-store fit. |
| 13 | Snow Leopard Calendar | Snow Leopard in the Himalayas | Calendars | Conservation story and seasonal landscape appeal. |
| 14 | Apollo 11 Command Module Poster | Apollo 11 Command Module Columbia | Posters | Space history recognition and family/education demand. |
| 15 | Antelope Canyon Canvas Print | Antelope Canyon Light Beams | Canvas Prints | High visual impact and decor fit. |
| 16 | Stonehenge Historic Map Set | Stonehenge | Posters | Existing demonstration record plus durable heritage recognition. |
| 17 | Elephant Migration Coffee Table Book | Elephant Migration in Amboseli | Coffee Table Books | Strong National Geographic-style narrative and conservation appeal. |
| 18 | Monarch Butterfly Puzzle | Monarch Butterfly Migration | Puzzles | Education, migration, and family learning fit. |
| 19 | The Arnolfini Portrait Framed Print | The Arnolfini Portrait | Framed Prints | Museum-grade art object with high recognition and source clarity. |
| 20 | Grand Canyon Calendar | Grand Canyon Storm Light | Calendars | Broad landscape appeal and repeat seasonal purchase potential. |

---

## 5. Category launch strategy

### Posters

Best for:

- High-recognition heritage sites
- Flagship species
- Classroom and family discovery

Priority subjects:

- Pyramids of Giza
- Lion
- Apollo 11 Command Module
- Stonehenge
- Grand Canyon

### Framed Prints

Best for:

- Public-domain artworks
- Premium heritage images
- Gift-ready decor

Priority subjects:

- Sunflowers
- Taj Mahal
- The Milkmaid
- The Arnolfini Portrait
- Venice and its Lagoon

### Canvas Prints

Best for:

- Landscapes
- Wildlife portraits
- High-color, high-emotion imagery

Priority subjects:

- Tiger
- Great Barrier Reef
- Antelope Canyon
- Northern Lights
- Snow Leopard

### Puzzles

Best for:

- Dense visual detail
- Maps and routes
- Family learning

Priority subjects:

- Great Wall of China
- The Night Watch
- Monarch Butterfly Migration
- Great Barrier Reef
- Stonehenge

### Calendars

Best for:

- Seasonal nature subjects
- Landscape and wildlife series
- Repeat purchase validation

Priority subjects:

- Northern Lights
- Grand Canyon
- Snow Leopard
- Great Barrier Reef
- Big Cats Collection

### Coffee Table Books

Best for:

- Premium narrative collections
- Heritage and conservation essays
- Patron and member gifts

Priority subjects:

- Machu Picchu
- Elephant Migration in Amboseli
- World Heritage Collection
- Great Cats of the World
- Pyramids of Giza

---

## 6. Product requirements before public promotion

1. Confirm rights/clearance posture for every launch image.
2. Replace editorial placeholders with launch-quality images.
3. Add product mockup images for product detail pages.
4. Keep all pricing as placeholder unless pricing is formally approved.
5. Keep Buy Interest language clear: no payment, no checkout, no order.
6. Add source attribution blocks per asset before production commercialization.
7. Keep `/admin/commercial` steward-only by convention until authentication exists.

---

## 7. Content requirements before public promotion

1. Finalize homepage hero image and alt text.
2. Add editorial descriptions for the Top 20 product candidates.
3. Add asset source family and source URL fields in a future portfolio enrichment pass.
4. Add collection pages for Big Cats, World Heritage, Art, Maps, and Education.
5. Add education notes for products intended for classrooms.
6. Add research/source notes for public-domain artworks and heritage assets.

---

## 8. Traffic and conversion targets

| Metric | Prototype target |
|--------|------------------|
| Product views | 250 |
| Wishlist events | 75 |
| Buy interest events | 40 |
| Checkout intent simulation events | 40 |
| Products with at least one buy interest | 10 |
| Categories with at least one buy interest | 6 |
| Homepage-to-shop navigation review | Confirmed during preview QA |

---

## 9. ADR-011 compliance

This report follows ADR-011:

- No Architecture v1.0 documents modified.
- No governance files modified.
- No agents added.
- No ADRs added.
- No checkout, payment, order, or preservation write path introduced.

---

## 10. Recommendation

Launch RC9 as a public prototype with a limited editorial announcement and controlled preview traffic. Use local dashboard sessions and qualitative review to identify the first production-ready product set, then defer any real commerce, authentication, aggregate analytics, or fulfillment design to a separately approved implementation path.
