# Agent Checks Registry

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Status** | Canonical |
| **Authority** | Open Grace Architecture Office |
| **Date** | 2026-06-22 |
| **Purpose** | Fleet-wide Evidence, Provenance, and Compliance check normalization |

This registry is the authoritative index of agent-check posture across the canonical agent suite. It aligns with [03-canonical-architecture.md](../architecture/canonical/03-canonical-architecture.md) §6.6 (Evidence Output Profile), §6.2 (Provenance), and [23-benchmark-agent.md](../architecture/canonical/23-benchmark-agent.md) §5.4 (Registered Canonical Agent Fleet).

---

## Registry

| Agent | Plane | Evidence Check | Provenance Check | Compliance Check | Benchmark Coverage | Status |
|-------|-------|----------------|------------------|------------------|-------------------|--------|
| Source Discovery Agent | Platform | Discovery record source URI and rights pre-screening signals | Provenance chain intact — discovery event, harvest run, agent version | Covenant-before-harvest; no canonical writes without approval | Registered — §AI Fabric Governance | Registered |
| Metadata Agent | Platform | Evidence Output Profile on Entity Assertions ([03](../architecture/canonical/03-canonical-architecture.md) §6.6) | Provenance chain intact — modeling event, source ARK, agent version | Schema validation (SHACL, Darwin Core); rights metadata mandatory | Registered — §AI Fabric Governance | Normalized |
| Preservation Agent | Platform | PREMIS fixity and migration events as audit evidence | Provenance chain intact — ingest event, agent version, PREMIS event | OAIS boundary respect; experience-plane write isolation | Registered — §AI Fabric Governance | Registered |
| Knowledge Graph Agent | Platform | Evidence Output Profile on link and relationship proposals ([03](../architecture/canonical/03-canonical-architecture.md) §6.6) | Provenance chain intact — modeling event, reconciliation run, agent version | Layer-boundary conformance; external links as claims with confidence | Registered — §AI Fabric Governance | Normalized |
| Quality Review Agent | Platform | Quality Review Records with findings and input snapshot hash | Provenance chain intact — review run, agent version, steward disposition | Explicit Checks: metadata, rights, accessibility (WCAG 2.1 AA), completeness | Registered — §AI Fabric Governance | Registered |
| Translation Agent | Platform | Translation memory alignment and segment-level source linkage | Provenance mandatory — source segment, method, approving event | Indigenous-language consent gates; terminology compliance benchmark | Registered — §AI Fabric Governance | Registered |
| Publishing Agent | Platform | Citation completeness; IIIF manifest validity benchmark | Provenance mandatory — graph snapshot, quality clearance, steward event | Editorial and rights gate compliance; no publish without approval | Registered — §AI Fabric Governance | Registered |
| Education Agent | Experience | Provenance appendix on learning resources; canonical anchor per factual claim | Provenance chain intact — source narratives, agent version, approving educator event | WCAG 2.1 AA; rights-before-classroom; curator authority on sensitive topics | Registered — §AI Fabric Governance | Normalized |
| Biodiversity Observatory Agent | Experience — Observatories | Evidence Output Profile on Observatory Observation Records ([03](../architecture/canonical/03-canonical-architecture.md) §6.6) | Provenance chain intact + canonical taxon anchors — datasets, ingest events, `prov:wasDerivedFrom` | No conservation status invention; coordinate sensitivity; steward approval before public alert | Registered — §AI Fabric Governance | Normalized |
| Climate Observatory Agent | Experience — Observatories | Evidence Output Profile on Observation Proposals ([03](../architecture/canonical/03-canonical-architecture.md) §6.6) | Provenance chain intact + graph anchors + partner attribution | No public heritage-risk without approval; uncertainty explicit; peer observatory boundaries | Registered — §AI Fabric Governance | Normalized |
| Heritage Observatory Agent | Experience — Observatories | Evidence Output Profile on Observation Proposals; evidence URIs and confidence on status ratings ([03](../architecture/canonical/03-canonical-architecture.md) §6.6) | Provenance chain intact — registered source, ingest event, agent version | State-party authority; security-sensitive threat gating; no unverified damage claims | Registered — §AI Fabric Governance | Normalized |
| Tourism Observatory Agent | Experience — Observatories | Evidence Output Profile on Observation Proposals ([03](../architecture/canonical/03-canonical-architecture.md) §6.6) | Provenance mandatory — PREMIS-aligned audit events per metric | Privacy k-anonymity gates; covenant compliance; no PII emission | Registered — §AI Fabric Governance | Normalized |
| Language Observatory Agent | Experience — Observatories | Evidence Output Profile on Vitality Observations ([03](../architecture/canonical/03-canonical-architecture.md) §6.6) | Provenance mandatory — feed URI, harvest event, steward approval | Community-consent compliance; no status downgrade without human approval | Registered — §AI Fabric Governance | Normalized |
| Standards Agent | Constitutional | Standards Compliance Reports as exportable evidence artifacts | Verification run ID, validator versions, input snapshot hash on reports | Explicit Checks: CIDOC-CRM SHACL, Darwin Core / DwC-A, schema.org JSON-LD | Registered — §AI Fabric Governance | Registered |
| Benchmark Agent | Constitutional | Benchmark Reports and fleet scorecards; PREMIS-aligned audit events | Benchmark run ID, dataset snapshot hash, suite version on reports | Architecture compliance Checks (§5.3); Evidence Output Profile validation on assertion-making agents | Self — meta-benchmarks §7 | Normalized |

---

## Check Definitions

### Evidence Check

Agents that emit factual assertions, link proposals, or observatory observations MUST populate the [Evidence Output Profile](../architecture/canonical/03-canonical-architecture.md#66-evidence-output-profile): `evidenceURIs[]`, `confidence`, `evidenceSummary`, `method`, `sourceRegistryRefs[]`, `provenanceEventId`. Governance agents emit exportable report artifacts as milestone or fleet evidence.

### Provenance Check

Every agent maintains an auditable chain per [03-canonical-architecture.md](../architecture/canonical/03-canonical-architecture.md) §6.2. Constitutional constraint language is **Provenance chain intact** (platform and observatory agents) or **Provenance mandatory** (translation, publishing, tourism, language agents) with domain-specific anchor requirements where applicable.

### Compliance Check

Binding compliance is verified through explicit `Checks` sections (Quality Review, Standards, Benchmark agents), constitutional constraints, standards registry bindings ([07-reference-standards.md](../architecture/canonical/07-reference-standards.md)), and ADR constraints ([08-decision-record.md](../architecture/canonical/08-decision-record.md)).

### Benchmark Coverage

**Registered** — agent appears in [23-benchmark-agent.md](../architecture/canonical/23-benchmark-agent.md) §5.4 with benchmarks declared in agent §AI Fabric Governance.

**Self** — Benchmark Agent meta-benchmarks against itself before fleet-wide production runs.

---

## Maintenance

Updates to this registry require alignment with agent specification changes and Architecture Office review. Superseded check postures are recorded in [remediation/agent-checks-audit-remediation.md](remediation/agent-checks-audit-remediation.md).

---

*Governance: [architecture-registry.md](architecture-registry.md) · Fleet: [23-benchmark-agent.md](../architecture/canonical/23-benchmark-agent.md) §5.4*
