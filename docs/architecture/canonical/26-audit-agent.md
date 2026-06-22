# Audit Agent

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Status** | Canonical |
| **Registration State** | Draft |
| **Authority** | Open Grace Audit & Compliance Office |
| **Date** | 2026-06-22 |
| **Capability** | AI Fabric - Governance Audit ([Capability Registry](../../governance/capability-registry.md)) |
| **Phase** | Cross-cutting - milestone gates, partner audits, and permanence review ([06-build-roadmap.md](06-build-roadmap.md)) |

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

The **Audit Agent** validates evidence integrity, provenance integrity, benchmark compliance, standards compliance, and steward approval chains across the Open Grace platform. It emits structured audit artifacts for the Open Grace Audit & Compliance Office, Architecture Office, councils, and partner stewards.

The Audit Agent is **read-only**. It does not approve deployments, perform canonical writes, modify records, or bypass steward authority. It inspects, verifies, and reports; humans and designated offices decide disposition.

Architecture v1.0 remains frozen. The Audit Agent operates within the existing Governance Audit capability declared in the [Capability Registry](../../governance/capability-registry.md) and does not add layers, observatories, products, or canonical write paths outside [ADR-011](08-decision-record.md#adr-011-architecture-freeze-v10).

---

## 2. Authority

| Authority | Scope |
|-----------|-------|
| **Open Grace Audit & Compliance Office** | Primary owner for audit methodology, audit report acceptance, and compliance posture review |
| **ADR-011 - Architecture Freeze v1.0** | Bounds audit scope to frozen Architecture v1.0; changes beyond registered capability scope require ADR ([ADR-011](08-decision-record.md#adr-011-architecture-freeze-v10)) |
| **Architecture Registry** | Defines the approved architecture baseline audited by this agent ([architecture-registry.md](../../governance/architecture-registry.md)) |
| **Capability Registry** | Registers Governance Audit capability and Draft registration state ([capability-registry.md](../../governance/capability-registry.md)) |

---

## 3. Responsibilities

| Responsibility | Description |
|----------------|-------------|
| **Evidence Audit** | Verify that report findings, assertions, proposals, and review records include required Evidence Output Profile fields and cite resolvable supporting material |
| **Provenance Audit** | Validate that provenance chains remain intact from source through discovery, ingest, preservation, modeling, graph placement, quality verification, publication, and governance review |
| **Standards Audit** | Review Standards Reports and Standards Agent outputs for Required and Recommended standard coverage, waiver traceability, and milestone-gate evidence sufficiency |
| **Benchmark Audit** | Review Benchmark Reports for registered suite execution, threshold comparison, reproducibility, and Architecture Office or council disposition status |
| **Steward Approval Audit** | Verify steward, curator, researcher, educator, partner, or Architecture Office approvals are present before protected actions affect canonical systems or public surfaces |
| **Registry Audit** | Compare Agent Registry, Capability Registry, Architecture Registry, Standards Registry, and Source Registry references against emitted artifacts and declared capabilities |
| **Preservation Audit** | Inspect PREMIS-aligned fixity, migration, retention, restore, and replication evidence without altering preservation records |
| **Constitutional Compliance Audit** | Verify covenant, rights, access, public-good, and mission constraints are reflected in evidence and disposition chains |
| **Architecture Compliance Audit** | Check reported behavior against canonical architecture, ADR constraints, layer boundaries, and no-write governance-agent boundaries |

---

## 4. Reference Models

The Audit Agent applies institutional patterns from [02-reference-models.md](02-reference-models.md):

| Model | Pattern Applied | Agent Behavior |
|-------|-----------------|----------------|
| **Harvard** | Centuries-scale stewardship, curatorial authority, differentiated treatment for rare or sensitive collections | Treat steward decisions as authoritative audit evidence; flag missing approval chains on authenticity, attribution, sensitivity, rights, or preservation-tier decisions |
| **MIT** | Reproducible research infrastructure, open access, repository discipline | Require repeatable audit methods, stable input snapshots, report manifests, and methodology identifiers for peer-reviewable compliance evidence |
| **Internet Archive** | Permanence ethic, temporal versioning, format migration, web-scale archival accountability | Verify preservation events, version history, fixity checks, and migration documentation are complete and durable across long horizons |
| **Google** | Quality-at-scale measurement, knowledge infrastructure, distributed operations | Audit fleet-wide benchmark, standards, registry, and provenance signals at platform scale while preserving explicit evidence references for each finding |

---

## 5. Inputs

| Input | Source |
|-------|--------|
| **Provenance Events** | PREMIS-aligned and institutional provenance events from discovery, ingest, preservation, modeling, graph placement, quality verification, publication, and governance review |
| **Benchmark Reports** | Benchmark Agent reports, scorecards, suite manifests, threshold comparisons, and remediation dispositions |
| **Standards Reports** | Standards Agent compliance reports, validator artifacts, waiver records, and milestone-gate summaries |
| **Quality Review Records** | Quality Review Agent findings, rights and accessibility outcomes, steward dispositions, and publication readiness records |
| **Research Review Records** | Research Agent findings, gold dataset manifests, methodology reviews, and Research Council dispositions |
| **Registry Records** | Architecture Registry, Capability Registry, Agent Registry, Source Registry, Standards Registry, and agent checks registry entries |
| **Steward Decisions** | Human approval records from stewards, curators, researchers, educators, councils, Architecture Office, and partner authorities |

---

## 6. Outputs

### 6.1 Audit Report

Each audit run emits **JSON-LD** with:

| Field | Requirement |
|-------|-------------|
| **Audit scope** | Platform slice, milestone gate, partner covenant, agent version, registry domain, or preservation corpus audited |
| **Audit domains** | Evidence, provenance, standards, benchmark, steward approval, registry, preservation, constitutional compliance, architecture compliance |
| **Method** | Audit method identifier, version, input selection criteria, and limitations |
| **Findings** | Structured findings with severity, affected records, cited requirements, and confidence |
| **Evidence** | Evidence Requirements fields from Section 10 on every material finding |
| **Disposition status** | `draft`, `submitted`, `accepted`, `remediation-required`, `waiver-required`, or `closed` |
| **Provenance** | Audit run identifier, agent version, input snapshot hash, and provenance event identifier |

Audit Reports are evidence artifacts. They do not approve deployments, write canonical state, or close remediation without human approval.

### 6.2 Evidence Audit Report

Focused report for Evidence Output Profile coverage:

- Missing or malformed `evidenceURIs[]`
- Missing confidence or unsupported confidence scale
- Insufficient `evidenceSummary`
- Method identifier absent or not registered
- Missing `sourceRegistryRefs[]`
- Missing or invalid `provenanceEventId`

### 6.3 Provenance Audit Report

Focused report for provenance integrity:

- Broken Source -> Discovery -> Ingest -> Preservation -> Modeling -> Graph -> Quality -> Publication chain
- Missing PREMIS-aligned events where required
- Input snapshot hash mismatch
- Report-to-record lineage gap
- Approval event not linked to affected record or report

### 6.4 Compliance Report

Aggregated standards, benchmark, constitutional, and architecture compliance status:

- Standards compliance posture by Required and Recommended level
- Benchmark threshold and regression posture
- Architecture freeze compliance against ADR-011
- Capability and registry consistency
- Steward approval completeness

### 6.5 Remediation Report

Non-binding remediation routing:

| Finding class | Routed to |
|---------------|-----------|
| Evidence field missing or incomplete | Owning agent maintainer; steward if assertion cannot be supported |
| Provenance chain gap | Data Governance Agent, Preservation Governance Agent, or source pipeline owner |
| Standards failure or undocumented waiver | Standards Agent; Architecture Office |
| Benchmark threshold failure | Benchmark Agent; relevant council |
| Missing steward approval | Owning steward, curator, researcher, educator, partner authority, or Architecture Office |
| Registry drift | Architecture Agent; Capability Registry maintainer; Architecture Office |
| Preservation fixity or migration gap | Preservation Agent; Preservation Governance Agent; steward |
| Constitutional or covenant violation | Audit & Compliance Office; Architecture Office; partner steward |

---

## 7. Checks

| Check domain | Specification |
|--------------|---------------|
| **Evidence integrity** | Evidence Requirements fields are present, syntactically valid, source-resolvable, and consistent with the finding being audited |
| **Provenance integrity** | Every audited artifact links to an auditable event chain per [03-canonical-architecture.md](03-canonical-architecture.md) Section 6.2 |
| **Standards compliance** | Standards Reports cite applicable standards and distinguish Required blockers from Recommended gaps per [07-reference-standards.md](07-reference-standards.md) |
| **Benchmark compliance** | Benchmark Reports include registered benchmark suite, input snapshot hash, threshold comparison, and human disposition |
| **Steward approval chain** | Human approval exists before canonical writes, public publication, sensitive-corpus release, migrations, restores, waivers, or gate acceptance |
| **Registry consistency** | Artifacts reference valid registry entries and do not declare capabilities absent from authoritative registries |
| **Preservation integrity** | Fixity, migration, retention, restore, and replication events are complete, PREMIS-aligned, and linked to preservation objects |
| **Constitutional compliance** | Rights, covenant, public-good, mission, and sensitive-knowledge constraints are satisfied or routed to human review |
| **Architecture compliance** | Behavior conforms to Architecture v1.0, ADR-011 freeze boundaries, layer boundaries, and governance-agent read-only constraints |

---

## 8. Constraints

- **Read-only.** The Audit Agent inspects records, events, reports, and registries; it never modifies them.
- **No canonical writes.** Audit findings are report artifacts only and do not create, update, delete, or publish canonical records.
- **No deployment authority.** The agent does not approve, promote, roll back, or block deployments on its own.
- **No steward bypass.** Steward, curator, council, partner, and Architecture Office authority remains final for approvals and waivers.
- **Architecture v1.0 bound.** Audit scope remains within the frozen architecture and Draft Governance Audit capability per [ADR-011](08-decision-record.md#adr-011-architecture-freeze-v10).
- **Registry is authoritative.** Capability, architecture, standard, source, and agent declarations come from the relevant registries; drift is reported, not corrected by the Audit Agent.
- **Evidence before conclusion.** Material findings without sufficient evidence are emitted as data-gap or inadmissible-audit findings, not compliance conclusions.

---

## 9. Success Criteria

- Audit Reports generated for 100% of assigned milestone gates, partner covenant audits, and governance review scopes
- Evidence Audit Reports validate Evidence Output Profile coverage on all material audited findings
- Provenance Audit Reports identify zero untriaged breaks in required provenance chains before gate acceptance
- Standards and Benchmark audit coverage includes report integrity, threshold/waiver traceability, and human disposition
- Steward Approval Audits confirm required human approval chains before canonical writes, publication, migrations, restores, or waivers
- Registry Audits detect no unreviewed capability, architecture, standards, source, or agent drift before production governance-chain use
- End-to-end demonstration: registry-scoped audit request -> read-only artifact inspection -> Audit Report -> remediation routing -> human acceptance

---

## 10. Evidence Requirements

| Output type | Evidence contract |
|-------------|-------------------|
| Audit Report | `evidenceURIs[]`, `confidence`, `evidenceSummary`, `method`, `sourceRegistryRefs[]`, `provenanceEventId` on every material finding |
| Evidence Audit Report | Evidence field inventory with references to affected artifacts and source registry entries |
| Provenance Audit Report | Provenance event graph references, input snapshot hash, and broken-chain location when applicable |
| Compliance Report | Standards, benchmark, ADR, registry, and steward decision references supporting each compliance status |
| Remediation Report | Finding reference, affected artifact, responsible office or agent, and human disposition requirement |

The required fields are:

| Field | Requirement |
|-------|-------------|
| **evidenceURIs[]** | URIs of supporting source records, preserved objects, reports, registry entries, or steward-reviewed documents |
| **confidence** | Numeric score (0.0-1.0) or registered confidence tier for each material finding |
| **evidenceSummary** | Human-readable summary of supporting evidence, limitations, and derivation context |
| **method** | Audit method identifier and version |
| **sourceRegistryRefs[]** | Registered Source Registry or registry-reference URIs for upstream sources |
| **provenanceEventId** | PREMIS-aligned or institutional provenance event identifier linking the finding to the audit run |

Governance agents emit exportable report artifacts ([agent-checks-registry.md](../../governance/agent-checks-registry.md)). Findings without sufficient evidence are inadmissible for gate or waiver decisions until remediated or explicitly accepted by human authority.

---

## 11. Provenance Requirements

| Requirement | Specification |
|-------------|---------------|
| **Audit run identity** | Unique identifier on every Audit Report and focused report |
| **Input traceability** | Snapshot hash of every audited report set, registry set, event set, corpus slice, and steward decision set |
| **Method binding** | Audit method identifier, version, and rule-pack reference on all material findings |
| **Provenance chain intact** | Audits preserve the Source -> Discovery -> Ingest -> Preservation -> Modeling -> Graph Placement -> Quality Verification -> Publication chain ([03-canonical-architecture.md](03-canonical-architecture.md), Section 6.2) |
| **Audit event linkage** | Human acceptance, waiver, remediation, or rejection of Audit Reports is persisted as a separate approval event by the responsible authority, not by the Audit Agent |

---

## 12. Compliance Requirements

| Requirement | Source |
|-------------|--------|
| Architecture freeze | [ADR-011](08-decision-record.md#adr-011-architecture-freeze-v10) |
| Approved architecture baseline | [Architecture Registry](../../governance/architecture-registry.md) |
| Governance Audit capability and Draft registration state | [Capability Registry](../../governance/capability-registry.md) |
| Evidence Output Profile | [03-canonical-architecture.md](03-canonical-architecture.md), Section 6.6 |
| Provenance model | [03-canonical-architecture.md](03-canonical-architecture.md), Section 6.2 |
| AI Fabric governance chain | [04-system-diagram.md](04-system-diagram.md), Section 2.2 |
| Standards compliance verification | [07-reference-standards.md](07-reference-standards.md), Section 14; [Standards Agent](22-standards-agent.md) |
| Benchmark compliance verification | [Benchmark Agent](23-benchmark-agent.md) |
| Agent check normalization | [agent-checks-registry.md](../../governance/agent-checks-registry.md) |

---

## 13. Human Approval Requirements

Human approval is required: **Yes**.

| Action | Approver |
|--------|----------|
| Accept Audit Report for milestone certification | Open Grace Audit & Compliance Office; Architecture Office when architecture-affecting |
| Accept partner covenant audit or external compliance evidence | Audit & Compliance Office; partner steward or designated partner authority |
| Accept remediation closure | Owning council, steward, or office for the remediated domain |
| Grant waiver for standards, benchmark, or architecture compliance finding | Architecture Office via ADR or documented waiver path |
| Certify steward approval chain for sensitive, indigenous, rights-restricted, or preservation-critical material | Responsible steward or partner authority |
| Promote Audit Agent from Draft to Operational | Architecture Office after Agent Registry registration, graph factory registration, Benchmark Agent coverage, and safety review |

---

## 14. Benchmark Requirements

| Benchmark | Threshold |
|-----------|-----------|
| Read-only enforcement | 100% of audit runs perform no canonical writes, record modifications, deployment actions, or registry writes |
| Evidence field detection | 100% detection on fixtures with missing required Evidence Requirements fields |
| Provenance break detection | 100% detection on fixed fixtures with injected chain gaps |
| Steward approval detection | 100% detection on protected-action fixtures with missing approval records |
| Registry drift detection | 100% detection on fixtures with unregistered capabilities, stale registry references, or mismatched agent declarations |
| Standards and benchmark report coverage | 100% assigned reports checked for required fields, threshold/waiver references, and human disposition |
| Reproducibility | 100% identical findings on fixed-input re-runs |

Evaluated by [Benchmark Agent](23-benchmark-agent.md); registration remains Draft until benchmark coverage is registered and accepted.

---

## 15. Failure Conditions

| Condition | Severity |
|-----------|----------|
| Canonical write, record modification, registry write, or deployment action from audit run | **Critical** - Safety Review failure |
| Audit Report used as deployment or canonical-write approval without human acceptance | **Critical** - steward authority violation |
| Material finding missing required evidence fields | **Blocker** - finding inadmissible |
| Provenance chain break not detected in assigned audit scope | **Blocker** |
| Standards or benchmark waiver accepted without Architecture Office or ADR trace | **Blocker** |
| Protected action lacks steward approval chain | **Blocker** |
| Registry drift reported without authoritative registry reference | **Warning** - report remediation required |
| Audit methodology absent or irreproducible | **Blocker** |

---

## 16. Relationship to Other Agents

| Agent | Relationship |
|-------|--------------|
| [Standards Agent](22-standards-agent.md) | Provides Standards Reports audited for standards compliance, waiver traceability, and milestone evidence sufficiency |
| [Benchmark Agent](23-benchmark-agent.md) | Provides Benchmark Reports audited for suite registration, threshold comparison, reproducibility, and human disposition |
| [Research Agent](25-research-agent.md) | Provides Research Review Records and gold dataset evidence for audit; Audit Agent checks evidence and approval integrity |
| [Architecture Agent](24-architecture-agent.md) | Receives architecture drift and ADR-required findings; Audit Agent does not create ADRs or alter architecture |
| [Quality Review Agent](13-quality-review-agent.md) | Provides Quality Review Records and steward dispositions audited before publication or research-channel release |
| [Preservation Agent](11-preservation-agent.md) | Provides preservation events, fixity records, and migration/restore evidence audited for preservation integrity |
| [Knowledge Graph Agent](12-knowledge-graph-agent.md) | Provides graph placement, link proposal, and provenance artifacts audited for layer-boundary and evidence integrity |
| [Data Governance Agent](32-data-governance-agent.md) | Receives lineage, rights, and retention findings requiring policy remediation |
| [Security Agent](27-security-agent.md) | Receives security-relevant audit findings; Audit Agent remains compliance-focused and read-only |

---

*Previous: [25-research-agent.md](25-research-agent.md) | Next: [27-security-agent.md](27-security-agent.md)*
