# RC9 Global Asset Portfolio Prototype

**Status:** Prototype data/report artifact  
**Authority:** Architecture v1.0, frozen by ADR-011  
**Scope:** Portfolio selection and commercial validation only  

RC9 creates a non-architectural portfolio prototype for identifying globally recognizable
assets, collections, series, and likely best-selling products. It does not modify
governance, architecture, agents, ADRs, registries, schemas, or canonical data stores.

## Frozen-architecture boundary

- Architecture v1.0 remains frozen.
- No governance documents were modified.
- No architecture documents were modified.
- No agents were added or changed.
- No ADRs were added or changed.
- RC9 outputs are implementation artifacts under `data/portfolio/` and this report.

## Data outputs

| File | Contents |
|------|----------|
| `data/portfolio/top_100_global_assets.json` | 100 ranked candidate assets |
| `data/portfolio/top_100_collections.json` | 100 ranked candidate collections |
| `data/portfolio/top_100_series.json` | 100 ranked candidate product/portfolio series |

Each record includes:

- `title`
- `category`
- `country`
- `recognition_score`
- `demand_score`
- `commercial_score`
- `portfolio_score`
- `recommended_products`

Scores are normalized from `0.00` to `1.00`.

## Selection criteria

| Intelligence layer | Use in RC9 |
|--------------------|------------|
| Recognition Intelligence | Global familiarity, institutional recognition, educational salience, source authority |
| Demand Intelligence | Search/social/travel/giftability proxy, evergreen audience appeal, classroom relevance |
| Commercial Intelligence | Fit for posters, framed prints, canvas prints, puzzles, calendars, books, maps, cards |
| Portfolio Intelligence | Balanced mix across heritage, nature, art, maps, science, geography, and education |

## Source classes

- UNESCO World Heritage
- GBIF flagship species
- Smithsonian Open Access
- National Gallery public domain
- Rijksmuseum public domain
- Library of Congress
- Public domain historical maps
- Award-winning wildlife photography subjects

## Top assets

| Rank | Asset | Category | Country | Product fit |
|------|-------|----------|---------|-------------|
| 1 | Machu Picchu | UNESCO World Heritage | Peru | Posters, framed prints, puzzles, calendars, coffee table books |
| 2 | Great Pyramid of Giza | UNESCO World Heritage | Egypt | Posters, framed prints, puzzles, educational cards |
| 3 | The Great Wall | UNESCO World Heritage | China | Posters, canvas prints, puzzles, calendars |
| 4 | Taj Mahal | UNESCO World Heritage | India | Posters, framed prints, canvas prints, calendars |
| 5 | Stonehenge | UNESCO World Heritage | United Kingdom | Posters, puzzles, educational cards |
| 6 | Angkor Wat | UNESCO World Heritage | Cambodia | Posters, canvas prints, puzzles, coffee table books |
| 7 | Petra | UNESCO World Heritage | Jordan | Posters, framed prints, canvas prints, puzzles |
| 8 | Acropolis of Athens | UNESCO World Heritage | Greece | Posters, puzzles, coffee table books, educational cards |
| 9 | Historic Centre of Rome | UNESCO World Heritage | Italy | Posters, framed prints, calendars, coffee table books |
| 10 | Chichen Itza | UNESCO World Heritage | Mexico | Posters, puzzles, calendars, educational cards |

## Top collections

| Rank | Collection | Category | Commercial role |
|------|------------|----------|-----------------|
| 1 | World Heritage Icons Collection | UNESCO World Heritage Collection | Highest-recognition launch collection |
| 2 | Ancient Wonders Collection | UNESCO World Heritage Collection | Strong poster/puzzle/book ladder |
| 3 | Great Civilizations Collection | UNESCO World Heritage Collection | Classroom and giftable history bundle |
| 4 | Sacred Architecture Collection | UNESCO World Heritage Collection | Framed/canvas print depth |
| 5 | Castles and Palaces Collection | UNESCO World Heritage Collection | Calendar and puzzle-friendly travel imagery |
| 6 | Historic Cities Collection | UNESCO World Heritage Collection | Bridges posters and historic maps |
| 7 | Cultural Landscapes Collection | UNESCO World Heritage Collection | Broad coffee-table and calendar value |
| 8 | UNESCO Natural Wonders Collection | UNESCO World Heritage Collection | Nature/travel crossover |
| 9 | National Parks of the World Collection | UNESCO World Heritage Collection | Evergreen family and outdoor demand |
| 10 | Island Heritage Collection | UNESCO World Heritage Collection | Distinct travel/landscape niche |

## Top series

| Rank | Series | Category | Commercial role |
|------|--------|----------|-----------------|
| 1 | Seven Wonders Wall Series | Poster Series | High-recognition wall art set |
| 2 | World Heritage Travel Poster Series | Poster Series | Core shop entry product |
| 3 | Ancient Civilizations Puzzle Series | Puzzle Series | Family and education SKU ladder |
| 4 | Global Monuments Calendar Series | Calendar Series | Seasonal cross-sell |
| 5 | Sacred Places Print Series | Fine Art Print Series | Premium framed/canvas candidate |
| 6 | Museum Masterpiece Wall Series | Fine Art Print Series | Public-domain art line |
| 7 | Van Gogh Color Series | Fine Art Print Series | High-demand color-led art products |
| 8 | Rembrandt Drama Series | Fine Art Print Series | Museum authority and premium framing |
| 9 | Vermeer Domestic Light Series | Fine Art Print Series | Giftable museum print series |
| 10 | Impressionist Garden Series | Fine Art Print Series | Decorative poster/calendar fit |

## Top 20 likely best-selling products

| Rank | Product | Category | Primary source | Rationale |
|------|---------|----------|----------------|-----------|
| 1 | Machu Picchu Travel Poster | Posters | UNESCO World Heritage | Highest combined recognition, travel demand, and wall-art fit |
| 2 | Sunflowers Framed Print | Framed Prints | National Gallery public domain | Public-domain art with exceptional consumer recognition |
| 3 | World Heritage Icons Calendar | Calendars | UNESCO World Heritage | Seasonal product with broad global imagery |
| 4 | Great Pyramid Educational Puzzle | Puzzles | UNESCO World Heritage | Family-friendly subject with strong learning value |
| 5 | African Lion Conservation Poster | Posters | GBIF flagship species | High wildlife demand and conservation storytelling |
| 6 | The Night Watch Canvas Print | Canvas Prints | Rijksmuseum public domain | Premium museum artwork with strong decor value |
| 7 | Waldseemuller World Map Framed Print | Historic Maps | Library of Congress | Distinct public-domain map product with gift appeal |
| 8 | Taj Mahal Framed Print | Framed Prints | UNESCO World Heritage | High-recognition monument with strong visual simplicity |
| 9 | Big Cats Educational Card Set | Educational Card Sets | GBIF flagship species | Classroom-friendly set from recognizable flagship species |
| 10 | Van Gogh Color Puzzle | Puzzles | National Gallery public domain | Art recognition plus puzzle-friendly color fields |
| 11 | Historic World Maps Coffee Table Book | Coffee Table Books | Library of Congress | Public-domain archive depth supports book packaging |
| 12 | Great Wall Canvas Print | Canvas Prints | UNESCO World Heritage | Panoramic subject suited to larger-format decor |
| 13 | Apollo 11 Space Mission Poster | Posters | Smithsonian Open Access | Strong science/history crossover audience |
| 14 | Wildlife in Winter Calendar | Calendars | Award-winning wildlife photography subjects | High seasonal visual demand and giftability |
| 15 | Stonehenge Educational Card Set | Educational Card Sets | UNESCO World Heritage | Existing RC1 recognition and classroom fit |
| 16 | Vermeer The Milkmaid Framed Print | Framed Prints | Rijksmuseum public domain | Museum-shop evergreen and premium framing candidate |
| 17 | Ancient Civilizations Puzzle Set | Puzzles | UNESCO World Heritage | Bundles multiple high-recognition heritage assets |
| 18 | National Parks of the World Poster Set | Posters | UNESCO World Heritage | Outdoor/travel demand and collection repeatability |
| 19 | Smithsonian Spaceflight Coffee Table Book | Coffee Table Books | Smithsonian Open Access | Recognizable artifacts and educational editorial depth |
| 20 | Coral Reef Biodiversity Puzzle | Puzzles | Wildlife photography subjects | Family learning plus vivid visual complexity |

## Commercial rationale

### Product category rationale

| Category | Rationale |
|----------|-----------|
| Posters | Lowest-friction validation product; strongest fit for heritage, wildlife, maps, and art |
| Framed Prints | Premium upgrade for museum, heritage, and historic map assets |
| Canvas Prints | Strong decor fit for landscapes, wildlife, and high-color paintings |
| Puzzles | Family and education-friendly format for maps, monuments, biodiversity, and art |
| Calendars | Seasonal bundling format; supports recurring collection refreshes |
| Coffee Table Books | Best for deep collections with narrative and visual depth |
| Historic Maps | Differentiated public-domain category with strong gift value |
| Educational Card Sets | Classroom, family learning, and institutional outreach format |

### Portfolio rationale

The RC9 portfolio is intentionally balanced:

1. **Fast validation products**: posters, prints, calendars, and puzzles.
2. **Premium products**: framed prints, canvas prints, and coffee table books.
3. **Educational products**: card sets and map-literacy products.
4. **Source diversity**: heritage, biodiversity, open-access museums, maps, public-domain art, and wildlife subjects.
5. **Global balance**: a mix of globally known assets and portfolio-depth series that can sustain future collection drops.

### Best-seller hypothesis

The most likely sellers combine:

- high recognition score,
- simple visual comprehension,
- public-domain or open-access feasibility,
- clear product-format fit,
- giftability,
- repeatable collection placement.

For that reason, the first validation wave should emphasize:

1. posters and framed prints for top monuments and public-domain art,
2. puzzles for ancient wonders, maps, and biodiversity,
3. calendars for World Heritage and wildlife collections,
4. educational card sets for heritage/species/map literacy,
5. coffee table books only after demand signals validate collection depth.

## Validation notes

RC9 is a prototype portfolio artifact. It should be validated through JSON structure checks,
required-field checks, and repository smoke tests. It should not trigger architecture,
governance, agent, registry, or ADR changes.
