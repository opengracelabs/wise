# Build Roadmap

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
| [06-build-roadmap.md](06-build-roadmap.md) | Founder execution sequence and institutional build order |

---

## 1. Purpose

This document defines the **founder execution sequence** for building Nature & Culture over a **100-year institutional horizon**. It is the authoritative statement of *in what order* capabilities must be established, *why* that order is binding, and *what conditions* must be satisfied before the institution advances to the next phase.

The build roadmap is not a product backlog, funding schedule, or engineering sprint plan. It is constitutional implementation guidance: the sequence through which Open Grace ensures that preservation, provenance, and knowledge integrity precede public experience, and that each generation of builders inherits a coherent capability stack rather than a collection of disconnected systems.

Mission and mandate derive from [01-mission-and-constitutional-charter.md](01-mission-and-constitutional-charter.md). Logical capability definitions are in [03-canonical-architecture.md](03-canonical-architecture.md). Component relationships and the operational stack are visualized in [04-system-diagram.md](04-system-diagram.md). Institutional patterns informing each phase are cataloged in [02-reference-models.md](02-reference-models.md).

---

## 2. Why Build Order Matters

Nature & Culture is designed to outlive any single technology generation, leadership tenure, or funding cycle. Build order is therefore a **structural constraint**, not a preference.

### 2.1 Dependency Integrity

Each capability consumes outputs from prior capabilities. Discovery produces candidacy records that the Acquisition Pipeline requires. PostgreSQL and FastAPI provide the transactional substrate on which registries depend. Knowledge Modeling requires preserved evidence. Public Search requires a Knowledge Graph. Citizen science observations require species authority, quality review, and contributor governance. Reordering these dependencies produces systems that appear functional but lack provenance, reconciliation, or curatorial authority — failures that compound over decades.

### 2.2 Institutional Trust

The public mandate in [01-mission-and-constitutional-charter.md](01-mission-and-constitutional-charter.md) requires that Nature & Culture **preserve**, **connect**, and **publish** with verifiable integrity. Trust is earned when every published entity traces to a source, passes quality gates, and survives leadership transition. Build order encodes that chain of custody from authoritative source to public experience.

### 2.3 Generational Continuity

A 100-year institution will replace its entire technology stack multiple times. What must persist across migrations is **capability**, not implementation. Phases define durable institutional functions — Source Registry, Species Registry, Translation Memory — that survive stack refresh. Skipping phases leaves gaps that successor generations must reconstruct under operational pressure.

### 2.4 Constitutional Separation

Open Grace governs *what must be true*. Nature & Culture delivers *what the public experiences*. Build order ensures the constitutional plane (governance, standards, provenance) is operational before experience-plane capabilities (search, mobile apps, tourism portals) expose institutional memory to the world. Premature public experience without underlying quality and rights infrastructure violates the separation defined in [03-canonical-architecture.md](03-canonical-architecture.md).

### 2.5 Reference Model Synthesis

The eleven reference models in [02-reference-models.md](02-reference-models.md) did not emerge simultaneously. Harvard's preservation ethic, GBIF's federated taxonomy, Europeana's aggregation patterns, and Wikimedia's community governance each matured over decades. The founder execution sequence synthesizes these patterns in dependency order so Nature & Culture inherits institutional wisdom rather than repeating historical failures.

---

## 3. Founder Principle

> **Build the smallest useful capability stack before expanding.**

Every phase must deliver the **minimum viable institutional capability** — complete enough to satisfy completion criteria and milestone gates, narrow enough to avoid premature breadth. Expansion within a phase is permitted only when the phase's core obligation is met. New phases may not begin until their prerequisite phases pass gate review.

This principle applies across the 100-year horizon: each generation adds the smallest increment of durable capability required by institutional mandate, not the largest feature set achievable with current resources.

---

## 4. Roadmap Horizons

The founder execution sequence spans the first institutional generation. Subsequent generations operate within the same phase architecture, refreshing implementation while preserving capability contracts.

| Horizon | Approximate Period | Institutional Focus |
|---------|-------------------|---------------------|
| **Founder Generation** | Years 1–15 | Establish the full 13-phase capability stack; first public experience; initial observatory network |
| **Expansion Generation** | Years 15–35 | Scale partner federation, language coverage, sovereignty zones; first major technology migration |
| **Consolidation Generation** | Years 35–60 | Graph and corpus scale; succession governance; vault media refresh; AI-assisted curation under human authority |
| **Permanence Generation** | Years 60–100 | Continuous operation; covenant renewal; generational knowledge transfer; format migration cycles |

Horizons are indicative. Phase completion is governed by milestone gates, not calendar deadlines.

---

## 5. Founder Execution Sequence

The founder execution sequence comprises **thirteen phases**, canonical and sequential. Phases may not be skipped. Limited overlap is permitted only when prerequisite phases have passed their milestone gates for the dependencies in question.

```
Phase  1 — Foundation
Phase  2 — Biodiversity
Phase  3 — Knowledge Infrastructure
Phase  4 — Quality Platform
Phase  5 — Research Fabric
Phase  6 — Translation Fabric
Phase  7 — Publishing Platform
Phase  8 — Education Platform
Phase  9 — Community Platform
Phase 10 — Public Experience
Phase 11 — Mobile & Citizen Science
Phase 12 — Observatory Network
Phase 13 — Digital Twin
```

Build order alignment with the operational stack: [04-system-diagram.md](04-system-diagram.md), Section 2.

---

## 6. Phase Specifications

Each phase specification includes: **objective**, **capabilities**, **prerequisites**, **completion criteria**, and **institutional outputs**. Capabilities listed are the minimum scope for phase completion.

---

### Phase 1 — Foundation

| Attribute | Detail |
|-----------|--------|
| **Objective** | Establish the institutional substrate: discover heritage and culture assets, register authoritative sources, integrate UNESCO frameworks, acquire digital objects with provenance, and deploy the core data and service layer with a minimal public presence. |
| **Prerequisites** | Open Grace constitutional charter ratified ([01-mission-and-constitutional-charter.md](01-mission-and-constitutional-charter.md)); Architecture Office operational |
| **Architecture alignment** | Discovery, Ingestion ([03-canonical-architecture.md](03-canonical-architecture.md), Sections 4.1–4.2); operational stack ([04-system-diagram.md](04-system-diagram.md), Sections 2.1–2.2) |

**Capabilities:**

| Capability | Function |
|------------|----------|
| **Discovery** | [Source Discovery Agent](../architecture/canonical/09-source-discovery-agent.md) catalogs heritage, nature, and culture assets across UNESCO, GBIF, Europeana-style providers, OAI-PMH harvests, and open datasets before canonical acquisition |
| **Source Registry** | Authoritative registry of data sources, partner institutions, harvest endpoints, and rights metadata |
| **UNESCO integration** | Alignment with World Heritage, intangible heritage, and UNESCO vocabulary for site and tradition modeling |
| **Acquisition Pipeline** | End-to-end ingest with checksum verification, format identification, provenance events, and rights pre-screening |
| **PostgreSQL** | Canonical transactional store for metadata, registries, workflow state, and audit logs |
| **FastAPI** | Service layer exposing registry, discovery, and acquisition APIs with OpenAPI contracts |
| **Website MVP** | Minimal public-facing site demonstrating institutional identity, mission, and initial catalog browse — not full public experience |

**Completion criteria:**

- Source Registry contains ≥ 10 registered authoritative sources with rights and harvest metadata
- UNESCO World Heritage site reference data integrated and queryable
- Acquisition Pipeline processes discovery records to checksum-verified deposits with PREMIS provenance events
- PostgreSQL schema versioned; migration tooling operational
- FastAPI services deployed with health checks, authentication for steward operations, and public read endpoints for catalog browse
- Website MVP live with institutional charter, ≥ 1,000 discovery records browsable, and accessibility baseline (WCAG 2.1 A)
- End-to-end demonstration: source → discovery → acquisition → registry → public browse

**Reference models:** UNESCO, Europeana, Smithsonian ([02-reference-models.md](02-reference-models.md))

---

### Phase 2 — Biodiversity

| Attribute | Detail |
|-----------|--------|
| **Objective** | Establish the nature domain: federated species data through GBIF, a canonical Species Registry, geospatial infrastructure, maps, and field guide foundations. |
| **Prerequisites** | Phase 1 milestone gate passed |
| **Architecture alignment** | Biodiversity domain ([03-canonical-architecture.md](03-canonical-architecture.md)); GBIF patterns ([02-reference-models.md](02-reference-models.md), Section 5) |

**Capabilities:**

| Capability | Function |
|------------|----------|
| **GBIF** | IPT feed ingestion, Darwin Core normalization, occurrence and taxonomy synchronization |
| **Species Registry** | Canonical taxonomic backbone with GBIF reconciliation, synonym handling, and stable identifiers |
| **PostGIS** | Geospatial extensions on PostgreSQL for occurrences, site boundaries, and ecosystem geometries |
| **Maps** | Base map services, layer composition, and geospatial query APIs for species and place |
| **Field Guides** | Structured species descriptions, media linkage, distribution data, and identification keys (foundational) |

**Completion criteria:**

- GBIF backbone taxonomy synchronized with weekly refresh; occurrence ingest operational
- Species Registry contains ≥ 100,000 accepted taxa with GBIF identifier reconciliation
- PostGIS spatial indexes operational; geospatial queries return results within institutional SLA
- Map services render species occurrence and World Heritage site layers
- ≥ 50 field guide entries published with species authority, media provenance, and distribution maps
- Cross-link demonstrated: heritage site ↔ co-occurring species within shared geography

**Reference models:** GBIF, National Geographic ([02-reference-models.md](02-reference-models.md))

---

### Phase 3 — Knowledge Infrastructure

| Attribute | Detail |
|-----------|--------|
| **Objective** | Transform preserved objects and domain registries into structured, interoperable knowledge with graph connectivity, authority reconciliation, and linked-data publication. |
| **Prerequisites** | Phase 1 milestone gate passed; Phase 2 milestone gate passed for biodiversity entity types |
| **Architecture alignment** | Knowledge Modeling, Knowledge Graph ([03-canonical-architecture.md](03-canonical-architecture.md), Sections 4.4–4.5) |

**Capabilities:**

| Capability | Function |
|------------|----------|
| **Knowledge Modeling** | [Metadata Agent](../architecture/canonical/10-metadata-agent.md) normalizes metadata, maps fields (CIDOC-CRM, Dublin Core, Darwin Core), validates schemas, and proposes authority records before entity assertions enter the graph |
| **Knowledge Graph** | Unified graph store connecting places, species, sites, artifacts, events, people, traditions, languages |
| **Authority Records** | Reconciliation against GeoNames, Wikidata, GBIF backbone, and institutional authority files |
| **Linked Data** | RDF export, persistent URIs, and SPARQL or equivalent query endpoint for external consumption |

**Completion criteria:**

- ≥ 10 entity types modeled with documented ontology mappings
- Knowledge Graph contains ≥ 500,000 entities with cross-domain relationships (heritage ↔ nature ↔ culture)
- Authority reconciliation operational for places, species, and people with match confidence scoring
- Linked Data endpoint publicly accessible; ≥ 100,000 entities available as RDF with license metadata
- Query performance meets institutional SLA for graph traversal and faceted entity lookup

**Reference models:** Wikimedia, Google, UNESCO ([02-reference-models.md](02-reference-models.md))

---

### Phase 4 — Quality Platform

| Attribute | Detail |
|-----------|--------|
| **Objective** | Institutionalize curatorial integrity through systematic data quality, rights clearance, accessibility verification, and editorial review before knowledge enters public and research channels. |
| **Prerequisites** | Phase 3 milestone gate passed |
| **Architecture alignment** | Quality Platform ([03-canonical-architecture.md](03-canonical-architecture.md)); Quality layer ([04-system-diagram.md](04-system-diagram.md), Section 2) |

**Capabilities:**

| Capability | Function |
|------------|----------|
| **Data Quality** | Automated scoring, duplicate detection, completeness metrics, and anomaly flagging |
| **Rights Review** | Rights metadata validation, clearance workflows, and restriction enforcement |
| **Accessibility Review** | WCAG compliance verification for published content and media alternatives |
| **Editorial Review** | Human curatorial queues, correction workflows, and quality annotations written back to graph |

**Completion criteria:**

- Quality scores assigned to ≥ 80% of graph entities
- Rights Review workflow operational; no entity published without rights status
- Accessibility Review process documented; ≥ 95% of published field guide and site content passes WCAG 2.1 AA
- Editorial Review queue staffed; median review turnaround within institutional SLA
- Duplicate entity rate < 2% within each entity type
- Quality annotations persisted in provenance chain

**Reference models:** Harvard, Smithsonian ([02-reference-models.md](02-reference-models.md))

---

### Phase 5 — Research Fabric

| Attribute | Detail |
|-----------|--------|
| **Objective** | Provide programmatic research access: dataset registry, citation management, and reproducible query exports for scholarly use. |
| **Prerequisites** | Phase 3 milestone gate passed; Phase 4 milestone gate passed for datasets entering research channel |
| **Architecture alignment** | Research Fabric ([03-canonical-architecture.md](03-canonical-architecture.md), Section 4.8) |

**Capabilities:**

| Capability | Function |
|------------|----------|
| **Research Registry** | Catalog of research-ready datasets, APIs, and query snapshots with version identifiers |
| **Citation Management** | DOI or equivalent persistent identifier assignment, citation metadata, and attribution chains |
| **Reproducibility** | Query snapshot export, version-pinned datasets, and provenance documentation for scholarly reuse |

**Completion criteria:**

- Research Registry contains ≥ 20 published datasets with full metadata and license terms
- Citation Management assigns persistent identifiers; citation format documented (DataCite or equivalent)
- Reproducibility: query snapshots reproducible within version tolerance; export formats include CSV, RDF, Parquet
- Public research API documented with rate limiting and fair-use policy
- ≥ 5 external research citations or integrations demonstrated

**Reference models:** MIT, Stanford, GBIF ([02-reference-models.md](02-reference-models.md))

---

### Phase 6 — Translation Fabric

| Attribute | Detail |
|-----------|--------|
| **Objective** | Make institutional knowledge linguistically accessible while preserving source-language authority and supporting indigenous language stewardship. |
| **Prerequisites** | Phase 3 milestone gate passed |
| **Architecture alignment** | Translation Fabric ([03-canonical-architecture.md](03-canonical-architecture.md), Section 4.9) |

**Capabilities:**

| Capability | Function |
|------------|----------|
| **Translation Agent** | [Translates content, manages terminology, supports indigenous-language workflows](../architecture/canonical/14-translation-agent.md) |
| **Translation Memory** | Institutional translation memory with segment alignment, reuse, and quality tracking |
| **Terminology Management** | Controlled glossaries for domain terms (heritage, biodiversity, conservation) per locale |
| **Indigenous Languages** | Community-governed workflows for indigenous language content; source-language preservation policy enforced |

**Completion criteria:**

- Translation Memory operational with ≥ 100,000 aligned segments
- Terminology Management glossaries for ≥ 5 languages covering core domain vocabulary
- Indigenous Languages workflow documented with community consent and attribution requirements
- ≥ 10 languages supported for entity labels and UI strings
- Source-language originals never replaced by translations; both persisted in graph
- Human review queue for sensitive and indigenous-language content

**Reference models:** UNESCO, Wikimedia ([02-reference-models.md](02-reference-models.md))

---

### Phase 7 — Publishing Platform

| Attribute | Detail |
|-----------|--------|
| **Objective** | Produce curated institutional publications — encyclopedia, atlases, field guides, and reports — from canonical knowledge under editorial authority. |
| **Prerequisites** | Phase 4 milestone gate passed; Phase 6 milestone gate passed for multilingual publications |
| **Architecture alignment** | Publishing ([03-canonical-architecture.md](03-canonical-architecture.md), Section 4.10); Publishing & Product Platform ([04-system-diagram.md](04-system-diagram.md)) |

**Capabilities:**

| Capability | Function |
|------------|----------|
| **Encyclopedia** | Structured encyclopedia articles with entity linking, citations, and multilingual editions |
| **Atlases** | Geographic and thematic atlases with map integration and IIIF or equivalent image delivery |
| **Field Guides** | Full field guide publication workflow building on Phase 2 foundations |
| **Reports** | Institutional and thematic reports with data visualization and export |

**Completion criteria:**

- Encyclopedia contains ≥ 500 published articles with entity links and citations
- ≥ 3 atlases published with interactive map integration
- Field guide catalog ≥ 200 species/site guides with identification keys
- ≥ 5 institutional reports published with underlying data packages in Research Registry
- Editorial workflow enforces Quality Platform gates before publication
- IIIF or equivalent manifests for image-rich publications

**Reference models:** Europeana, National Geographic ([02-reference-models.md](02-reference-models.md))

---

### Phase 8 — Education Platform

| Attribute | Detail |
|-----------|--------|
| **Objective** | Deliver curriculum-aligned learning experiences, structured pathways, and teacher resources grounded in canonical knowledge. |
| **Prerequisites** | Phase 7 milestone gate passed |
| **Architecture alignment** | Education domain ([03-canonical-architecture.md](03-canonical-architecture.md), Experience Plane) |

**Capabilities:**

| Capability | Function |
|------------|----------|
| **Courses** | Structured courses with modules, assessments, and progress tracking |
| **Learning Pathways** | Sequenced exploration paths across heritage, nature, and culture domains |
| **Teacher Resources** | Lesson plans, downloadable materials, and curriculum mapping to national and UNESCO standards |

**Completion criteria:**

- ≥ 10 courses published across heritage, biodiversity, and culture domains
- ≥ 20 learning pathways operational with entity-linked content
- Teacher Resources hub with ≥ 100 lesson plans and curriculum alignment documentation
- Student-safe environment with age-appropriate content filtering
- Multilingual educational content in ≥ 5 languages via Translation Fabric

**Reference models:** MIT, Smithsonian ([02-reference-models.md](02-reference-models.md))

---

### Phase 9 — Community Platform

| Attribute | Detail |
|-----------|--------|
| **Objective** | Enable governed public contribution: contributors, expert reviewers, moderation, and community governance integrated with acquisition and quality workflows. |
| **Prerequisites** | Phase 1 milestone gate passed; Phase 4 milestone gate passed |
| **Architecture alignment** | Community ([03-canonical-architecture.md](03-canonical-architecture.md), Experience Plane) |

**Capabilities:**

| Capability | Function |
|------------|----------|
| **Contributors** | Registration, profiles, submission tools, and attribution in provenance |
| **Experts** | Expert reviewer designation, domain credentials, and elevated review authority |
| **Moderation** | Content moderation queues integrated with Quality Platform workflows |
| **Governance** | Community governance policies, appeal processes, and Open Grace covenant alignment |

**Completion criteria:**

- Contributor portal operational; ≥ 500 registered contributors
- Expert reviewer program with ≥ 50 designated experts across domains
- Moderation workflow integrated with Editorial and Rights Review queues
- Community governance charter published and aligned with Open Grace constitutional framework
- Community submissions flow through Acquisition Pipeline with full provenance
- Contributor attribution visible on published entities

**Reference models:** Wikimedia, Internet Archive ([02-reference-models.md](02-reference-models.md))

---

### Phase 10 — Public Experience

| Attribute | Detail |
|-----------|--------|
| **Objective** | Launch the full Nature & Culture public portal: search, maps, APIs, and research access for global audiences. |
| **Prerequisites** | Phase 3, 4, 5, 6, and 7 milestone gates passed |
| **Architecture alignment** | Public Experience ([03-canonical-architecture.md](03-canonical-architecture.md), Section 5); Public Experience layer ([04-system-diagram.md](04-system-diagram.md)) |

**Capabilities:**

| Capability | Function |
|------------|----------|
| **Search** | Full-text, semantic, geospatial, and faceted search across the corpus |
| **Maps** | Public interactive maps integrating heritage sites, species, and thematic layers |
| **APIs** | Documented public APIs for entities, search, maps, and collections |
| **Research Portal** | Researcher-facing portal with dataset discovery, API keys, and citation tools |

**Completion criteria:**

- Public website launched with entity pages for heritage, species, places, and traditions
- Search operational with sub-second p95 latency; faceted search across ≥ 5 dimensions
- Maps integrate World Heritage, species occurrence, and publishing content layers
- Public APIs documented with developer portal; authentication and rate limiting operational
- Research Portal provides dataset discovery and citation export
- WCAG 2.1 AA compliance verified; low-bandwidth mode available
- ≥ 20 languages supported via Translation Fabric

**Reference models:** Google, Europeana, National Geographic ([02-reference-models.md](02-reference-models.md))

---

### Phase 11 — Mobile & Citizen Science

| Attribute | Detail |
|-----------|--------|
| **Objective** | Extend public experience to mobile devices and structured community observation contributions. |
| **Prerequisites** | Phase 9 and Phase 10 milestone gates passed |
| **Architecture alignment** | Citizen Science ([04-system-diagram.md](04-system-diagram.md), Public Experience) |

**Capabilities:**

| Capability | Function |
|------------|----------|
| **Mobile Apps** | Native or progressive mobile applications for exploration, offline access, and field use |
| **Observations** | Structured observation records (species, heritage condition, cultural events) with geolocation and media |
| **Community Contributions** | Mobile and web contribution flows integrated with Community Platform and Acquisition Pipeline |

**Completion criteria:**

- Mobile apps published for iOS and Android (or equivalent PWA with offline capability)
- Observation submission operational with geolocation, media upload, and species/site linking
- Community contributions pass through moderation and quality workflows before graph integration
- ≥ 10,000 observations ingested with provenance and contributor attribution
- Field guide and map content available offline on mobile

**Reference models:** GBIF, National Geographic, Wikimedia ([02-reference-models.md](02-reference-models.md))

---

### Phase 12 — Observatory Network

| Attribute | Detail |
|-----------|--------|
| **Objective** | Establish longitudinal monitoring across heritage condition, biodiversity trends, climate indicators, tourism impact, and sustainability metrics. |
| **Prerequisites** | Phase 2, 5, and 10 milestone gates passed |
| **Architecture alignment** | Observatory Network ([04-system-diagram.md](04-system-diagram.md)) |

**Capabilities:**

| Capability | Function |
|------------|----------|
| **Heritage** | World Heritage site condition monitoring, threat tracking, and conservation status dashboards |
| **Biodiversity** | Species population trends, occurrence anomaly detection, and ecosystem health indicators |
| **Climate** | Climate data integration and correlation with heritage and biodiversity observatories |
| **Tourism** | Tourism flow and impact monitoring at heritage and natural sites |
| **Sustainability** | Sustainability indicators aligned with SDGs and institutional reporting |

**Completion criteria:**

- ≥ 5 observatories operational across distinct domains (heritage, biodiversity, climate minimum)
- Real-time or near-real-time data ingestion from partner feeds and field sensors
- Public and researcher dashboards with trend visualization and alert thresholds
- Observatory data packages published in Research Registry with citation metadata
- Heritage observatory covers ≥ 50 World Heritage sites with baseline condition data

**Reference models:** UNESCO, GBIF, National Geographic ([02-reference-models.md](02-reference-models.md))

---

### Phase 13 — Digital Twin

| Attribute | Detail |
|-----------|--------|
| **Objective** | Integrate geospatial, heritage, and conservation intelligence into a unified global model supporting visualization, simulation, and decision support for long-horizon stewardship. |
| **Prerequisites** | Phase 2, 3, 10, and 12 milestone gates passed |
| **Architecture alignment** | Digital Twin ([04-system-diagram.md](04-system-diagram.md), Public Experience) |

**Capabilities:**

| Capability | Function |
|------------|----------|
| **Global geospatial model** | Unified planetary-scale geospatial substrate integrating sites, ecosystems, occurrences, and observatory feeds |
| **Heritage visualization** | 3D and immersive visualization of heritage sites, artifacts, and reconstruction where ethically appropriate |
| **Conservation intelligence** | Analytical layer correlating threat data, observatory trends, and knowledge graph relationships for conservation decision support |

**Completion criteria:**

- Global geospatial model integrates World Heritage boundaries, species distributions, and observatory layers
- Heritage visualization operational for ≥ 20 sites with documented provenance and community consent where required
- Conservation intelligence dashboards demonstrate threat correlation across ≥ 3 data domains
- Digital Twin APIs available to researchers and partner institutions under governance policy
- Ethical review process documented for visualization of sensitive cultural heritage
- Performance and storage architecture documented for 100-year maintenance

**Reference models:** Google, UNESCO, Stanford ([02-reference-models.md](02-reference-models.md))

---

## 7. Milestone Gates

No phase may advance until its milestone gate passes. Gate review is conducted by the Open Grace Architecture Office with stewardship sign-off.

### 7.1 Universal Gate Requirements

Every phase gate requires all of the following:

| Gate Dimension | Requirement |
|----------------|-------------|
| **Completion** | All phase completion criteria (Section 6) met and evidenced |
| **Provenance** | Every entity and object in scope traces to registered source with audit trail |
| **Standards** | Implementation aligned with constitutional standards registry |
| **Architecture** | Capability contracts documented; deviations recorded in decision record |
| **Security** | Threat model reviewed; steward authentication and authorization verified |
| **Succession** | Runbooks, schema documentation, and operational knowledge deposited for successor generation |
| **Review** | Architecture Office written sign-off |

### 7.2 Phase Transition Rules

| Rule | Description |
|------|-------------|
| **No skipping** | Phases may not be skipped. Capabilities belonging to a later phase may not substitute for earlier phase obligations. |
| **Dependency gating** | A phase may begin only when all listed prerequisite phases have passed milestone gates. |
| **Controlled overlap** | Work on phase *N+1* may begin in preparatory mode (design, schema draft) before phase *N* completes, but production deployment of phase *N+1* capabilities requires phase *N* gate passage. |
| **Regression** | If a gate review fails, the phase remains open. Remediation is documented; re-review required. |
| **Amendment** | Changes to phase order or completion criteria require constitutional-level architecture decision record. |

### 7.3 Gate Review Artifact

Each gate review produces a **Milestone Gate Record** containing: phase identifier, review date, criteria checklist, evidence references, conditions (if conditional pass), and signatory authority. Gate records are institutional artifacts retained for the 100-year horizon.

---

## 8. Phase Dependency Matrix

```
Phase  1 ─────────────────────────────────────────────┐
         ├──► Phase  2 ──► Phase  3 ──► Phase  4 ──┬──► Phase  5
         │                      │         │         ├──► Phase  6 ──► Phase  7 ──► Phase  8
         │                      │         │         │
         └──────────────────────┴─────────┴─────────┴──► Phase  9 ──► Phase 11
                                    │
                                    ├──► Phase 10 ──┬──► Phase 11
                                    │               ├──► Phase 12 ──► Phase 13
                                    └───────────────┘
```

---

## 9. 100-Year Continuation

The thirteen founder phases establish the **complete institutional capability stack**. The 100-year horizon governs how that stack is maintained, scaled, and transferred across generations.

| Period | Institutional Initiatives |
|--------|--------------------------|
| **Years 1–15** | Complete founder execution sequence; first covenant network; initial language and partner coverage |
| **Years 15–30** | Sovereignty zones for partner nations; 50+ languages; technology stack first migration; graph scale to billions of entities |
| **Years 30–50** | Second-generation leadership succession; vault media refresh; AI-assisted curation under human authority; observatory network global coverage |
| **Years 50–75** | Third technology generation; format migration cycles; expanded Digital Twin fidelity; indigenous language corpus maturity |
| **Years 75–100** | Continuous operation; covenant renewal; generational knowledge transfer; archive media refresh every 15 years; constitutional amendment review |

Capability contracts defined in [03-canonical-architecture.md](03-canonical-architecture.md) persist across technology migrations. Implementation choices (PostgreSQL, FastAPI, PostGIS) are founder-generation expressions; successor generations replace implementations while preserving registry, graph, and provenance semantics.

---

## 10. Dependencies on Open Grace

Before Phase 1 begins, Open Grace must establish:

1. Constitutional charter ratified ([01-mission-and-constitutional-charter.md](01-mission-and-constitutional-charter.md))
2. Architecture Office operational with authority over this roadmap
3. Standards registry initialized
4. Initial architecture decision records filed
5. First partner covenants signed (UNESCO-aligned bodies, GBIF nodes, or equivalent)

---

## 11. Roadmap Authority

This document is canonical. Changes to phase order, completion criteria, or gate requirements require Architecture Office proposal and constitutional-level decision record approval.

Timeline adjustments within phases — provided completion criteria and gate requirements are unchanged — require Architecture Office approval and documented notation in the gate record.

The founder principle — *build the smallest useful capability stack before expanding* — is binding on all phases and may not be waived without constitutional amendment.

---

*Previous: [04-system-diagram.md](04-system-diagram.md)*
