# Knowledge Graph Agent

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Status** | Canonical |
| **Authority** | Open Grace Architecture Office |
| **Date** | 2026-06-22 |
| **Capability** | Knowledge Graph ([03-canonical-architecture.md](03-canonical-architecture.md), §4.5) |
| **Phase** | Foundation ([06-build-roadmap.md](06-build-roadmap.md), Phase 5) |

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

---

## 1. Purpose

The **Knowledge Graph Agent** automates the Knowledge Graph capability ([03-canonical-architecture.md](03-canonical-architecture.md), §4.5). It links modeled entities across heritage, nature, and culture domains; builds typed relationships with temporal and geographic bounds; detects duplicate and near-duplicate entities; and maintains graph integrity through reconciliation and constraint validation.

The agent does not replace curatorial authority. It proposes entity links, relationship assertions, and merge candidates as **Entity Assertions** (RDF triples) and reconciliation reports for steward review before canonical graph writes.

---

## 2. Responsibilities

| Responsibility | Description |
|----------------|-------------|
| **Link entities** | Resolve internal entities to external authority files (Wikidata, GBIF backbone, GeoNames); propose `sameAs`, `exactMatch`, and `closeMatch` links with confidence scores |
| **Build relationships** | Infer and assert typed relationships across domains (e.g., species at site, artifact from tradition, event at place); attach temporal bounds and geographic anchors |
| **Detect duplicates** | Identify duplicate and near-duplicate entities within and across entity types using label similarity, identifier overlap, spatial proximity, and graph neighborhood signals |
| **Maintain graph integrity** | Validate ontology constraints, detect orphaned nodes, broken external links, and contradictory assertions; emit integrity reports and correction proposals |

---

## 3. Reference Models

The agent synthesizes patterns from two primary reference models ([02-reference-models.md](02-reference-models.md)):

| Model | Pattern Applied | Agent Behavior |
|-------|-----------------|----------------|
| **Wikidata** | Community-maintained linked data, multilingual labels, heterogeneous entity types, external identifier hub | External entity linking via Wikidata QIDs; multilingual label alignment; reuse of Wikidata property patterns for cross-domain relationships |
| **Google Knowledge Graph** | Entity-centric unification across heterogeneous sources, entity resolution at scale, knowledge panel–style entity consolidation | Entity resolution across modeling outputs; confidence-scored merge candidates; unified entity identity across heritage, nature, and culture silos |

Supporting authority alignment follows [07-reference-standards.md](07-reference-standards.md): GBIF Taxonomic Backbone (species), GeoNames (places), and CIDOC-CRM / Darwin Core relationship vocabularies (domain semantics).

---

## 4. Position in Architecture

```
Knowledge Modeling outputs (Entity Assertions, RDF triples)
        ↓
Knowledge Graph Agent
        ↓
Link proposals + relationship assertions + deduplication candidates + integrity reports
        ↓
Steward review (human approval)
        ↓
Canonical Knowledge Graph (SPARQL / GraphQL)
        ↓
Search, Quality Platform, Research Fabric, Experience Plane
```

The agent operates in the **Knowledge** subgraph of the Platform Plane ([04-system-diagram.md](04-system-diagram.md), §3). All outputs pass through the AI Fabric governance chain before entering the canonical graph ([04-system-diagram.md](04-system-diagram.md), §2.2).

**Upstream inputs:** [Metadata Agent](10-metadata-agent.md) Entity Assertions, Knowledge Modeling layer, Source Discovery Agent external-linking hints ([09-source-discovery-agent.md](09-source-discovery-agent.md), §8), preserved object descriptors.

**Downstream consumers:** Search (index documents), Quality Platform (quality annotations), Research Fabric (API exports), Public Experience (entity pages).

---

## 5. Connector Targets

### 5.1 Wikidata

| Attribute | Specification |
|-----------|---------------|
| **Sources** | Wikidata Query Service, Wikidata entity API, Wikidata property and class registries |
| **Harvest pattern** | Batch entity lookup by label and identifier; scheduled reconciliation of existing external links |
| **Output entities** | QID links, multilingual labels, property mappings, authority-file crosswalks |
| **Standards** | RDF, SKOS, Wikidata data model ([07-reference-standards.md](07-reference-standards.md)) |

### 5.2 Google Knowledge Graph (patterns)

| Attribute | Specification |
|-----------|---------------|
| **Sources** | Internal entity resolution models informed by Google KG entity-centric patterns; no dependency on proprietary Google APIs for canonical operations |
| **Harvest pattern** | Cross-source entity clustering on modeled outputs; confidence-scored identity resolution |
| **Output entities** | Unified entity candidates, merge proposals, relationship type suggestions |
| **Standards** | schema.org alignment for web-facing entity types ([07-reference-standards.md](07-reference-standards.md)) |

### 5.3 GBIF Taxonomic Backbone

| Attribute | Specification |
|-----------|---------------|
| **Sources** | GBIF species API, taxonomic backbone snapshots |
| **Harvest pattern** | Species name resolution; taxon ID linking for nature-domain entities |
| **Output entities** | Taxon identifiers, accepted-name mappings, synonym disambiguation |
| **Standards** | Darwin Core, GBIF Taxonomic Backbone ([07-reference-standards.md](07-reference-standards.md)) |

### 5.4 GeoNames

| Attribute | Specification |
|-----------|---------------|
| **Sources** | GeoNames gazetteer, administrative boundary datasets |
| **Harvest pattern** | Place-name resolution; geospatial proximity matching for site and occurrence entities |
| **Output entities** | GeoNames IDs, coordinates, administrative hierarchy links |
| **Standards** | GeoJSON, GeoSPARQL ([07-reference-standards.md](07-reference-standards.md)) |

---

## 6. Outputs

### 6.1 Entity Link Proposals

Each proposed external link includes:

- Internal entity URI
- External authority identifier (Wikidata QID, GBIF taxon key, GeoNames ID)
- Link type (`sameAs`, `exactMatch`, `closeMatch`)
- Confidence score and supporting evidence (label match, identifier overlap, spatial/temporal alignment)
- Provenance: agent version, reconciliation run identifier

### 6.2 Relationship Assertions

Each proposed relationship includes:

- Subject and object entity URIs
- Typed predicate (domain ontology–aligned: CIDOC-CRM, Darwin Core extensions, internal cross-domain predicates)
- Temporal bounds (`time:hasBeginning`, `time:hasEnd`) when applicable
- Geographic anchor (GeoSPARQL geometry or place entity link)
- Confidence score and derivation method (rule-based, graph inference, external authority)

### 6.3 Deduplication Candidates

Each merge candidate pair or cluster includes:

- Entity URIs in the candidate set
- Similarity signals (label, identifier, spatial, neighborhood overlap)
- Recommended survivor entity and property merge plan
- Risk flags (conflicting assertions, distinct provenance, curatorial hold)

### 6.4 Integrity Reports

Periodic graph health reports covering:

- Orphaned entities (no inbound or outbound relationships)
- Broken external links (authority file no longer resolves)
- Ontology constraint violations
- Contradictory assertions (mutually exclusive types, impossible temporal ranges)
- Duplicate rate by entity type

All outputs are **proposals** until a steward approves them through the human-approval gate.

---

## 7. AI Fabric Governance

| Gate | Requirement |
|------|-------------|
| **Agent Registry** | Agent version, connector scope, ontology bindings, and resolution thresholds registered before production runs |
| **Benchmarks** | Link precision/recall, duplicate detection rate, false-merge rate, integrity violation count, cross-domain link coverage |
| **Evaluations** | Periodic review against Phase 5 success criteria and Quality Platform duplicate-rate targets |
| **Safety Reviews** | Verify agent does not auto-merge high-risk entities, overwrite curatorial decisions, or assert unverified external links |
| **Human Approval** | Curators approve link batches, merge operations, and high-impact relationship assertions before canonical graph writes |

**Council assignment:** Implementation Council (resolution pipelines, SPARQL tooling) and Research Council (ontology alignment, cross-domain relationship inference). Execution Council runs scheduled reconciliation and integrity scans.

---

## 8. Phase Alignment

| Phase | Agent Scope |
|-------|-------------|
| **Knowledge Modeling (Phase 4)** | Receive modeled entity assertions; begin Wikidata and GeoNames linking on place and people entities |
| **Knowledge Graph (Phase 5)** | Full entity linking, cross-domain relationship building, deduplication, integrity monitoring; graph population to ≥ 1M entities |
| **Search (Phase 6)** | Emit index-ready entity bundles for search pipeline consumption |
| **Quality Platform (Phase 7)** | Feed deduplication candidates and integrity violations to curation queues; accept quality annotations as feedback signals |

---

## 9. Success Criteria

Aligned with Knowledge Graph phase completion criteria ([06-build-roadmap.md](06-build-roadmap.md)):

- ≥ 1M entities in canonical graph with cross-domain relationships (heritage ↔ nature ↔ culture)
- External linking coverage ≥ 60% on eligible entity types (places, species, people with authority-file candidates)
- Duplicate entity rate < 2% within each entity type (Quality Platform target)
- SPARQL queries < 2s p95 on standard entity and relationship patterns
- Integrity scans operational with steward-facing correction queue
- End-to-end demonstration: modeling output → agent linking → steward approval → graph query → search index

---

## 10. Constraints

- **No canonical writes without approval.** The agent proposes; curators approve. High-confidence auto-linking is permitted only for pre-approved entity types and thresholds registered in Agent Registry.
- **Unified graph, domain-faithful semantics.** Follow ADR-004 ([08-decision-record.md](08-decision-record.md)): one graph, but relationships must use domain-appropriate predicates (CIDOC-CRM, Darwin Core), not lowest-common-denominator modeling.
- **Provenance chain intact.** Every assertion traces to a modeling event, reconciliation run, and agent version ([03-canonical-architecture.md](03-canonical-architecture.md), Provenance).
- **External links are claims, not truth.** Wikidata and authority-file links carry confidence and evidence; curators may override.
- **Quality Platform coordination.** Deduplication is shared responsibility: agent detects candidates; Quality Platform owns curatorial workflow and writes quality annotations back to the graph.
