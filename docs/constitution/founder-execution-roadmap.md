# Founder Execution Roadmap

| Field | Value |
|-------|-------|
| **Version** | 1.1 |
| **Status** | Execution Companion |
| **Authority** | Open Grace Architecture Office |
| **Date** | 2026-06-22 |

## Document Map

| Document | Purpose |
|----------|---------|
| [01-mission-and-constitutional-charter.md](../architecture/canonical/01-mission-and-constitutional-charter.md) | Mission, charter, and constitutional relationship |
| [03-canonical-architecture.md](../architecture/canonical/03-canonical-architecture.md) | Canonical 100-year logical architecture |
| [04-system-diagram.md](../architecture/canonical/04-system-diagram.md) | Canonical system diagram |
| [06-build-roadmap.md](../architecture/canonical/06-build-roadmap.md) | **Canonical** founder build order (ADR-003) |
| [08-decision-record.md](../architecture/canonical/08-decision-record.md) | Architecture decision records |
| [founder-execution-roadmap.md](founder-execution-roadmap.md) | Founder-generation execution guidance (this document) |

---

## 1. Purpose

This document provides **founder-generation execution guidance** for implementing the canonical build order. It records engineering substrate choices, milestone gate procedures, and execution constraints for the first institutional generation.

**Canonical authority for phase order:** [06-build-roadmap.md](../architecture/canonical/06-build-roadmap.md), binding per [ADR-003](../architecture/canonical/08-decision-record.md#adr-003-founder-build-order). All architecture, capability definitions, and phase specifications reside under `docs/architecture/canonical/`. This companion document does not define phase order and may not introduce alternate sequencing.

Mission and mandate derive from [01-mission-and-constitutional-charter.md](../architecture/canonical/01-mission-and-constitutional-charter.md). Logical capability definitions are in [03-canonical-architecture.md](../architecture/canonical/03-canonical-architecture.md).

---

## 2. Founder Build Order (ADR-003)

The founder build order comprises **fifteen phases**, canonical and sequential. Phases may not be skipped. Full specifications: [06-build-roadmap.md](../architecture/canonical/06-build-roadmap.md), Section 3–4.

```
 1. Discovery
 2. Ingestion
 3. Preservation
 4. Knowledge Modeling
 5. Knowledge Graph
 6. Search
 7. Quality Platform
 8. Research Fabric
 9. Translation Fabric
10. Publishing
11. Public Experience
12. Products
13. Education
14. Community
15. Observatories
```

---

## 3. Founder Demonstration Surface

During **Phases 1–3** (Discovery, Ingestion, Preservation), the institution MAY operate a **Founder Demonstration Surface** — a restricted, steward-operated preview used to demonstrate the provenance chain and institutional identity to funders, partners, and gate reviewers.

The Founder Demonstration Surface is **not** Public Experience (Phase 11). The term **Website MVP** is superseded by this definition.

| Constraint | Requirement |
|------------|-------------|
| **Purpose** | Demonstrate source → discovery → acquisition → preservation chain; institutional charter visibility |
| **Scope** | Read-only browse of discovery and acquisition records with provenance disclaimers |
| **Access** | Steward-gated deployment; no marketing launch or public-experience success criteria |
| **Accessibility** | WCAG 2.1 Level A minimum (Level AA required at Phase 11) |
| **Data** | No canonical write path from the demonstration surface; all writes through Ingestion |
| **Phase gate** | Does not satisfy Phase 11 completion criteria or substitute for Public Experience |

Founder Demonstration Surface completion evidence may support Phase 1–3 milestone gates only. See [06-build-roadmap.md](../architecture/canonical/06-build-roadmap.md), Section 3.1.

---

## 4. Founder Engineering Substrate

Founder-generation implementation choices are documented in [04-system-diagram.md](../architecture/canonical/04-system-diagram.md), Section 2.1. These are technology-generation expressions; capability contracts in [03-canonical-architecture.md](../architecture/canonical/03-canonical-architecture.md) persist across stack refresh.

| Phase range | Execution substrate (founder generation) |
|-------------|------------------------------------------|
| **1–3** | PostgreSQL (metadata, registries, workflow state); FastAPI service layer; Source Registry; Acquisition Pipeline; optional Founder Demonstration Surface |
| **4–5** | PostGIS extensions; GBIF IPT and Darwin Core normalization; graph cluster deployment |
| **6–10** | OpenSearch indexing; translation pipeline; publishing workflow |
| **11–15** | Global CDN; mobile clients; observatory ingestion pipelines |

Successor generations replace implementations while preserving registry, graph, and provenance semantics.

---

## 5. Founder Principle

> **Build the smallest useful capability stack before expanding.**

Every phase must deliver the **minimum viable institutional capability** — complete enough to satisfy completion criteria and milestone gates, narrow enough to avoid premature breadth. New phases may not begin until prerequisite phases pass gate review per [06-build-roadmap.md](../architecture/canonical/06-build-roadmap.md), Section 6.

---

## 6. Milestone Gates

No phase may advance until its milestone gate passes. Gate review is conducted by the Open Grace Architecture Office with stewardship sign-off.

### 6.1 Universal Gate Requirements

| Gate Dimension | Requirement |
|----------------|-------------|
| **Completion** | Phase success criteria met per [06-build-roadmap.md](../architecture/canonical/06-build-roadmap.md), Section 4 |
| **Provenance** | Every entity and object in scope traces to registered source with audit trail |
| **Standards** | Compliance verified against [07-reference-standards.md](../architecture/canonical/07-reference-standards.md) |
| **Architecture** | Capability contracts documented; deviations recorded in [08-decision-record.md](../architecture/canonical/08-decision-record.md) |
| **Security** | Threat model reviewed; steward authentication and authorization verified |
| **Succession** | Runbooks, schema documentation, and operational knowledge deposited for successor generation |
| **Review** | Architecture Office written sign-off |

### 6.2 Phase Transition Rules

| Rule | Description |
|------|-------------|
| **No skipping** | Phases may not be skipped per ADR-003 |
| **Dependency gating** | A phase may begin only when listed dependencies have passed milestone gates |
| **Controlled overlap** | Preparatory work on phase *N+1* permitted before phase *N* completes; production deployment requires phase *N* gate passage |
| **Amendment** | Changes to phase order require constitutional-level ADR |

### 6.3 Gate Review Artifact

Each gate review produces a **Milestone Gate Record**: phase identifier, review date, criteria checklist, evidence references, conditions (if conditional pass), and signatory authority.

---

## 7. Roadmap Horizons

| Horizon | Approximate Period | Institutional Focus |
|---------|-------------------|---------------------|
| **Founder Generation** | Years 1–15 | Complete ADR-003 fifteen-phase stack; Public Experience (Phase 11); initial observatory network (Phase 15) |
| **Expansion Generation** | Years 15–35 | Partner federation, language coverage, sovereignty zones; first major technology migration |
| **Consolidation Generation** | Years 35–60 | Graph and corpus scale; succession governance; vault media refresh |
| **Permanence Generation** | Years 60–100 | Continuous operation; covenant renewal; generational knowledge transfer |

Horizons are indicative. Phase completion is governed by milestone gates, not calendar deadlines.

---

## 8. Dependencies on Open Grace

Before Phase 1 begins, Open Grace must establish:

1. Constitutional charter ratified ([01-mission-and-constitutional-charter.md](../architecture/canonical/01-mission-and-constitutional-charter.md))
2. Architecture Office operational
3. Standards registry initialized ([07-reference-standards.md](../architecture/canonical/07-reference-standards.md))
4. Initial ADRs filed ([08-decision-record.md](../architecture/canonical/08-decision-record.md))
5. First partner covenants signed

---

## 9. Document Authority

| Document | Authority |
|----------|-----------|
| [06-build-roadmap.md](../architecture/canonical/06-build-roadmap.md) | **Canonical** phase order, specifications, and success criteria (ADR-003) |
| This document | Execution companion only; engineering substrate and gate procedures |

Changes to phase order require an ADR in [08-decision-record.md](../architecture/canonical/08-decision-record.md). Updates to execution notes in this document require Architecture Office approval and must not alter ADR-003 phase order or [06-build-roadmap.md](../architecture/canonical/06-build-roadmap.md) success criteria.

---

*Companion to: [06-build-roadmap.md](../architecture/canonical/06-build-roadmap.md) · Authority: [docs/architecture/canonical/](../architecture/canonical/)*
