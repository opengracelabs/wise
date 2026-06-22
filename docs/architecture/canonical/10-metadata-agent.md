# Metadata Agent

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Status** | Canonical |
| **Authority** | Open Grace Architecture Office |
| **Date** | 2026-06-22 |
| **Capability** | Knowledge Modeling ([03-canonical-architecture.md](03-canonical-architecture.md), §4.4) |
| **Phase** | Knowledge Modeling ([06-build-roadmap.md](06-build-roadmap.md), Phase 4) |

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

The **Metadata Agent** automates the Knowledge Modeling capability ([03-canonical-architecture.md](03-canonical-architecture.md), §4.4). It transforms preserved object descriptors and partner metadata into normalized, schema-valid entity assertions spanning heritage, nature, and culture domains.

The agent does not acquire bitstreams, assign ARKs, or publish to the public experience. It normalizes metadata, maps fields to canonical ontologies, validates schemas, and proposes authority records for human review before knowledge-graph placement.

---

## 2. Responsibilities

| Responsibility | Description |
|----------------|-------------|
| **Normalize metadata** | Transform heterogeneous source metadata (Dublin Core, EDM, LIDO, DwC-A, PREMIS) into a canonical internal representation while preserving source values and provenance |
| **Map fields** | Apply crosswalk rules from source schemas to CIDOC-CRM classes and properties, Darwin Core terms, and SKOS concepts; route domain-specific fields to the correct ontology layer |
| **Validate schemas** | Enforce structural and semantic constraints via SHACL shapes, JSON Schema, and standard-specific validators before entity assertions are emitted |
| **Create authority records** | Propose authority linkages and SKOS concept records for places, species, people, and organizations; reconcile against GeoNames, GBIF Taxonomic Backbone, Wikidata, and VIAF with match confidence scoring |

---

## 3. Reference Models

The agent applies three primary metadata frameworks ([07-reference-standards.md](07-reference-standards.md)):

| Model | Pattern Applied | Agent Behavior |
|-------|-----------------|----------------|
| **CIDOC-CRM** | Conceptual ontology for cultural heritage entities; event-centric modeling of production, use, and custody | Map heritage metadata to CRM classes (`E22 Man-Made Object`, `E53 Place`, `E39 Actor`, `E5 Event`); express provenance chains as CRM events; preserve source-to-CRM mapping provenance |
| **Dublin Core** | Base descriptive metadata vocabulary shared across domains | Normalize Dublin Core Terms (`dc:`, `dcterms:`) as the common descriptive layer; map DC elements to domain-specific extensions (CRM, Darwin Core) without loss of original literals |
| **Darwin Core** | Species occurrence and taxonomic interoperability | Map biodiversity metadata to Darwin Core terms (`dwc:scientificName`, `dwc:decimalLatitude`, `dwc:eventDate`); validate DwC-A packages; link taxonomic names to GBIF backbone candidacy |

Institutional patterns from [02-reference-models.md](02-reference-models.md) inform agent behavior:

| Model | Agent Pattern |
|-------|---------------|
| **UNESCO** | World Heritage site and tradition entities modeled with place and event CRM bindings |
| **GBIF** | Occurrence and taxonomy normalization; Species Registry reconciliation hints |
| **Wikimedia** | Wikidata entity linking suggestions for cross-domain authority resolution |

---

## 4. Position in Architecture

```
Preserved Object Descriptors (OAIS AIP + Dublin Core / PREMIS)
        ↓
Ingest metadata (EDM, LIDO, DwC-A, partner ontologies)
        ↓
Metadata Agent
        ↓
Normalization + Field Mapping + Schema Validation + Authority Proposals
        ↓
Entity Assertions (RDF triples) — candidate, pending human approval
        ↓
Knowledge Graph
        ↑
Quality Platform (authority reconciliation feedback, curation queues)
```

The agent operates in the **Model** subgraph of the Platform Plane ([04-system-diagram.md](04-system-diagram.md), §3). All outputs pass through the AI Fabric governance chain before entering the canonical graph ([04-system-diagram.md](04-system-diagram.md), §2.2).

**Upstream dependency:** [Source Discovery Agent](09-source-discovery-agent.md) supplies discovery metadata and source registry context; [Preservation Agent](11-preservation-agent.md) supplies preserved object descriptors. **Downstream consumer:** [Knowledge Graph Agent](12-knowledge-graph-agent.md) receives approved Entity Assertions per the interface contract ([03-canonical-architecture.md](03-canonical-architecture.md), §7).

---

## 5. Schema Targets

### 5.1 CIDOC-CRM (Heritage and Culture)

| Attribute | Specification |
|-----------|---------------|
| **Input formats** | LIDO, EDM, museum collection metadata, archival descriptive records |
| **Mapping pattern** | Source field → CRM class/property → RDF triple with `crm:P*` predicates |
| **Validation** | SHACL shapes for required CRM bindings (identity, place, temporal, actor) |
| **Output entities** | Artifacts, events, actors, places, traditions, linguistic objects |

### 5.2 Dublin Core (Cross-Domain Descriptive Layer)

| Attribute | Specification |
|-----------|---------------|
| **Input formats** | OAI-PMH Dublin Core, BagIt descriptive metadata, PREMIS agent and event records |
| **Mapping pattern** | Preserve original DC literals; emit normalized `dcterms:` assertions as descriptive overlay |
| **Validation** | JSON Schema for required descriptive elements (`dcterms:title`, `dcterms:identifier`, `dcterms:rights`) |
| **Output entities** | Descriptive metadata bundles attached to all domain entity types |

### 5.3 Darwin Core (Nature and Biodiversity)

| Attribute | Specification |
|-----------|---------------|
| **Input formats** | DwC-A archives, GBIF IPT occurrence records, EML dataset metadata |
| **Mapping pattern** | Source field → `dwc:` term → occurrence and taxon entity assertions |
| **Validation** | Darwin Core term constraints; coordinate and date format checks; taxonomic name parsing |
| **Output entities** | Occurrences, taxa, datasets, sampling events, georeferences |

---

## 6. Authority Record Creation

The agent proposes authority records; stewards approve before canonical graph placement.

### 6.1 Authority Targets

| Entity Type | Authority Registry | Match Signals |
|-------------|-------------------|---------------|
| **Places** | GeoNames, Wikidata | Name variants, administrative hierarchy, coordinates |
| **Species** | GBIF Taxonomic Backbone | Scientific name, authorship, rank, synonym chains |
| **People** | Wikidata, VIAF, ISNI/ORCID | Name forms, dates, institutional affiliations |
| **Organizations** | Wikidata, ISNI | Name, jurisdiction, institutional type |

### 6.2 Authority Record Output

Each proposed authority record includes:

| Field | Requirement |
|-------|-------------|
| **Internal URI** | Stable provisional identifier pending steward approval |
| **External links** | Candidate matches with registry-specific identifiers (GeoNames ID, GBIF usageKey, Wikidata QID) |
| **Match confidence** | Scored 0.0–1.0 with method (exact, fuzzy, coordinate-proximity, taxonomic-synonym) |
| **SKOS representation** | `skos:prefLabel`, `skos:altLabel`, `skos:exactMatch` / `skos:closeMatch` as appropriate |
| **Provenance** | Modeling event identifier, source metadata field, agent version, reconciliation run timestamp |

Low-confidence matches route to the Quality Platform curation queue rather than automatic graph placement.

---

## 7. Outputs

Entity Assertions and authority proposals conform to the canonical [Evidence Output Profile](03-canonical-architecture.md#66-evidence-output-profile) ([03-canonical-architecture.md](03-canonical-architecture.md), §6.6).

### 7.1 Normalized Metadata Records

Each processed preserved object or metadata package emits a normalized record with:

- Source schema identification and version
- Canonical field mapping table (source path → target ontology term)
- Preserved original literals with language tags
- Normalization event provenance (PREMIS-aligned)

### 7.2 Entity Assertions

Each candidate knowledge entity is emitted as **RDF triples** with:

| Field | Requirement |
|-------|-------------|
| **Entity type** | CIDOC-CRM class, Darwin Core category, or SKOS concept as appropriate |
| **Descriptive overlay** | Dublin Core Terms assertions |
| **Authority links** | Proposed external authority matches with confidence scores |
| **Temporal bounds** | `crm:P4_has_time-span` or `dcterms:temporal` when available |
| **Geographic anchors** | `crm:P53_has_former_or_current_location`, GeoJSON, or `dwc:` georeference terms |
| **Rights metadata** | RightsStatements.org or Creative Commons URI propagated from source |
| **Provenance** | Modeling event identifier, source preserved-object ARK, agent version |
| **Evidence profile** | [Evidence Output Profile](03-canonical-architecture.md#66-evidence-output-profile): `evidenceURIs[]`, `confidence`, `evidenceSummary`, `method`, `sourceRegistryRefs[]`, `provenanceEventId` |

Entity Assertions are **candidates** until a steward approves them through the human-approval gate. Assertions without a complete Evidence Output Profile route to the Quality Platform curation queue.

### 7.3 Validation Reports

Each processing run emits a validation report containing:

- Schema validation pass/fail per standard (CIDOC-CRM SHACL, Dublin Core JSON Schema, Darwin Core constraints)
- Unmapped field inventory with suggested crosswalk candidates
- Authority reconciliation summary (matched, proposed, unresolved)
- Quality signals for the Quality Platform (completeness, consistency, duplication risk)

---

## 8. AI Fabric Governance

| Gate | Requirement |
|------|-------------|
| **Agent Registry** | Agent version, ontology crosswalk scope, and authority registry connectors registered before production runs |
| **Benchmarks** | Mapping coverage, schema validation pass rate, authority match precision, normalization fidelity |
| **Evaluations** | Periodic review against Phase 4 Knowledge Modeling success criteria |
| **Safety Reviews** | Verify agent does not assert false authorities, overwrite source metadata, or bypass rights metadata |
| **Human Approval** | Stewards approve Entity Assertion batches and authority linkages before canonical graph writes |

**Council assignment:** Implementation Council (crosswalk and validator development) and Engineering Council (pipeline orchestration). Research Council advises on ontology alignment and new schema adapters.

---

## 9. Phase Alignment

| Phase | Agent Scope |
|-------|-------------|
| **Preservation (Phase 3)** | Dublin Core and PREMIS normalization from preserved object descriptors; validation-only mode |
| **Knowledge Modeling (Phase 4)** | Full CIDOC-CRM and Darwin Core field mapping; authority record proposals; Entity Assertion emission |
| **Knowledge Graph (Phase 5)** | Approved assertions ingested; entity resolution feedback loop from graph deduplication |
| **Quality Platform (Phase 6+)** | Authority reconciliation corrections written back to crosswalk rules; curation queue integration |

---

## 10. Success Criteria

Aligned with Knowledge Modeling phase completion criteria ([06-build-roadmap.md](06-build-roadmap.md)):

- ≥ 5 entity types modeled with documented CIDOC-CRM and Darwin Core crosswalks
- Dublin Core descriptive overlay applied to all normalized metadata records
- Schema validation operational for heritage (SHACL), descriptive (JSON Schema), and biodiversity (Darwin Core) inputs
- Authority reconciliation proposals generated for places, species, and people with match confidence scoring
- ≥ 80% schema validation pass rate on pilot partner metadata corpora
- End-to-end demonstration: preserved object → agent normalization → field mapping → validation → authority proposal → steward approval → knowledge graph placement

---

## 11. Constraints

- **No canonical graph writes without approval.** The agent proposes Entity Assertions; stewards approve.
- **Source fidelity preserved.** Normalization adds canonical representations; original metadata literals are never discarded ([03-canonical-architecture.md](03-canonical-architecture.md), Provenance).
- **Provenance chain intact.** Every Entity Assertion traces to a modeling event, source preserved-object ARK, and agent version ([03-canonical-architecture.md](03-canonical-architecture.md), §6.2).
- **Unified graph, domain-aware mapping.** Heritage and biodiversity metadata coexist in one knowledge graph per ADR-004 ([08-decision-record.md](08-decision-record.md)); the agent routes fields to the correct ontology layer without siloing domains.
- **Authority proposals, not assertions.** External authority links require steward approval or Quality Platform reconciliation before becoming canonical.
- **Rights metadata mandatory.** No entity assertion omits machine-readable rights inherited from source metadata ([07-reference-standards.md](07-reference-standards.md), §4.3).
- **Modeling follows preservation.** Agent inputs are preserved object descriptors and registered source metadata only; no direct public-source bypass of the acquisition pipeline.
