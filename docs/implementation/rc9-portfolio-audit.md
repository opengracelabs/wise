# RC9 Portfolio Audit

**Status:** Implementation audit artifact  
**Authority:** Architecture v1.0, frozen by ADR-011  
**Scope:** Audit of RC9 portfolio data only  

This audit reviews:

- `data/portfolio/top_100_global_assets.json`
- `data/portfolio/top_100_collections.json`
- `data/portfolio/top_100_series.json`

It does not modify governance, architecture, agents, ADRs, registries, schemas, or
canonical data stores.

## Frozen-architecture boundary

- Architecture v1.0 remains frozen.
- No governance changes are proposed or made.
- No architecture changes are proposed or made.
- No agents are proposed or added.
- No ADRs are proposed or added.
- Recommendations below are portfolio-selection recommendations only.

## Executive assessment

**Portfolio score: 84 / 100**

The RC9 portfolio is commercially strong and immediately useful for validation.
It has high visual appeal, strong product mapping, and clear use of public/open
source classes. Its main weaknesses are geographic concentration, heavy reliance
on UNESCO and U.S./Western European public-domain institutions, limited Indigenous
and African cultural representation beyond globally familiar monuments, and a
few missing flagship museum/art/map candidates.

## Evaluation by audit dimension

| Dimension | Score | Assessment |
|-----------|------:|------------|
| Geographic diversity | 7 / 10 | Global framing is present, but U.S., U.K., Netherlands, Italy, and Europe-facing assets are overrepresented. Africa, South Asia beyond India, Southeast Asia beyond Angkor/Bagan/Ha Long, Indigenous regions, and Oceania need more depth. |
| UNESCO coverage | 9 / 10 | Strong top-tier UNESCO presence across monuments, natural parks, landscapes, and historic cities. Coverage is high but leans toward globally famous tourist icons. |
| Species coverage | 8 / 10 | Strong flagship mammal and conservation species coverage. Birds, insects, marine biodiversity, plants, amphibians, and ecosystem-level species sets are underweighted. |
| Cultural heritage coverage | 8 / 10 | Strong ancient monuments, museum art, national memory, and historic city coverage. Missing depth in Africa, Indigenous Americas, Islamic world, South Asia beyond Taj Mahal, and intangible/craft-linked heritage. |
| Historic maps coverage | 8 / 10 | Good Library of Congress and public-domain map representation, including world, city, celestial, battlefield, and exploration maps. Needs more non-U.S./non-European cartographic traditions. |
| Educational value | 9 / 10 | Educational card sets, classroom collections, species literacy, map literacy, and world heritage learning are well represented. |
| Product potential | 9 / 10 | Posters, framed prints, canvas prints, puzzles, calendars, coffee table books, maps, and card sets are consistently mapped. Product ladder is clear. |
| Public-domain availability | 8 / 10 | National Gallery, Rijksmuseum, Smithsonian Open Access, Library of Congress, and public-domain maps are strong. Wildlife photography subjects require rights-cleared image sourcing before production. UNESCO subjects require rights-cleared imagery despite public site recognition. |
| Visual appeal | 9 / 10 | Monuments, wildlife, masterworks, maps, and space/science subjects are visually strong. Some education/history items have weaker immediate visual pull. |
| Portfolio balance | 8 / 10 | Balanced across heritage, species, art, maps, science, and education, but over-indexed on posters/prints and Western open-access art institutions. |

## Coverage findings

### Geographic diversity

**Strengths**

- Global anchor assets include Peru, Egypt, China, India, Cambodia, Jordan,
  Greece, Mexico, Tanzania, Australia, Ecuador, Japan, Indonesia, Vietnam,
  Cuba, and Chile.
- Collections and series include "Global" bundles that can support broad
  geographic interpretation.

**Gaps**

- United States, United Kingdom, Netherlands, and Western Europe dominate the
  public-domain art/map/source-heavy portions.
- Africa is represented mostly through wildlife and a few iconic UNESCO sites.
- South Asia is underrepresented beyond India/Taj Mahal.
- Indigenous heritage and Oceania are thin beyond Uluru-Kata Tjuta and Rapa Nui.
- Middle East coverage is present but not deep beyond Petra and Egypt.

### UNESCO coverage

**Strengths**

- The global assets list opens with high-recognition UNESCO icons.
- Natural sites, cultural landscapes, historic cities, and monuments are all
  represented.
- UNESCO collections and series support posters, puzzles, calendars, and books.

**Gaps**

- Coverage favors tourism-recognized sites over underrepresented heritage regions.
- Missing high-recognition candidates include Pyramids-adjacent Egyptian series,
  Lalibela, Timbuktu manuscripts/urban heritage, Mesa Verde, Borobudur, Persepolis,
  and Samarkand.

### Species coverage

**Strengths**

- Flagship mammals and conservation icons are strong: lion, tiger, elephant,
  giant panda, polar bear, snow leopard, jaguar, cheetah, gorilla, orangutan,
  whales, turtle, rhino, red panda, bald eagle, and koala.
- Education products map naturally to species literacy and conservation stories.

**Gaps**

- Mammals are overrepresented.
- Plants, amphibians, reptiles beyond turtle/Komodo, coral species, insects
  beyond monarch, and keystone ecosystem species are underrepresented.
- Missing flagship candidates include great white shark, manta ray, poison dart
  frog, axolotl, baobab, saguaro, sequoia, and Darwin's finches.

### Cultural heritage coverage

**Strengths**

- Strong ancient monuments and museum masterworks.
- Good public-domain art representation from National Gallery and Rijksmuseum.
- Library of Congress adds civic, photographic, and social-history material.

**Gaps**

- African material culture, Islamic art/architecture, South Asian art, East Asian
  painting/craft, Indigenous cultural heritage, textiles, manuscripts, and
  archaeological object series need more representation.
- The British Museum reference model is mentioned in the wider RC9 report, but
  object-style antiquities are not yet a strong data category.

### Historic maps coverage

**Strengths**

- Strong commercial fit for framed maps, posters, puzzles, and coffee table books.
- World maps, exploration maps, city maps, Sanborn maps, battlefield maps, and
  celestial maps are present.

**Gaps**

- Non-Western map traditions are underrepresented.
- Missing candidates include Piri Reis map, Kangnido map, Tabula Rogeriana,
  Fra Mauro map, Mappa Mundi, Polynesian navigation charts, and Indigenous
  cartographic knowledge where rights and cultural sensitivity permit.

### Educational value

**Strengths**

- Classroom card sets appear across heritage, species, art, and maps.
- Puzzles and calendars support family learning.
- Coffee table books can package narrative depth.

**Gaps**

- Education products should be split by grade band and sensitivity tier in future
  implementation work, without changing architecture.
- More explicit learning standards alignment would improve validation.

### Product potential

**Strengths**

- Posters and framed/canvas prints have the clearest immediate validation path.
- Puzzles are strong for maps, art, biodiversity, and monuments.
- Calendars are strong for seasonal collection testing.
- Educational card sets offer institutional/classroom differentiation.

**Gaps**

- Coffee table books are promising but require editorial investment and should
  follow demand validation.
- Historic maps are distinctive but need high-resolution, rights-cleared files.
- Wildlife photography subjects need rights sourcing before production.

### Public-domain availability

**Strengths**

- Public-domain/open-access institutional sources are represented.
- The National Gallery, Rijksmuseum, Smithsonian Open Access, and Library of
  Congress categories are production-friendly for validation.

**Gaps**

- UNESCO site recognition is not equivalent to image rights clearance.
- Wildlife photography subjects are subjects, not cleared assets.
- Some map and archive assets may require item-level public-domain verification.

### Visual appeal

**Strengths**

- High-recognition monuments, masterworks, wildlife, maps, and space imagery have
  strong visual merchandising value.
- The portfolio supports both decor and education contexts.

**Gaps**

- Some Library of Congress civic/history assets are educationally valuable but
  less visually immediate than art, maps, monuments, and wildlife.

### Portfolio balance

**Strengths**

- The data includes assets, collections, and series across the major RC9 source
  classes.
- Product categories are consistently represented.

**Gaps**

- Posters, framed prints, and canvas prints dominate.
- Underweighted categories include historic maps as standalone hero products,
  educational card sets, and coffee table books tied to non-Western collections.

## Overrepresented categories

1. UNESCO monument/travel icons.
2. U.S.-sourced Library of Congress and Smithsonian material.
3. Western European public-domain art via National Gallery and Rijksmuseum.
4. Mammalian flagship species.
5. Posters and wall-art formats.
6. Generic "Global" collection/series framing.

## Underrepresented categories

1. African cultural heritage beyond wildlife and a few sites.
2. Indigenous heritage, with cultural sensitivity and rights review.
3. South Asian, Southeast Asian, Middle Eastern, and Latin American collections
   beyond the most recognizable monuments.
4. Non-Western cartographic traditions.
5. Plant, insect, amphibian, reptile, and marine species diversity.
6. Manuscripts, textiles, decorative arts, craft, and archaeological objects.
7. Education-first products segmented by learner level.
8. Rights-cleared wildlife image collections.

## Missing flagship assets

These are portfolio gaps to consider for future data revisions, subject to
rights, cultural sensitivity, and source availability review:

1. Borobudur
2. Persepolis
3. Lalibela Rock-Hewn Churches
4. Timbuktu manuscripts and historic city heritage
5. Mesa Verde
6. Samarkand
7. Borobudur temple reliefs series candidate
8. Great Zimbabwe
9. Lascaux cave art interpretive candidate
10. Himeji Castle
11. Mount Fuji
12. Torres del Paine or Patagonia landscape candidate
13. Amazon rainforest biodiversity candidate
14. Baobab flagship species/ecosystem candidate
15. Great white shark
16. Manta ray
17. Axolotl
18. Sequoia or giant redwood
19. Darwin's finches
20. Piri Reis map
21. Fra Mauro map
22. Hereford Mappa Mundi candidate
23. Harlem Renaissance public-domain visual culture candidate
24. WPA National Parks poster archive candidate
25. Japanese woodblock public-domain masterworks candidate

## Missing flagship collections

1. African Kingdoms and Cities Collection
2. Islamic Architecture and Geometry Collection
3. South Asian Sacred Sites Collection
4. Indigenous North American Heritage Collection
5. Andean Civilizations Collection
6. Mesoamerican Civilizations Collection
7. Silk Roads Cities Collection
8. East Asian Woodblock and Ink Collection
9. Manuscripts and Illuminated Pages Collection
10. Textiles and Pattern Heritage Collection
11. Global Archaeology Objects Collection
12. Ocean Biodiversity Collection
13. Plant Biodiversity and Forest Giants Collection
14. Amphibians and Reptiles Conservation Collection
15. Pollinators and Native Plants Collection
16. Non-Western Cartography Collection
17. Maritime Navigation Traditions Collection
18. Public Domain Science Illustration Collection
19. WPA Posters and Civic Design Collection
20. Historic Astronomy Plates Collection
21. Women's History Public Domain Collection
22. Global Freedom Movements Collection
23. Children's Museum Learning Collection
24. Climate and Conservation Education Collection
25. World Languages and Scripts Collection

## Missing flagship series

1. African Heritage Poster Series
2. Islamic Geometry Print Series
3. South Asian Monument Puzzle Series
4. Indigenous Knowledge Education Series
5. Andean Civilizations Card Series
6. Mesoamerican Cities Product Series
7. Silk Roads Map and City Series
8. East Asian Woodblock Wall Series
9. Manuscript Illumination Print Series
10. Textile Pattern Calendar Series
11. Archaeology Object Authority Series
12. Ocean Species Classroom Series
13. Forest Giants Conservation Series
14. Amphibians and Reptiles Card Series
15. Native Plants and Pollinators Series
16. Non-Western Historic Maps Series
17. Maritime Navigation Chart Series
18. Public Domain Science Illustration Series
19. WPA Parks Poster Series
20. Historic Astronomy Plate Series
21. Women in Public Memory Series
22. Global Freedom Movements Poster Series
23. Climate Stewardship Classroom Series
24. World Scripts Educational Card Series
25. Rights-Cleared Wildlife Photography Series

## Top 25 highest-priority assets

Priority combines current rank, commercial fit, visual appeal, educational value,
source clarity, and portfolio gap coverage.

| Priority | Asset | Status | Primary rationale |
|---------:|-------|--------|-------------------|
| 1 | Machu Picchu | Current | Strongest combined recognition, demand, and product fit |
| 2 | Sunflowers | Current | High-recognition public-domain art with exceptional print/puzzle potential |
| 3 | Great Pyramid of Giza | Current | Global recognition and education value |
| 4 | African Lion | Current | High wildlife demand and conservation storytelling |
| 5 | The Night Watch | Current | Premium public-domain museum masterwork |
| 6 | Waldseemuller World Map | Current | Distinctive historic map hero product |
| 7 | Taj Mahal | Current | High visual appeal and global recognition |
| 8 | The Great Wall | Current | Strong panoramic poster/canvas fit |
| 9 | Apollo 11 Command Module Columbia | Current | Science/history crossover with education value |
| 10 | Stonehenge | Current | Existing RC1 anchor and classroom fit |
| 11 | Tiger | Current | High-demand flagship species |
| 12 | Giant Panda | Current | High-demand conservation and family-learning appeal |
| 13 | The Milkmaid | Current | Premium public-domain art product candidate |
| 14 | Great Barrier Reef | Current | Nature, conservation, and puzzle/calendar fit |
| 15 | Petra | Current | Strong heritage visual identity |
| 16 | Borobudur | Missing | High-priority Southeast Asian heritage gap |
| 17 | Great Zimbabwe | Missing | High-priority African cultural heritage gap |
| 18 | Lalibela Rock-Hewn Churches | Missing | High-priority African sacred architecture gap |
| 19 | Piri Reis map | Missing | High-priority non-Western cartography gap |
| 20 | Japanese woodblock public-domain masterworks | Missing | High-demand public-domain art gap |
| 21 | Sequoia or giant redwood | Missing | Plant/ecosystem flagship gap |
| 22 | Axolotl | Missing | Amphibian flagship and education gap |
| 23 | Manta ray | Missing | Marine biodiversity flagship gap |
| 24 | WPA National Parks poster archive | Missing | Strong public-domain poster-commerce gap |
| 25 | Amazon rainforest biodiversity candidate | Missing | Ecosystem-level portfolio balance gap |

## Top 25 highest-priority collections

| Priority | Collection | Status | Primary rationale |
|---------:|------------|--------|-------------------|
| 1 | World Heritage Icons Collection | Current | Best launch collection for global recognition |
| 2 | National Gallery Van Gogh Collection | Current | Highest-demand public-domain art collection |
| 3 | Big Cats Collection | Current | Strongest wildlife commerce collection |
| 4 | Public Domain Masterpiece Collection | Current | Broadest art-commerce validation set |
| 5 | Library of Congress Historic Maps Collection | Current | Distinctive map product line |
| 6 | Smithsonian Spaceflight Collection | Current | Science/history education crossover |
| 7 | UNESCO Natural Wonders Collection | Current | Nature/travel calendar and puzzle strength |
| 8 | Rijksmuseum Rembrandt Collection | Current | Premium museum-shop print depth |
| 9 | Endangered Species Collection | Current | Conservation education and giftability |
| 10 | Global Classroom Starter Collection | Current | Education-first differentiation |
| 11 | African Kingdoms and Cities Collection | Missing | Corrects African cultural heritage gap |
| 12 | Islamic Architecture and Geometry Collection | Missing | Adds major visual/cultural series potential |
| 13 | South Asian Sacred Sites Collection | Missing | Corrects South Asia depth gap |
| 14 | Indigenous North American Heritage Collection | Missing | Adds sensitivity-aware Indigenous coverage |
| 15 | East Asian Woodblock and Ink Collection | Missing | Adds high-demand public-domain art format |
| 16 | Non-Western Cartography Collection | Missing | Corrects historic map source imbalance |
| 17 | Plant Biodiversity and Forest Giants Collection | Missing | Corrects species/ecosystem imbalance |
| 18 | Ocean Biodiversity Collection | Missing | Adds marine education and visual appeal |
| 19 | Manuscripts and Illuminated Pages Collection | Missing | Adds heritage object and book potential |
| 20 | Textiles and Pattern Heritage Collection | Missing | Adds decor-ready cultural heritage format |
| 21 | WPA Posters and Civic Design Collection | Missing | Strong public-domain poster validation |
| 22 | Public Domain Science Illustration Collection | Missing | Adds education and wall-art crossover |
| 23 | Climate and Conservation Education Collection | Missing | Adds mission-aligned education line |
| 24 | World Languages and Scripts Collection | Missing | Adds language/culture learning value |
| 25 | Rights-Cleared Wildlife Photography Collection | Missing | Converts subject interest into production-ready assets |

## Top 25 highest-priority series

| Priority | Series | Status | Primary rationale |
|---------:|--------|--------|-------------------|
| 1 | Seven Wonders Wall Series | Current | Highest-recognition wall-art bundle |
| 2 | World Heritage Travel Poster Series | Current | Core poster validation line |
| 3 | Van Gogh Color Series | Current | High-demand public-domain art line |
| 4 | Big Cats Conservation Series | Current | Strong wildlife product ladder |
| 5 | Historic World Maps Series | Current | Distinctive map-commerce line |
| 6 | Smithsonian Space Mission Series | Current | Science/history education crossover |
| 7 | Ancient Civilizations Puzzle Series | Current | Family education and puzzle fit |
| 8 | Museum Masterpiece Wall Series | Current | Premium art print line |
| 9 | Endangered Species Classroom Series | Current | Strong education/card set line |
| 10 | World Heritage Coffee Table Series | Current | Editorial depth after demand validation |
| 11 | African Heritage Poster Series | Missing | Corrects African heritage gap |
| 12 | Islamic Geometry Print Series | Missing | High visual appeal and decor potential |
| 13 | South Asian Monument Puzzle Series | Missing | Corrects South Asia depth gap |
| 14 | East Asian Woodblock Wall Series | Missing | High-demand public-domain art opportunity |
| 15 | Non-Western Historic Maps Series | Missing | Corrects cartographic imbalance |
| 16 | Ocean Species Classroom Series | Missing | Adds marine biodiversity education line |
| 17 | Forest Giants Conservation Series | Missing | Adds plant/ecosystem flagship line |
| 18 | WPA Parks Poster Series | Missing | Strong poster product-market fit |
| 19 | Public Domain Science Illustration Series | Missing | Adds education and art crossover |
| 20 | Manuscript Illumination Print Series | Missing | Adds heritage object/book potential |
| 21 | Textile Pattern Calendar Series | Missing | Adds decor and cultural diversity |
| 22 | World Scripts Educational Card Series | Missing | Adds language/culture education value |
| 23 | Rights-Cleared Wildlife Photography Series | Missing | Converts wildlife subject demand into production readiness |
| 24 | Climate Stewardship Classroom Series | Missing | Adds mission-aligned educational value |
| 25 | Global Freedom Movements Poster Series | Missing | Adds civic/history depth beyond U.S. memory |

## Portfolio score rationale

The portfolio receives **84 / 100** because it is commercially viable and
well-structured for validation, but not yet globally balanced enough for a
stronger institutional portfolio score.

**Score contributors**

- Strong visual/product-market fit: +18 / 20
- Strong source-class clarity: +16 / 20
- Strong educational value: +18 / 20
- Moderate geographic/source balance: +14 / 20
- Moderate rights-readiness: +18 / 20

**Primary deductions**

- Overweight U.S./U.K./Netherlands source material.
- Overweight UNESCO tourism icons.
- Overweight mammals within species coverage.
- Underweight non-Western maps, Indigenous heritage, African cultural heritage,
  plant/ecosystem biodiversity, and rights-cleared wildlife image assets.
- Some high-demand subjects still require item-level rights clearance.

## Recommended next portfolio-only actions

These are implementation/data curation actions only and do not require
architecture, governance, agent, or ADR changes:

1. Add missing flagship candidates to a future portfolio data revision.
2. Add item-level rights-readiness markers before production planning.
3. Split wildlife subjects into rights-cleared image assets versus subject
   demand candidates.
4. Add region tags for portfolio balancing.
5. Add education-level tags for card sets and classroom products.
6. Add product-readiness tiers: immediate, needs image sourcing, needs editorial
   packaging, needs sensitivity review.
7. Expand non-Western public-domain art/map candidates.
8. Build a separate "underrepresented but high-mission-value" watchlist.

## Audit conclusion

RC9 is a strong commercial validation portfolio with clear product potential.
It is ready for validation as a prototype, but should not be treated as a final
global asset canon. The highest-value next improvement is better geographic,
cultural, species, and rights-readiness balance while preserving the frozen
Architecture v1.0 boundary under ADR-011.
