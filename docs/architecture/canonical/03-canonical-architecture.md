# Canonical Architecture

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Status** | Canonical |
| **Authority** | Open Grace Architecture Office |
| **Date** | 2026-06-22 |

## Document Map

| Document | Purpose |
|----------|---------|
| [01-mission-and-constitutional-charter.md](01-mission-and-constitutional-charter.md) | Mission, charter, and constitutional relationship |
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
| [15-publishing-agent.md](15-publishing-agent.md) | Publishing Agent specification |
| [16-education-agent.md](16-education-agent.md) | Education Agent specification |
| [17-biodiversity-observatory-agent.md](17-biodiversity-observatory-agent.md) | Biodiversity Observatory Agent specification |
| [18-climate-observatory-agent.md](18-climate-observatory-agent.md) | Climate Observatory Agent specification |
| [19-heritage-observatory-agent.md](19-heritage-observatory-agent.md) | Heritage Observatory Agent specification |
| [20-tourism-observatory-agent.md](20-tourism-observatory-agent.md) | Tourism Observatory Agent specification |
| [21-language-observatory-agent.md](21-language-observatory-agent.md) | Language Observatory Agent specification |
| [22-standards-agent.md](22-standards-agent.md) | Standards Agent specification |
| [23-benchmark-agent.md](23-benchmark-agent.md) | Benchmark Agent specification |

---

## 1. Purpose

This document defines the **canonical 100-year logical architecture** for Open Grace and Nature & Culture. It describes what the system is, how its layers relate, and the principles that govern design across technology generations.

Physical deployment is documented in [05-physical-architecture.md](05-physical-architecture.md). Visual representation is in [04-system-diagram.md](04-system-diagram.md). Build sequencing is in [06-build-roadmap.md](06-build-roadmap.md).

---

## 2. Architectural Overview

The system comprises three planes:

```
┌──────────────────────────────────────────────────────────────────┐
│  CONSTITUTIONAL PLANE — Open Grace                               │
│  Charter · Governance · Standards Authority · Succession          │
└──────────────────────────────┬───────────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────────┐
│  PLATFORM PLANE — Core Capabilities (founder build order)        │
│  Discovery → Ingestion → Preservation → Knowledge → Search →   │
│  Quality → Research → Translation → Publishing                     │
└──────────────────────────────┬───────────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────────┐
│  EXPERIENCE PLANE — Nature & Culture (public-facing)             │
│  Public Experience · Products · Education · Community ·          │
│  Observatories                                                   │
└──────────────────────────────────────────────────────────────────┘
```

---

## 3. Constitutional Plane — Open Grace

Open Grace is not implemented as a single application. It is expressed through:

| Component | Function |
|-----------|----------|
| **Constitutional Charter** | Mission, amendments, non-negotiable commitments ([01-mission-and-constitutional-charter.md](01-mission-and-constitutional-charter.md)) |
| **Architecture Office** | Canonical architecture authority; maintains this document suite |
| **Standards Registry** | Binding technical standards ([07-reference-standards.md](07-reference-standards.md)); automated conformance verification via [Standards Agent](22-standards-agent.md) |
| **Decision Record** | Immutable log of architectural decisions ([08-decision-record.md](08-decision-record.md)) |
| **Stewardship Policy** | Preservation tiers, provenance requirements, access rules |
| **Covenant Framework** | Agreements with partner institutions (UNESCO-aligned, GBIF nodes, museums, archives) |
| **Benchmark Program** | Agent performance, quality metric, and architecture compliance evaluation ([23-benchmark-agent.md](23-benchmark-agent.md)) |

Open Grace has no public user interface. Its artifacts are governance documents, policies, and architectural contracts.

---

## 4. Platform Plane — Core Capabilities

The platform plane implements the **founder build order** (see [06-build-roadmap.md](06-build-roadmap.md)). Each capability is a distinct architectural domain with defined interfaces.

### 4.1 Discovery

**Purpose:** Find heritage, nature, and culture assets across partner institutions, public datasets, and contributor networks before they enter the canonical store.

| Attribute | Specification |
|-----------|--------------|
| Inputs | Partner APIs, OAI-PMH harvests, GBIF IPT feeds, web crawls, contributor submissions |
| Outputs | Discovery records with source attribution, rights metadata, and ingestion candidacy scores |
| Reference models | Europeana, National Geographic, Google ([02-reference-models.md](02-reference-models.md)) |
| Agent | [Source Discovery Agent](09-source-discovery-agent.md) — automates UNESCO, GBIF, Europeana, and public-domain source discovery |

### 4.2 Ingestion

**Purpose:** Acquire digital objects and metadata into the canonical preservation pipeline with full provenance.

| Attribute | Specification |
|-----------|--------------|
| Inputs | Discovery records, direct deposits, digitization outputs, observatory feeds |
| Outputs | Ingest packages: bitstream + descriptive metadata + provenance event log |
| Requirements | Checksum verification, virus scanning, format identification, rights validation |
| Reference models | Smithsonian, Stanford, GBIF |

### 4.3 Preservation

**Purpose:** Store, protect, and perpetually maintain digital objects across format generations.

| Attribute | Specification |
|-----------|--------------|
| Inputs | Ingest packages |
| Outputs | Preserved objects with persistent identifiers, replication proofs, migration history |
| Tiers | Hot (active access), Warm (available), Cold (archival), Deep (offline vault) — see [05-physical-architecture.md](05-physical-architecture.md) |
| Requirements | OAIS compliance, 3+ geographic replicas, format migration schedule |
| Reference models | Harvard, Internet Archive, MIT |
| Agent | [Preservation Agent](11-preservation-agent.md) — verifies files, generates checksums, tracks provenance, monitors preservation risk |

### 4.4 Knowledge Modeling

**Purpose:** Transform preserved objects and metadata into structured, interoperable knowledge representations.

| Attribute | Specification |
|-----------|--------------|
| Inputs | Preserved objects, external authority files, partner ontologies |
| Outputs | Normalized entities: places, species, artifacts, events, people, traditions, languages |
| Standards | CIDOC-CRM, Darwin Core, SKOS, schema.org extensions ([07-reference-standards.md](07-reference-standards.md)) |
| Reference models | UNESCO, Wikimedia, GBIF |
| Agent | [Metadata Agent](10-metadata-agent.md) — normalizes metadata, maps fields, validates schemas, and proposes authority records |

### 4.5 Knowledge Graph

**Purpose:** Connect modeled entities into a unified, queryable graph spanning heritage, nature, and culture.

| Attribute | Specification |
|-----------|--------------|
| Inputs | Knowledge modeling outputs, Wikidata links, GBIF backbone, GeoNames, partner graphs |
| Outputs | Entity graph with typed relationships, temporal bounds, geographic anchors, multilingual labels |
| Interface | SPARQL endpoint, GraphQL API, entity resolution service |
| Reference models | Google Knowledge Graph, Wikidata, Europeana |
| Agent | [Knowledge Graph Agent](12-knowledge-graph-agent.md) — links entities, builds relationships, detects duplicates, maintains graph integrity |

### 4.6 Search

**Purpose:** Enable discovery of any entity, object, or collection across the full corpus in any supported language.

| Attribute | Specification |
|-----------|--------------|
| Inputs | Knowledge graph, full-text indexes, media features, geospatial indexes |
| Outputs | Ranked results, faceted navigation, entity panels, cross-lingual matches |
| Capabilities | Full-text, semantic, geospatial, temporal, visual similarity |
| Reference models | Google, Europeana |

### 4.7 Quality Platform

**Purpose:** Ensure accuracy, authenticity, completeness, and curatorial integrity of the canonical memory.

| Attribute | Specification |
|-----------|--------------|
| Inputs | Knowledge graph, contributor submissions, automated quality signals |
| Outputs | Quality scores, curation queues, correction workflows, authority reconciliation |
| Functions | Duplicate detection, attribution verification, taxonomy validation, rights audit |
| Reference models | Harvard, Smithsonian |
| Agent | [Quality Review Agent](13-quality-review-agent.md) — evaluates metadata quality, rights clearance, accessibility compliance, and content completeness; routes items to curatorial review queues |

### 4.8 Research Fabric

**Purpose:** Provide researchers, scientists, and scholars with programmatic access to datasets, APIs, and analytical tools.

| Attribute | Specification |
|-----------|--------------|
| Inputs | Knowledge graph, preserved objects, aggregated datasets |
| Outputs | Research APIs, bulk exports, citation-ready datasets, notebook environments |
| Requirements | Open access, DOI assignment, reproducible query snapshots |
| Reference models | MIT, Stanford, GBIF |

### 4.9 Translation Fabric

**Purpose:** Make every entity, description, and interface element available in every supported language.

| Attribute | Specification |
|-----------|--------------|
| Inputs | Source language content, translation memory, community translations |
| Outputs | Localized content with provenance (human, machine, community), quality tiers |
| Requirements | Source-language preservation, translation attribution, fallback chains |
| Reference models | UNESCO, Wikimedia |
| Agent | [Translation Agent](14-translation-agent.md) — translates content, manages terminology, supports indigenous-language workflows |

### 4.10 Publishing

**Purpose:** Produce curated publications, exhibits, datasets, and media packages from the canonical memory.

| Attribute | Specification |
|-----------|--------------|
| Inputs | Knowledge graph selections, preserved media, editorial workflows |
| Outputs | Exhibits, story packages, open datasets, IIIF manifests, API collections |
| Reference models | Europeana, National Geographic |
| Agent | [Publishing Agent](15-publishing-agent.md) — assembles encyclopedias, field guides, books, and reports; generates IIIF manifests; enforces editorial gates |

---

## 5. Experience Plane — Nature & Culture

The experience plane is the public face of the institution. All experiences consume platform plane APIs; no experience plane component writes directly to preservation storage.

### 5.1 Public Experience

The primary public portal: search, explore, entity pages, maps, timelines, and visual narratives.

- Consumes: Search, Knowledge Graph, Translation Fabric, Publishing
- Serves: Web, mobile, low-bandwidth, accessibility-compliant interfaces

### 5.2 Products

Derived public products built on canonical memory: apps, APIs for third parties, embeddable widgets, data products.

- Constitutional constraint: Products must not gate access to canonical public memory ([01-mission-and-constitutional-charter.md](01-mission-and-constitutional-charter.md))

### 5.3 Education

Curriculum-aligned learning experiences, lesson plans, interactive explorations, and classroom tools.

- Consumes: Publishing, Knowledge Graph, Translation Fabric
- Reference models: MIT OpenCourseWare, Smithsonian education
- Agent: [Education Agent](16-education-agent.md) — generates curriculum-aligned learning resources, curriculum mappings, and teacher guides for educator approval

### 5.4 Community

Contributor tools, citizen science interfaces, translation participation, and local heritage documentation.

- Consumes: Discovery, Ingestion, Quality Platform, Translation Fabric
- Reference models: Wikimedia, Internet Archive

### 5.5 Observatories

Live and longitudinal monitoring interfaces for nature (species, ecosystems) and culture (language vitality, site conditions, tourism impact, sustainability metrics).

- Agent: [Heritage Observatory Agent](19-heritage-observatory-agent.md) — tracks World Heritage site condition, threats, and conservation status; emits Observatory Observation Records for steward review
- Agent: [Tourism Observatory Agent](20-tourism-observatory-agent.md) — tracks visitor patterns and sustainability indicators at heritage and natural sites
- Agent: [Biodiversity Observatory Agent](17-biodiversity-observatory-agent.md) — tracks **species**, **occurrences**, and **threatened taxa**; emits trend signals and conservation alerts for steward approval
- Consumes: Ingestion, Knowledge Graph, Research Fabric
- Reference models: GBIF, National Geographic, UNESCO World Heritage monitoring
- Agent: [Climate Observatory Agent](18-climate-observatory-agent.md) — ingests climate and conservation feeds; operates **climate impacts**, **protected areas**, and **heritage risk** tracks; emits Observatory Observation Proposals for steward approval before canonical observatory writes
- Agent: [Language Observatory Agent](21-language-observatory-agent.md) — tracks **endangered languages** and **revitalization programs**; ingests vitality signals from partner feeds; emits Vitality Observations and Revitalization Program Records for language-steward approval before canonical observatory writes

---

## 6. Cross-Cutting Concerns

### 6.1 Identity and Access

| Actor | Access Pattern |
|-------|---------------|
| Public users | Anonymous read access to all canonical public memory |
| Contributors | Authenticated submission via Community platform |
| Curators | Role-based access to Quality Platform |
| Researchers | Authenticated API access via Research Fabric |
| Partner institutions | Federated identity via covenant framework |
| Administrators | Open Grace governance tools (non-public) |

### 6.2 Provenance

Every object maintains an immutable provenance chain:

```
Source → Discovery Event → Ingest Event → Preservation Event →
Modeling Event → Graph Placement → Quality Verification → Publication
```

Provenance is stored alongside the object and queryable via the Knowledge Graph.

### 6.3 Rights

Rights metadata follows Europeana Rights Statements and Creative Commons. No object enters the public experience without a machine-readable rights declaration.

### 6.4 Identifiers

| Entity Type | Identifier Scheme |
|-------------|------------------|
| Canonical objects | ARK (Archival Resource Key) |
| Research datasets | DOI |
| Graph entities | Internal URI + Wikidata/GBIF external links |
| Publications | DOI or Handle |

### 6.5 Events and Observability

All platform components emit structured events to a central observability plane (not public-facing). Events support audit, capacity planning, and quality analytics.

### 6.6 Evidence Output Profile

Assertion-making agents attach the following fields to every factual assertion, link proposal, and observatory observation. The profile is normative for agents that emit Entity Assertions, relationship or link proposals, and Observatory Observation Records or Proposals.

| Field | Requirement |
|-------|-------------|
| **evidenceURIs[]** | URIs of supporting source records, preserved objects, partner feeds, or steward-reviewed documents |
| **confidence** | Numeric score (0.0–1.0) or enumerated confidence tier per agent output schema |
| **evidenceSummary** | Human-readable summary of the supporting material and derivation context |
| **method** | Derivation method identifier (e.g., `rule-based`, `spatial-join`, `machine-inferred`, `feed-direct`, `steward-reviewed`) |
| **sourceRegistryRefs[]** | Registered Source Registry entry URIs for upstream sources |
| **provenanceEventId** | PREMIS-aligned or institutional event identifier linking the output to the agent run |

Agents without sufficient supporting material MUST NOT emit the assertion; they route to steward review or emit a data-gap signal instead.

---

## 7. Interface Contracts

Layers communicate through defined contracts only:

| From | To | Contract |
|------|----|----------|
| Discovery | Ingestion | Discovery Record (JSON-LD) |
| Ingestion | Preservation | Ingest Package (BagIt + PREMIS) |
| Preservation | Knowledge Modeling | Preserved Object Descriptor (OAIS AIP) |
| Knowledge Modeling | Knowledge Graph | Entity Assertion (RDF triples) |
| Knowledge Graph | Search | Index Documents (entity + text + geo) |
| Knowledge Graph | All Experience | GraphQL / SPARQL API |
| Translation Fabric | All Experience | Localized Content Bundle |
| Quality Platform | Knowledge Graph | Quality Annotations |
| Publishing | Public Experience | Published Collection Manifest |
| Research Fabric | External | REST API + bulk export |

---

## 8. 100-Year Durability Principles

| Principle | Implementation |
|-----------|---------------|
| **Abstraction over implementation** | Layers defined by contracts, not vendors |
| **Format agility** | Normalization on ingest; migration on schedule |
| **Geographic sovereignty** | Multi-region deployment with data residency options ([05-physical-architecture.md](05-physical-architecture.md)) |
| **Governance permanence** | Open Grace charter survives technology changes |
| **Incremental build** | Founder build order delivers value at each phase ([06-build-roadmap.md](06-build-roadmap.md)) |
| **Open standards** | No proprietary lock-in on preservation formats ([07-reference-standards.md](07-reference-standards.md)) |
| **Amendment traceability** | All changes recorded in ADRs ([08-decision-record.md](08-decision-record.md)) |

---

## 9. What This Architecture Is Not

- **Not a monolith** — Each capability is independently evolvable within its contract.
- **Not a single vendor stack** — Physical layer may use multiple providers across regions.
- **Not a closed corpus** — Federated discovery and partner covenants extend reach indefinitely.
- **Not English-first** — Translation Fabric is a platform capability, not a localization layer.
- **Not a commercial platform** — Revenue from Products must not compromise free public access.

---

## 10. Architecture Authority

The Open Grace Architecture Office maintains this document. Proposed changes require an ADR in [08-decision-record.md](08-decision-record.md) and must demonstrate alignment with [01-mission-and-constitutional-charter.md](01-mission-and-constitutional-charter.md).

---

*Previous: [02-reference-models.md](02-reference-models.md) · Next: [04-system-diagram.md](04-system-diagram.md)*
