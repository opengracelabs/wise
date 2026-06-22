# RC13 Global Representation Report

| Field | Value |
|-------|-------|
| **Status** | Implementation report (non-governance) |
| **Date** | 2026-06-22 |
| **Scope** | Geographic, cultural, biodiversity, and Indigenous representation of the RC13 portfolio (200 assets, 200 collections, 200 series) |
| **Constraints** | Does not modify Architecture v1.0, governance, ADRs, or agents (ADR-011) |

## Summary

RC13 expands the RC9 portfolio from 100 to 200 assets, adding **100 region-balanced assets** (`data/portfolio/expansion_candidates.json`) that close the gaps identified in [rc11-gap-analysis.md](rc11-gap-analysis.md). Europe's share of assets falls from **41% to 24%**; geographic evenness rises from **76.7 to 86.8** (0-100 entropy), and a balanced flagship tier now scores **GRI 93.0** (see [rc13-portfolio-rescore.md](rc13-portfolio-rescore.md)).

Candidate distribution across the six target regions (plus support categories):

| Target region | Candidates |
|---------------|-----------:|
| Sub-Saharan Africa | 16 |
| West Asia | 16 |
| South Asia | 14 |
| Indigenous Cultures | 12 |
| Oceania | 11 |
| Central Asia | 8 |
| Biodiversity (cross-cutting) | 12 |
| Cartography (cross-cutting) | 6 |
| Other global icons | 5 |

---

## 1. Regional coverage

| Region | RC9 | RC13 | Change | Representative additions |
|--------|----:|-----:|--------|--------------------------|
| Europe | 41 | 48 | share 41%→24% | (rebalanced by dilution) |
| Africa | 8 | 26 | ×3.25 | Great Zimbabwe, Lalibela, Meroë, Ngorongoro, Okavango |
| West Asia | 3 | 19 | ×6.3 | Persepolis, Göbekli Tepe, Ephesus, Dome of the Rock, Palmyra |
| N. America | 10 | 18 | ×1.8 | Statue of Liberty, Yosemite, Mesa Verde, Chaco Canyon |
| South Asia | 2 | 16 | ×8 | Mount Everest, Varanasi, Ajanta/Ellora, Paro Taktsang, Sigiriya |
| Oceania | 2 | 15 | ×7.5 | Sydney Opera House, Uluru, Milford Sound, Aoraki |
| S. America | 7 | 14 | ×2 | Nazca Lines, Tiwanaku, Caral, Torres del Paine |
| E. Asia | 8 | 9 | +1 | Diamond Sutra |
| Central Asia | 1 | 9 | ×9 | Registan/Samarkand, Bukhara, Khiva, Bamiyan, Tian Shan |
| SE. Asia | 5 | 6 | +1 | Ha Long Bay |
| Polar / Oceans | 6 | 11 | +5 | Narwhal, Reindeer, Orca, Manta Ray, Coral |

**Verdict:** the four highest-priority gaps from RC11 (Sub-Saharan Africa, West Asia, Central Asia, South Asia) are now materially represented; Oceania and the Americas' Indigenous heritage are substantially strengthened.

## 2. Cultural coverage

Newly represented or strengthened cultural traditions (assets + collections + series):

- **African:** Benin Bronzes, Nok terracotta, Nubian/Kush (Meroë), Ethiopian Christianity (Lalibela), Mali/Timbuktu — collections *African Kingdoms*, *Masks and Sculpture of Africa*; series *The Mali Empire and Timbuktu*, *Ancient Nubia and Kush*.
- **Mesopotamian / Near Eastern:** Ishtar Gate, Standard of Ur, Ziggurat of Ur — collection *Empires of Mesopotamia*; series *The First Cities of Mesopotamia*, *Babylon: City of Wonders*.
- **Persian / Central Asian:** Persepolis, Naqsh-e Jahan, Shahnameh folios, Registan — collections *Ancient Persia*, *Timurid Splendour*; series *The Persian Empire*, *Samarkand and the Timurids*.
- **South Asian sacred art:** Ajanta/Ellora, Khajuraho, Brihadeeswarar, Meenakshi — collection *Temples of India*; series *Buddhist India*, *The Mughal Empire*.
- **Oceanic / Aboriginal:** Kakadu rock art, Aboriginal Dreaming paintings, Māori meeting house — collection *Aboriginal Art*; series *First Australians*, *Songlines*.
- **Norse / Arctic / Sami:** Sami heritage, Inuksuk, Reindeer — series *The Sami and the Reindeer*, *Peoples of the Arctic*.
- **Cartographic traditions:** Islamic (Piri Reis, Babylonian Imago Mundi), European atlases (Ortelius, Catalan Atlas, Cantino), lunar (Hevelius) — collection *Islamic Cartography*; series *Mapping the Heavens*.

## 3. Biodiversity coverage

Species rise from **25 to 53**, broadening taxa and biomes:

| Group | Added |
|-------|-------|
| African megafauna | Giraffe, Black Rhinoceros, Hippopotamus, Chimpanzee, Leopard, Plains Zebra |
| Birds | Scarlet Macaw, Greater Flamingo, Indian Peafowl, Golden Eagle, Himalayan Monal, Kiwi |
| Marine | Orca, Manta Ray, Reef-building Coral |
| Polar | Reindeer, Narwhal |
| Reptiles / other | Galápagos Giant Tortoise, Saltwater Crocodile, Pangolin, One-horned Rhinoceros |
| Oceania / neotropics | Red Kangaroo, Platypus, Three-toed Sloth |
| Asian megafauna | Asian Elephant, Arabian Oryx, Bactrian Camel |

Collections/series add *Parrots of the World*, *Antelope of Africa*, *Sharks and Rays*, *Pangolins and Rare Mammals*, *Whales of the Southern Ocean*, and more — improving coverage of under-represented orders (birds, reptiles, marine invertebrates).

## 4. Indigenous representation

A dedicated thread (12 asset candidates + collections + series) now spans:

- **Americas:** Teotihuacan, Nazca Lines, Mesa Verde, Chaco Canyon, Cahokia, Tiwanaku, Caral, Moche portrait vessels, Haida totem poles, Inuksuk.
- **Oceania:** Uluru-Kata Tjuta (Anangu), Kakadu rock art, Aboriginal Dreaming paintings, Māori meeting house.
- **Arctic / Northern Europe:** Sami cultural heritage, Inuit Inuksuk, Reindeer herding.
- **Collections/series:** *First Nations of the Americas*, *Andean Civilizations*, *Arctic Peoples*, *Dreamtime Art*, *Pueblos of the Southwest*; *First Peoples of the Americas*, *Songlines*, *Peoples of the Arctic*.

**Guardrail:** Indigenous heritage must be presented with provenance, community attribution, and rights clearance; sensitive or restricted material is excluded until cleared. Inclusion here is a portfolio-prioritization signal, not a publication decision.

## 5. Remaining gaps

| Gap | Note | Priority |
|-----|------|----------|
| Russia / Eastern Europe | Only Saint Basil's added; Hermitage, Kremlin, Caucasus absent | Medium |
| Caribbean | Still unrepresented | Medium |
| Pacific (beyond Australia/NZ) | Only Nan Madol; Hawai'i, Rapa Nui present (Moai), Fiji/Samoa absent | Medium |
| Southeast Asia depth | Ha Long Bay added; Ayutthaya, Bagan (present), Luang Prabang thin | Medium |
| Central Africa & Sahel | Limited beyond West/East/Southern Africa | Medium |
| Modern & contemporary culture | Portfolio remains historical; 20th-21st c. design/architecture thin | Low-Medium |
| Women & non-Western artists | Art still skews Western canon (Merian present); broaden authorship | Medium |
| Intangible heritage | Music, dance, oral traditions are collection/series-only, not asset-level | Low |
| Category evenness | Heritage/species now dominate (63/53 of 200); maps/manuscripts still small (15/7) | Low |

### Recommended next wave (RC15 direction)
Add ~10-15 assets for Russia/Eastern Europe and the wider Pacific; deepen Southeast Asia and the Sahel; broaden authorship (women and non-Western artists); and grow the cartographic/manuscript tier. These keep raising geographic evenness without diluting the flagship tier.

---

## 6. Scorecard

| Dimension | RC9 | RC13 | Status |
|-----------|-----|------|--------|
| Geographic evenness (0-100) | 76.7 | 86.8 | ✅ improved |
| Europe share | 41% | 24% | ✅ rebalanced |
| Species (biodiversity) | 25 | 53 | ✅ broadened |
| Target regions represented | 1-3 each (thin) | 9-26 each | ✅ closed |
| Indigenous thread | minimal | 12 assets + collections/series | ✅ established |
| Headline representation score (GRI) | 84.0 | 93.0 (representative tier) | ✅ 90+ met |

---

*Implementation report. Does not modify Architecture v1.0, governance, ADRs, or agents (ADR-011). Data: `data/portfolio/expansion_candidates.json`, `top_200_global_assets.json`, `top_200_collections.json`, `top_200_series.json`. Per ADR-010 the portfolio is a prioritization seed and never gates canonical public memory.*
