# Governance Consistency Audit

| Field | Value |
|-------|-------|
| **Status** | Audit report |
| **Date** | 2026-06-22 |
| **Scope** | `docs/governance/`, `docs/architecture/canonical/`, canonical agent specifications, capability registry, Unified Compliance Model |
| **Authority reviewed** | ADR-011 Architecture Freeze v1.0; Architecture Registry; Capability Registry; Agent Checks Registry; AI Fabric governance chain |
| **Architecture effect** | None - audit only |

Architecture v1.0 remains frozen. This report audits documentation consistency only. It does not modify Architecture v1.0, the governance model, ADRs, registries, or agent specifications, and it does not introduce capabilities or require an ADR.

---

## 1. Executive Summary

The governance and agent documentation shows a strong compliance pattern for the registered 09-23 agent fleet, but it is not yet fully consistent across the post-freeze governance-agent layer and registry surface.

The main consistency gap is that `unified-compliance-model.md` was not found in the repository. As a result, the Unified Compliance Model must be inferred from:

- [04-system-diagram.md](../architecture/canonical/04-system-diagram.md) lines 203-236: AI Fabric sequence of Agent Registry, Benchmarks, Evaluations, Safety Reviews, and Human Approval
- [23-benchmark-agent.md](../architecture/canonical/23-benchmark-agent.md) lines 123-154: architecture compliance checks and registered canonical fleet
- [agent-checks-registry.md](../governance/agent-checks-registry.md) lines 17-55: Evidence, Provenance, Compliance, and Benchmark normalization
- [capability-registry.md](../governance/capability-registry.md) lines 24-59: capability ownership, Draft/Operational posture, and human approval summaries
- [08-decision-record.md](../architecture/canonical/08-decision-record.md) lines 523-561: ADR-011 freeze decision and consequences
- [architecture-registry.md](../governance/architecture-registry.md) lines 15-32: approved Architecture v1.0 entry and change-control sequence

**Overall compliance score:** 67 / 100

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Responsibility ownership | 74 | Most 09-23 agents have clear ownership; 24-25 and planned 26-35 have incomplete registry/check ownership. |
| Duplicate ownership control | 61 | Several overlaps are intentional but not consistently boundary-mapped. |
| Missing ownership control | 58 | Evaluations, Safety Reviews, Agent Registry operations, and 24+ check ownership are not fully assigned. |
| Governance sequence compliance | 64 | 09-23 follow the AI Fabric sequence; 24-25 are Draft and lack full sequence normalization. |
| Boundary rule compliance | 70 | No-write and steward-gate rules are strong in many specs, but observatory graph-write terminology is uneven. |
| ADR-011 / freeze compliance | 68 | Core freeze is cited, but post-freeze registry/spec expansion creates unresolved documentation tension. |
| Reference integrity | 62 | The new audit report avoids broken links; existing Research Agent and future-spec references still contain missing targets. |

---

## 2. Audit Method

### 2.1 Files and areas reviewed

| Area | Files reviewed |
|------|----------------|
| Governance registries | [architecture-registry.md](../governance/architecture-registry.md), [capability-registry.md](../governance/capability-registry.md), [agent-checks-registry.md](../governance/agent-checks-registry.md) |
| Governance reports | [constitutional-validation-report.md](../governance/constitutional-validation-report.md), [p0-remediation-report.md](../governance/p0-remediation-report.md), [agent-checks-audit-remediation.md](../governance/remediation/agent-checks-audit-remediation.md) |
| Canonical architecture | [03-canonical-architecture.md](../architecture/canonical/03-canonical-architecture.md), [04-system-diagram.md](../architecture/canonical/04-system-diagram.md), [08-decision-record.md](../architecture/canonical/08-decision-record.md) |
| Agent specifications | [09-source-discovery-agent.md](../architecture/canonical/09-source-discovery-agent.md) through [25-research-agent.md](../architecture/canonical/25-research-agent.md) |
| Unified Compliance Model | `unified-compliance-model.md` was searched for by filename and phrase; no matching file was found. |

### 2.2 Inferred Unified Compliance Model

Because the named model document is absent, the audit uses the following inferred model:

1. **Architecture authority:** Architecture Registry and ADR-011 define the frozen Architecture v1.0 baseline.
2. **Capability authority:** Capability Registry declares capability IDs, registration state, benchmark posture, standards coverage, and human approval requirement.
3. **Agent check authority:** Agent Checks Registry normalizes Evidence, Provenance, Compliance, Benchmark Coverage, and Status for registered agents.
4. **Governance sequence:** Agent outputs pass through Agent Registry, Benchmarks, Evaluations, Safety Reviews, and Human Approval before affecting canonical systems.
5. **Boundary rule:** Agents may propose, report, validate, or route; canonical writes, graph writes, publication, deployment, and steward-sensitive actions require explicit human approval or registered low-risk profiles.
6. **Freeze rule:** New architecture layers, observatories, products, governance powers, or agent authority require ADR-governed disposition under ADR-011.

---

## 3. Conflicts Found

### C-01: Missing Unified Compliance Model document

| Field | Value |
|-------|-------|
| **Severity** | High |
| **Evidence** | No `unified-compliance-model.md` file was found; phrase searches for "Unified Compliance Model" did not identify a model document. |
| **Conflict** | The audit objective references a model that is not present as a single source of truth. |
| **Impact** | Responsibility ownership and sequence rules must be inferred from multiple files, increasing drift risk. |

### C-02: Capability Registry extends beyond current canonical benchmark and checks fleet

| Field | Value |
|-------|-------|
| **Severity** | High |
| **Evidence** | Capability Registry lists agents 24-35 as Draft capabilities ([capability-registry.md](../governance/capability-registry.md) lines 26-37). Benchmark Agent fleet enumeration lists only agents 09-23 ([23-benchmark-agent.md](../architecture/canonical/23-benchmark-agent.md) lines 132-152). Agent Checks Registry also ends at Benchmark Agent ([agent-checks-registry.md](../governance/agent-checks-registry.md) lines 17-33). |
| **Conflict** | Capability ownership exists for 24-35, but benchmark/check normalization does not yet cover those capabilities. |
| **Impact** | Draft state is understandable, but compliance status is split across registries. |

### C-03: Post-freeze governance-agent expansion creates documentation tension

| Field | Value |
|-------|-------|
| **Severity** | High |
| **Evidence** | ADR-011 states planned Architecture, Research, and Audit specifications remain deferred until required and warns operational registries must not precede constitutional completion ([08-decision-record.md](../architecture/canonical/08-decision-record.md) lines 558-561). Current documentation includes Architecture Agent and Research Agent specs and a Capability Registry with 24-35 Draft entries. |
| **Conflict** | Current repository state has moved beyond the historical ADR-011 consequence language without a single reconciliation note. |
| **Impact** | Readers can interpret current Draft specs either as permitted governance clarification or as post-freeze expansion. |

### C-04: Governance reports are stale relative to current registry state

| Field | Value |
|-------|-------|
| **Severity** | Medium |
| **Evidence** | Constitutional Validation Report still lists `capability-registry.md` as not created and Architecture/Research/Audit agents as planned ([constitutional-validation-report.md](../governance/constitutional-validation-report.md) lines 90-109). |
| **Conflict** | Historical validation status conflicts with current registry/spec existence. |
| **Impact** | Audit readers may treat superseded status as current unless report lifecycle state is explicit. |

---

## 4. Duplicate Responsibilities

| ID | Responsibility | Overlapping owners | Evidence | Assessment |
|----|----------------|--------------------|----------|------------|
| D-01 | Architecture compliance | Architecture Agent; Benchmark Agent; Standards Agent | Architecture Agent performs architecture compliance review ([24-architecture-agent.md](../architecture/canonical/24-architecture-agent.md) lines 83-96); Benchmark Agent has Architecture Compliance domain ([23-benchmark-agent.md](../architecture/canonical/23-benchmark-agent.md) lines 123-130); Standards Agent emits milestone conformance reports ([22-standards-agent.md](../architecture/canonical/22-standards-agent.md) lines 183-191). | Duplicate but partly intentional. Missing explicit ordering: advisory architecture review vs automated benchmark compliance vs standards gate evidence. |
| D-02 | Provenance completeness | Quality Review Agent; Standards Agent; Agent Checks Registry | Agent Checks Registry normalizes provenance checks ([agent-checks-registry.md](../governance/agent-checks-registry.md) lines 39-49); Standards Agent checks CRM provenance patterns; Quality Review checks metadata quality and provenance. | Duplicate without a registry-level ownership split for record-level vs ontology-level vs fleet-level provenance. |
| D-03 | Accessibility compliance | Quality Review Agent; planned Accessibility Agent | Quality Review owns accessibility checks in the registered fleet; Capability Registry reserves `wise.capability.accessibility` for a future Accessibility Agent ([capability-registry.md](../governance/capability-registry.md) line 35). | Future duplicate risk. Needs boundary language before any operational promotion. |
| D-04 | Standards conformance | Standards Agent; planned Standards Compliance Agent | Standards Agent is active for CIDOC-CRM, Darwin Core, and schema.org. Capability Registry lists a future Standards Compliance Agent ([capability-registry.md](../governance/capability-registry.md) line 36). | Future duplicate risk between domain standards validation and cross-system compliance. |
| D-05 | Knowledge Graph governance | Knowledge Graph Agent; planned Knowledge Graph Governance Agent; observatory agents | KG Agent owns graph links and relationship proposals; Capability Registry lists `30-knowledge-graph-agent.md` as Knowledge Graph Governance ([capability-registry.md](../governance/capability-registry.md) line 32); observatory specs refer to graph annotations or placement. | Split may be valid, but graph-write and graph-annotation terminology is not consistently bounded. |
| D-06 | Rights and data governance | Quality Review Agent; planned Data Governance Agent; Research Agent | Quality Review owns rights checks; Data Governance is planned in Capability Registry ([capability-registry.md](../governance/capability-registry.md) line 34); Research Agent coordinates with Data Governance ([25-research-agent.md](../architecture/canonical/25-research-agent.md) lines 244-246). | Cross-cutting ownership gap until Data Governance boundaries are specified. |

---

## 5. Missing Responsibilities

| ID | Missing or unclear ownership | Evidence | Impact |
|----|------------------------------|----------|--------|
| M-01 | Evaluations gate executor | AI Fabric sequence includes Evaluations ([04-system-diagram.md](../architecture/canonical/04-system-diagram.md) lines 231-236), but governance registries do not assign an owner for executing or accepting Evaluations. | Gate exists as a sequence step but not as an owned responsibility. |
| M-02 | Safety Reviews gate executor | AI Fabric sequence includes Safety Reviews ([04-system-diagram.md](../architecture/canonical/04-system-diagram.md) lines 231-236); agent specs describe safety review checks, but no central owner is registered. | Safety Review disposition may be inconsistent across agents. |
| M-03 | Agent Registry operational ownership | Capability Registry defines Draft/Operational state and references Agent Registry registration ([capability-registry.md](../governance/capability-registry.md) lines 43-51), but no owner registry entry is present. | Operational promotion path is incomplete. |
| M-04 | 24-25 Agent Checks rows | Agent Checks Registry lists 09-23 only ([agent-checks-registry.md](../governance/agent-checks-registry.md) lines 17-33), while Capability Registry includes 24 and 25 ([capability-registry.md](../governance/capability-registry.md) lines 26-27). | Draft agents lack normalized Evidence/Provenance/Compliance posture. |
| M-05 | Research Agent lifecycle metadata | Research Agent header lacks explicit Registration State and Human Approval Required fields, unlike Architecture Agent ([25-research-agent.md](../architecture/canonical/25-research-agent.md) lines 3-10; [24-architecture-agent.md](../architecture/canonical/24-architecture-agent.md) lines 3-12). | Registry/spec alignment is weaker for `wise.capability.research-council`. |
| M-06 | Future capability specifications 26-35 | Capability Registry lists Draft entries 26-35 as filenames, but files are not present in `docs/architecture/canonical/`. | Ownership is declared before specification-level boundaries exist. |
| M-07 | Unified Compliance Model owner | The model document is absent. | No named maintainer or authoritative location for the cross-registry compliance model. |

---

## 6. Governance Gaps

### G-01: Governance sequence is documented but not uniformly normalized

The sequence Agent Registry -> Benchmarks -> Evaluations -> Safety Reviews -> Human Approval is visible in [04-system-diagram.md](../architecture/canonical/04-system-diagram.md) lines 231-236. Agents 09-23 generally contain AI Fabric governance tables. Architecture Agent and Research Agent instead use Draft-specific benchmark and approval sections, and they are not in Benchmark Agent fleet enumeration or Agent Checks Registry.

### G-02: Architecture Registry change-control sequence is not bridged to AI Fabric sequence

Architecture Registry requires Architecture Review, Standards Review, Governance Review, and Open Grace Architecture Office approval ([architecture-registry.md](../governance/architecture-registry.md) lines 25-32). AI Fabric requires registry, benchmarks, evaluations, safety reviews, and human approval. No bridge document states when each sequence applies, whether they are serial or parallel, or which review wins on conflict.

### G-03: Draft capability semantics are present but unevenly applied

Capability Registry defines Draft as not operational and not fleet-registered ([capability-registry.md](../governance/capability-registry.md) lines 43-51). Architecture Agent now has a lifecycle clarification, but Research Agent and planned 26-35 entries do not have equivalent spec-level lifecycle notes.

### G-04: Historical reports are not clearly marked as stale against current state

Constitutional Validation Report states the Capability Registry is not created and governance agents are planned ([constitutional-validation-report.md](../governance/constitutional-validation-report.md) lines 90-109). This is historically useful but operationally inconsistent unless clearly treated as superseded.

---

## 7. Boundary Rule Compliance

### 7.1 Compliant patterns

- AI Fabric explicitly requires human approval before canonical impact ([04-system-diagram.md](../architecture/canonical/04-system-diagram.md) lines 203-236).
- Knowledge Graph Agent outputs require curator approval before canonical graph writes ([04-system-diagram.md](../architecture/canonical/04-system-diagram.md) lines 212-213).
- Translation, observatory, education, publishing, standards, and benchmark flows repeatedly reference steward, curator, Architecture Office, or council review.
- Architecture Agent explicitly prohibits deployment approval, canonical writes, record modification, and steward bypass ([24-architecture-agent.md](../architecture/canonical/24-architecture-agent.md) lines 56-67 and 189-196).
- Research Agent states it does not write canonical metadata, assert graph entities, publish canonical facts, or bypass steward approval ([25-research-agent.md](../architecture/canonical/25-research-agent.md) lines 54-69).

### 7.2 Boundary ambiguities

| ID | Boundary ambiguity | Evidence | Risk |
|----|--------------------|----------|------|
| B-01 | Observatory graph placement terminology varies by agent. | Tourism success criteria include "graph placement" ([20-tourism-observatory-agent.md](../architecture/canonical/20-tourism-observatory-agent.md) lines 245-253); Language says approved time series are written to Knowledge Graph ([21-language-observatory-agent.md](../architecture/canonical/21-language-observatory-agent.md) lines 78-89); Climate routes approved records to graph annotations ([18-climate-observatory-agent.md](../architecture/canonical/18-climate-observatory-agent.md) lines 86-97). Heritage explicitly prohibits graph assertions ([19-heritage-observatory-agent.md](../architecture/canonical/19-heritage-observatory-agent.md) lines 139-145). | Potential confusion between approved observatory records, graph annotations, and canonical Entity Assertions. |
| B-02 | Planned governance agents have no spec-level no-write boundaries. | Capability Registry lists 26-35, but specs are absent ([capability-registry.md](../governance/capability-registry.md) lines 28-37). | Draft entries cannot yet be audited for canonical write, deployment, or steward-bypass constraints. |
| B-03 | Peer observatory names exceed current spec set. | Climate lists Heritage, Biodiversity, Conservation, Tourism, and Sustainability observatories ([18-climate-observatory-agent.md](../architecture/canonical/18-climate-observatory-agent.md) lines 97-103). | Conservation and Sustainability observatory ownership is not specified in the current agent set. |

---

## 8. ADR-011 and Freeze Compliance

| Finding | Status | Evidence | Assessment |
|---------|--------|----------|------------|
| ADR-011 baseline exists and is cited. | Compliant | ADR-011 records Architecture v1.0 in the Architecture Registry and freezes the baseline ([08-decision-record.md](../architecture/canonical/08-decision-record.md) lines 529-541). | Core freeze authority is clear. |
| Architecture Agent respects freeze. | Compliant | Architecture Agent states its specification clarifies review behavior and does not add deployment, canonical write, or steward powers ([24-architecture-agent.md](../architecture/canonical/24-architecture-agent.md) lines 56-67). | Advisory-only Draft posture is aligned. |
| Research Agent respects freeze but has weaker registry metadata. | Partially compliant | Research Agent binds investigations to frozen layers and requires ADR for scope expansion ([25-research-agent.md](../architecture/canonical/25-research-agent.md) lines 62-69), but lacks explicit Registration State and Human Approval Required header fields. | Meaning is mostly aligned; registry metadata consistency is incomplete. |
| Capability Registry 26-35 creates freeze tension. | Gap | Draft entries 26-35 exist without specs ([capability-registry.md](../governance/capability-registry.md) lines 28-37), while ADR-011 warns against speculative expansion ([08-decision-record.md](../architecture/canonical/08-decision-record.md) lines 523-561). | Needs a reconciliation note or deferred-entry policy; no architecture change is made by this audit. |

---

## 9. Reference Integrity Findings

| ID | Finding | Evidence | Severity |
|----|---------|----------|----------|
| R-01 | `unified-compliance-model.md` is missing. | Filename and phrase searches found no model file. | High |
| R-02 | Research Agent links to missing 26-35 spec files. | Research Agent Document Map and Relationships link to `26-audit-agent.md` through `35-frontend-architecture-agent.md` ([25-research-agent.md](../architecture/canonical/25-research-agent.md) lines 41-50 and 244-250). | Medium |
| R-03 | Capability Registry references future spec filenames as non-links. | Capability Registry lists `26-audit-agent.md` through `35-frontend-architecture-agent.md` as Draft filenames ([capability-registry.md](../governance/capability-registry.md) lines 28-37). | Low; non-links avoid broken Markdown, but targets are absent. |
| R-04 | Agent Checks Registry does not include Architecture or Research Agent rows. | Registry ends at Benchmark Agent ([agent-checks-registry.md](../governance/agent-checks-registry.md) lines 17-33). | Medium |

---

## 10. Compliance Score

**Overall score: 67 / 100**

### Scoring rationale

| Category | Weight | Score | Notes |
|----------|--------|-------|-------|
| Ownership clarity | 20 | 15 | Most 09-23 owners clear; 24+ incomplete. |
| Duplicate control | 15 | 9 | Duplicates are mostly manageable but not matrixed. |
| Missing ownership | 15 | 8 | Evaluations, Safety Reviews, Agent Registry operations, and 24+ checks lack clear owners. |
| Governance sequence | 15 | 10 | AI Fabric chain is clear; Draft governance agents are not normalized. |
| Boundary compliance | 15 | 11 | Strong no-write/steward-gate pattern with graph-placement ambiguities. |
| ADR-011 / freeze posture | 10 | 7 | Freeze is cited, but post-freeze registry/spec expansion needs reconciliation. |
| Reference integrity | 10 | 7 | In-scope report links are valid; existing corpus has missing future-spec targets. |

### Interpretation

- **80-100:** Audit-ready unified governance model.
- **65-79:** Mostly coherent with material registry and ownership gaps.
- **50-64:** Fragmented governance model requiring reconciliation before operational use.
- **Below 50:** Governance sequence or authority model unreliable.

The current score falls in the **mostly coherent with material registry and ownership gaps** range.

---

## 11. Recommended Corrections

These are recommendations only. They do not modify architecture, governance, ADRs, or agent specs.

| Priority | Recommendation | Expected effect | Architecture / ADR impact |
|----------|----------------|-----------------|---------------------------|
| P0 | Create or identify the authoritative Unified Compliance Model location and owner. | Removes inference-based compliance and establishes a single control model. | Should be framed as documentation consolidation unless it changes authority. |
| P0 | Add an ownership matrix for Agent Registry, Benchmarks, Evaluations, Safety Reviews, and Human Approval. | Assigns missing gate owners. | No ADR needed if it records existing authority only. |
| P1 | Normalize Architecture Agent and Research Agent in Agent Checks Registry once their Draft posture is accepted for check tracking. | Closes 24-25 Evidence/Provenance/Compliance registry gap. | No ADR if Draft/non-operational status remains unchanged. |
| P1 | Clarify that Benchmark Agent Section 5.4 remains the operational fleet source of truth and Capability Registry 24-35 entries are Draft placeholders. | Reconciles capability registry with benchmark fleet enumeration. | No ADR if no operational promotion occurs. |
| P1 | Mark historical governance reports as superseded or historical where they conflict with current registry state. | Reduces stale-status confusion. | No ADR needed for report metadata clarification. |
| P1 | Define boundary splits for architecture compliance, standards conformance, provenance checks, accessibility, and graph-governance overlaps. | Reduces duplicate ownership risk. | No ADR if it only clarifies current ownership. |
| P2 | Remove or convert broken Markdown links to not-yet-existing future specs in Research Agent, or create those specs through the proper process. | Restores Markdown reference integrity. | Creating new specs may require Architecture Office determination under ADR-011; link cleanup alone should not. |
| P2 | Harmonize observatory graph-write terminology: observation records, graph annotations, Entity Assertions, and relationship placements. | Reduces boundary ambiguity between observatory agents and Knowledge Graph Agent. | No ADR if terms are clarified without changing write authority. |

---

## 12. Audit Conclusion

The documented governance model is directionally consistent with Architecture v1.0 for the operational 09-23 agent fleet. The largest consistency issues are not runtime behavior changes; they are documentation and registry alignment gaps:

1. The Unified Compliance Model is missing as a named source.
2. Capability Registry extends to Draft agents 24-35 while Benchmark and Agent Checks registries still cover only 09-23.
3. Architecture Agent and Research Agent are advisory/read-only in substance but not equally normalized across registry/check metadata.
4. Some responsibilities are duplicated without a single ownership matrix.
5. Existing historical reports and future-spec references create reference and status drift.

No ADR is introduced or required by this audit report. Any future correction that changes Architecture v1.0 authority, operational agent status, governance powers, or frozen scope should follow the existing Architecture Office and ADR-011 process.
