# Biodiversity Observatory Agent

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Status** | Canonical |
| **Authority** | Open Grace Architecture Office |
| **Date** | 2026-06-22 |
| **Capability** | Observatories — Biodiversity domain ([03-canonical-architecture.md](03-canonical-architecture.md), §5.5) |
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
| [12-knowledge-graph-agent.md](12-knowledge-graph-agent.md) | Knowledge Graph Agent specification |
| [13-quality-review-agent.md](13-quality-review-agent.md) | Quality Review Agent specification |
| [14-translation-agent.md](14-translation-agent.md) | Translation Agent specification |
| [15-education-agent.md](15-education-agent.md) | Education Agent specification |
| [16-heritage-observatory-agent.md](16-heritage-observatory-agent.md) | Heritage Observatory Agent specification |
| [16-biodiversity-observatory-agent.md](16-biodiversity-observatory-agent.md) | Biodiversity Observatory Agent specification |
| [16-climate-observatory-agent.md](16-climate-observatory-agent.md) | Climate Observatory Agent specification |
| [16-tourism-observatory-agent.md](16-tourism-observatory-agent.md) | Tourism Observatory Agent specification |

---

## 1. Purpose

The **Biodiversity Observatory Agent** automates the biodiversity observatory within the Observatory Network capability ([03-canonical-architecture.md](03-canonical-architecture.md), §5.5). It tracks species populations and taxonomic changes, monitors occurrence streams for anomalies and trends, and maintains threatened-taxa watchlists with conservation-status alerts — emitting **Observatory Observation Records** (JSON-LD / GeoJSON) and **Trend Reports** for steward approval before observatory feeds enter public dashboards, Research Fabric exports, or conservation intelligence layers.

The agent does not assert conservation policy, override IUCN or national red-list authority, or publish alert thresholds without review. It monitors, correlates, and proposes; biodiversity stewards and conservation reviewers approve.

---

## 2. Responsibilities

| Responsibility | Description |
|----------------|-------------|
| **Track species** | Monitor Species Registry entities for population trend signals, taxonomic revision impacts, distribution range shifts, and cross-link integrity with GBIF backbone; compute baseline and rolling-window metrics per taxon and geography |
| **Track occurrences** | Ingest and analyze occurrence streams from GBIF synchronization, citizen science submissions, and partner feeds; detect influx anomalies, spatial clustering changes, seasonal pattern deviations, and data-quality regressions; anchor every signal to Darwin Core occurrence entities with provenance |
| **Track threatened taxa** | Maintain watchlists of taxa with IUCN Red List or national conservation-status designations; monitor status changes, occurrence decline or recovery signals, and overlap with World Heritage and protected-area geometries; emit conservation-priority alerts with confidence tiers |

---

## 3. Reference Models

The agent synthesizes patterns from three primary reference models ([02-reference-models.md](02-reference-models.md)):

| Model | Pattern Applied | Agent Behavior |
|-------|-----------------|----------------|
| **GBIF** | Federated occurrence publishing, Darwin Core interoperability, taxonomic backbone reconciliation, open science infrastructure | Consume synchronized occurrence and taxonomy feeds; compute spatiotemporal aggregates aligned with Darwin Core terms; reconcile monitored taxa to GBIF usageKeys; publish observatory data packages with dataset-level citation metadata |
| **National Geographic** | Field observation storytelling, species-at-risk framing, geospatial exploration of living systems | Surface trend narratives grounded in graph-linked occurrences; prioritize visually and geographically coherent monitoring units (ecoregions, site buffers, migration corridors); route high-salience alerts to public conservation views with steward-approved framing |
| **IUCN Red List** (conservation authority) | Global threatened-species taxonomy, conservation status categories, criteria-based assessment | Ingest Red List status designations and revision events; map institutional taxa to IUCN assessed names; flag status uplistings, downlistings, and data-deficient taxa requiring occurrence corroboration; never override published IUCN categories without steward-documented rationale |

Supporting standards alignment follows [07-reference-standards.md](07-reference-standards.md): Darwin Core, DwC-A, GBIF Taxonomic Backbone, GeoJSON, ISO 19115 (geospatial metadata), JSON-LD.

---

## 4. Position in Architecture

```
Species Registry + GBIF occurrence sync + citizen science observations + IUCN status feeds
        ↓
Knowledge Graph (taxa, occurrences, places, protected areas, heritage sites)
        ↓
Biodiversity Observatory Agent
        ↓
Species trend signals + occurrence anomaly scores + threatened-taxa alerts
        ↓
Observatory Observation Records (JSON-LD) + trend reports + threatened-taxa alerts — pending steward review where required
        ↓
Approved observatory feeds → Research Fabric, conservation dashboards, Digital Twin layers
```

The agent operates in the **Observatory Network** subgraph of the Experience Plane ([04-system-diagram.md](04-system-diagram.md), §2). All outputs pass through the AI Fabric governance chain before affecting canonical systems ([04-system-diagram.md](04-system-diagram.md), §2.2).

**Upstream inputs:** Species Registry and GBIF-synchronized entities ([10-metadata-agent.md](10-metadata-agent.md), [12-knowledge-graph-agent.md](12-knowledge-graph-agent.md)), occurrence ingest from Phase 2 Biodiversity capabilities, quality-cleared citizen science submissions, IUCN and national red-list status datasets, World Heritage and protected-area geometries from the Knowledge Graph.

**Downstream consumers:** Research Fabric (observatory data packages with DOI candidacy), Public Experience conservation portal and maps, Education Agent classroom-safe observatory datasets ([15-education-agent.md](15-education-agent.md)), Digital Twin conservation intelligence ([04-system-diagram.md](04-system-diagram.md)).

---

## 5. Observatory Tracks

The Biodiversity Observatory Agent organizes monitoring across three tracks. Each track produces typed observation records linked to canonical taxon or occurrence entities and a registered source.

### 5.1 Species

| Attribute | Specification |
|-----------|---------------|
| **Sources** | Species Registry accepted taxa, GBIF backbone revisions, field guide distribution summaries, graph-linked heritage-site co-occurrence sets |
| **Processing pattern** | Taxon scope selection → baseline metric computation → trend window comparison → taxonomic revision impact assessment → proposal emission |
| **Output entities** | Species trend records with population proxy metrics (occurrence frequency, range envelope change, recorder effort normalization), taxon URI anchors, and temporal bounds |
| **Standards** | Darwin Core taxon terms (`dwc:taxonID`, `dwc:scientificName`, `dwc:taxonRank`); GBIF usageKey linkage; GeoJSON for distribution envelopes ([07-reference-standards.md](07-reference-standards.md)) |

### 5.2 Occurrences

| Attribute | Specification |
|-----------|---------------|
| **Sources** | GBIF IPT synchronization, Darwin Core occurrence entities, PostGIS-indexed observation coordinates, moderated citizen science submissions |
| **Processing pattern** | Stream ingest → spatial-temporal binning → anomaly detection (influx, absence, spatial shift) → data-quality scoring → correlation with species and place entities → proposal emission |
| **Output entities** | Occurrence anomaly records with affected grid cells or site buffers, deviation scores, contributing dataset provenance, and recommended steward review tier |
| **Standards** | Darwin Core occurrence terms (`dwc:occurrenceID`, `dwc:eventDate`, `dwc:decimalLatitude`, `dwc:decimalLongitude`); DwC-A export for approved observatory packages; GeoJSON for spatial aggregates |

### 5.3 Threatened Taxa

| Attribute | Specification |
|-----------|---------------|
| **Sources** | IUCN Red List status tables, national and regional red lists, Species Registry conservation-status annotations, occurrence decline/recovery signals from §5.1 and §5.2 |
| **Processing pattern** | Watchlist maintenance → status revision ingest → occurrence corroboration → priority scoring (status severity × trend direction × geographic overlap with protected areas) → alert proposal emission |
| **Output entities** | Threatened-taxa alert records with IUCN category, national list equivalents, trend corroboration summary, affected geographies, and recommended public disclosure tier |
| **Standards** | IUCN Red List category vocabulary (mapped to SKOS concept scheme); Darwin Core `dwc:establishmentMeans` and institutional conservation-status extension properties; JSON-LD alert descriptors with `prov:wasDerivedFrom` provenance |

---

## 6. Alert and Trend Logic

The agent maintains configurable monitoring profiles; conservation stewards approve canonical thresholds.

### 6.1 Trend Windows

| Window | Use |
|--------|-----|
| **Rolling 30-day** | Near-real-time occurrence influx and absence detection |
| **Seasonal year-over-year** | Phenology and migration pattern deviation |
| **Multi-year baseline** | Longitudinal species population proxy trends |
| **Status-revision event** | Immediate threatened-taxa watchlist refresh on IUCN or national list updates |

### 6.2 Alert Severity Tiers

| Tier | Criteria | Routing |
|------|----------|---------|
| **Informational** | Minor occurrence variance within expected bounds | Dashboard annotation only; auto-approvable for internal views |
| **Watch** | Sustained trend deviation or data-quality regression | Biodiversity steward review queue |
| **Priority** | Threatened taxon with corroborated decline signal or range contraction | Conservation reviewer queue; blocks public alert until approved |
| **Critical** | Status uplisting candidate, sudden occurrence collapse in protected area, or cross-domain heritage-site overlap threat | Curator and conservation officer joint review; public disclosure requires explicit approval |

Machine-assigned tiers are proposals; stewards may override severity before canonical observatory writes.

---

## 7. Outputs

### 7.1 Observatory Observation Records

Each observation is emitted as **JSON-LD** with:

| Field | Requirement |
|-------|-------------|
| **Observation type** | `species-trend`, `occurrence-anomaly`, or `threatened-taxa-alert` |
| **Taxon anchors** | Species Registry URI, GBIF usageKey, scientific name, and rank |
| **Geographic scope** | GeoJSON geometry or referenced place / protected-area entity URI |
| **Temporal bounds** | ISO 8601 interval for the observation window |
| **Metric summary** | Quantitative trend or anomaly score with method documentation |
| **Source provenance** | Contributing datasets, ingest events, and graph entity URIs with `prov:wasDerivedFrom` |
| **Alert tier** | Proposed severity per §6.2 |
| **Review requirement** | Auto-approvable (informational only), steward review, or joint conservation review |

Observation records are **candidates** until a biodiversity steward or conservation reviewer approves them through the human-approval gate when policy requires review (public alerts, threatened-taxa priority signals, first-time baseline for a taxon).

### 7.2 Trend Reports

Each scheduled processing run emits a trend report containing:

- Species monitored vs. watchlist scope
- Occurrence volume and anomaly counts by geography and time window
- Threatened-taxa alert summary by IUCN category
- Data-quality regression inventory (coordinate issues, taxon mismatch, stale sync)
- Cross-domain links: heritage sites with co-occurring threatened taxa
- Recommended monitoring profile adjustments

### 7.3 Observatory Data Packages

Approved observations are packaged for Research Fabric export with:

- DwC-A or JSON-LD serialization per [07-reference-standards.md](07-reference-standards.md)
- Dataset-level citation metadata and DOI candidacy
- GeoJSON layers for map services
- Audit trail linking package contents to approved Observation Records

---

## 8. AI Fabric Governance

| Gate | Requirement |
|------|-------------|
| **Agent Registry** | Agent version, monitoring profiles, alert threshold defaults, IUCN vocabulary mappings, and feed connector scope registered before production runs |
| **Benchmarks** | Taxon reconciliation accuracy, anomaly detection precision/recall (human spot-check), threatened-taxa alert false-positive rate, trend metric reproducibility |
| **Evaluations** | Periodic review against Phase 15 Observatories success criteria |
| **Safety Reviews** | Verify agent does not fabricate conservation status, override IUCN authority, publish unreviewed critical alerts, or expose restricted occurrence coordinates beyond governance policy |
| **Human Approval** | Biodiversity stewards and conservation reviewers approve Observation Records before canonical observatory feed writes; critical and priority alerts always require human approval |

**Council assignment:** Research Council (trend methodology, IUCN alignment, anomaly models) and Implementation Council (feed pipelines, dashboard integration). Community Council advises on indigenous territory sensitivity and culturally restricted species disclosure.

---

## 9. Phase Alignment

| Phase | Agent Scope |
|-------|-------------|
| **Biodiversity (Phase 2)** | Readiness only: Species Registry and occurrence ingest must be operational before monitoring begins |
| **Knowledge Graph (Phase 5)** | Taxon–occurrence–place relationship integrity required for cross-domain alerts |
| **Research Fabric (Phase 8)** | Observatory data package export contract; citation metadata |
| **Observatories (Phase 15)** | Full species, occurrence, and threatened-taxa tracking; alert workflows; public and researcher dashboards |
| **Digital Twin (Phase 16+)** | Approved observatory layers feed conservation intelligence correlation |
| **Community (Phase 14)** | Citizen science occurrence submissions as monitored input after quality clearance |

---

## 10. Success Criteria

Aligned with Observatories phase completion criteria ([06-build-roadmap.md](06-build-roadmap.md)):

- Biodiversity observatory operational with species, occurrence, and threatened-taxa tracking live
- ≥ 10,000 taxa under active trend monitoring with GBIF-reconciled identifiers
- Occurrence anomaly detection processing near-real-time or daily partner feeds within institutional SLA
- Threatened-taxa watchlist covers ≥ 95% of IUCN-assessed taxa present in the Species Registry
- ≥ 3 approved observatory data packages published in Research Registry with citation metadata
- Public conservation dashboard displays steward-approved trends and alerts with provenance links
- Cross-domain demonstration: threatened taxon occurrence decline correlated with World Heritage site buffer geometry
- Zero unapproved critical alerts published to public channels

---

## 11. Constraints

- **No conservation status invention.** IUCN and national red-list categories are authoritative; the agent correlates and alerts, it does not assess species de novo.
- **Canonical taxon anchors mandatory.** Every trend or alert links to Species Registry and GBIF backbone identifiers ([03-canonical-architecture.md](03-canonical-architecture.md), Provenance).
- **Coordinate sensitivity.** Occurrence coordinates subject to partner embargoes, taxon sensitivity flags, and indigenous territory policies are aggregated or withheld per governance rules — never exposed in public alerts without clearance.
- **Steward approval before public alert.** Priority and critical tiers require human review before conservation portal publication.
- **Open science alignment.** Observatory data packages follow GBIF open-access patterns; restrictions propagate from source dataset rights metadata ([02-reference-models.md](02-reference-models.md), §5).
- **Cross-domain integrity.** Heritage–nature links (site ↔ species co-occurrence) derive from Knowledge Graph relationships, not unsourced spatial guesses ([08-decision-record.md](08-decision-record.md)).
