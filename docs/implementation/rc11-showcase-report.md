# RC11 Showcase Portfolio Report

| Field | Value |
|-------|-------|
| **Status** | Implementation report (non-governance) |
| **Date** | 2026-06-22 |
| **Scope** | Curated showcase subset of the RC9 portfolio: Top 25 assets, collections, series, and products, with launch recommendations |
| **Constraints** | Does not modify Architecture v1.0, governance, ADRs, or agents (ADR-011) |

## Deliverables

| Artifact | Path |
|----------|------|
| Top 25 Showcase Assets | `data/portfolio/top_25_showcase_assets.json` |
| Top 25 Showcase Collections | `data/portfolio/top_25_showcase_collections.json` |
| Top 25 Showcase Series | `data/portfolio/top_25_showcase_series.json` |
| Top 25 Showcase Products | `data/portfolio/top_25_showcase_products.json` |
| Gap Analysis (+ Top 50 to add) | `docs/implementation/rc11-gap-analysis.md` |

> Showcase items are curated from the RC9 portfolio (`data/portfolio/top_100_*.json`) and re-scored with showcase-specific factors. Scores are **editorial 0-100 estimates**, not measured analytics. Per ADR-010, products are derived goods; canonical public memory is never paywalled.
>
> **Input note:** the brief referenced `docs/implementation/rc9-portfolio-audit.md`, which does not exist; this report uses the RC9 data files and plan/product docs instead.

---

## Scoring methodology

| Set | Factors | Weighting |
|-----|---------|-----------|
| Assets | global_significance, visual_appeal, educational_value, commercial_potential, public_domain_readiness | `0.25·sig + 0.20·visual + 0.20·edu + 0.20·comm + 0.15·pd` |
| Collections | collection_strength, breadth, educational_value, commercial_potential | `0.30·strength + 0.20·breadth + 0.25·edu + 0.25·comm` (balanced 5×5 themes) |
| Series | narrative_strength, educational_value, product_potential | `0.40·narrative + 0.30·edu + 0.30·product` |
| Products | design_appeal, market_demand, production_feasibility, margin_potential | `0.30·design + 0.30·demand + 0.20·feasibility + 0.20·margin` |

---

## 1. Top 25 Showcase Assets

Selection factors: global significance · visual appeal · educational value · commercial potential · public-domain readiness.

| # | Asset | Category | Score |
|---|-------|----------|------:|
| 1 | The Starry Night | artwork | 94.5 |
| 2 | The Great Wave off Kanagawa | artwork | 94.3 |
| 3 | Taj Mahal | heritage_site | 93.5 |
| 4 | Pyramids of Giza | heritage_site | 92.6 |
| 5 | Machu Picchu | heritage_site | 92.5 |
| 6 | Girl with a Pearl Earring | artwork | 92.1 |
| 7 | Grand Canyon | natural_site | 91.7 |
| 8 | Great Wall of China | heritage_site | 91.6 |
| 9 | Lion (Panthera leo) | species | 91.2 |
| 10 | Sunflowers | artwork | 91.0 |
| 11 | Colosseum | heritage_site | 90.9 |
| 12 | Tiger (Panthera tigris) | species | 90.5 |
| 13 | Mount Fuji | natural_site | 90.2 |
| 14 | The Night Watch | artwork | 90.1 |
| 15 | Petra | heritage_site | 89.9 |
| 16 | The Birth of Venus | artwork | 89.8 |
| 17 | Giant Panda | species | 89.8 |
| 18 | Angkor Wat | heritage_site | 89.6 |
| 19 | The Birds of America plates | artwork | 89.6 |
| 20 | Great Barrier Reef | natural_site | 89.5 |
| 21 | African Elephant | species | 87.8 |
| 22 | Mercator World Map (1569) | map | 87.3 |
| 23 | Snow Leopard | species | 87.0 |
| 24 | Waldseemüller World Map (1507) | map | 86.8 |
| 25 | Emperor Penguin | species | 86.1 |

Category mix: artwork 7, heritage_site 7, species 6, natural_site 3, map 2. Public-domain artworks and maps lead on readiness; sites/species require own/commissioned or CC-licensed photography before commercial use.

## 2. Top 25 Showcase Collections (balanced 5 themes × 5)

| Theme | Collections (score) |
|-------|---------------------|
| **Heritage** | Wonders of the Ancient World (92.8) · World Heritage Icons (92.1) · Ancient Egypt (88.5) · Castles and Fortresses (87.4) · Lost Cities (86.5) |
| **Biodiversity** | Big Cats of the World (91.7) · Endangered Earth (89.8) · African Wildlife (88.8) · Coral Reefs (86.5) · Birds of Paradise (86.2) |
| **Geography** | Oceans of the World (89.0) · Sacred Mountains (88.7) · Great Rivers of the World (87.2) · Great Deserts (86.9) · Mountains of the World (86.2) |
| **Culture** | Ancient Maps (89.9) · Renaissance Masterpieces (88.9) · Japanese Woodblock Prints (86.5) · Temples of Asia (85.8) · Cathedrals of Europe (85.6) |
| **Climate** | Rainforests of the World (87.2) · Polar Regions (86.1) · Volcanoes of the World (85.7) · The Northern Lights (84.3) · Glaciers and Ice (83.6) |

## 3. Top 25 Showcase Series

Requirements: narrative strength · educational value · product potential.

| # | Series | Score | # | Series | Score |
|---|--------|------:|---|--------|------:|
| 1 | Great Civilizations | 93.5 | 14 | Mapping the World | 88.6 |
| 2 | Lions Through History | 92.9 | 15 | Renaissance Genius | 88.6 |
| 3 | The Pharaohs of Egypt | 92.2 | 16 | The Great Migrations | 88.4 |
| 4 | The Rise and Fall of Rome | 90.9 | 17 | The Story of Machu Picchu | 88.1 |
| 5 | Seven Wonders of the Ancient World | 90.8 | 18 | Empires of the Maya | 87.1 |
| 6 | Endangered Species | 90.3 | 19 | Vikings: Seafarers of the North | 86.8 |
| 7 | The Story of Petra | 90.2 | 20 | Whales of the World Ocean | 86.6 |
| 8 | Tigers of Asia | 90.0 | 21 | Elephants of Africa | 86.6 |
| 9 | The Voyages of Discovery | 89.6 | 22 | Hokusai and the Floating World | 86.6 |
| 10 | Darwin and the Galápagos | 89.4 | 23 | The Story of Stonehenge | 86.4 |
| 11 | The Story of the Silk Road | 88.8 | 24 | The Great Apes | 85.6 |
| 12 | The Story of the Taj Mahal | 88.8 | 25 | The Polar Explorers | 85.6 |
| 13 | Pompeii: A City Frozen in Time | 88.8 | | | |

## 4. Top 25 Showcase Products (6 categories)

Distribution: Posters 4 · Framed Prints 4 · Canvas Prints 4 · Puzzles 4 · Calendars 4 · Coffee Table Books 5.

| # | Product | Category | Score |
|---|---------|----------|------:|
| 1 | Starry Night Poster | Posters | 90.3 |
| 2 | The Great Wave Poster | Posters | 90.0 |
| 3 | Starry Night Gallery Canvas | Canvas Prints | 89.5 |
| 4 | Fine Art Masterpiece Framed Print | Framed Prints | 89.2 |
| 5 | Wildlife Canvas Print | Canvas Prints | 89.2 |
| 6 | Iconic Wonders Poster | Posters | 88.7 |
| 7 | Girl with a Pearl Earring Framed Print | Framed Prints | 88.3 |
| 8 | Natural Wonder Canvas Print | Canvas Prints | 88.0 |
| 9 | Starry Night Jigsaw (1000 pc) | Puzzles | 87.8 |
| 10 | The Great Wave Jigsaw (1000 pc) | Puzzles | 87.5 |
| 11 | Wonders of the World Jigsaw (1000 pc) | Puzzles | 87.2 |
| 12 | Wildlife Jigsaw (1000 pc) | Puzzles | 87.2 |
| 13 | Wildlife Wall Calendar | Calendars | 87.2 |
| 14 | Big Cats Poster | Posters | 87.0 |
| 15 | Heritage Site Framed Print | Framed Prints | 86.6 |
| 16 | Endangered Species Canvas Series | Canvas Prints | 86.4 |
| 17 | World Heritage Wall Calendar | Calendars | 86.0 |
| 18 | Natural Wonders Wall Calendar | Calendars | 86.0 |
| 19 | Audubon Birds Framed Print Set | Framed Prints | 85.8 |
| 20 | Big Cats Coffee Table Book | Coffee Table Books | 85.4 |
| 21 | Masters of Art Coffee Table Book | Coffee Table Books | 84.9 |
| 22 | World Heritage Coffee Table Book | Coffee Table Books | 84.8 |
| 23 | Endangered Species Calendar | Calendars | 84.0 |
| 24 | Great Civilizations Coffee Table Book | Coffee Table Books | 83.8 |
| 25 | Ancient Maps Coffee Table Book | Coffee Table Books | 82.6 |

---

## 5. Recommended Top 10 launch products

The highest-scoring products cluster in wall art and puzzles. The recommended launch set keeps the strongest performers **and guarantees all six categories** are represented at launch (so the storefront reads as a complete range and de-risks demand concentration). Public-domain artwork SKUs (Van Gogh, Hokusai, Vermeer) are prioritized — they are reproduction-ready today with no photography-rights dependency.

| Rank | Product | Category | Score | Why launch first |
|------|---------|----------|------:|------------------|
| 1 | Starry Night Poster | Posters | 90.3 | Top score; PD art; lowest-friction entry SKU |
| 2 | The Great Wave Poster | Posters | 90.0 | PD art; global recognition; strong margin at scale |
| 3 | Starry Night Gallery Canvas | Canvas Prints | 89.5 | Premium PD-art SKU; higher AOV |
| 4 | Fine Art Masterpiece Framed Print | Framed Prints | 89.2 | High-AOV PD art; museum-shop staple |
| 5 | Wildlife Canvas Print | Canvas Prints | 89.2 | Best-selling decor genre; broad audience |
| 6 | Iconic Wonders Poster | Posters | 88.7 | Heritage breadth; travel/gift appeal |
| 7 | Starry Night Jigsaw (1000 pc) | Puzzles | 87.8 | High-detail PD art; family + gift market |
| 8 | Wildlife Wall Calendar | Calendars | 87.2 | Best calendar genre; recurring annual revenue |
| 9 | Big Cats Coffee Table Book | Coffee Table Books | 85.4 | High-margin flagship; showcases authority |
| 10 | Heritage Site Framed Print | Framed Prints | 86.6 | Heritage decor; travel commemoration |

**Category coverage of the launch set:** Posters ×3, Canvas ×2, Framed ×2, Puzzles ×1, Calendars ×1, Coffee Table Books ×1 — all six categories live at launch.

**Launch gating (non-negotiable):** every SKU ships only after its source asset(s) pass discovery → preservation → metadata → rights/quality and carry a confirmed public-domain or licensed high-resolution master. PD artworks/maps (Van Gogh, Hokusai, Vermeer, Audubon, Mercator, Waldseemüller) clear fastest; site/species/landscape SKUs depend on cleared photography.

---

## 6. Portfolio health & next steps

- **Strengths:** deep, recognizable art + heritage + flagship-species coverage; strong PD-ready artwork/map base for immediate productization.
- **Gaps (see `rc11-gap-analysis.md`):** Sub-Saharan Africa, Middle East/West Asia, Central Asia, South Asia, Oceania, and Indigenous cultures are thin; the Top 50 additions are sequenced to close them.
- **Next:** ingest Gap-Analysis Wave A (regional/cultural balance), wire the showcase catalogue into the Phase 12 storefront per `top_20_product_candidates.md` and `rc9-public-launch-plan.md`, and clear rights for the Top 10 launch SKUs.

---

*Implementation report. Does not modify Architecture v1.0, governance, ADRs, or agents (ADR-011). Sources: `data/portfolio/top_25_showcase_*.json`, `top_100_*.json`.*
