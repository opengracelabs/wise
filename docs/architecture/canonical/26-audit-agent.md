# Audit Agent

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Status** | Draft |
| **Authority** | Open Grace Architecture Office |
| **Date** | 2026-06-22 |
| **Capability ID** | `wise:agent:audit` |
| **Capability Number** | 26 |
| **Capability** | Governance / Audit & Compliance |
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
| [24-architecture-agent.md](24-architecture-agent.md) | Architecture Agent specification |
| [25-research-agent.md](25-research-agent.md) | Research Agent specification |
| [../../governance/capability-registry.md](../../governance/capability-registry.md) | Draft capability registration posture |

---

## 1. Purpose

The **Audit Agent** supports Governance / Audit & Compliance by assembling evidence for covenant, standards, provenance, and AI Fabric governance audits. It verifies that review packets contain traceable evidence, human approvals, benchmark posture, standards coverage, and ADR references required for Architecture Office or steward disposition.

The agent does not certify compliance on its own, modify canonical records, create graph factories, create database seeds, register itself as operational, or bypass human auditors. It gathers and tests evidence; human authorities decide.

---

## 2. Authority

| Authority | Scope |
|-----------|-------|
| **Open Grace Architecture Office** | Primary authority for milestone certification, waivers, and architecture-affecting audit disposition |
| **Audit & Compliance function** | Evidence packet preparation, audit finding classification, and compliance workflow support |
| **Partner stewards** | Covenant, rights, and sensitive-corpus review authority |
| **ADR-011** | Architecture v1.0 freeze constraint; operational expansion requires ADR-governed change |

---

## 3. Responsibilities

| Responsibility | Description |
|----------------|-------------|
| **Evidence packet assembly** | Collect benchmark, standards, provenance, approval, and ADR evidence into reviewable audit packets |
| **Provenance-chain verification** | Check Source -> Evidence -> Preservation -> Knowledge -> Quality -> Research -> Public Access traceability |
| **Covenant compliance review** | Identify rights, stewardship, cultural sensitivity, and partner-covenant findings for human review |
| **Governance-chain audit** | Verify Agent Registry, benchmarks, evaluations, safety reviews, and human approvals are present before production-impacting actions |
| **Exception traceability** | Link waivers and exceptions to accepted ADRs, steward approvals, or Architecture Office dispositions |

---

## 4. Inputs

| Input | Source |
|-------|--------|
| Architecture and capability registries | Governance registry documents |
| Benchmark reports | [23-benchmark-agent.md](23-benchmark-agent.md) outputs when registered |
| Standards reports | [22-standards-agent.md](22-standards-agent.md) outputs |
| Architecture review reports | [24-architecture-agent.md](24-architecture-agent.md) outputs |
| Research findings | [25-research-agent.md](25-research-agent.md) outputs |
| Provenance and preservation events | PREMIS-aligned preservation and governance logs |
| Human approvals | Steward, Architecture Office, council, and partner disposition records |

---

## 5. Outputs

### 5.1 Audit Findings Reports

Each audit emits **JSON-LD** with:

| Field | Requirement |
|-------|-------------|
| **Audit scope** | Milestone, capability, corpus, partner covenant, or governance-chain segment |
| **Evidence inventory** | Linked reports, approvals, provenance events, ADRs, and registry references |
| **Findings** | Pass, gap, exception, or blocker findings with severity |
| **Required disposition** | Human authority needed for acceptance, waiver, remediation, or escalation |
| **Standards coverage** | Binding standards and compliance sources reviewed |
| **Benchmark coverage** | Benchmark reports or required benchmark declarations reviewed |
| **Provenance** | Audit run identifier, input snapshot hashes, reviewer chain |

Audit findings are candidate evidence until accepted by the Architecture Office, audit authority, or relevant steward.

### 5.2 Compliance Exception Registers

When evidence gaps or violations exist, the agent emits an exception register with owner, severity, required human disposition, and remediation references.

### 5.3 Certification Packets

For milestone review, the agent assembles packets containing:

- architecture review evidence,
- standards conformance evidence,
- benchmark posture,
- safety review evidence,
- steward and Architecture Office approvals,
- ADR and waiver references.

---

## 6. Checks

| Check domain | Specification |
|--------------|---------------|
| **Evidence completeness** | Required reports, approvals, and provenance references are present |
| **Provenance integrity** | Audit packet preserves source-to-disposition traceability |
| **Standards coverage** | Required standards and compliance sources are cited |
| **Benchmark coverage** | Required benchmark evidence or benchmark declarations are present |
| **Human approval** | Disposition authority is explicit and non-automated |
| **ADR traceability** | Exceptions and freeze-affecting changes link to ADR lifecycle |
| **Operational posture** | Draft capabilities are not graph-bound, seeded, or added to production registries |

---

## 7. Constraints

- **Draft only.** This specification documents a draft governance capability and does not register an operational agent.
- **No certification by automation.** Audit Agent outputs are evidence; human authorities certify or reject.
- **No operational artifacts.** Do not create graph factories, database seeds, runtime manifests, or production registry entries from this spec.
- **ADR-011 bound.** Audit workflows must flag architecture expansion and operational registration changes for ADR review.
- **Covenant authority preserved.** Partner and steward decisions cannot be overridden by automated audit findings.

---

## 8. Success Criteria

- 100% of audit packets include benchmark, standards, human approval, and provenance posture.
- 100% of exceptions identify a human disposition authority.
- Zero draft capabilities are marked operational by Audit Agent output.
- 100% of covenant-affecting findings route to steward or partner review.
- End-to-end demonstration: evidence packet -> audit findings report -> human disposition -> remediation or certification record.

---

## 9. Evidence Requirements

| Output type | Evidence contract |
|-------------|-------------------|
| Audit Findings Reports | `evidenceRefs[]`, `approvalRefs[]`, `standardRefs[]`, `benchmarkRefs[]`, `provenanceEventIds[]` |
| Compliance Exception Registers | Finding severity, owner, required disposition, remediation reference |
| Certification Packets | Complete review-chain artifacts with immutable input references |

Blocker findings must cite the missing or conflicting evidence source and the human authority required to resolve it.

---

## 10. Provenance Requirements

| Requirement | Specification |
|-------------|---------------|
| **Audit identity** | Unique audit identifier on every report and packet |
| **Input traceability** | Snapshot hash, commit SHA, event identifier, or report URI for each input |
| **Approval traceability** | Human approver, authority role, timestamp, and scope recorded |
| **PREMIS alignment** | Preservation and governance audit events remain PREMIS-aligned where applicable |
| **Exception lifecycle** | Exception status and remediation disposition remain linked to original finding |

---

## 11. Compliance Requirements

| Requirement | Source |
|-------------|--------|
| AI Fabric governance chain | [04-system-diagram.md](04-system-diagram.md), §2.2 |
| Evidence Output Profile | [03-canonical-architecture.md](03-canonical-architecture.md), §6.6 |
| Provenance model | [03-canonical-architecture.md](03-canonical-architecture.md), §6.2 |
| Rights and covenant model | [03-canonical-architecture.md](03-canonical-architecture.md), §6.3 |
| Architecture freeze | [ADR-011](08-decision-record.md#adr-011-architecture-freeze-v10) |
| Standards registry | [07-reference-standards.md](07-reference-standards.md) |

---

## 12. Human Approval Requirements

| Action | Approver |
|--------|----------|
| Accept milestone certification packet | Open Grace Architecture Office |
| Accept covenant or sensitive-corpus audit finding | Partner steward or designated rights authority |
| Waive audit blocker or compliance exception | Architecture Office; ADR required when architecture-affecting |
| Promote draft capability toward operational registration | Architecture Office after benchmarks, standards, safety review, and implementation readiness |

Human approval is required for certification, waivers, covenant disposition, and promotion decisions.

---

## 13. Benchmark Requirements

| Benchmark | Threshold |
|-----------|-----------|
| Evidence completeness detection | 100% known missing required artifacts flagged |
| Approval traceability coverage | 100% accepted packets include human approval references |
| False certification rate | 0% automated certification without human acceptance |
| Standards coverage classification | 100% audit scopes identify required standards posture |
| Exception routing accuracy | 100% blocker findings route to correct human authority |

Benchmark coverage is required before this draft capability can be considered for operational promotion.

---

## 14. Failure Conditions

| Condition | Severity |
|-----------|----------|
| Marks itself or another draft governance capability operational | **Blocker** |
| Creates or requires graph factory/database seed artifacts | **Blocker** |
| Certifies compliance without human approval | **Blocker** |
| Omits benchmark, standards, or human approval posture from certification packet | **Blocker** |
| Covenant-affecting finding lacks steward or partner routing | **Blocker** |
| Finding lacks evidence reference | **Warning** |

---

## 15. Relationship to Other Agents

| Agent | Relationship |
|-------|--------------|
| [Architecture Agent](24-architecture-agent.md) | Supplies architecture review evidence and ADR routing findings |
| [Research Agent](25-research-agent.md) | Supplies research findings and gold-dataset evidence for audit packets |
| [Benchmark Agent](23-benchmark-agent.md) | Supplies benchmark reports and quality/performance posture |
| [Standards Agent](22-standards-agent.md) | Supplies standards conformance evidence |
| [Preservation Agent](11-preservation-agent.md) | Supplies PREMIS-aligned preservation and fixity evidence |
| [Quality Review Agent](13-quality-review-agent.md) | Supplies quality and rights review evidence |

---

*Previous: [25-research-agent.md](25-research-agent.md) · Next: [27-security-agent.md](27-security-agent.md)*
