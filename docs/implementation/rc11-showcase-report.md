# RC11 Showcase Portfolio

**Status:** Implementation showcase artifact  
**Authority:** Architecture v1.0, frozen by ADR-011  
**Scope:** Showcase portfolio selection only  

RC11 distills the RC9 portfolio and audit into a launch-oriented showcase set.
It uses the RC9 audit findings plus portfolio data under `data/portfolio/`.
It does not modify governance, architecture, agents, ADRs, registries, schemas,
or canonical data stores.

## Frozen-architecture boundary

- Architecture v1.0 remains frozen.
- No governance changes are proposed or made.
- No architecture changes are proposed or made.
- No agents are proposed or added.
- No ADRs are proposed or added.
- RC11 outputs are implementation data/report artifacts only.

## Data outputs

| File | Purpose |
|------|---------|
| `data/portfolio/top_50_products.json` | Derived product input used for showcase products |
| `data/portfolio/top_25_showcase_assets.json` | Top 25 showcase assets |
| `data/portfolio/top_25_showcase_collections.json` | Top 25 showcase collections |
| `data/portfolio/top_25_showcase_series.json` | Top 25 showcase series |
| `data/portfolio/top_25_showcase_products.json` | Top 25 showcase products |

## Selection method

RC11 prioritizes:

- recognition score,
- visual appeal,
- educational value,
- commercial value,
- global significance,
- source and rights-readiness signals from RC9,
- balance across heritage, biodiversity, geography, culture, and climate.

## Top showcase assets

| Rank | Asset | Category | Country | Score |
|-----:|-------|----------|---------|------:|
| 1 | Machu Picchu | UNESCO World Heritage | Peru | 97 |
| 2 | Great Pyramid of Giza | UNESCO World Heritage | Egypt | 97 |
| 3 | The Great Wall | UNESCO World Heritage | China | 96 |
| 4 | Taj Mahal | UNESCO World Heritage | India | 95 |
| 5 | African Lion | GBIF Flagship Species | Multiple | 95 |
| 6 | Sunflowers | National Gallery Public Domain | United Kingdom | 95 |
| 7 | Great Barrier Reef | UNESCO World Heritage | Australia | 95 |
| 8 | Tiger | GBIF Flagship Species | Multiple | 95 |
| 9 | The Night Watch | Rijksmuseum Public Domain | Netherlands | 94 |
| 10 | Stonehenge | UNESCO World Heritage | United Kingdom | 94 |
| 11 | Waldseemuller World Map | Public Domain Historical Map | United States | 95 |
| 12 | Apollo 11 Command Module Columbia | Smithsonian Open Access | United States | 94 |
| 13 | Petra | UNESCO World Heritage | Jordan | 94 |
| 14 | Angkor Wat | UNESCO World Heritage | Cambodia | 94 |
| 15 | African Elephant | GBIF Flagship Species | Multiple | 94 |
| 16 | Giant Panda | GBIF Flagship Species | China | 94 |
| 17 | Galapagos Islands | UNESCO World Heritage | Ecuador | 94 |
| 18 | Serengeti National Park | UNESCO World Heritage | Tanzania | 94 |
| 19 | Acropolis of Athens | UNESCO World Heritage | Greece | 94 |
| 20 | Hubble Space Telescope Imagery | Smithsonian Open Access | United States | 94 |
| 21 | The Milkmaid | Rijksmuseum Public Domain | Netherlands | 93 |
| 22 | Historic Centre of Rome | UNESCO World Heritage | Italy | 93 |
| 23 | Chichen Itza | UNESCO World Heritage | Mexico | 93 |
| 24 | Polar Bear | GBIF Flagship Species | Multiple | 94 |
| 25 | Migrant Mother | Library of Congress | United States | 91 |

### Asset rationale

The showcase asset set intentionally combines:

- global heritage icons for recognition and immediate audience comprehension,
- flagship species for biodiversity and conservation storytelling,
- public-domain museum masterworks for rights-readier print validation,
- historical maps and science assets for education and product differentiation.

## Top showcase collections

| Rank | Collection | Balance contribution | Score |
|-----:|------------|----------------------|------:|
| 1 | World Heritage Icons Collection | Heritage, geography, culture | 95 |
| 2 | UNESCO Natural Wonders Collection | Biodiversity, geography, climate | 94 |
| 3 | Big Cats Collection | Biodiversity, culture | 94 |
| 4 | National Gallery Van Gogh Collection | Culture | 92 |
| 5 | Library of Congress Historic Maps Collection | Geography, culture, education | 94 |
| 6 | Endangered Species Collection | Biodiversity, climate, education | 94 |
| 7 | Smithsonian Spaceflight Collection | Culture, education | 93 |
| 8 | Rijksmuseum Rembrandt Collection | Culture | 91 |
| 9 | National Parks of the World Collection | Biodiversity, geography, climate | 93 |
| 10 | Biodiversity Classroom Collection | Biodiversity, education, climate | 93 |
| 11 | National Gallery Impressionism Collection | Culture | 91 |
| 12 | Rijksmuseum Vermeer Collection | Culture | 90 |
| 13 | Coral Reef Life Collection | Biodiversity, climate, education | 92 |
| 14 | World Exploration Maps Collection | Geography, culture, education | 93 |
| 15 | Ocean Giants Collection | Biodiversity, climate | 92 |
| 16 | Smithsonian Natural History Collection | Biodiversity, education, culture | 93 |
| 17 | Ancient Wonders Collection | Heritage, geography, culture | 93 |
| 18 | Great Civilizations Collection | Heritage, culture, education | 93 |
| 19 | Celestial Maps Collection | Geography, education, culture | 91 |
| 20 | Award-Winning Wildlife Subjects Collection | Biodiversity, climate | 90 |
| 21 | Art History Classroom Cards Collection | Culture, education | 90 |
| 22 | Map Literacy Cards Collection | Geography, education | 90 |
| 23 | Open Access Science Collection | Education, culture, climate | 91 |
| 24 | Nature and Culture Launch Collection | Heritage, biodiversity, culture, climate | 92 |
| 25 | Giftable Public Memory Collection | Heritage, culture, education | 91 |

### Collection balance

The selected collections deliberately correct RC9 audit risks by giving showcase
space to biodiversity, geography, climate, science, and education rather than
only UNESCO monuments and Western public-domain art.

## Top showcase series

| Rank | Series | Narrative | Education | Product | Score |
|-----:|--------|----------:|----------:|--------:|------:|
| 1 | Seven Wonders Wall Series | 98 | 94 | 96 | 96 |
| 2 | World Heritage Travel Poster Series | 95 | 92 | 97 | 95 |
| 3 | Van Gogh Color Series | 92 | 90 | 97 | 94 |
| 4 | Big Cats Conservation Series | 96 | 94 | 95 | 95 |
| 5 | Historic World Maps Series | 94 | 97 | 94 | 95 |
| 6 | Smithsonian Space Mission Series | 96 | 97 | 92 | 95 |
| 7 | Ancient Civilizations Puzzle Series | 95 | 96 | 94 | 95 |
| 8 | Museum Masterpiece Wall Series | 91 | 91 | 96 | 93 |
| 9 | Endangered Species Classroom Series | 95 | 98 | 90 | 94 |
| 10 | World Heritage Coffee Table Series | 96 | 94 | 88 | 93 |
| 11 | African Safari Icons Series | 94 | 92 | 95 | 94 |
| 12 | Global Monuments Calendar Series | 91 | 90 | 95 | 92 |
| 13 | Rembrandt Drama Series | 92 | 90 | 94 | 92 |
| 14 | Vermeer Domestic Light Series | 91 | 90 | 93 | 91 |
| 15 | Ocean Giants Series | 93 | 94 | 90 | 92 |
| 16 | Award-Winning Wildlife Calendar Series | 89 | 88 | 94 | 90 |
| 17 | Celestial Maps Series | 91 | 95 | 91 | 92 |
| 18 | Dinosaur Discovery Series | 90 | 96 | 91 | 92 |
| 19 | Global Places Calendar Series | 90 | 90 | 93 | 91 |
| 20 | Historic Map Puzzle Series | 90 | 95 | 91 | 92 |
| 21 | Species Alphabet Cards | 88 | 97 | 88 | 91 |
| 22 | Art History Flash Cards | 88 | 96 | 87 | 90 |
| 23 | Premium Canvas Masterworks Series | 88 | 88 | 95 | 90 |
| 24 | Nature and Culture Core Series | 93 | 93 | 90 | 92 |
| 25 | Global Asset Portfolio Launch Series | 94 | 92 | 92 | 93 |

### Series rationale

The strongest showcase series combine a clear audience-facing story with a
repeatable product line. The top tier is strongest where narrative, education,
and product potential are all above 90.

## Top showcase products

| Rank | Product | Category | Score |
|-----:|---------|----------|------:|
| 1 | Machu Picchu Travel Poster | Posters | 97 |
| 2 | Great Pyramid Educational Puzzle | Puzzles | 96 |
| 3 | Sunflowers Framed Print | Framed Prints | 95 |
| 4 | World Heritage Icons Calendar | Calendars | 95 |
| 5 | African Lion Conservation Poster | Posters | 95 |
| 6 | Waldseemuller World Map Framed Print | Framed Prints | 95 |
| 7 | Taj Mahal Framed Print | Framed Prints | 95 |
| 8 | Van Gogh Color Puzzle | Puzzles | 95 |
| 9 | Great Wall Canvas Print | Canvas Prints | 95 |
| 10 | Great Barrier Reef Canvas Print | Canvas Prints | 95 |
| 11 | Tiger Conservation Canvas Print | Canvas Prints | 95 |
| 12 | The Night Watch Canvas Print | Canvas Prints | 94 |
| 13 | Big Cats Portfolio Book | Coffee Table Books | 94 |
| 14 | Apollo 11 Space Mission Poster | Posters | 94 |
| 15 | Stonehenge Educational Puzzle | Puzzles | 94 |
| 16 | Ancient Civilizations Puzzle Set | Puzzles | 94 |
| 17 | Smithsonian Spaceflight Coffee Table Book | Coffee Table Books | 94 |
| 18 | Petra Desert Rose Poster | Posters | 94 |
| 19 | Giant Panda Family Puzzle | Puzzles | 94 |
| 20 | Historic World Maps Coffee Table Book | Coffee Table Books | 93 |
| 21 | National Parks of the World Poster Set | Posters | 93 |
| 22 | Yellowstone National Park Poster | Posters | 93 |
| 23 | National Gallery Impressionism Calendar | Calendars | 93 |
| 24 | World Exploration Maps Poster Set | Posters | 93 |
| 25 | The Milkmaid Framed Print | Framed Prints | 93 |

## Top 10 products to launch first

| Launch rank | Product | Why first |
|------------:|---------|-----------|
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

## Product category coverage

| Category | Showcase role |
|----------|---------------|
| Posters | Fastest validation format for heritage, wildlife, science, and maps |
| Framed Prints | Premium but accessible public-domain art/map/heritage format |
| Canvas Prints | Higher-margin decor format for landmarks, wildlife, and masterworks |
| Puzzles | Family learning format for monuments, maps, art, and biodiversity |
| Calendars | Seasonal collection format for heritage, art, wildlife, and geography |
| Coffee Table Books | Editorial format for collection depth after demand validation |

## RC11 conclusion

RC11 produces a focused showcase portfolio suitable for validation while
preserving the Architecture v1.0 freeze under ADR-011. The first launch wave
should favor products with the fewest rights and production uncertainties:
public-domain art, public-domain maps, Smithsonian Open Access objects, and
rights-cleared heritage/wildlife imagery for posters, prints, puzzles, and
calendars.
