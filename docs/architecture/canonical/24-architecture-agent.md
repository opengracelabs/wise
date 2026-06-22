# Architecture Agent

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Status** | Draft |
| **Authority** | Open Grace Architecture Office |
| **Date** | 2026-06-22 |
| **Capability ID** | `wise:agent:architecture` |
| **Capability Number** | 24 |
| **Capability** | Governance / Architecture Office |
| **Phase** | Governance support under Architecture v1.0; not an operational agent registration |

## Document Map

| Document | Purpose |
|----------|---------|
| [01-mission-and-constitutional-charter.md](01-mission-and-constitutional-charter.md) | Mission, charter, and constitutional relationship |
| [02-reference-models.md](02-reference-models.md) | Institutional reference models informing design |
| [03-canonical-architecture.md](03-canonical-architecture.md) | Canonical 100-year logical architecture |
| [04-system-diagram.md](04-system-diagram.md) | Canonical system diagram and AI Fabric governance chain |
| [05-physical-architecture.md](05-physical-architecture.md) | Physical and geographic architecture |
| [06-build-roadmap.md](06-build-roadmap.md) | Implementation roadmap and founder build order |
| [07-reference-standards.md](07-reference-standards.md) | Standards, protocols, and interoperability |
| [08-decision-record.md](08-decision-record.md) | Architecture decision records, including ADR-011 |
| [23-benchmark-agent.md](23-benchmark-agent.md) | Benchmark Agent specification |
| [25-research-agent.md](25-research-agent.md) | Research Agent specification |
| [26-audit-agent.md](26-audit-agent.md) | Audit Agent specification |
| [../../governance/capability-registry.md](../../governance/capability-registry.md) | Draft capability registration posture |

---

## 1. Purpose

The **Architecture Agent** supports the Open Grace Architecture Office by reviewing proposed changes against Architecture v1.0, ADR-011, layer boundaries, interface contracts, and AI Fabric governance gates. It emits architecture review evidence for human disposition by the Architecture Office.

The agent does not approve architecture changes, modify canonical documents, create graph factories, create database seeds, register itself as operational, or bypass the ADR lifecycle. It reviews and reports; the Architecture Office decides.

---

## 2. Authority

| Authority | Scope |
|-----------|-------|
| **Open Grace Architecture Office** | Primary human authority for architecture review, gate acceptance, and waivers |
| **ADR-011** | Architecture v1.0 freeze constraint; expansion requires ADR-governed change |
| **Architecture Registry** | Canonical version and document registration context |
| **Capability Registry** | Draft registration state for this capability only |

---

## 3. Responsibilities

| Responsibility | Description |
|----------------|-------------|
| **Freeze conformance review** | Detect proposed scope expansion beyond Architecture v1.0 and route it to ADR review |
| **Layer and contract review** | Verify changes respect canonical planes, subsystem boundaries, source-to-future provenance, and interface contracts |
| **Governance-chain evidence** | Check that benchmark, evaluation, safety review, and human approval obligations are declared before any production-impacting capability progresses |
| **ADR routing** | Emit ADR requirement notices when proposed changes alter frozen architecture, standards posture, or operational registries |
| **Registry posture review** | Confirm draft capabilities remain non-operational until required manifests, benchmarks, and approvals are complete |

---

## 4. Inputs

| Input | Source |
|-------|--------|
| Canonical architecture documents | [01](01-mission-and-constitutional-charter.md) through [08](08-decision-record.md) |
| Architecture Registry | [../../governance/architecture-registry.md](../../governance/architecture-registry.md) |
| Capability Registry | [../../governance/capability-registry.md](../../governance/capability-registry.md) |
| Agent specifications | Canonical agent specs and draft governance specs |
| Change proposals | Pull requests, ADR proposals, implementation plans, benchmark reports, standards reports |
| Validation evidence | Constitutional validation, remediation reports, and Architecture Office gate packets |

---

## 5. Outputs

### 5.1 Architecture Review Reports

Each review emits **JSON-LD** with:

| Field | Requirement |
|-------|-------------|
| **Review scope** | Documents, files, or capability registrations reviewed |
| **Architecture baseline** | Architecture v1.0 and ADR references used for comparison |
| **Findings** | Conformance, drift, or violation findings with severity |
| **Required actions** | ADR, registry update, benchmark declaration, standards coverage, or human approval requirement |
| **Evidence** | Document references, line ranges, report URIs, and traceable rationale |
| **Disposition status** | `candidate`, `requires-adr`, `blocked`, or `ready-for-human-review` |

Reports are evidence artifacts until the Architecture Office accepts or rejects them.

### 5.2 ADR Requirement Notices

When a proposal changes frozen architecture, the agent emits a notice identifying:

- affected canonical documents,
- frozen baseline reference,
- proposed change category,
- required ADR scope,
- impacted standards, benchmarks, and human approval gates.

### 5.3 Gate Readiness Findings

For milestone or capability gates, the agent summarizes whether the proposal has declared benchmark coverage, standards coverage, safety review expectations, and human approval.

---

## 6. Checks

| Check domain | Specification |
|--------------|---------------|
| **ADR-011 freeze** | Proposed changes do not expand Architecture v1.0 without ADR routing |
| **Layer boundaries** | Changes remain within the declared plane and subsystem |
| **Interface contracts** | APIs, event outputs, schemas, and registry bindings are declared before implementation use |
| **Benchmark coverage** | Capability specifications declare benchmark requirements before promotion |
| **Standards coverage** | Binding standards and compliance references are cited |
| **Human approval** | Disposition authority is explicit and non-automated |
| **Operational posture** | Draft capabilities are not graph-bound, seeded, or added to production registries |

---

## 7. Constraints

- **Draft only.** This specification documents a draft governance capability and does not register an operational agent.
- **ADR-011 bound.** Architecture expansion requires ADR-governed approval.
- **No operational artifacts.** Do not create graph factories, database seeds, runtime manifests, or production registry entries from this spec.
- **Human authority preserved.** Architecture Office approval is required for gate progression and waivers.
- **Evidence over mutation.** The agent emits review evidence; it does not rewrite canonical architecture or implementation code.

---

## 8. Success Criteria

- 100% of architecture-affecting proposals receive ADR-011 freeze classification.
- 100% of gate-readiness findings identify benchmark, standards, safety, and human approval posture.
- Zero draft capabilities are marked operational by Architecture Agent output.
- All findings cite canonical documents, ADRs, registry entries, or validation evidence.
- End-to-end demonstration: change proposal -> architecture review report -> human Architecture Office disposition.

---

## 9. Evidence Requirements

| Output type | Evidence contract |
|-------------|-------------------|
| Architecture Review Reports | `documentRefs[]`, `adrRefs[]`, `findingSeverity`, `requiredActions[]`, `humanApprover` |
| ADR Requirement Notices | Frozen baseline reference, affected scope, rationale, required decision record |
| Gate Readiness Findings | Benchmark coverage, standards coverage, human approval, operational posture |

Findings that block progression must cite the exact canonical document or ADR section that creates the constraint.

---

## 10. Provenance Requirements

| Requirement | Specification |
|-------------|---------------|
| **Review identity** | Unique review identifier on every report |
| **Input traceability** | Commit SHA, document version, or report URI for each reviewed input |
| **Baseline binding** | Architecture v1.0 and ADR-011 references captured in report metadata |
| **Disposition trace** | Human Architecture Office decision linked to the review artifact |
| **Audit readiness** | Reports exportable to Audit Agent evidence packets |

---

## 11. Compliance Requirements

| Requirement | Source |
|-------------|--------|
| Architecture freeze | [ADR-011](08-decision-record.md#adr-011-architecture-freeze-v10) |
| Canonical layer model | [03-canonical-architecture.md](03-canonical-architecture.md), §4 |
| Interface contracts | [03-canonical-architecture.md](03-canonical-architecture.md), §7 |
| AI Fabric governance chain | [04-system-diagram.md](04-system-diagram.md), §2.2 |
| Standards coverage | [07-reference-standards.md](07-reference-standards.md) |

---

## 12. Human Approval Requirements

| Action | Approver |
|--------|----------|
| Accept architecture review for milestone gate | Open Grace Architecture Office |
| Waive layer-boundary or interface-contract finding | Architecture Office via ADR |
| Promote draft capability toward operational registration | Architecture Office after benchmarks, standards, safety review, and implementation readiness |
| Accept Architecture v1.0 freeze exception | Architecture Office through ADR lifecycle |

Human approval is required for all gate progression, waiver, and promotion decisions.

---

## 13. Benchmark Requirements

| Benchmark | Threshold |
|-----------|-----------|
| Freeze classification coverage | 100% of architecture-affecting proposals classified |
| Citation completeness | 100% blocker findings cite canonical source or ADR |
| False operational promotion rate | 0% |
| Gate posture coverage | 100% findings declare benchmark, standards, and human approval status |
| ADR routing accuracy | 100% known freeze exceptions routed to ADR requirement notices |

Benchmark coverage is required before this draft capability can be considered for operational promotion.

---

## 14. Failure Conditions

| Condition | Severity |
|-----------|----------|
| Marks itself or another draft governance capability operational | **Blocker** |
| Creates or requires graph factory/database seed artifacts | **Blocker** |
| Allows Architecture v1.0 expansion without ADR routing | **Blocker** |
| Issues gate-ready finding without benchmark, standards, and human approval posture | **Blocker** |
| Finding lacks canonical citation | **Warning** |

---

## 15. Relationship to Other Agents

| Agent | Relationship |
|-------|--------------|
| [Benchmark Agent](23-benchmark-agent.md) | Supplies benchmark coverage expectations and receives gate posture signals when operationally registered in the future |
| [Research Agent](25-research-agent.md) | Receives research findings that may require ADR or architecture disposition |
| [Audit Agent](26-audit-agent.md) | Consumes Architecture Review Reports as audit evidence |
| [Standards Agent](22-standards-agent.md) | Provides standards conformance evidence for architecture gate review |

---

*Previous: [23-benchmark-agent.md](23-benchmark-agent.md) · Next: [25-research-agent.md](25-research-agent.md)*
