# Language Observatory Agent

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Status** | Canonical |
| **Authority** | Open Grace Architecture Office |
| **Date** | 2026-06-22 |
| **Capability** | Observatories — Language ([03-canonical-architecture.md](03-canonical-architecture.md), §5.5) |
| **Phase** | Observatories ([06-build-roadmap.md](06-build-roadmap.md), Phase 15) |

## Document Map

| Document | Purpose |
|----------|---------|
| [01-mission.md](01-mission.md) | Mission, charter, and constitutional relationship |
| [02-reference-models.md](02-reference-models.md) | Institutional reference models informing design |
| [03-canonical-architecture.md](03-canonical-architecture.md) | Canonical 100-year logical architecture |
| [04-system-diagram.md](04-system-diagram.md) | Canonical system diagram |
| [05-physical-architecture.md](05-physical-architecture.md) | Physical and geographic architecture |
| [06-build-roadmap.md](06-build-roadmap.md) | Implementation roadmap and founder build order |
| [07-reference-standards.md](07-reference-standards.md) | Standards, protocols, and interoperability |
| [08-decision-record.md](08-decision-record.md) | Architecture decision records |
| [09-source-discovery-agent.md](09-source-discovery-agent.md) | Source Discovery Agent specification |
| [10-metadata-agent.md](10-metadata-agent.md) | Metadata Agent specification |
| [11-preservation-agent.md](11-preservation-agent.md) | Preservation Agent specification |
| [12-knowledge-graph-agent.md](12-knowledge-graph-agent.md) | Knowledge Graph Agent specification |
| [13-quality-review-agent.md](13-quality-review-agent.md) | Quality Review Agent specification |
| [14-translation-agent.md](14-translation-agent.md) | Translation Agent specification |
| [15-education-agent.md](15-education-agent.md) | Education Agent specification |
| [16-climate-observatory-agent.md](16-climate-observatory-agent.md) | Climate Observatory Agent specification |
| [17-language-observatory-agent.md](17-language-observatory-agent.md) | Language Observatory Agent specification |

---

## 1. Purpose

The **Language Observatory Agent** automates the Language Observatory within the Observatory Network ([03-canonical-architecture.md](03-canonical-architecture.md), §5.5). It tracks endangered languages and revitalization programs over time; ingests vitality signals from partner feeds and public datasets; and emits **Vitality Observations** and **Revitalization Program Records** (JSON-LD) for language-steward and curator approval before longitudinal data enters the Knowledge Graph, Research Fabric, or public observatory dashboards.

The agent does not assert speaker counts or vitality status as canonical fact without review, publish community-sensitive linguistic data without consent gates, or replace language-authority judgments with machine classifications. It monitors, correlates, and proposes; language stewards, community authorities, and curators approve.

---

## 2. Responsibilities

| Responsibility | Description |
|----------------|-------------|
| **Track endangered languages** | Monitor ISO 639-3 language entities for vitality decline, speaker-population trends, intergenerational transmission status, geographic contraction, and documentation gaps; correlate signals from UNESCO, Ethnologue, Glottolog, and partner covenant feeds; emit time-series Vitality Observations linked to graph language entities |
| **Track revitalization programs** | Discover and monitor language nests, immersion schools, documentation initiatives, orthography standardization efforts, media-in-language projects, and policy programs; link programs to language entities, places, and steward organizations; emit Revitalization Program Records with outcome indicators and funding or governance metadata where available |

---

## 3. Reference Models

The agent synthesizes patterns from three primary reference models ([02-reference-models.md](02-reference-models.md)):

| Model | Pattern Applied | Agent Behavior |
|-------|-----------------|----------------|
| **UNESCO** | Linguistic diversity mandate, Atlas of the World's Languages in Danger, intangible heritage registers, state-party reporting on endangered languages | Ingest UNESCO language-vitality classifications and revitalization initiative metadata; align language entities with UNESCO vocabulary; surface languages crossing vitality thresholds for steward alert |
| **Wikimedia** | Wikidata language items, multilingual community governance, open linguistic datasets with contributor attribution | Use Wikidata language and writing-system items as reconciliation hints (not canonical assertions); accept community-contributed vitality corrections through covenant-governed submission workflows |
| **GBIF** | Federated occurrence monitoring, longitudinal trend dashboards, open data packages with citation metadata | Apply observatory feed patterns to language vitality time series; publish Research Registry data packages with DOI citation metadata; compute trend deltas and anomaly alerts analogous to species occurrence monitoring |

Supporting standards alignment follows [07-reference-standards.md](07-reference-standards.md): ISO 639-3, BCP 47, ISO 15924, GeoJSON, JSON-LD, EML.

---

## 4. Position in Architecture

```
External feeds (UNESCO, Ethnologue, Glottolog, partner covenants, community submissions)
        ↓
Source Registry + Observatory feed catalog
        ↓
Language Observatory Agent
        ↓
Vitality Observations + Revitalization Program Records (JSON-LD) — candidate, pending steward approval
        ↓
Approved observatory time series written to Knowledge Graph + Research Registry
        ↓
Observatory dashboards, alerts, Education datasets, Translation Fabric locale prioritization
```

The agent operates in the **Observatory Network** subgraph of the Experience Plane ([04-system-diagram.md](04-system-diagram.md), §2). All outputs pass through the AI Fabric governance chain before affecting canonical systems ([04-system-diagram.md](04-system-diagram.md), §2.2).

**Upstream inputs:** Language entities and place relationships from the Knowledge Graph ([12-knowledge-graph-agent.md](12-knowledge-graph-agent.md)), discovery of language data sources from the Source Discovery Agent ([09-source-discovery-agent.md](09-source-discovery-agent.md)), ISO 639-3 and BCP 47 language tags from the Metadata Agent ([10-metadata-agent.md](10-metadata-agent.md)), translation locale coverage from the Translation Agent ([14-translation-agent.md](14-translation-agent.md)).

**Downstream consumers:** Observatory dashboards (public and researcher views), Research Fabric (longitudinal datasets), Education Agent (classroom-safe vitality datasets), Translation Fabric (endangered-language locale prioritization), Community platform (revitalization program contribution loop).

---

## 5. Tracking Targets

### 5.1 Endangered Languages

| Attribute | Specification |
|-----------|---------------|
| **Sources** | UNESCO Atlas of the World's Languages in Danger, Ethnologue vitality status, Glottolog language inventory, national census language tables (where openly licensed), partner covenant vitality feeds, community steward submissions |
| **Processing pattern** | Language entity resolution (ISO 639-3) → vitality signal ingestion → EGIDS or equivalent scale normalization → trend computation → threshold crossing detection → observation emission |
| **Output entities** | Vitality Observations with timestamped status, speaker-count estimates (with confidence tier), intergenerational transmission indicator, geographic extent, and documentation-coverage score |
| **Standards** | ISO 639-3 language identification; BCP 47 for locale variants; GeoJSON for geographic extent; JSON-LD observatory record schema ([07-reference-standards.md](07-reference-standards.md)) |

### 5.2 Revitalization Programs

| Attribute | Specification |
|-----------|---------------|
| **Sources** | UNESCO revitalization initiative registries, national indigenous-language policy databases, immersion-school and language-nest directories, documentation-grant programs, community-submitted program descriptions, partner institution feeds |
| **Processing pattern** | Program discovery → language and place entity linking → outcome-indicator extraction → governance and consent gate → program record emission |
| **Output entities** | Revitalization Program Records with program type, target language(s), geography, start date, steward organization, activity categories (education, media, documentation, policy), and reported outcome indicators |
| **Standards** | SKOS program-type vocabulary; ORCID/ISNI for steward organizations; GeoJSON for service areas; PREMIS-aligned provenance for feed lineage ([07-reference-standards.md](07-reference-standards.md)) |

### 5.3 Community-Governed and Sensitive Data

| Attribute | Specification |
|-----------|---------------|
| **Sources** | Covenant-governed community feeds, language-steward corrections, restricted speaker-population data under partner agreements |
| **Processing pattern** | Consent gate → attribution capture → sensitivity classification → steward review queue → approved-only observatory write |
| **Output entities** | Community-attributed vitality corrections and program updates with language-steward approval record |
| **Standards** | UNDRIP-aligned consent and attribution metadata; tiered access labels for restricted vitality data ([07-reference-standards.md](07-reference-standards.md)) |

---

## 6. Vitality Metrics Framework

The agent maintains a normalized vitality metrics registry; language stewards approve canonical status classifications.

### 6.1 Vitality Indicators

| Indicator | Description |
|-----------|-------------|
| **Intergenerational transmission** | Whether the language is acquired by children in the home or community setting |
| **Speaker population** | Estimated fluent and partial speaker counts with confidence tier and source attribution |
| **Domain contraction** | Reduction in functional domains (home, education, media, government, ceremony) |
| **Geographic extent** | Contracting or expanding territorial use; linkage to place entities |
| **Documentation coverage** | Presence of grammars, dictionaries, corpora, and audiovisual archives in institutional memory |
| **Orthography and standardization** | Writing-system adoption status (ISO 15924); community orthography authority |
| **Digital vitality** | Web, social, and broadcast presence in the language (where ethically collectible) |

### 6.2 Vitality Scale Normalization

External classifications are mapped to an institutional vitality scale without erasing source taxonomy:

| Field | Requirement |
|-------|-------------|
| **Language URI** | Stable ISO 639-3–linked graph entity identifier |
| **Observation date** | ISO 8601 timestamp for the measurement event |
| **Source classification** | Original status from feed (e.g., UNESCO degree of endangerment, Ethnologue EGIDS) |
| **Normalized tier** | Institutional comparable tier for dashboard aggregation |
| **Confidence tier** | `authoritative`, `partner-reported`, `machine-inferred`, or `community-submitted` |
| **Provenance** | Feed URI, harvest event, steward approval when applicable |
| **Review requirement** | Auto-approvable (unchanged repeat observation), standard steward review, or sensitive-community queue |

Machine-inferred vitality changes route to language stewards; the agent does not downgrade a language's status without human approval.

---

## 7. Outputs

### 7.1 Vitality Observations

Each candidate vitality measurement is emitted as a **Vitality Observation** with:

| Field | Requirement |
|-------|-------------|
| **Language entity** | ISO 639-3–linked graph URI |
| **Observation date** | Timestamp of measurement or report |
| **Vitality indicators** | Structured indicator values per §6.1 |
| **Source classification** | Original external status with source URI |
| **Normalized tier** | Comparable institutional vitality tier |
| **Geographic extent** | GeoJSON polygon or place-entity references when applicable |
| **Confidence tier** | Data-quality and authority classification |
| **Attribution** | Source organization, contributor, and harvest event |
| **Review requirement** | Auto-approvable, standard review, or community-sensitive queue |

Vitality Observations are **candidates** until a language steward or curator approves them through the human-approval gate.

### 7.2 Revitalization Program Records

Each candidate program is emitted as a **Revitalization Program Record** with:

| Field | Requirement |
|-------|-------------|
| **Program identifier** | Stable URI for the program entity |
| **Target language(s)** | ISO 639-3–linked language entity URIs |
| **Program type** | SKOS-typed category (immersion, nest, documentation, media, policy, orthography, etc.) |
| **Geography** | Place entities and GeoJSON service area |
| **Steward organization** | ORCID/ISNI or institutional URI |
| **Timeline** | Start date, end date (if concluded), milestone events |
| **Outcome indicators** | Learner counts, publication outputs, broadcast hours, policy adoption — with confidence tier |
| **Consent and access** | Public, researcher, or restricted-community tier |
| **Review requirement** | Auto-approvable, standard review, or community-sensitive queue |

### 7.3 Observatory Reports and Alerts

Each processing run emits:

- **Vitality trend report** — languages with declining, stable, or improving trajectories over configurable windows
- **Threshold alerts** — languages crossing endangerment boundaries or losing intergenerational transmission
- **Revitalization coverage report** — programs active per language, geography, and program type; gaps where endangered languages lack documented programs
- **Research Registry packages** — citation-ready longitudinal datasets with DOI metadata for approved time series

---

## 8. AI Fabric Governance

| Gate | Requirement |
|------|-------------|
| **Agent Registry** | Agent version, supported vitality scales, feed connectors, sensitivity routing rules, and community-consent policy parameters registered before production runs |
| **Benchmarks** | Entity-resolution accuracy (language matching), false-alert rate on threshold crossings, steward approval turnaround, community-consent compliance rate |
| **Evaluations** | Periodic review against Phase 15 Observatories success criteria |
| **Safety Reviews** | Verify agent does not publish restricted speaker data without consent, assert vitality downgrades without review, or misattribute revitalization outcomes to communities without steward approval |
| **Human Approval** | Language stewards and curators approve Vitality Observations and Revitalization Program Records before canonical observatory writes; sensitive-community data always requires review |

**Council assignment:** Research Council (vitality metrics, feed partnerships, trend methodology) and Implementation Council (observatory pipelines, dashboard integration). Community Council advises on consent, attribution, and sensitive-data policy for indigenous and endangered languages.

---

## 9. Phase Alignment

| Phase | Agent Scope |
|-------|-------------|
| **Knowledge Graph (Phase 5)** | Readiness only: ISO 639-3 language entity inventory; place-language relationship baseline |
| **Translation Fabric (Phase 9)** | Consume locale coverage gaps to inform endangered-language translation prioritization; do not duplicate translation workflows |
| **Research Fabric (Phase 8)** | Publish approved vitality time series as Research Registry data packages |
| **Observatories (Phase 15)** | Full endangered-language tracking; revitalization program monitoring; public and researcher dashboards; alert system |
| **Community (Phase 14)** | Community revitalization program submissions; steward correction workflows; covenant-governed vitality updates |

---

## 10. Success Criteria

Aligned with Observatories phase completion criteria ([06-build-roadmap.md](06-build-roadmap.md)):

- Language Observatory live with public and researcher views
- ≥ 1,000 endangered languages tracked with baseline vitality observations
- ≥ 100 revitalization programs linked to language entities with steward-approved records
- Longitudinal vitality time series operational for ≥ 50 languages with ≥ 2 observation points
- Threshold alert system operational for vitality boundary crossings
- Community-consent workflow documented and enforced for sensitive speaker-population data
- End-to-end demonstration: external feed → language entity resolution → Vitality Observation → steward approval → graph time series → dashboard trend → Research Registry citation package

---

## 11. Constraints

- **No canonical vitality writes without approval.** The agent observes and proposes; language stewards and curators approve.
- **Community consent required.** Indigenous and community-governed languages follow covenant-defined consent before publication of sensitive vitality data ([14-translation-agent.md](14-translation-agent.md), §5.4).
- **Source classifications preserved.** External taxonomies (UNESCO, EGIDS) are retained alongside normalized tiers; the agent does not collapse source authority into a single opaque score.
- **Wikidata and Ethnologue are hints, not assertions.** External language metadata informs reconciliation; canonical vitality status requires institutional approval.
- **Provenance mandatory.** Every observation traces to source feed, harvest event, and approving steward ([03-canonical-architecture.md](03-canonical-architecture.md), Provenance).
- **Translation Fabric boundary respected.** The agent monitors language vitality; the Translation Agent ([14-translation-agent.md](14-translation-agent.md)) manages localized content. Vitality signals may inform locale prioritization but do not bypass translation review gates.
- **Free access preserved.** Public observatory views must not gate access to underlying canonical public memory ([01-mission.md](01-mission.md)).
