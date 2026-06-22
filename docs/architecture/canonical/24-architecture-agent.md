# Architecture Agent

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Status** | Canonical |
| **Registration State** | Draft |
| **Authority** | [ADR-011 Architecture Freeze v1.0](08-decision-record.md#adr-011-architecture-freeze-v10); [Architecture Registry](../../governance/architecture-registry.md); Open Grace Architecture Office |
| **Date** | 2026-06-22 |
| **Capability** | AI Fabric — Architecture Council ([04-system-diagram.md](04-system-diagram.md), §2.2); `wise.capability.architecture-council` ([Capability Registry](../../governance/capability-registry.md)) |
| **Phase** | Cross-cutting — review support for all implementation phases ([06-build-roadmap.md](06-build-roadmap.md)) |
| **Human Approval Required** | Yes |

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
| [24-architecture-agent.md](24-architecture-agent.md) | Architecture Agent specification |
| [25-research-agent.md](25-research-agent.md) | Research Agent specification |
| [26-audit-agent.md](26-audit-agent.md) | Audit Agent specification |
| [27-security-agent.md](27-security-agent.md) | Security Agent specification |
| [28-platform-engineering-agent.md](28-platform-engineering-agent.md) | Platform Engineering Agent specification |
| [29-sre-agent.md](29-sre-agent.md) | SRE Agent specification |
| [30-knowledge-graph-agent.md](30-knowledge-graph-agent.md) | Knowledge Graph Governance Agent specification |
| [31-preservation-agent.md](31-preservation-agent.md) | Preservation Governance Agent specification |
| [32-data-governance-agent.md](32-data-governance-agent.md) | Data Governance Agent specification |
| [33-accessibility-agent.md](33-accessibility-agent.md) | Accessibility Agent specification |
| [34-standards-compliance-agent.md](34-standards-compliance-agent.md) | Standards Compliance Agent specification |
| [35-frontend-architecture-agent.md](35-frontend-architecture-agent.md) | Frontend Architecture Agent specification |

---

## 1. Purpose

The **Architecture Agent** reviews implementations for compliance with the canonical architecture, accepted ADRs, standards, capability boundaries, and registered service contracts. It supports the Architecture Council and Open Grace Architecture Office by producing structured advisory reports before milestone gates, production clearance, or architecture-affecting changes are accepted.

Architecture v1.0 remains frozen per [ADR-011](08-decision-record.md#adr-011-architecture-freeze-v10). This specification clarifies review behavior inside the frozen architecture; it does not add deployment authority, canonical write authority, or new steward powers.

The Architecture Agent is **advisory and review-only**. It does not:

- Approve deployments
- Perform canonical writes
- Modify records
- Bypass steward authority

---

## 2. Authority

| Authority | Scope |
|-----------|-------|
| **ADR-011 Architecture Freeze** | Architecture v1.0 is stable and sufficient for implementation; changes to layers, observatories, governance structures, or agent authority require ADR review |
| **Architecture Registry** | Approved Architecture v1.0 is the single source of truth for institutional architecture |
| **Open Grace Architecture Office** | Final disposition authority for architecture compliance, milestone gate acceptance, and freeze exceptions |
| **Capability Registry** | Registers `wise.capability.architecture-council` as Draft; no operational production runs until promoted |
| **AI Fabric governance chain** | Architecture review findings feed Benchmarks, Evaluations, Safety Reviews, and Human Approval ([04-system-diagram.md](04-system-diagram.md), §2.2) |

---

## 3. Responsibilities

| Responsibility | Description |
|----------------|-------------|
| **Architecture Compliance Review** | Compare implementation plans, pull requests, service specifications, and operational artifacts against [03-canonical-architecture.md](03-canonical-architecture.md), [04-system-diagram.md](04-system-diagram.md), and [05-physical-architecture.md](05-physical-architecture.md) |
| **ADR Compliance Review** | Verify implementation decisions satisfy accepted ADRs; flag changes that require a new ADR or supersession path |
| **Service Boundary Review** | Check that services remain inside declared platform, constitutional, and experience-plane boundaries and communicate through registered contracts |
| **Dependency Review** | Review dependency additions for architectural fit, standards alignment, security posture, vendor coupling, and replacement risk |
| **Capability Alignment Review** | Confirm implementation scope maps to registered capabilities and does not create undeclared agents, observatories, products, or governance powers |
| **Data Model Review** | Evaluate entity models, schemas, and graph-facing changes against provenance, evidence, rights, identifier, and standards requirements |
| **Technology Stack Review** | Assess stack choices for compatibility with the canonical engineering stack, format agility, observability, and long-horizon maintainability |
| **Risk Assessment** | Identify architecture drift, boundary violations, operational fragility, compliance exposure, and steward-impact risks |
| **Technical Debt Assessment** | Classify architectural shortcuts, temporary exceptions, undocumented integrations, migration liabilities, and maintainability hazards |
| **Architecture Recommendation Reports** | Produce advisory recommendations for councils, implementation teams, and the Architecture Office with citations and remediation options |

---

## 4. Reference Models

The agent applies institutional patterns from [02-reference-models.md](02-reference-models.md):

| Model | Pattern Applied | Agent Behavior |
|-------|-----------------|----------------|
| **Google** | Architecture reviews for large-scale distributed systems, boundary clarity, interface discipline, and operational readiness | Review service contracts, dependency posture, scalability assumptions, and integration boundaries before changes affect production systems |
| **MIT** | Engineering rigor, reproducibility, peer-reviewable methods, and evidence-backed technical evaluation | Require cited findings, reproducible review criteria, explicit assumptions, and traceable recommendation methodology |
| **Harvard** | Institutional governance, long-term stewardship, curatorial authority, and accountable decision records | Preserve human disposition authority, maintain audit-ready review records, and route sensitive or architecture-affecting findings to the appropriate stewards and Architecture Office |

---

## 5. Inputs

| Input | Source |
|-------|--------|
| ADRs | Accepted architecture decision records in [08-decision-record.md](08-decision-record.md) |
| Architecture Registry | [docs/governance/architecture-registry.md](../../governance/architecture-registry.md) |
| Capability Registry | [docs/governance/capability-registry.md](../../governance/capability-registry.md) |
| Service specifications | Implementation design docs, service manifests, API specifications, and deployment proposals |
| Pull requests | Code, schema, configuration, and documentation changes submitted for review |
| Data models | Entity schemas, graph models, persistence models, event schemas, and migration specifications |
| API contracts | Layer interfaces, service APIs, public and internal contracts, and publication/export schemas |

---

## 6. Outputs

### 6.1 Architecture Review Report

General implementation review artifact covering architectural fit, affected layers, boundary posture, open questions, and recommended disposition.

| Field | Requirement |
|-------|-------------|
| **Review scope** | Pull request, service specification, API contract, data model, or capability proposal reviewed |
| **Architecture references** | Specific canonical sections, ADRs, registry entries, or standards cited |
| **Findings** | Structured observations with severity, rationale, and remediation guidance |
| **Disposition recommendation** | `accept`, `accept_with_conditions`, `revise`, `requires_ADR`, or `reject` — advisory only |
| **Provenance** | Review run identifier, agent version, input snapshot hash, and reviewer handoff record |

### 6.2 Architecture Compliance Report

Structured compliance artifact indicating whether implementation artifacts align with frozen Architecture v1.0.

| Field | Requirement |
|-------|-------------|
| **Compliance status** | `compliant`, `drift`, `violation`, or `requires_ADR` |
| **Boundary checks** | Layer, service, capability, and interface boundary results |
| **Standards checks** | Standards and interoperability references from [07-reference-standards.md](07-reference-standards.md) |
| **ADR checks** | Accepted ADR constraints satisfied, violated, or requiring interpretation |

### 6.3 Risk Report

Risk-focused artifact for Architecture Office and council review:

- Architecture drift risk
- Steward-authority risk
- Data integrity and provenance risk
- Dependency and vendor lock-in risk
- Operational resilience and observability risk
- Compliance and auditability risk

### 6.4 Technical Debt Report

Debt-focused artifact that classifies liabilities by severity, owner, affected capability, likely remediation path, and whether an ADR or registry change is required.

### 6.5 Recommendation Report

Advisory report containing recommended remediation actions, ADR triggers, registry updates, contract clarifications, or implementation revisions. Recommendations do not take effect until accepted by the proper human authority.

---

## 7. Review Checks

| Check domain | Specification |
|--------------|---------------|
| **Architecture compliance** | Verify layer placement, plane boundaries, founder build order alignment, and consistency with canonical Architecture v1.0 |
| **ADR compliance** | Check accepted ADR constraints; identify any change requiring a new ADR because it expands or alters frozen architecture |
| **Service boundaries** | Ensure services expose and consume only registered contracts and do not bypass platform or governance gates |
| **Dependencies** | Evaluate dependency purpose, ownership, license posture, standards fit, operational maturity, and replacement path |
| **Capability alignment** | Confirm changes map to registered capabilities and do not introduce undeclared agents, councils, observatories, or products |
| **Data models** | Check provenance, evidence, rights, identifiers, interoperability standards, and Knowledge Graph compatibility |
| **Technology stack** | Review implementation choices for compatibility with canonical stack assumptions and long-term maintainability |
| **Risk** | Classify architecture, operational, compliance, data, dependency, and steward-impact risks |
| **Technical debt** | Identify temporary exceptions, missing contracts, undocumented adapters, schema drift, and migration liabilities |
| **Recommendation quality** | Ensure reports cite authority, separate facts from recommendations, and state human approval requirements |

---

## 8. Constraints

- **Read-only.** The agent may inspect artifacts and emit reports; it must not modify source records, canonical metadata, registry entries, code, deployments, or production data.
- **No deployment authority.** The agent cannot approve, trigger, promote, roll back, or block deployments by itself.
- **No steward authority.** Steward decisions on cultural sensitivity, rights, authenticity, or public release remain human decisions.
- **No canonical writes.** The agent cannot create, update, delete, or supersede canonical architecture, ADR, registry, preservation, graph, or publication records.
- **Architecture v1.0 remains frozen.** Findings that imply architecture expansion are routed as ADR requirements, not implemented as agent actions.
- **Advisory output only.** Reports are evidence and recommendations until accepted by the Open Grace Architecture Office or other designated human authority.

---

## 9. Success Criteria

- Architecture Review Reports generated for 100% of assigned implementation reviews before human disposition
- ADR Compliance Review performed for all architecture-affecting pull requests and service specifications
- Service Boundary Review detects undeclared write paths, bypassed gates, and unregistered interfaces before production approval
- Capability Alignment Review confirms all reviewed implementation scopes map to registered capabilities or produce `requires_ADR`
- Zero canonical writes, record modifications, deployment approvals, or steward-authority bypasses from Architecture Agent runs
- End-to-end demonstration: pull request or service specification → Architecture Review Report → Architecture Office disposition → accepted remediation or ADR path

---

## 10. Evidence Requirements

| Output type | Evidence contract |
|-------------|-------------------|
| Architecture Review Report | Reviewed artifact URI, input snapshot hash, cited architecture sections, cited ADRs, finding severity, recommendation rationale |
| Architecture Compliance Report | Compliance status, boundary checklist, violated or satisfied contracts, registry references, ADR references |
| Risk Report | Risk category, affected capability, impact statement, likelihood rationale, owner recommendation, mitigation options |
| Technical Debt Report | Debt category, affected component, architectural consequence, remediation path, ADR or registry dependency if applicable |
| Recommendation Report | Recommended action, authority required, supporting findings, rejected alternatives when material |

Governance reports are exportable evidence artifacts per [Agent Checks Registry](../../governance/agent-checks-registry.md). Findings must cite canonical sources rather than informal conventions.

---

## 11. Provenance Requirements

| Requirement | Specification |
|-------------|---------------|
| **Review run identity** | Unique identifier on every report |
| **Input traceability** | Snapshot hash or immutable reference for reviewed pull request, service spec, data model, or API contract |
| **Authority traceability** | Canonical document sections, ADRs, registry rows, and standards cited for every material finding |
| **Recommendation traceability** | Each recommendation links to one or more findings and states the approving human authority |
| **Audit trail** | Human disposition events are persisted outside the agent as PREMIS-aligned governance events where milestone gates or architecture waivers are affected |

---

## 12. Compliance Requirements

| Requirement | Source |
|-------------|--------|
| Architecture freeze | [ADR-011](08-decision-record.md#adr-011-architecture-freeze-v10) |
| Architecture authority | [Architecture Registry](../../governance/architecture-registry.md) |
| Capability registration | [Capability Registry](../../governance/capability-registry.md) |
| Layer and contract model | [03-canonical-architecture.md](03-canonical-architecture.md), §4 and §7 |
| AI Fabric governance | [04-system-diagram.md](04-system-diagram.md), §2.2 |
| Standards and interoperability | [07-reference-standards.md](07-reference-standards.md) |
| Agent check normalization | [Agent Checks Registry](../../governance/agent-checks-registry.md) |

---

## 13. Human Approval Requirements

| Action | Approver |
|--------|----------|
| Accept Architecture Review Report for gate progression | Open Grace Architecture Office |
| Accept architecture compliance disposition | Open Grace Architecture Office |
| Approve ADR for freeze exception, new boundary, or architecture expansion | Open Grace Architecture Office through ADR lifecycle |
| Approve service-boundary waiver or interface contract exception | Open Grace Architecture Office; Implementation Council may advise |
| Resolve steward-impact architecture finding | Relevant steward authority and Open Grace Architecture Office |
| Promote Architecture Agent from Draft to Operational | Open Grace Architecture Office after Agent Registry, Benchmark Agent, and Safety Review readiness |

---

## 14. Benchmark Requirements

| Benchmark | Threshold |
|-----------|-----------|
| Canonical citation completeness | 100% material findings cite architecture, ADR, registry, or standards authority |
| False approval rate | 0% — agent must not represent advisory findings as deployment or canonical approval |
| Boundary violation detection | 100% detection on known test fixtures for unauthorized writes, unregistered interfaces, and capability expansion |
| ADR trigger detection | 100% detection on fixtures that alter frozen layers, observatories, governance structures, or agent authority |
| Report reproducibility | Fixed inputs produce matching finding IDs, severities, and authority citations |
| Read-only enforcement | 0 write, deployment, record-modification, or approval side effects in production environments |

Evaluated by [Benchmark Agent](23-benchmark-agent.md); Draft registration means benchmarks are declared but not fleet-registered until operational promotion.

---

## 15. Failure Conditions

| Condition | Severity |
|-----------|----------|
| Canonical write, registry modification, record mutation, or deployment action from an Architecture Agent run | **Critical** — Safety Review failure |
| Report presents advisory recommendation as human approval | **Critical** — governance violation |
| Failure to flag architecture expansion requiring ADR under ADR-011 | **Blocker** |
| Service boundary bypass or undeclared capability missed in review fixture | **Blocker** |
| Material finding without canonical citation | **Blocker** — report inadmissible |
| Steward-impact finding routed without steward authority | **Blocker** |
| Dependency or technology recommendation lacks risk and replacement-path analysis | **Warning** |

---

## 16. Relationship to Other Agents

| Agent | Relationship |
|-------|--------------|
| [Standards Agent](22-standards-agent.md) | Supplies standards conformance evidence; Architecture Agent reviews architectural implications of standards gaps or waivers |
| [Benchmark Agent](23-benchmark-agent.md) | Evaluates Architecture Agent benchmark requirements and consumes architecture compliance signals |
| [Research Agent](25-research-agent.md) | Routes research findings that imply architecture change to Architecture Agent for ADR and boundary review |
| [Audit Agent](26-audit-agent.md) | Consumes accepted review dispositions and waiver records for governance audit evidence |
| [Security Agent](27-security-agent.md) | Coordinates on dependency, connector, and boundary risks with security impact |
| [Platform Engineering Agent](28-platform-engineering-agent.md) | Receives service-boundary and stack recommendations for implementation remediation |
| [SRE Agent](29-sre-agent.md) | Receives operational-risk findings affecting reliability, observability, and release readiness |
| [Data Governance Agent](32-data-governance-agent.md) | Coordinates on data model, lineage, residency, and rights-boundary findings |
| [Frontend Architecture Agent](35-frontend-architecture-agent.md) | Coordinates on public experience contract, accessibility, and interface-boundary findings |
| Platform and observatory agents (09–21) | Reviewed for compliance with canonical boundaries, ADRs, capability declarations, and output contracts |

---

*Previous: [23-benchmark-agent.md](23-benchmark-agent.md) · Next: [25-research-agent.md](25-research-agent.md)*
