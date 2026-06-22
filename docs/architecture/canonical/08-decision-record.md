# Architecture Decision Records

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Status** | Canonical |
| **Authority** | Open Grace Architecture Office |
| **Date** | 2026-06-22 |

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
| [11-preservation-agent.md](11-preservation-agent.md) | Preservation Agent specification |

---

## 1. Purpose

This document records **Architecture Decision Records (ADRs)** — the formal, immutable log of why the Open Grace and Nature & Culture architecture was designed as documented in this canonical suite. ADRs provide institutional memory across leadership transitions and technology generations.

### ADR Format

Each record follows this structure:

- **Status** — Proposed, Accepted, Deprecated, Superseded
- **Date** — Decision date
- **Context** — What situation required a decision
- **Decision** — What was decided
- **Rationale** — Why this choice over alternatives
- **Consequences** — Positive and negative outcomes
- **References** — Cross-links to canonical documents

---

## 2. ADR Index

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| [ADR-001](#adr-001-dual-institution-model) | Dual Institution Model | Accepted | 2026-06-22 |
| [ADR-002](#adr-002-governance-experience-separation) | Governance-Experience Separation | Accepted | 2026-06-22 |
| [ADR-003](#adr-003-founder-build-order) | Founder Build Order | Accepted | 2026-06-22 |
| [ADR-004](#adr-004-unified-knowledge-graph) | Unified Knowledge Graph | Accepted | 2026-06-22 |
| [ADR-005](#adr-005-100-year-architecture-horizon) | 100-Year Architecture Horizon | Accepted | 2026-06-22 |
| [ADR-006](#adr-006-reference-model-synthesis) | Reference Model Synthesis | Accepted | 2026-06-22 |
| [ADR-007](#adr-007-tiered-physical-storage) | Tiered Physical Storage | Accepted | 2026-06-22 |
| [ADR-008](#adr-008-translation-as-platform-capability) | Translation as Platform Capability | Accepted | 2026-06-22 |
| [ADR-009](#adr-009-oais-preservation-foundation) | OAIS Preservation Foundation | Accepted | 2026-06-22 |
| [ADR-010](#adr-010-free-access-constitutional-commitment) | Free Access Constitutional Commitment | Accepted | 2026-06-22 |

---

## ADR-001: Dual Institution Model

| Field | Value |
|-------|-------|
| **Status** | Accepted |
| **Date** | 2026-06-22 |
| **Deciders** | Open Grace Architecture Office |

### Context

A single institution must simultaneously serve two incompatible time horizons: the permanent stewardship of cultural and natural heritage (centuries) and the dynamic delivery of public digital experiences (years). Conflating governance and public identity creates risk that short-term pressures — funding, technology trends, political influence — erode the preservation mission.

### Decision

Establish two distinct institutions:

1. **Open Grace** — Constitutional governance layer (non-public)
2. **Nature & Culture** — Public-facing institution

### Rationale

- The Smithsonian and Harvard models demonstrate that institutional trust requires governance structures that outlive individual leaders and technology platforms ([02-reference-models.md](02-reference-models.md)).
- Wikimedia's separation of foundation governance from project communities shows that governance independence protects mission integrity.
- A public brand (Nature & Culture) can evolve its experience without amending constitutional preservation commitments.

### Consequences

**Positive:**
- Mission protection survives leadership and technology changes
- Public brand can be designed for accessibility without compromising governance formality
- Clear accountability: Open Grace owns "what must be true"; Nature & Culture owns "what the public experiences"

**Negative:**
- Two institutional identities require careful communication
- Governance overhead before public launch
- Potential confusion if separation is not clearly documented

### References

- [01-mission.md](01-mission.md) — Sections 2, 3
- [04-system-diagram.md](04-system-diagram.md) — Section 5

---

## ADR-002: Governance-Experience Separation

| Field | Value |
|-------|-------|
| **Status** | Accepted |
| **Date** | 2026-06-22 |
| **Deciders** | Open Grace Architecture Office |

### Context

ADR-001 establishes two institutions. This ADR defines the architectural boundary between them.

### Decision

Open Grace governs through documents, policies, and standards — not through public software. Nature & Culture operates exclusively through the Experience Plane, consuming Platform Plane APIs. No Experience Plane component writes directly to Preservation storage.

### Rationale

- Direct write access from public interfaces creates security and integrity risks
- All content entering the canonical store must pass through Ingestion with provenance ([03-canonical-architecture.md](03-canonical-architecture.md), Section 4.2)
- Community contributions (Phase 14) flow through Ingestion, not around it

### Consequences

**Positive:**
- Provenance integrity guaranteed for all canonical objects
- Public experience can be rebuilt or replaced without affecting preservation
- Clear audit boundary between governance and operations

**Negative:**
- Community contributions have higher latency (ingestion pipeline)
- Additional API layer between experience and data

### References

- [03-canonical-architecture.md](03-canonical-architecture.md) — Sections 3, 5, 7
- [04-system-diagram.md](04-system-diagram.md) — Section 5

---

## ADR-003: Founder Build Order

| Field | Value |
|-------|-------|
| **Status** | Accepted |
| **Date** | 2026-06-22 |
| **Deciders** | Open Grace Architecture Office |

### Context

Limited resources at founding require a principled sequence for building 15 platform and experience capabilities. The temptation is to build public-facing experiences first to demonstrate value. However, experiences without preserved, modeled knowledge are hollow.

### Decision

Adopt the canonical founder build order:

Discovery → Ingestion → Preservation → Knowledge Modeling → Knowledge Graph → Search → Quality Platform → Research Fabric → Translation Fabric → Publishing → Public Experience → Products → Education → Community → Observatories

Phases may not be skipped. Public Experience (Phase 11) is deliberately late.

### Rationale

- Internet Archive and Harvard demonstrate that preservation infrastructure must precede access ([02-reference-models.md](02-reference-models.md))
- Europeana's aggregation model requires metadata and graph infrastructure before meaningful search
- National Geographic's public storytelling succeeds because Smithsonian-scale collections exist behind it
- Building Public Experience before Search and Publishing would deliver an empty portal

### Consequences

**Positive:**
- Every public feature is backed by real preserved knowledge
- Early phases build irreversible institutional assets (preserved objects, graph)
- Quality and provenance are structural, not retrofitted

**Negative:**
- No public launch until Year 5–6
- Requires patient capital and governance
- Founder must resist pressure to "launch something" prematurely

### References

- [06-build-roadmap.md](06-build-roadmap.md) — Sections 3, 4
- [04-system-diagram.md](04-system-diagram.md) — Section 4

---

## ADR-004: Unified Knowledge Graph

| Field | Value |
|-------|-------|
| **Status** | Accepted |
| **Date** | 2026-06-22 |
| **Deciders** | Open Grace Architecture Office |

### Context

Heritage, nature, and culture are typically siloed: museums use CIDOC-CRM, biodiversity uses Darwin Core, archives use RiC-O. Users experience the world as unified — a World Heritage site contains species, traditions, and artifacts in one place.

### Decision

Build a single unified Knowledge Graph spanning all three domains rather than three separate graphs with crosswalks.

### Rationale

- Google's Knowledge Graph demonstrates entity-centric unification across domains ([02-reference-models.md](02-reference-models.md))
- Wikidata proves a single graph can serve heterogeneous entity types at scale
- UNESCO's mandate explicitly spans natural and cultural heritage together
- Cross-domain queries ("species found at World Heritage sites with associated traditions") require unified graph, not federated crosswalks

### Consequences

**Positive:**
- Cross-domain discovery and search
- Single API for all experience plane consumers
- Reduced integration complexity

**Negative:**
- Ontology management complexity (CIDOC-CRM + Darwin Core coexistence)
- Larger graph database operational requirements
- Risk of lowest-common-denominator modeling if not carefully governed

### References

- [03-canonical-architecture.md](03-canonical-architecture.md) — Sections 4.4, 4.5
- [07-reference-standards.md](07-reference-standards.md) — Sections 4.1, 4.2

---

## ADR-005: 100-Year Architecture Horizon

| Field | Value |
|-------|-------|
| **Status** | Accepted |
| **Date** | 2026-06-22 |
| **Deciders** | Open Grace Architecture Office |

### Context

Institutional planning horizons range from quarterly (commercial) to perpetual (constitutional monarchies). A horizon too short produces technical debt that threatens preservation. A horizon too long prevents actionable planning.

### Decision

Adopt a **100-year canonical architecture horizon** with generational sub-horizons (10, 30, 100 years).

### Rationale

- Harvard Library's 400-year operation proves multi-century stewardship is achievable with correct governance ([02-reference-models.md](02-reference-models.md))
- Internet Archive's permanence ethic targets "forever" but plans concretely in decades
- 100 years spans ~3 technology generations (analog → digital → AI → unknown), sufficient for format migration planning
- Nature & Culture mission explicitly references "all future generations" ([01-mission.md](01-mission.md))

### Consequences

**Positive:**
- Format migration is planned, not reactive
- Technology choices evaluated for longevity
- Governance succession planned across generations

**Negative:**
- 100-year planning has inherent uncertainty
- May over-invest in durability at the expense of early velocity
- Requires periodic architecture refresh as assumptions age

### References

- [01-mission.md](01-mission.md) — Section 4
- [05-physical-architecture.md](05-physical-architecture.md) — Sections 3, 7
- [06-build-roadmap.md](06-build-roadmap.md) — Section 7

---

## ADR-006: Reference Model Synthesis

| Field | Value |
|-------|-------|
| **Status** | Accepted |
| **Date** | 2026-06-22 |
| **Deciders** | Open Grace Architecture Office |

### Context

No single existing institution covers the full scope of Nature & Culture's mission: permanent digital memory of heritage, nature, and culture, freely accessible in every language. The architecture must learn from proven institutions without replicating any one model.

### Decision

Adopt eleven canonical reference models (UNESCO, Smithsonian, GBIF, Europeana, Wikimedia, MIT, Stanford, Harvard, Google, Internet Archive, National Geographic) as non-binding design inputs, synthesized through the architecture layers defined in [03-canonical-architecture.md](03-canonical-architecture.md).

### Rationale

- Each reference model contributes proven patterns for specific architectural layers ([02-reference-models.md](02-reference-models.md), Section 14)
- Synthesis avoids single-institution blind spots (e.g., Google lacks preservation depth; Internet Archive lacks curatorial quality)
- Reference models provide evidence for ADRs, lending institutional credibility to design choices

### Consequences

**Positive:**
- Architecture grounded in proven practice, not theory
- Partner institutions recognize their contributions
- Design decisions are explainable to funders and governance bodies

**Negative:**
- Synthesis complexity — no off-the-shelf template to follow
- Risk of incoherence if patterns from incompatible models are combined without care
- Reference models may evolve independently, requiring periodic review

### References

- [02-reference-models.md](02-reference-models.md) — Full document
- [07-reference-standards.md](07-reference-standards.md) — Section 12

---

## ADR-007: Tiered Physical Storage

| Field | Value |
|-------|-------|
| **Status** | Accepted |
| **Date** | 2026-06-22 |
| **Deciders** | Open Grace Architecture Office |

### Context

Storing all digital objects on high-performance media is economically unsustainable at planetary scale. Storing everything on offline tape makes active access impossible. A tiering strategy is required.

### Decision

Implement four storage tiers (Hot, Warm, Cold, Deep) with automated lifecycle transitions and curatorial override, deployed across three minimum geographic zones (Alpha, Beta, Gamma).

### Rationale

- Harvard's special collections model demonstrates tiered access for objects of varying fragility and demand ([02-reference-models.md](02-reference-models.md))
- Internet Archive's physical vaults demonstrate offline survivability for deep archive
- Google's multi-region replication demonstrates geographic redundancy for active content
- OAIS Archival Storage function maps naturally to tiered storage ([07-reference-standards.md](07-reference-standards.md), Section 3)

### Consequences

**Positive:**
- Sustainable economics at scale
- Geographic and media redundancy
- Offline survivability for catastrophic scenarios

**Negative:**
- Retrieval latency increases with tier depth
- Lifecycle automation may prematurely tier actively curated objects without override
- Multi-zone operations complexity

### References

- [05-physical-architecture.md](05-physical-architecture.md) — Sections 3, 4
- [04-system-diagram.md](04-system-diagram.md) — Section 6

---

## ADR-008: Translation as Platform Capability

| Field | Value |
|-------|-------|
| **Status** | Accepted |
| **Date** | 2026-06-22 |
| **Deciders** | Open Grace Architecture Office |

### Context

Nature & Culture's mission requires content "in every language." Localization is typically treated as a UI concern — translating interface strings after the platform is built. This produces English-first architecture with translated surfaces.

### Decision

Translation Fabric is a **Platform Plane capability** (Phase 9), not an Experience Plane afterthought. It serves all layers: graph labels, search, publishing, and public experience.

### Rationale

- UNESCO's six official languages and Wikimedia's 300+ language editions demonstrate that multilingualism must be structural ([02-reference-models.md](02-reference-models.md))
- Entity labels in the Knowledge Graph must be multilingual for cross-lingual search to function
- Source-language content is always preserved; translations are additive with provenance
- Mission statement explicitly requires "every language" ([01-mission.md](01-mission.md))

### Consequences

**Positive:**
- True multilingual search and discovery
- Endangered languages can be supported through community translation
- No English-first bias in knowledge representation

**Negative:**
- Significant engineering investment before public launch
- Translation quality varies by language resource availability
- Graph complexity increases with multilingual labels

### References

- [03-canonical-architecture.md](03-canonical-architecture.md) — Section 4.9
- [06-build-roadmap.md](06-build-roadmap.md) — Phase 9
- [07-reference-standards.md](07-reference-standards.md) — Section 9

---

## ADR-009: OAIS Preservation Foundation

| Field | Value |
|-------|-------|
| **Status** | Accepted |
| **Date** | 2026-06-22 |
| **Deciders** | Open Grace Architecture Office |

### Context

Multiple preservation frameworks exist (OAIS, ISO 16363, TRAC, CoreTrustSeal). The architecture must adopt a reference model for preservation function definition.

### Decision

Adopt **OAIS (ISO 14721)** as the required preservation reference model, with PREMIS for preservation metadata and BagIt for ingest packaging.

### Rationale

- OAIS is the most widely adopted preservation reference model globally
- Harvard, MIT (DSpace), and Internet Archive all align with OAIS principles
- OAIS functional entities map directly to architecture layers ([07-reference-standards.md](07-reference-standards.md), Section 3.1)
- PREMIS and BagIt are OAIS-aligned standards with broad tool support
- 100-year durability requires a model designed for indefinite preservation

### Alternatives Considered

| Alternative | Why Not Selected |
|------------|-----------------|
| Custom preservation model | No institutional recognition; reinventing proven practice |
| ISO 16363 (audit only) | Audit standard, not functional model |
| CoreTrustSeal | Certification, not architecture |

### Consequences

**Positive:**
- Interoperability with partner archives and museums
- Proven migration and fixity patterns
- Preservation function clarity across teams

**Negative:**
- OAIS complexity may slow early development
- Some OAIS concepts (e.g., Submission Information Package) require careful mapping to modern cloud storage

### References

- [07-reference-standards.md](07-reference-standards.md) — Section 3
- [03-canonical-architecture.md](03-canonical-architecture.md) — Section 4.3
- [05-physical-architecture.md](05-physical-architecture.md) — Section 7

---

## ADR-010: Free Access Constitutional Commitment

| Field | Value |
|-------|-------|
| **Status** | Accepted |
| **Date** | 2026-06-22 |
| **Deciders** | Open Grace Architecture Office |

### Context

Digital heritage institutions face funding pressure to monetize collections. Paywalls, tiered access, and commercial licensing create revenue but contradict the mission of universal access.

### Decision

Canonical public memory is **freely accessible to every person** with no paywall. This is a constitutional commitment under Open Grace, not a business policy. Products (Phase 12) may generate revenue but must not gate access to canonical public memory.

### Rationale

- Wikimedia's radical accessibility demonstrates sustainability without paywalls ([02-reference-models.md](02-reference-models.md))
- Europeana's free access model enables cross-institutional discovery at scale
- MIT Open Access Policy establishes academic precedent for open knowledge
- Mission statement: "freely accessible to every person" ([01-mission.md](01-mission.md))
- Internet Archive's "Universal access to all knowledge" as institutional north star

### Consequences

**Positive:**
- Mission alignment is unambiguous and enforceable
- Partner institutions trust that contributed content remains public
- Community contributors participate without access barriers

**Negative:**
- Revenue model must come from Products and services, not content access
- Requires sustainable funding independent of content monetization
- Rights-restricted partner content may require careful handling (metadata public, bitstream restricted)

### References

- [01-mission.md](01-mission.md) — Sections 2, 6
- [03-canonical-architecture.md](03-canonical-architecture.md) — Sections 5.2, 9
- [06-build-roadmap.md](06-build-roadmap.md) — Phase 12

---

## 3. ADR Lifecycle

### 3.1 Creating a New ADR

1. Assign the next sequential ADR number
2. Write the ADR using the format in Section 1
3. Set status to **Proposed**
4. Submit to Architecture Office for review
5. Upon acceptance, set status to **Accepted** and add to the index

### 3.2 Superseding an ADR

1. Create a new ADR with the replacement decision
2. Set the old ADR status to **Superseded** with a link to the new ADR
3. Update affected canonical documents

### 3.3 ADRs Are Immutable

Once Accepted, ADR content is not edited. Corrections, reversals, or refinements require a new ADR that supersedes the original.

---

## 4. Decision Record Authority

The Open Grace Architecture Office is the sole authority for accepting, superseding, or deprecating ADRs. ADRs constitute institutional memory and must be preserved in the governance zone ([05-physical-architecture.md](05-physical-architecture.md), Section 9.1).

---

*Previous: [07-reference-standards.md](07-reference-standards.md) · Return to: [01-mission.md](01-mission.md)*
