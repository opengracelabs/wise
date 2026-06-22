# Source Discovery Agent

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Status** | Canonical |
| **Authority** | Open Grace Architecture Office |
| **Date** | 2026-06-22 |
| **Capability** | Discovery ([03-canonical-architecture.md](03-canonical-architecture.md), §4.1) |
| **Phase** | Foundation ([06-build-roadmap.md](06-build-roadmap.md), Phase 1) |

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
| [12-knowledge-graph-agent.md](12-knowledge-graph-agent.md) | Knowledge Graph Agent specification |
| [13-quality-review-agent.md](13-quality-review-agent.md) | Quality Review Agent specification |
| [12-knowledge-graph-agent.md](12-knowledge-graph-agent.md) | Knowledge Graph Agent specification |

---

## 1. Purpose

The **Source Discovery Agent** automates the Discovery capability ([03-canonical-architecture.md](03-canonical-architecture.md), §4.1). It finds heritage, nature, and culture assets and metadata sources across partner institutions and public datasets, registers harvest endpoints in the Source Registry, and emits candidate **Discovery Records** (JSON-LD) for human review before ingestion.

The agent does not acquire bitstreams, write to Preservation, or assert knowledge-graph entities. It discovers and catalogs what exists, where it lives, and whether it is a viable ingestion candidate.

---

## 2. Responsibilities

| Responsibility | Description |
|----------------|-------------|
| **Find UNESCO sites** | Discover World Heritage sites, intangible heritage inventories, and UNESCO-aligned vocabularies; register site reference data and boundary metadata for knowledge modeling |
| **Find GBIF datasets** | Discover GBIF publisher IPT feeds, dataset registrations, and Darwin Core metadata; index occurrence and taxonomy sources for federated biodiversity ingestion |
| **Find public-domain collections** | Identify openly licensed and public-domain cultural collections (Creative Commons, RightsStatements.org `NoC-*`, institutional open-access policies) suitable for lawful reuse |
| **Find metadata sources** | Discover OAI-PMH harvest endpoints, partner APIs, dataset catalogs, and contributor registries; normalize provider and rights metadata without centralizing assets |

---

## 3. Reference Models

The agent synthesizes patterns from three primary reference models ([02-reference-models.md](02-reference-models.md)):

| Model | Pattern Applied | Agent Behavior |
|-------|-----------------|----------------|
| **UNESCO** | Global heritage mandate, World Heritage framework, multilingual site and tradition modeling | Harvest World Heritage site lists, state-party boundaries, intangible heritage registers; align place entities with UNESCO vocabulary |
| **Europeana** | Metadata aggregation without central asset storage, rights expression, provider registry | Federate OAI-PMH and API metadata; express rights via EDM and RightsStatements.org; register contributing institutions in Source Registry |
| **GBIF** | Federated data publishing, Darwin Core interoperability, open science infrastructure | Discover IPT endpoints and dataset metadata; pre-screen Darwin Core and DwC-A sources; link species occurrences to taxonomic backbone candidacy |

---

## 4. Position in Architecture

```
External Sources (UNESCO, GBIF nodes, Europeana providers, OAI-PMH, APIs, crawls)
        ↓
Source Discovery Agent
        ↓
Source Registry + Discovery Catalog
        ↓
Discovery Records (JSON-LD) — candidate, pending human approval
        ↓
Ingestion (Acquisition Pipeline)
```

The agent operates in the **Acquire** subgraph of the Platform Plane ([04-system-diagram.md](04-system-diagram.md), §3). All outputs pass through the AI Fabric governance chain before entering the canonical catalog ([04-system-diagram.md](04-system-diagram.md), §2.2).

---

## 5. Connector Targets

### 5.1 UNESCO

| Attribute | Specification |
|-----------|---------------|
| **Sources** | World Heritage List, intangible heritage inventories, UNESCO Thesaurus |
| **Harvest pattern** | Scheduled API and reference-data sync |
| **Output entities** | Sites, traditions, state-party affiliations, boundary geometries (when available) |
| **Standards** | SKOS vocabularies, ISO 639-3 language codes, World Heritage metadata practices ([07-reference-standards.md](07-reference-standards.md)) |

### 5.2 GBIF

| Attribute | Specification |
|-----------|---------------|
| **Sources** | GBIF Registry, IPT installations, published datasets |
| **Harvest pattern** | IPT feed discovery; dataset metadata harvest (occurrence ingest deferred to Biodiversity phase) |
| **Output entities** | Publishers, datasets, Darwin Core field mappings, taxonomic scope |
| **Standards** | Darwin Core, DwC-A, EML ([07-reference-standards.md](07-reference-standards.md)) |

### 5.3 Europeana (and Europeana-style providers)

| Attribute | Specification |
|-----------|---------------|
| **Sources** | Europeana API, OAI-PMH aggregators, national and institutional cultural portals |
| **Harvest pattern** | OAI-PMH harvest; API metadata pull; provider registry sync |
| **Output entities** | Cultural objects (metadata only), aggregators, rights statements, provider institutions |
| **Standards** | EDM, Dublin Core, OAI-PMH, RightsStatements.org ([07-reference-standards.md](07-reference-standards.md)) |

### 5.4 Public-Domain Collections

| Attribute | Specification |
|-----------|---------------|
| **Sources** | Open GLAM initiatives, Wikimedia Commons category trees, institutional open-access portals, web crawl of declared open collections |
| **Harvest pattern** | Rights pre-screening before catalog admission; metadata-only discovery when assets remain at source |
| **Output entities** | Collections, rights declarations, reuse constraints, attribution requirements |
| **Standards** | Creative Commons, RightsStatements.org, Schema.org ([07-reference-standards.md](07-reference-standards.md), §4.3) |

---

## 6. Outputs

### 6.1 Source Registry Entries

Each discovered source is registered with:

- Stable source identifier
- Institution or publisher name
- Harvest endpoint (API, OAI-PMH base URL, IPT feed URL)
- Rights posture summary
- Covenant status (proposed, pending, approved)
- Last harvest timestamp and harvest health

### 6.2 Discovery Records

Each candidate asset or metadata record is emitted as **JSON-LD** with:

| Field | Requirement |
|-------|-------------|
| **Source attribution** | Link to registered Source Registry entry |
| **Rights metadata** | Machine-readable rights category (RightsStatements.org or Creative Commons URI) |
| **Ingestion candidacy score** | Computed score based on rights clarity, metadata completeness, partner status, and duplication risk |
| **Provenance** | Discovery event identifier, harvest run, agent version |
| **External identifiers** | UNESCO, GBIF, Europeana, Wikidata, or provider-local IDs when available |

Discovery Records are **candidates** until a steward approves them through the human-approval gate.

---

## 7. AI Fabric Governance

| Gate | Requirement |
|------|-------------|
| **Agent Registry** | Agent version, connector scope, and operational parameters registered before production runs |
| **Benchmarks** | Coverage (sources per domain), rights accuracy, deduplication rate, metadata completeness |
| **Evaluations** | Periodic review against Phase 1 success criteria |
| **Safety Reviews** | Verify agent does not ingest restricted content, violate partner terms, or bypass rights gates |
| **Human Approval** | Stewards approve Source Registry entries and Discovery Record batches before canonical indexing |

**Council assignment:** Implementation Council (connector development) and Execution Council (scheduled harvest runs). Research Council advises on new source categories and vocabulary alignment.

---

## 8. Phase Alignment

| Phase | Agent Scope |
|-------|-------------|
| **Foundation (Phase 1)** | UNESCO site reference data; Europeana-style OAI-PMH harvest; GBIF IPT feed discovery; public-domain collection identification; Source Registry population |
| **Biodiversity (Phase 2)** | GBIF occurrence and taxonomy ingest candidacy scoring; Species Registry cross-reference hints |
| **Knowledge Graph (Phase 3+)** | External linking suggestions (Wikidata, GeoNames, GBIF backbone) on discovery records — suggestions only, not assertions |

---

## 9. Success Criteria

Aligned with Foundation phase completion criteria ([06-build-roadmap.md](06-build-roadmap.md)):

- Source Registry contains ≥ 10 registered authoritative sources with rights and harvest metadata
- UNESCO World Heritage site reference data discovered, registered, and queryable
- ≥ 3 partner or public sources connected via agent-managed connectors
- ≥ 100,000 discovery records indexed (catalog roadmap target)
- Rights pre-screening applied to all agent-emitted discovery records
- End-to-end demonstration: source → agent discovery → registry → steward approval → acquisition candidacy

---

## 10. Constraints

- **No canonical writes without approval.** The agent proposes; stewards approve.
- **Metadata aggregation, not asset centralization.** Follow Europeana's aggregation-with-attribution pattern ([02-reference-models.md](02-reference-models.md), §6).
- **Covenant before privileged harvest.** Partner sources require covenant framework approval ([03-canonical-architecture.md](03-canonical-architecture.md), Covenant Framework).
- **Provenance chain intact.** Every discovery record traces to a registered source and a logged discovery event ([03-canonical-architecture.md](03-canonical-architecture.md), Provenance).
- **Discovery precedes experience.** No discovery record enters public browse without passing acquisition and quality gates (ADR-003, [08-decision-record.md](08-decision-record.md)).
