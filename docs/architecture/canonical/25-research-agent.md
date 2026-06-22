# Research Agent

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Status** | Canonical |
| **Authority** | Open Grace Architecture Office |
| **Date** | 2026-06-22 |
| **Capability** | AI Fabric — Research Council ([04-system-diagram.md](04-system-diagram.md), §2.2) |
| **Phase** | Cross-cutting — Research Fabric phases onward ([06-build-roadmap.md](06-build-roadmap.md)) |

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

The **Research Agent** automates Research Council support within the AI Fabric governance chain ([04-system-diagram.md](04-system-diagram.md), §2.2). It conducts structured investigations, gathers and synthesizes evidence from authoritative sources and platform corpora, maintains gold evaluation datasets for agent benchmarks, and emits **Research Findings Reports** (JSON-LD) for council and Architecture Office review.

The agent does not write canonical metadata, assert knowledge-graph entities, publish research conclusions as canonical fact, or bypass steward approval. It investigates, documents evidence, and reports; researchers and stewards decide disposition.

---

## 2. Authority

| Authority | Scope |
|-----------|-------|
| **Research Council** | Primary council assignment; methodology, gold datasets, evaluation design |
| **Open Grace Architecture Office** | Accepts research findings that affect architecture, standards, or milestone gates |
| **Research Fabric** | Authenticated researcher access layer ([03-canonical-architecture.md](03-canonical-architecture.md), §4.8) — read scope for investigations |
| **Architecture v1.0** | Investigations operate within frozen layers; scope expansion requires ADR ([ADR-011](08-decision-record.md#adr-011-architecture-freeze-v10)) |

---

## 3. Responsibilities

| Responsibility | Description |
|----------------|-------------|
| **Structured investigation** | Execute reproducible research protocols on source corpora, partner feeds, and platform outputs; document hypotheses, methods, and limitations |
| **Evidence gathering** | Collect supporting material with URIs, confidence tiers, and derivation context per Evidence Output Profile where findings inform assertions |
| **Gold dataset curation** | Maintain version-controlled evaluation datasets for Benchmark Agent quality metric suites |
| **Methodology review** | Assess reproducibility, peer-reviewability, and institutional alignment (MIT pattern, [02-reference-models.md](02-reference-models.md)) |
| **Findings synthesis** | Emit Research Findings Reports with cited sources, uncertainty bounds, and recommended actions |

---

## 4. Inputs

| Input | Source |
|-------|--------|
| Authoritative sources | UNESCO, GBIF, Wikidata, Europeana, and registered Source Registry entries ([04-system-diagram.md](04-system-diagram.md), §2) |
| Platform corpora | Preservation descriptors, Entity Assertions, graph exports — read-only |
| Research Fabric APIs | Authenticated bulk export and query endpoints |
| Investigation briefs | Council assignments, milestone gate questions, Benchmark Agent dataset requests |
| Reference models | [02-reference-models.md](02-reference-models.md) — MIT reproducibility, Harvard accountability |
| Standards registry | [07-reference-standards.md](07-reference-standards.md) — ontology versions, interoperability contracts |

---

## 5. Outputs

### 5.1 Research Findings Reports

Each investigation emits **JSON-LD** with:

| Field | Requirement |
|-------|-------------|
| **Investigation scope** | Question, corpus slice, time bounds, domain |
| **Method** | Reproducible protocol identifier; limitations stated |
| **Findings** | Structured conclusions with uncertainty and confidence |
| **Evidence** | `evidenceURIs[]`, `sourceRegistryRefs[]`, supporting excerpts or dataset references |
| **Recommendations** | Non-binding actions for councils, stewards, or Architecture Office |
| **Provenance** | Investigation run identifier, agent version, input snapshot hash, dataset versions |

### 5.2 Gold Evaluation Datasets

Version-controlled held-out datasets for Benchmark Agent quality benchmarks:

- Manifest with DOI or institutional URI when published
- Steward approval before production benchmark use
- Change log linked to investigation runs

### 5.3 Data-Gap Signals

When evidence is insufficient for a requested conclusion, emit explicit data-gap signals rather than speculative assertions.

---

## 6. Checks

| Check domain | Specification |
|--------------|---------------|
| **Reproducibility** | Investigation protocol documented; identical inputs yield identical findings |
| **Source registration** | All cited sources resolve to Source Registry entries or authoritative URIs |
| **Evidence sufficiency** | Findings that inform assertions include complete Evidence Output Profile fields ([03-canonical-architecture.md](03-canonical-architecture.md), §6.6) |
| **Rights respect** | No investigation exports restricted corpora without rights clearance |
| **Freeze compliance** | Investigations do not propose new layers, observatories, or governance structures without ADR |
| **Uncertainty explicit** | Confidence tiers and limitations documented on all material findings |

---

## 7. Constraints

- **Investigate, do not assert.** Research outputs are findings and recommendations, not canonical Entity Assertions.
- **Architecture v1.0 bound.** Investigations operate within existing layers and observatories per [ADR-011](08-decision-record.md#adr-011-architecture-freeze-v10).
- **No canonical writes.** Read-only access to Preservation, Knowledge Graph, and public experience unless explicit test-environment isolation.
- **Reproducibility required.** Follow MIT open-evaluation patterns ([02-reference-models.md](02-reference-models.md)); publish methodology to Research Registry when approved.
- **Steward authority preserved.** Findings affecting cultural sensitivity, indigenous knowledge, or rights route to human review.
- **Gold dataset governance.** Dataset changes require Research Council approval before Benchmark Agent production use.

---

## 8. Success Criteria

- Research Findings Reports generated for 100% of council-assigned investigations within SLA
- Gold datasets registered for all Benchmark Agent quality metric suites requiring held-out evaluation
- Reproducibility demonstrated: re-run investigations match prior findings on fixed inputs
- Zero canonical writes from research runs in production environment
- End-to-end demonstration: investigation brief → evidence gathering → Research Findings Report → council disposition → benchmark dataset registration

---

## 9. Evidence Requirements

| Output type | Evidence contract |
|-------------|-------------------|
| Research Findings Reports | `evidenceURIs[]`, `confidence`, `evidenceSummary`, `method`, `sourceRegistryRefs[]`, `provenanceEventId` on material findings |
| Gold datasets | Manifest with provenance, version hash, steward approval reference |
| Data-gap signals | Explicit insufficient-evidence declaration with searched corpus scope |

Governance agents emit exportable report artifacts ([docs/governance/agent-checks-registry.md](../../governance/agent-checks-registry.md)). Findings that do not inform factual assertions may omit numeric confidence when reporting pure methodology gaps.

---

## 10. Provenance Requirements

| Requirement | Specification |
|-------------|---------------|
| **Investigation run identity** | Unique identifier on every Research Findings Report |
| **Input traceability** | Snapshot hash of corpora, queries, and source versions investigated |
| **Method binding** | Protocol identifier and version on all findings |
| **Provenance chain intact** | Investigations read platform artifacts without breaking Source → Discovery → Ingest → Preservation → Modeling → Graph chain ([03-canonical-architecture.md](03-canonical-architecture.md), §6.2) |
| **Audit events** | Council disposition on findings persisted PREMIS-aligned when findings affect gates or datasets |

---

## 11. Compliance Requirements

| Requirement | Source |
|-------------|--------|
| Research Fabric access model | [03-canonical-architecture.md](03-canonical-architecture.md), §4.8 |
| Evidence Output Profile | [03-canonical-architecture.md](03-canonical-architecture.md), §6.6 |
| Architecture freeze | [ADR-011](08-decision-record.md#adr-011-architecture-freeze-v10) |
| Rights and covenant | [03-canonical-architecture.md](03-canonical-architecture.md), §6.3; partner covenants |
| Reproducibility standards | [07-reference-standards.md](07-reference-standards.md); Research Registry conventions |

---

## 12. Human Approval Requirements

| Action | Approver |
|--------|----------|
| Accept Research Findings Report for gate or policy action | Research Council; Architecture Office when architecture-affecting |
| Publish gold dataset to production benchmarks | Research Council |
| Release investigation affecting indigenous or sensitive corpora | Steward and Research Council |
| Elevate finding to canonical assertion | Metadata Agent or domain steward via standard approval gates — not Research Agent |

---

## 13. Benchmark Requirements

| Benchmark | Threshold |
|-----------|-----------|
| Investigation reproducibility | 100% match on fixed-input re-runs |
| Source citation completeness | 100% material findings cite registered sources |
| False assertion rate | 0% — no canonical writes from research runs |
| Gold dataset integrity | Manifest hash stable across benchmark cycles unless version bumped |
| Methodology documentation coverage | 100% investigations include protocol identifier |

Evaluated by [Benchmark Agent](23-benchmark-agent.md); meta-benchmarks on dataset curation accuracy.

---

## 14. Failure Conditions

| Condition | Severity |
|-----------|----------|
| Canonical write from research run | **Critical** — Safety Review failure |
| Finding without source citation | **Blocker** — report inadmissible |
| Speculative assertion presented as finding | **Blocker** — steward escalation |
| Gold dataset used in production without council approval | **Blocker** |
| Investigation proposing new layer/observatory without ADR flag | **Warning** — route to Architecture Agent |
| Broken reproducibility on re-run | **Blocker** — hold dataset and report |

---

## 15. Relationship to Other Agents

| Agent | Relationship |
|-------|--------------|
| [Benchmark Agent](23-benchmark-agent.md) | Primary consumer of gold datasets; Research Agent supplies quality metric evaluation corpora |
| [Architecture Agent](24-architecture-agent.md) | Gates ADR requirements when research findings imply architecture change |
| [Metadata Agent](10-metadata-agent.md) | Entity Assertions originate from modeling; Research Agent informs but does not replace |
| [Knowledge Graph Agent](12-knowledge-graph-agent.md) | Graph exports inform investigations; link proposals remain curator-gated |
| [Standards Agent](22-standards-agent.md) | Advises on ontology version upgrades and standard adapter evaluation |
| [Audit Agent](26-audit-agent.md) | Supplies investigation evidence for covenant and compliance audits |
| Observatory agents (17–21) | Observatory feeds are investigation inputs; no new observatories created |
| [Data Governance Agent](32-data-governance-agent.md) | Coordinates lineage and retention policy for research corpora |

---

*Previous: [24-architecture-agent.md](24-architecture-agent.md) · Next: [26-audit-agent.md](26-audit-agent.md)*
