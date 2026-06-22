# Capability Registry

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Status** | Canonical |
| **Authority** | Open Grace Architecture Office |
| **Date** | 2026-06-22 |
| **Purpose** | Authoritative index of agent capabilities, registration posture, and governance coverage |

This registry is the authoritative index of agent capabilities across the canonical agent suite. It aligns with [03-canonical-architecture.md](../architecture/canonical/03-canonical-architecture.md), [04-system-diagram.md](../architecture/canonical/04-system-diagram.md) §2.2 (AI Fabric governance chain), and [23-benchmark-agent.md](../architecture/canonical/23-benchmark-agent.md) §5.4 (Registered Canonical Agent Fleet).

**Registration State** values:

- **Draft** — specification complete; not operational. No graph factory, no production runs, no fleet benchmark registration.
- **Operational** — registered in Agent Registry, graph-bound, and eligible for production governance-chain runs.

Agents 09–23 remain registered via the operational Agent Registry manifest. Entries below cover agents 24–35 only.

---

## Registry

| Capability ID | Agent | Number | Plane | Spec | Registration State | Benchmark Coverage | Standards Coverage | Human Approval Requirement |
|---------------|-------|--------|-------|------|--------------------|--------------------|--------------------|----------------------------|
| `wise:agent:architecture` | Architecture Agent | 24 | Governance / Architecture Office | [24-architecture-agent.md](../architecture/canonical/24-architecture-agent.md) | Draft | Required | Required | Required |
| `wise.capability.research-council` | Research Agent | 25 | AI Fabric — Research Council | [25-research-agent.md](../architecture/canonical/25-research-agent.md) | Draft | Pending — spec §13 declared, not fleet-registered | Research Fabric access (03 §4.8); Evidence Output Profile (03 §6.6); rights/covenant (03 §6.3); reproducibility (07) | Research Council for findings and gold datasets; Architecture Office when architecture-affecting; steward for sensitive corpora |
| `wise:agent:audit` | Audit Agent | 26 | Governance / Audit & Compliance | [26-audit-agent.md](../architecture/canonical/26-audit-agent.md) | Draft | Required | Required | Required |
| `wise.capability.security` | Security Agent | 27 | Open Grace — Security | [27-security-agent.md](../architecture/canonical/27-security-agent.md) | Draft | Pending — spec §13 declared, not fleet-registered | Identity and Access (03 §6.1); interface contracts (03 §7); domain security gates; ISO 27001 alignment (04 §2) | Architecture Office for production clearance; Implementation Council + Architecture Office for new connectors |
| `wise.capability.platform-engineering` | Platform Engineering Agent | 28 | AI Fabric — Implementation Council | [28-platform-engineering-agent.md](../architecture/canonical/28-platform-engineering-agent.md) | Draft | Pending — spec §13 declared, not fleet-registered | Engineering stack (04 §2.1); physical architecture (05); interface contracts (03 §7); security connector policy (27) | Implementation Council for deployment acceptance; Architecture Office for connector registration and ADR waivers |
| `wise.capability.sre` | SRE Agent | 29 | AI Fabric — Execution Council | [29-sre-agent.md](../architecture/canonical/29-sre-agent.md) | Draft | Pending — spec §13 declared, not fleet-registered | Observability model (03 §6.5); OpenTelemetry/Prometheus/Grafana/Loki (04 §2.1); Benchmark SLA baselines (23 §5.1) | Execution Council for release decisions; Architecture Office for release-hold overrides; Implementation Council for SLO changes |
| `wise.capability.knowledge-graph-governance` | Knowledge Graph Governance Agent | 30 | Platform — Knowledge Graph Governance | [30-knowledge-graph-agent.md](../architecture/canonical/30-knowledge-graph-agent.md) | Draft | Pending — spec §13 declared, not fleet-registered | Evidence Output Profile (03 §6.6); CRM/DwC graph bindings (22); layer-boundary conformance; federation policy | Architecture Council for policy action; Architecture Office via ADR for federation expansion; curator for link/merge |
| `wise.capability.preservation-governance` | Preservation Governance Agent | 31 | Platform — Preservation Governance | [31-preservation-agent.md](../architecture/canonical/31-preservation-agent.md) | Draft | Pending — spec §13 declared, not fleet-registered | OAIS boundary; PREMIS fixity/migration; provenance (03 §6.2); physical sovereignty (05) | Steward for migration and restore; Architecture Office for Permanence Readiness Assessment and replication waivers |
| `wise.capability.data-governance` | Data Governance Agent | 32 | Cross-cutting — Data Governance | [32-data-governance-agent.md](../architecture/canonical/32-data-governance-agent.md) | Draft | Pending — spec §13 declared, not fleet-registered | Provenance (03 §6.2); rights model (03 §6.3); physical residency (05); quality rights gates (13) | Architecture Office for gate acceptance and residency exceptions; rights officer/steward for violations and reclassification |
| `wise.capability.accessibility` | Accessibility Agent | 33 | Cross-cutting — Accessibility | [33-accessibility-agent.md](../architecture/canonical/33-accessibility-agent.md) | Draft | Pending — spec §13 declared, not fleet-registered | WCAG 2.1 AA (04 §2, 07); Quality Platform gates (13); education accessibility (16); Experience Plane scope (03 §4) | Architecture Office for milestone gate; accessibility reviewer + Architecture Office for critical violations; educator/curator for education content |
| `wise.capability.standards-compliance` | Standards Compliance Agent | 34 | Constitutional — Cross-System Standards | [34-standards-compliance-agent.md](../architecture/canonical/34-standards-compliance-agent.md) | Draft | Pending — spec §13 declared, not fleet-registered | Standards registry §14 (07); global frameworks (04 §2); Standards Agent checks (22); agent-checks registry | Architecture Office for milestone gate and Required-framework waivers; partner steward for covenant certification |
| `wise.capability.frontend-architecture` | Frontend Architecture Agent | 35 | Experience — Frontend Architecture | [35-frontend-architecture-agent.md](../architecture/canonical/35-frontend-architecture-agent.md) | Draft | Pending — spec §13 declared, not fleet-registered | Interface contracts (03 §7); Experience Plane scope (03 §4); schema.org profiles (22); WCAG coordination (33); translation gates (14) | Implementation Council for deployment; Architecture Office via ADR for new surfaces and contract waivers; Execution Council for performance budget overrides |

---

## Field Definitions

### Registration State

**Draft** entries have canonical specifications but are not graph-bound, not seeded to the operational Agent Registry database, and not included in Benchmark Agent fleet scorecards until promoted to Operational.

### Number

Canonical agent number associated with the specification filename.

### Benchmark Coverage

**Required** — agent specification declares benchmark obligations; coverage is required before any operational promotion.

**Pending** — agent spec §13 declares benchmarks to be evaluated by [Benchmark Agent](../architecture/canonical/23-benchmark-agent.md); not yet registered in §5.4 fleet.

**Registered** — agent appears in [23-benchmark-agent.md](../architecture/canonical/23-benchmark-agent.md) §5.4 with benchmarks declared in agent §AI Fabric Governance or §13.

### Standards Coverage

**Required** — agent specification declares binding standards/compliance obligations; coverage is required before any operational promotion.

Binding standards and compliance sources cited in each agent spec §11 Compliance Requirements and constitutional constraints.

### Human Approval Requirement

**Required** — human disposition authority is mandatory before gate progression, waiver, certification, or operational promotion.

Summary of disposition authority from each agent spec §12 Human Approval Requirements. No agent auto-approves production changes or milestone gates.

---

## Maintenance

Updates to this registry require alignment with agent specification changes and Architecture Office review. Promotion from Draft to Operational requires Agent Registry manifest update, graph factory registration, and Benchmark Agent fleet registration per [23-benchmark-agent.md](../architecture/canonical/23-benchmark-agent.md).

---

*Governance: [architecture-registry.md](architecture-registry.md) · Checks: [agent-checks-registry.md](agent-checks-registry.md) · Fleet: [23-benchmark-agent.md](../architecture/canonical/23-benchmark-agent.md) §5.4*
