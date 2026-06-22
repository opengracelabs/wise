# RC13 Global Coverage Report

**Status:** Implementation coverage artifact  
**Authority:** Architecture v1.0, frozen by ADR-011  
**Scope:** Expanded portfolio coverage analysis only  

RC13 expands global representation in the portfolio data while preserving the
Architecture v1.0 freeze. It does not modify governance, architecture, agents,
ADRs, registries, schemas, or canonical data stores.

## Frozen-architecture boundary

- Architecture v1.0 remains frozen.
- No governance changes are proposed or made.
- No architecture changes are proposed or made.
- No agents are proposed or added.
- No ADRs are proposed or added.
- RC13 outputs are implementation data/report artifacts only.

## RC13 data outputs

| File | Count | Purpose |
|------|------:|---------|
| `data/portfolio/expansion_candidates.json` | 100 | Representation-focused expansion candidates |
| `data/portfolio/top_200_global_assets.json` | 200 | Expanded asset portfolio |
| `data/portfolio/top_200_collections.json` | 200 | Expanded collection portfolio |
| `data/portfolio/top_200_series.json` | 200 | Expanded series portfolio |

## Regional representation

RC13 focuses on underrepresented regions identified in the RC9 audit.

| Region / focus | Added coverage |
|----------------|----------------|
| Sub-Saharan Africa | Great Zimbabwe, Lalibela, Timbuktu, Aksum, Tsodilo, Okavango, Virunga, Bwindi, Namib, Lake Malawi, baobab, African wild dog, shoebill, Ethiopian wolf, Swahili Coast, textile and object contexts |
| West Asia | Persepolis, Isfahan, Gobekli Tepe, Cappadocia, Aleppo, Baalbek, Hegra, Socotra, Arabian oryx, Piri Reis map, Tabula Rogeriana, Islamic geometry, Arabic astronomy manuscripts, Persian miniatures |
| Central Asia | Samarkand, Bukhara, Khiva, Silk Roads corridor, Tamgaly, Pamirs, snow leopard maps, saiga, Bactrian camel, Aral Sea climate maps, steppe and nomadic culture contexts |
| South Asia | Borobudur, Ajanta, Ellora, Hampi, Sigiriya, Kathmandu Valley, Lumbini, Mohenjo-daro, Sundarbans, Bengal tiger, Ganges river dolphin, Himalayan monal, Mughal art, Indian Ocean maps |
| Oceania | Kakadu, Shark Bay, Lord Howe, Te Wahipounamu, Pacific navigation, Marshall Islands stick charts, Moai context, kakapo, kiwi, kea, Tasmanian devil, Coral Triangle, Pacific atoll climate maps |
| Indigenous cultures | Mesa Verde, Chaco, Cahokia, Poverty Point, Head-Smashed-In Buffalo Jump, Writing-on-Stone, Teotihuacan, Palenque, Nazca, Chan Chan, Tikal, Amazon biodiversity, Andean condor, quipu, Arctic Inuit knowledge context |

## Cultural representation

RC13 expands cultural coverage beyond the initial concentration in UNESCO travel
icons and Western public-domain art.

### Improved cultural areas

- African kingdoms, cities, manuscripts, textiles, and rock art.
- Islamic architecture, geometry, manuscripts, and maps.
- Silk Roads and Central Asian urban heritage.
- South Asian cave temples, sacred sites, Mughal art, and trade maps.
- Pacific navigation, Maori and Aboriginal cultural contexts.
- Indigenous North American, Mesoamerican, Andean, Amazonian, and Arctic contexts.

### Cultural caution

Several candidates are marked `sensitivity_review_required` or
`needs_partner_clearance`. These candidates improve representation in the
portfolio prototype but should not be treated as production-ready without
appropriate cultural, rights, and partner review.

## Biodiversity representation

RC13 reduces mammal-only concentration by adding:

- plants and ecosystems: baobab forests, cedar of Lebanon, Amazon rainforest,
  Coral Triangle, Sundarbans, Okavango, Namib, Lake Malawi;
- birds: shoebill, Indian peafowl, Himalayan monal, kiwi, kea,
  birds-of-paradise;
- marine and freshwater biodiversity: Ganges river dolphin, coral reef and
  reef-climate candidates;
- threatened mammals beyond existing icons: African wild dog, Ethiopian wolf,
  saiga antelope, Bactrian camel, kakapo-adjacent island conservation contexts.

## Indigenous representation

RC13 adds Indigenous representation as a portfolio discovery and education layer,
not as an unrestricted product claim.

### Added Indigenous contexts

- Tsodilo rock art.
- Tamgaly petroglyphs.
- Polynesian navigation star compass.
- Marshall Islands stick chart.
- Aboriginal rock art context.
- Maori carving pattern study.
- Mesa Verde, Chaco, Cahokia, Poverty Point.
- Head-Smashed-In Buffalo Jump.
- Writing-on-Stone / Aisinai'pi.
- Nazca, Chan Chan, Tikal, Teotihuacan, Palenque.
- Quipu and Andean knowledge context.
- Arctic Inuit knowledge context.

### Safeguards in data

The expanded portfolio uses readiness labels such as:

- `sensitivity_review_required`,
- `needs_partner_clearance`,
- `public_domain_item_review`,
- `public_domain_data_needs_design`.

These labels preserve caution while allowing representation gaps to be visible.

## Public-domain readiness

RC13 adds public-domain readiness metadata to expanded asset, collection, and
series files.

| Readiness label | Meaning |
|-----------------|---------|
| `public_domain_ready` | Existing source class is generally public-domain/open for validation |
| `open_access_ready` | Open-access institutional source, item-level checks still recommended |
| `public_domain_likely` | Candidate likely has public-domain pathways |
| `public_domain_item_review` | Item-level public-domain verification required |
| `public_domain_data_needs_design` | Public data may support original map/design work |
| `image_rights_required` | Site/subject recognition exists but imagery must be cleared |
| `needs_image_clearance` | Wildlife or ecosystem image rights must be sourced |
| `needs_partner_clearance` | Cultural partner or institution review needed |
| `sensitivity_review_required` | Cultural sensitivity review required before use |

## Remaining gaps

RC13 improves representation but does not fully close all gaps.

1. Indigenous content still requires deeper partner-led review before production.
2. African cultural object representation needs rights-safe institutional sources.
3. West Asian and South Asian manuscript/art items need item-level provenance and
   rights review.
4. Wildlife and ecosystem candidates need rights-cleared images.
5. Plant, fungi, insect, amphibian, and freshwater species remain underweighted.
6. Climate maps require careful data sourcing and design attribution.
7. Public-domain readiness is now visible, but many items are not production-ready.
8. The expanded portfolio is still a prototype, not a canonical global canon.

## Coverage conclusion

RC13 materially improves global representation by adding focused candidates for
Sub-Saharan Africa, West Asia, Central Asia, South Asia, Oceania, and Indigenous
cultures. It raises the portfolio from a commercially strong but concentrated
RC9 baseline toward a more balanced RC13 portfolio suitable for future
validation. It follows ADR-011 and introduces no architecture, governance, agent,
or ADR changes.
