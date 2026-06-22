# Standards Agent

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Status** | Canonical |
| **Authority** | Open Grace Architecture Office |
| **Date** | 2026-06-22 |
| **Capability** | Standards Registry ([03-canonical-architecture.md](03-canonical-architecture.md), §3) |
| **Phase** | Cross-cutting; milestone gates from Knowledge Modeling onward ([06-build-roadmap.md](06-build-roadmap.md)) |

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
| [17-language-observatory-agent.md](17-language-observatory-agent.md) | Language Observatory Agent specification |
| [18-standards-agent.md](18-standards-agent.md) | Standards Agent specification |

---

## 1. Purpose

The **Standards Agent** automates compliance verification against the Open Grace Standards Registry ([07-reference-standards.md](07-reference-standards.md)). It runs structural and semantic conformance checks for binding metadata and web-facing standards; aggregates pass/fail signals across platform pipelines; and emits **Standards Compliance Reports** (JSON-LD) for Architecture Office review before milestone gates advance.

The agent does not modify canonical metadata, waive Required-standard failures, or substitute for Architecture Office judgment on Recommended standards. It verifies, scores, and reports; stewards and the Architecture Office decide disposition.

---

## 2. Responsibilities

| Responsibility | Description |
|----------------|-------------|
| **CIDOC-CRM conformance** | Verify heritage entity assertions against CRM class bindings, event-centric provenance patterns, and institutional SHACL shapes; measure crosswalk coverage and mapping provenance completeness |
| **Darwin Core conformance** | Verify biodiversity records and DwC-A packages against Darwin Core term constraints, coordinate and date formats, and taxonomic field consistency; flag GBIF backbone linkage gaps |
| **Schema.org conformance** | Verify web-facing JSON-LD outputs against schema.org type assignments, required property coverage, and authority identifier alignment for search and publishing surfaces |
| **Milestone gate reporting** | Aggregate automated compliance results per phase; surface Required-standard blockers and Recommended-standard gaps for Architecture Office review ([07-reference-standards.md](07-reference-standards.md), §14) |

---

## 3. Reference Models

The agent applies institutional patterns from [02-reference-models.md](02-reference-models.md) and adoption levels from [07-reference-standards.md](07-reference-standards.md):

| Model | Pattern Applied | Agent Behavior |
|-------|-----------------|----------------|
| **Smithsonian** | Interdisciplinary cataloging with domain-faithful metadata profiles | Enforce heritage-domain CRM bindings without collapsing museum object semantics into generic descriptive fields |
| **GBIF** | Darwin Core as the interoperability contract for biodiversity data | Validate DwC term usage, occurrence geometry, and taxonomic name fields against backbone reconciliation expectations |
| **Google** | schema.org as the web entity vocabulary for discoverable structured data | Verify JSON-LD entity pages, encyclopedia articles, and publication packages expose correct schema.org types and linked identifiers |

**Boundary with sibling agents:**

| Agent | Scope |
|-------|-------|
| [Metadata Agent](10-metadata-agent.md) | Per-record normalization, field mapping, and ingest-time schema validation |
| [Quality Review Agent](13-quality-review-agent.md) | Institutional quality scoring (completeness, rights, accessibility, editorial readiness) |
| **Standards Agent** | Registry-level conformance verification and milestone gate evidence |

---

## 4. Position in Architecture

```
Standards Registry ([07-reference-standards.md](07-reference-standards.md))
        ↓
Entity Assertions + publication packages + API contracts + validator artifacts
        ↓
Standards Agent
        ↓
Conformance checks (CIDOC-CRM, Darwin Core, schema.org) + coverage metrics
        ↓
Standards Compliance Reports — candidate, pending Architecture Office review
        ↓
Milestone gates · Architecture Office · partner audit evidence
        ↑
Metadata Agent validation reports · Quality Review signals · Publishing outputs
```

The agent operates in the **Constitutional** subgraph of the Open Grace plane ([04-system-diagram.md](04-system-diagram.md), §2). All outputs pass through the AI Fabric governance chain ([04-system-diagram.md](04-system-diagram.md), §2.2).

**Upstream inputs:** Metadata Agent validation reports ([10-metadata-agent.md](10-metadata-agent.md)), Knowledge Graph entity inventories ([12-knowledge-graph-agent.md](12-knowledge-graph-agent.md)), Publishing Agent publication packages ([15-publishing-agent.md](15-publishing-agent.md)), registered SHACL shapes and JSON Schema profiles.

**Downstream consumers:** Architecture Office milestone reviews, partner covenant audits, build-roadmap phase gates ([06-build-roadmap.md](06-build-roadmap.md)).

---

## 5. Conformance Checks

### 5.1 CIDOC-CRM (Heritage and Culture)

| Attribute | Specification |
|-----------|---------------|
| **Adoption level** | Required ([07-reference-standards.md](07-reference-standards.md), §4.1) |
| **Inputs** | Heritage entity RDF triples, LIDO/EDM source mappings, Metadata Agent CRM crosswalk tables, institutional SHACL shape sets |
| **Checks** | Valid CRM class assignment (`E22 Man-Made Object`, `E53 Place`, `E39 Actor`, `E5 Event`, and extensions); legal `crm:P*` predicate usage; required identity, place, temporal, and actor bindings per shape; event-centric provenance chain presence; source-to-CRM mapping provenance retained |
| **Validators** | SHACL 1.1; CRM namespace and range/domain rules; institutional heritage profiles |
| **Output signals** | CRM conformance score (0–100), shape violation list, unmapped heritage field inventory, crosswalk coverage percentage |
| **Failure severity** | Required-standard violation → milestone blocker |

### 5.2 Darwin Core (Nature and Biodiversity)

| Attribute | Specification |
|-----------|---------------|
| **Adoption level** | Required ([07-reference-standards.md](07-reference-standards.md), §4.2) |
| **Inputs** | DwC-A archives, occurrence and taxon entity assertions, GBIF IPT export samples, Metadata Agent DwC validation reports |
| **Checks** | Darwin Core term vocabulary conformance (`dwc:scientificName`, `dwc:decimalLatitude`, `dwc:decimalLongitude`, `dwc:eventDate`, `dwc:countryCode`, and institutional required-term profiles); coordinate range validity; ISO 8601 date parsing; taxonomic rank and name authorship consistency; DwC-A star schema and core/extension integrity |
| **Validators** | Darwin Core term constraints; DwC-A structural validators; GBIF data-quality rule subsets where applicable |
| **Output signals** | DwC conformance score (0–100), term-level violation list, taxonomic parsing failures, backbone linkage gap report |
| **Failure severity** | Required-standard violation → milestone blocker |

### 5.3 Schema.org (Web-Facing Structured Data)

| Attribute | Specification |
|-----------|---------------|
| **Adoption level** | Recommended ([07-reference-standards.md](07-reference-standards.md), §4.1) |
| **Inputs** | Public entity pages, encyclopedia articles, field guide entries, publication JSON-LD packages, search result entity panels |
| **Checks** | Valid JSON-LD syntax; `https://schema.org` context and type declarations; type appropriateness (`schema:Place`, `schema:Taxon`, `schema:CreativeWork`, `schema:MuseumObject`, `schema:Event`, and institutional type map); required property coverage per type profile (`name`, `identifier`, `description`, `sameAs`, `geo`/`location` where applicable); consistency between schema.org surface identifiers and canonical authority URIs |
| **Validators** | JSON-LD processor; schema.org type/property profiles; institutional web-entity mapping table |
| **Output signals** | schema.org conformance score (0–100), type mismatch list, missing-property inventory, identifier alignment warnings |
| **Failure severity** | Recommended-standard gap → Architecture Office review; does not alone block phase progression unless elevated to Required by ADR |

---

## 6. Outputs

### 6.1 Standards Compliance Reports

Each verification run emits **JSON-LD** with:

| Field | Requirement |
|-------|-------------|
| **Standard** | `CIDOC-CRM`, `Darwin-Core`, or `Schema.org` |
| **Scope** | Corpus slice, entity type, pipeline stage, or milestone gate identifier |
| **Adoption level** | `Required` or `Recommended` per [07-reference-standards.md](07-reference-standards.md) |
| **Conformance score** | 0–100 weighted by check severity |
| **Pass/fail** | Aggregate result with per-check breakdown |
| **Violations** | Machine- and human-readable finding list with remediation pointers |
| **Coverage metrics** | Crosswalk coverage, term usage distribution, type mapping completeness |
| **Provenance** | Verification run identifier, validator versions, agent version, input snapshot hash |

Reports are **evidence artifacts** until the Architecture Office accepts them for milestone gate progression.

### 6.2 Milestone Gate Summaries

Per build phase ([06-build-roadmap.md](06-build-roadmap.md)):

- Required-standard pass rate against institutional threshold
- Open blocker inventory with owning remediation agent or council
- Recommended-standard gap register for Architecture Office prioritization
- Trend deltas from prior verification runs

### 6.3 Remediation Routing

| Finding class | Routed to |
|---------------|-----------|
| CRM shape violations, unmapped heritage fields | Metadata Agent crosswalk maintainers; Implementation Council |
| DwC term or DwC-A structural failures | Metadata Agent biodiversity adapters; GBIF integration owners |
| schema.org type or property gaps | Publishing Agent; Public Experience structured-data owners |
| Registry-level profile gaps | Architecture Office Standards Review |

---

## 7. AI Fabric Governance

| Gate | Requirement |
|------|-------------|
| **Agent Registry** | Validator versions, SHACL shape sets, DwC profiles, schema.org type maps, and milestone thresholds registered before production runs |
| **Benchmarks** | False-pass rate on known non-conformant fixtures; check reproducibility; coverage metric stability |
| **Evaluations** | Periodic review against phase success criteria and [07-reference-standards.md](07-reference-standards.md) §14 compliance model |
| **Safety Reviews** | Verify agent cannot auto-waive Required failures, alter source metadata, or mark milestones passed without Architecture Office acceptance |
| **Human Approval** | Architecture Office accepts Compliance Reports for milestone gates; waivers require ADR ([08-decision-record.md](08-decision-record.md)) |

**Council assignment:** Architecture Council (profiles, adoption interpretation) and Implementation Council (validator pipelines). Research Council advises on ontology version upgrades and new standard adapters.

---

## 8. Phase Alignment

| Phase | Agent Scope |
|-------|-------------|
| **Knowledge Modeling (Phase 4)** | CIDOC-CRM and Darwin Core checks on pilot corpora; baseline crosswalk coverage metrics |
| **Knowledge Graph (Phase 5)** | Graph-wide CRM and DwC conformance sweeps on approved entity types |
| **Search (Phase 6)** | schema.org checks on entity panel JSON-LD and search surface structured data |
| **Quality Platform (Phase 7)** | Coordinate with Quality Review Agent; separate institutional quality from registry conformance |
| **Publishing (Phase 10)** | schema.org verification on encyclopedia, field guide, and book publication packages |
| **All phases** | Milestone gate summaries per [06-build-roadmap.md](06-build-roadmap.md) and [07-reference-standards.md](07-reference-standards.md) §14 |

---

## 9. Success Criteria

Aligned with standards compliance verification ([07-reference-standards.md](07-reference-standards.md), §14) and Knowledge Modeling phase targets ([06-build-roadmap.md](06-build-roadmap.md)):

- CIDOC-CRM SHACL validation operational on ≥ 5 heritage entity types with documented crosswalks
- Darwin Core validation operational on occurrence, taxon, and DwC-A pilot corpora
- schema.org validation operational on web-facing entity and publication JSON-LD outputs
- ≥ 80% Required-standard pass rate on pilot partner metadata corpora (coordinated with Metadata Agent)
- Milestone gate reports generated automatically for Phases 4–7 with Architecture Office review workflow
- End-to-end demonstration: corpus ingest → Metadata Agent validation → Standards Agent conformance report → Architecture Office gate acceptance

---

## 10. Constraints

- **Required standards are non-negotiable.** CIDOC-CRM and Darwin Core failures block milestone progression unless waived by ADR.
- **No canonical writes.** The agent reads platform outputs and emits reports; it does not modify entity assertions or publication packages.
- **Registry is authoritative.** Check profiles derive from [07-reference-standards.md](07-reference-standards.md); deviations require ADR.
- **Distinct from quality review.** Institutional completeness, rights, and accessibility remain Quality Review Agent responsibilities ([13-quality-review-agent.md](13-quality-review-agent.md)).
- **Source fidelity preserved.** Conformance checks evaluate canonical representations; original source literals remain authoritative per Metadata Agent constraints ([10-metadata-agent.md](10-metadata-agent.md), §11).
- **Partner audit readiness.** Reports must be exportable as evidence for covenant compliance and external institutional review.

---

*Previous: [17-language-observatory-agent.md](17-language-observatory-agent.md) · Next: [04-system-diagram.md](04-system-diagram.md)*
