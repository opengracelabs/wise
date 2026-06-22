# RC11 Portfolio Gap Analysis

| Field | Value |
|-------|-------|
| **Status** | Implementation analysis (non-governance) |
| **Date** | 2026-06-22 |
| **Scope** | Coverage gaps in `data/portfolio/top_100_global_assets.json` (+ collections/series) and a recommended Top 50 to add next |
| **Constraints** | Does not modify Architecture v1.0, governance, ADRs, or agents (ADR-011) |

> **Note on inputs.** The brief lists `docs/implementation/rc9-portfolio-audit.md` for review; that file does not exist in the repository. This analysis is therefore performed directly against the RC9 data files (`data/portfolio/top_100_*.json`) and the RC9 plan/product docs.

---

## 1. Current coverage (top 100 global assets)

| Dimension | Distribution |
|-----------|--------------|
| Category | species 25, artwork 24, heritage_site 23, natural_site 14, map 8, manuscript 6 |
| Continent (approx.) | Europe ~40, Asia ~18, North America ~13, Africa ~9, South America ~5, Oceania ~3, transnational/"Oceans/Arctic" ~12 |

**Structural skew.** The corpus is **Euro- and East-Asia-centric**, art-heavy, and thin on Sub-Saharan Africa, the Middle East/West Asia, Central Asia, South Asia (beyond the Taj Mahal), Oceania/Pacific, and Indigenous cultures worldwide. These gaps matter both for **mission breadth** (a global memory of nature and culture) and **commercial reach** (regional markets and under-served collector niches).

---

## 2. Missing UNESCO / iconic sites

Currently present: Taj Mahal, Great Wall, Machu Picchu, Giza, Colosseum, Petra, Angkor Wat, Acropolis, Chichen Itza, Stonehenge, Christ the Redeemer, Sagrada Familia, Alhambra, Mont-Saint-Michel, Forbidden City, Terracotta Army, Hagia Sophia, Cappadocia, Pompeii, Borobudur, Bagan, Moai, Kyoto temples.

**Notable absences (high-recognition):**
- **Oceania:** Sydney Opera House, Uluru-Kata Tjuta.
- **Americas:** Statue of Liberty, Teotihuacan, Nazca Lines, Mesa Verde / Cliff Palace, Chichen Itza is present but Tikal/Tulum absent, Yosemite (natural).
- **Europe:** Notre-Dame de Paris, Saint Basil's Cathedral / Moscow Kremlin, Neuschwanstein, Venice & its Lagoon, Tower of London.
- **Middle East / West Asia:** Persepolis (Iran), Ishtar Gate / Babylon (Iraq), Palmyra (Syria), Ephesus (Turkey), Göbekli Tepe (Turkey).
- **Sub-Saharan Africa:** Great Zimbabwe, Lalibela rock churches (Ethiopia), Timbuktu (Mali), Pyramids of Meroe (Sudan), Ngorongoro/Serengeti is present (natural).
- **Central / South Asia:** Registan, Samarkand (Uzbekistan); Ajanta & Ellora Caves, Khajuraho, Varanasi (India).
- **Southeast Asia:** Ha Long Bay (Vietnam), Ayutthaya (Thailand).

## 3. Missing species

Present: 25 flagship taxa (big cats, panda, elephant, whales, bears, penguin, etc.).

**Gaps across taxa and biomes:**
- **African megafauna:** Giraffe, Hippopotamus, Black/White Rhinoceros, Leopard (distinct from snow leopard), Chimpanzee, Zebra.
- **Birds:** Scarlet Macaw, Toco Toucan, Greater Flamingo, Indian Peafowl, Golden Eagle, Snowy Owl, Atlantic Puffin.
- **Marine:** Orca (Killer Whale), Bottlenose Dolphin, Manta Ray, Common Octopus, Seahorse, Coral (reef-building).
- **Reptiles/amphibians/invertebrates:** Galápagos Giant Tortoise, Panther Chameleon, Poison Dart Frog, Honeybee, Pangolin (most-trafficked mammal).
- **Oceania / neotropics / polar:** Red Kangaroo, Platypus, Quokka, Three-toed Sloth, Capybara, Reindeer/Caribou, Arctic Fox, Narwhal.

## 4. Missing maps

Present (8): Waldseemüller 1507, Mercator 1569, Blaeu Atlas Maior, Tabula Rogeriana, Hereford Mappa Mundi, Carta Marina 1539, Uranometria 1603, Lewis & Clark.

**Gaps in the cartographic canon:**
- Babylonian Map of the World (Imago Mundi) — earliest known world map.
- Ptolemy's *Geographia* (Renaissance reconstruction).
- Catalan Atlas (1375), Fra Mauro Map (c.1450).
- Cantino Planisphere (1502), Piri Reis Map (1513).
- Ortelius *Theatrum Orbis Terrarum* (1570) — first modern atlas.
- Hevelius *Selenographia* (1647) — first detailed Moon map.

## 5. Missing cultures

Under-represented or absent cultural traditions:
- **African:** Benin Bronzes (Nigeria), Nok terracotta, Aksumite, Malian/Songhai.
- **Mesopotamian / Near Eastern:** Sumer (Standard of Ur), Babylon (Ishtar Gate), Assyrian reliefs.
- **Persian / Central Asian:** Achaemenid (Persepolis), Timurid (Samarkand).
- **Indigenous Oceania & Australia:** Aboriginal rock art (Kakadu), Māori carving, Polynesian navigation.
- **Indigenous Americas:** Ancestral Puebloan, Plains nations, Andean pre-Inca (Nazca, Moche, Tiwanaku).
- **Norse / Celtic:** Viking ship burials (Oseberg), Celtic metalwork (Book of Kells present).
- **South Asian sacred art:** Hindu/Buddhist sculpture beyond Angkor/Borobudur.

## 6. Missing regions

| Region | Current state | Priority |
|--------|---------------|----------|
| Sub-Saharan Africa | Few natural sites; **no Sub-Saharan heritage site** | **High** |
| Middle East / West Asia | Petra + 2 Turkey only; no Iran/Iraq/Levant | **High** |
| Central Asia | None | **High** |
| South Asia | Taj Mahal only | **High** |
| Oceania / Pacific | Great Barrier Reef + Koala only | Medium-High |
| Russia / Eastern Europe | None | Medium |
| Caribbean / Central America (indigenous) | Chichen Itza only | Medium |
| Arctic Indigenous | None (species only) | Medium |

---

## 7. Recommended Top 50 assets to add next

Prioritized to close the gaps above while keeping global recognition and product potential high. (`region` = gap addressed; `pd_readiness` flags whether public-domain imagery is straightforward.)

### Heritage & cultural sites (20)
| # | Asset | Country/Region | Gap |
|---|-------|----------------|-----|
| 1 | Sydney Opera House | Australia | Oceania |
| 2 | Statue of Liberty | USA | Americas icon |
| 3 | Persepolis | Iran | West Asia / Persian |
| 4 | Uluru-Kata Tjuta | Australia | Oceania / Indigenous |
| 5 | Great Zimbabwe | Zimbabwe | Sub-Saharan Africa |
| 6 | Rock-Hewn Churches, Lalibela | Ethiopia | Sub-Saharan Africa |
| 7 | Timbuktu | Mali | Sub-Saharan Africa |
| 8 | Pyramids of Meroë | Sudan | Nubian Africa |
| 9 | Göbekli Tepe | Turkey | Neolithic Near East |
| 10 | Ephesus | Turkey | Classical West Asia |
| 11 | Registan, Samarkand | Uzbekistan | Central Asia |
| 12 | Ajanta & Ellora Caves | India | South Asia |
| 13 | Teotihuacan | Mexico | Mesoamerica |
| 14 | Nazca Lines | Peru | Andean pre-Inca |
| 15 | Mesa Verde Cliff Palace | USA | Indigenous N. America |
| 16 | Saint Basil's Cathedral | Russia | Eastern Europe |
| 17 | Notre-Dame de Paris | France | European icon |
| 18 | Ha Long Bay | Vietnam | Southeast Asia |
| 19 | Newgrange (Brú na Bóinne) | Ireland | Neolithic Europe |
| 20 | Venice & its Lagoon | Italy | European icon |

### Species (15)
| # | Asset | Region | Gap |
|---|-------|--------|-----|
| 21 | Giraffe | Africa | African megafauna |
| 22 | Black Rhinoceros | Africa | Endangered megafauna |
| 23 | Leopard (Panthera pardus) | Africa/Asia | Big cat |
| 24 | Chimpanzee | Africa | Great ape |
| 25 | Orca (Killer Whale) | Oceans | Marine apex |
| 26 | Galápagos Giant Tortoise | Ecuador | Evolution icon |
| 27 | Scarlet Macaw | Americas | Neotropical bird |
| 28 | Greater Flamingo | Africa/Americas | Wetland bird |
| 29 | Red Kangaroo | Australia | Oceania |
| 30 | Platypus | Australia | Oceania monotreme |
| 31 | Giant Pangolin | Africa/Asia | Most-trafficked mammal |
| 32 | Three-toed Sloth | South America | Neotropics |
| 33 | Reindeer (Caribou) | Arctic | Arctic / Indigenous |
| 34 | Narwhal | Arctic | Marine Arctic |
| 35 | Indian Peafowl | South Asia | South Asia bird |

### Maps & manuscripts (8)
| # | Asset | Source | Gap |
|---|-------|--------|-----|
| 36 | Babylonian Map of the World (Imago Mundi) | British Museum (PD) | Earliest world map |
| 37 | Ptolemy's Geographia | LoC / Europeana (PD) | Classical cartography |
| 38 | Catalan Atlas (1375) | BnF (PD) | Medieval cartography |
| 39 | Cantino Planisphere (1502) | Europeana (PD) | Age of Discovery |
| 40 | Piri Reis Map (1513) | PD | Ottoman cartography |
| 41 | Ortelius Theatrum Orbis Terrarum (1570) | LoC (PD) | First modern atlas |
| 42 | Hevelius Selenographia (1647) | PD | First Moon map |
| 43 | Diamond Sutra (Dunhuang) | British Library (PD) | Earliest printed book |

### Cultural artworks & artefacts (7)
| # | Asset | Culture/Region | Gap |
|---|-------|----------------|-----|
| 44 | Benin Bronzes | Nigeria | West African art |
| 45 | Ishtar Gate of Babylon | Iraq | Mesopotamian |
| 46 | Standard of Ur | Iraq (Sumer) | Mesopotamian |
| 47 | Oseberg Viking Ship | Norway | Norse |
| 48 | Kakadu Aboriginal Rock Art | Australia | Indigenous Oceania |
| 49 | Nok Terracotta | Nigeria | Ancient African |
| 50 | Moche Portrait Vessels | Peru | Andean pre-Inca |

---

## 8. Sequencing

1. **Wave A (regional balance):** #1-20 sites + #44-50 cultural artefacts — close the Africa / West Asia / Central Asia / Oceania / Indigenous gaps that most affect mission credibility.
2. **Wave B (biodiversity breadth):** #21-35 species — broaden taxa and biomes for the conservation and education lines.
3. **Wave C (cartographic canon):** #36-43 maps/manuscripts — high public-domain readiness, fast to productize.

Each addition must pass the standard pipeline (discovery → preservation → metadata → rights/quality) before appearing publicly or as a sellable product; public-domain imagery (maps, manuscripts, museum open-access artworks) is fastest to clear.

---

*Implementation analysis. Does not modify Architecture v1.0, governance, ADRs, or agents (ADR-011). Inputs: `data/portfolio/top_100_*.json`, `docs/implementation/rc9-public-launch-plan.md`.*
