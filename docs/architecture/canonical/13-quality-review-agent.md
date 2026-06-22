# Quality Review Agent

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Status** | Canonical |
| **Authority** | Open Grace Architecture Office |
| **Date** | 2026-06-22 |
| **Capability** | Quality Platform ([03-canonical-architecture.md](03-canonical-architecture.md), §4.7) |
| **Phase** | Quality Platform ([06-build-roadmap.md](06-build-roadmap.md), Phase 7) |

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

The **Quality Review Agent** automates the Quality Platform capability ([03-canonical-architecture.md](03-canonical-architecture.md), §4.7). It evaluates canonical entities, preserved objects, and contributor submissions for metadata quality, rights clearance, accessibility compliance, and content completeness; assigns machine-generated quality scores; and routes flagged items to curatorial review queues as **Quality Review Records** (JSON-LD) for human disposition before publication or research-channel release.

The agent does not publish content, override curatorial decisions, or write canonical quality annotations without steward approval. It assesses, scores, and queues; curators decide.

---

## 2. Responsibilities

| Responsibility | Description |
|----------------|-------------|
| **Metadata quality** | Validate schema conformance, required-field completeness, authority reconciliation, and provenance metadata against institutional profiles (Dublin Core, LIDO, MODS, Darwin Core); flag anomalies, stale values, and missing cross-references |
| **Rights review** | Validate machine-readable rights statements (RightsStatements.org, Creative Commons); detect missing, ambiguous, or conflicting rights metadata; route clearance-required items to rights stewards |
| **Accessibility review** | Verify WCAG 2.1 AA readiness for published-facing content: alt text, captions, transcripts, color contrast signals, heading structure, and locale-aware text alternatives |
| **Content completeness** | Score entity and object completeness across descriptive text, media surrogates, taxonomic or cultural context, geographic and temporal anchors, and translation coverage against publication thresholds |

---

## 3. Reference Models

The agent synthesizes patterns from two primary reference models ([02-reference-models.md](02-reference-models.md)):

| Model | Pattern Applied | Agent Behavior |
|-------|-----------------|----------------|
| **Smithsonian** | Collection stewardship at scale, conservation metadata, interdisciplinary cataloging, institutional trust through systematic review | Apply collection-wide metadata profiles; enforce provenance and condition metadata checks; score catalog completeness across natural history and cultural heritage object types |
| **Harvard** | Curatorial authority, centuries-scale stewardship, special-collections handling, curatorial workflow as quality gate | Route high-significance and restricted items to expert review queues; apply tiered review depth by collection sensitivity; preserve audit trails for every quality disposition |

Supporting standards alignment follows [07-reference-standards.md](07-reference-standards.md): PREMIS (audit events), SKOS (authority reconciliation), RightsStatements.org and Creative Commons (rights), WCAG 2.1 (accessibility).

---

## 4. Position in Architecture

```
Knowledge Graph + Preservation descriptors + contributor submissions
        ↓
Quality Review Agent
        ↓
Quality scores + review queues + clearance flags + completeness reports
        ↓
Steward review (curator, rights officer, accessibility reviewer)
        ↓
Quality Annotations written to Knowledge Graph (approved only)
        ↓
Publishing, Research Fabric, Public Experience
```

The agent operates in the **Quality** subgraph of the Platform Plane ([04-system-diagram.md](04-system-diagram.md), §2). All outputs pass through the AI Fabric governance chain before affecting canonical systems ([04-system-diagram.md](04-system-diagram.md), §2.2).

**Upstream inputs:** Knowledge Graph entities ([12-knowledge-graph-agent.md](12-knowledge-graph-agent.md)), deduplication and integrity signals from the Knowledge Graph Agent, preserved object metadata from Ingestion and Preservation, contributor submissions from Community.

**Downstream consumers:** Publishing (editorial gates), Research Fabric (dataset clearance), Public Experience (publication eligibility), Observatories (quality metrics).

---

## 5. Review Domains

### 5.1 Metadata Quality

| Attribute | Specification |
|-----------|---------------|
| **Inputs** | Entity RDF triples, Dublin Core / MODS / LIDO descriptors, Darwin Core records, PREMIS events |
| **Checks** | Required-field coverage, datatype validity, authority-file alignment (SKOS), temporal and geographic consistency, provenance chain completeness |
| **Output signals** | Metadata quality score (0–100), field-level deficiency list, authority reconciliation suggestions |
| **Standards** | Dublin Core, LIDO (Permitted), MODS (Recommended), Darwin Core, PREMIS, SKOS ([07-reference-standards.md](07-reference-standards.md)) |

### 5.2 Rights Review

| Attribute | Specification |
|-----------|---------------|
| **Inputs** | Rights metadata on entities and preserved objects, partner covenant constraints, license URIs |
| **Checks** | Presence and parseability of rights statements; consistency between declared rights and reuse intent; restriction flags (embargo, cultural sensitivity, partner withholding) |
| **Output signals** | Rights clearance status (`cleared`, `restricted`, `pending`, `ambiguous`), steward queue assignment, publication block flags |
| **Standards** | RightsStatements.org, Creative Commons, EDM rights expressions ([07-reference-standards.md](07-reference-standards.md)) |

### 5.3 Accessibility Review

| Attribute | Specification |
|-----------|---------------|
| **Inputs** | Published-facing text, IIIF manifests, image and AV surrogates, UI-bound entity summaries |
| **Checks** | Alt text presence and quality, caption and transcript coverage, heading hierarchy, contrast heuristics, keyboard-navigable structure signals, `hreflang` and locale coverage |
| **Output signals** | Accessibility compliance score, WCAG 2.1 AA violation list, remediation recommendations |
| **Standards** | WCAG 2.1 AA, HTML5, IIIF, hreflang ([07-reference-standards.md](07-reference-standards.md)) |

### 5.4 Content Completeness

| Attribute | Specification |
|-----------|---------------|
| **Inputs** | Entity graph neighborhood, media surrogates, descriptive narratives, translation records |
| **Checks** | Minimum descriptive depth by entity type, media surrogate availability, cross-domain relationship coverage, translation tier coverage against institutional thresholds |
| **Output signals** | Completeness score by dimension (description, media, context, locale), publication-readiness tier (`draft`, `review`, `ready`, `blocked`) |
| **Standards** | Institutional completeness profiles per entity type; Translation Fabric provenance tiers ([03-canonical-architecture.md](03-canonical-architecture.md), §4.9) |

---

## 6. Outputs

### 6.1 Quality Scores

Each reviewed entity or object receives:

- Composite quality score (weighted across metadata, rights, accessibility, completeness)
- Dimension scores with threshold pass/fail against Phase 7 targets
- Review timestamp, agent version, and input snapshot hash
- Link to originating entity URI or preservation identifier

### 6.2 Quality Review Records

Each flagged or queued item is emitted as **JSON-LD** with:

| Field | Requirement |
|-------|-------------|
| **Entity reference** | Canonical entity URI or preservation object identifier |
| **Review domain** | `metadata`, `rights`, `accessibility`, `completeness`, or `composite` |
| **Severity** | `info`, `warning`, `blocker` |
| **Finding** | Machine- and human-readable description of the deficiency |
| **Recommended action** | Remediation step, steward role, or escalation path |
| **Provenance** | Review run identifier, agent version, upstream signals consumed |

Quality Review Records are **recommendations** until a steward approves disposition and any resulting Quality Annotations.

### 6.3 Curation Queue Entries

Queue items routed to role-specific dashboards:

| Queue | Steward Role | Trigger Examples |
|-------|--------------|------------------|
| **Metadata** | Cataloger / data steward | Missing required fields, authority conflicts, provenance gaps |
| **Rights** | Rights officer | Ambiguous license, embargo expiry, partner restriction |
| **Accessibility** | Accessibility reviewer | Missing alt text, no transcript, contrast failure |
| **Editorial** | Curator | Low completeness score, cultural sensitivity, high-significance object |

### 6.4 Quality Annotations (approved writes)

After steward approval, persisted graph annotations include:

- Approved quality score and dimension breakdown
- Disposition (`accepted`, `corrected`, `restricted`, `withdrawn`)
- Steward identity and review timestamp (PREMIS-aligned audit event)
- Remediation actions taken and residual flags

---

## 7. AI Fabric Governance

| Gate | Requirement |
|------|-------------|
| **Agent Registry** | Agent version, scoring profiles, review thresholds, and queue routing rules registered before production runs |
| **Benchmarks** | Scoring consistency, false-blocker rate, rights classification accuracy, accessibility detection recall, steward turnaround impact |
| **Evaluations** | Periodic review against Phase 7 success criteria and constitution Quality Platform completion criteria |
| **Safety Reviews** | Verify agent does not auto-publish restricted content, bypass rights gates, or downgrade curatorial holds |
| **Human Approval** | Curators, rights officers, and accessibility reviewers approve dispositions and Quality Annotation writes |

**Council assignment:** Implementation Council (scoring pipelines, queue integration) and Research Council (completeness profiles, authority reconciliation rules). Execution Council runs scheduled review sweeps and regression benchmarks.

---

## 8. Phase Alignment

| Phase | Agent Scope |
|-------|-------------|
| **Knowledge Graph (Phase 5)** | Receive entity inventory; begin metadata quality and completeness scoring on graph entities |
| **Search (Phase 6)** | Coordinate publication-readiness signals with search index eligibility rules |
| **Quality Platform (Phase 7)** | Full metadata, rights, accessibility, and completeness review; curation queues operational; quality annotations written back to graph |
| **Publishing (Phase 10)** | Enforce editorial gates: no exhibit or story package publishes without cleared Quality Review Record |
| **Community (Phase 14)** | Review contributor submissions before graph admission; feed moderation queues |

---

## 9. Success Criteria

Aligned with Quality Platform phase completion criteria ([06-build-roadmap.md](06-build-roadmap.md)) and constitution Phase 4 Quality Platform criteria:

- Quality scores assigned to ≥ 80% of graph entities
- Rights Review workflow operational; no entity published without declared rights status
- Accessibility Review process documented; ≥ 95% of published field guide and site content passes WCAG 2.1 AA
- Editorial Review queue operational; median steward turnaround within institutional SLA
- Duplicate entity rate < 2% (coordinated with Knowledge Graph Agent deduplication)
- Quality annotations persisted in provenance chain with PREMIS-aligned audit events
- End-to-end demonstration: entity → agent review → steward disposition → quality annotation → publication gate

---

## 10. Constraints

- **No publication without clearance.** The agent enforces gates; stewards grant clearance. Automated pass is permitted only for pre-approved entity types and score thresholds registered in Agent Registry.
- **Curatorial authority is final.** Follow Harvard's curatorial workflow pattern ([02-reference-models.md](02-reference-models.md), §10): expert judgment overrides machine scores on significance, authenticity, and cultural sensitivity.
- **Rights before reuse.** Follow Europeana and Smithsonian rights-expression patterns ([02-reference-models.md](02-reference-models.md), §4, §6): ambiguous rights block publication and research export.
- **Provenance chain intact.** Every quality score and annotation traces to a review run, agent version, and steward disposition ([03-canonical-architecture.md](03-canonical-architecture.md), Provenance).
- **Knowledge Graph Agent coordination.** Deduplication candidates originate from the Knowledge Graph Agent; Quality Review Agent owns clearance workflow and writes approved quality annotations ([12-knowledge-graph-agent.md](12-knowledge-graph-agent.md), §10).
- **Quality precedes experience.** No entity enters public browse or research channels without passing Quality Platform gates (ADR-003, [08-decision-record.md](08-decision-record.md)).
