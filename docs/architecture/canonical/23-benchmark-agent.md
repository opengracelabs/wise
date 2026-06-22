# Benchmark Agent

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Status** | Canonical |
| **Authority** | Open Grace Architecture Office |
| **Date** | 2026-06-22 |
| **Capability** | AI Fabric — Benchmarks ([04-system-diagram.md](04-system-diagram.md), §2.2) |
| **Phase** | Cross-cutting — Foundation through Permanence ([06-build-roadmap.md](06-build-roadmap.md)) |

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

---

## 1. Purpose

The **Benchmark Agent** automates the **Benchmarks** gate in the AI Fabric governance chain ([04-system-diagram.md](04-system-diagram.md), §2.2). It evaluates registered platform and observatory agents for **agent performance**, **quality metrics**, and **architecture compliance**; aggregates benchmark results across the agent fleet; and emits **Benchmark Reports** (JSON-LD) for Architecture Office and council review before agents advance to Evaluations, Safety Reviews, and production approval.

The agent does not deploy agents, alter canonical architecture, override steward decisions, or grant production clearance on its own. It measures, scores, and reports; the Architecture Office and human approvers decide.

---

## 2. Responsibilities

| Responsibility | Description |
|----------------|-------------|
| **Agent performance** | Measure operational performance of registered agents against declared SLAs: throughput, latency, error rates, resource utilization, queue depth, and run success/failure ratios; detect regressions across agent versions |
| **Quality metrics** | Execute and aggregate domain-specific benchmark suites defined in each agent specification (coverage, precision/recall, validation pass rates, steward-impact metrics); compare results against phase success criteria and registered thresholds |
| **Architecture compliance** | Verify agents, connectors, and emitted artifact schemas conform to canonical architecture contracts, standards registry bindings, ADR constraints, and Agent Registry declarations; flag drift, shadow integrations, and undocumented capabilities |

---

## 3. Reference Models

The agent synthesizes patterns from three primary reference models ([02-reference-models.md](02-reference-models.md)):

| Model | Pattern Applied | Agent Behavior |
|-------|-----------------|----------------|
| **MIT** | Reproducible research, open evaluation, benchmark transparency, peer-reviewable methodology | Version-controlled benchmark suites; reproducible run manifests; publish benchmark datasets and scoring scripts to Research Registry when approved |
| **Harvard** | Centuries-scale audit trails, institutional accountability, policy compliance verification | Immutable benchmark run logs; disposition trails linking failures to remediation ADRs; compliance checks against stewardship and covenant constraints |
| **Google** | Quality-at-scale measurement, SLO monitoring, regression detection across large distributed systems | Fleet-wide performance dashboards; automated regression gates on agent version promotion; percentile latency and availability tracking |

Supporting standards alignment follows [07-reference-standards.md](07-reference-standards.md): JSON-LD (benchmark reports), PREMIS (audit events), OpenTelemetry (performance telemetry), SPDX (dependency compliance signals where applicable).

---

## 4. Position in Architecture

```
Agent Registry (registered agents, versions, benchmark definitions, thresholds)
        ↓
Platform and observatory agent telemetry + held-out evaluation datasets
        ↓
Canonical architecture suite + standards registry + ADR constraints
        ↓
Benchmark Agent
  ├── Domain: Agent performance
  ├── Domain: Quality metrics
  └── Domain: Architecture compliance
        ↓
Benchmark Reports — pass, warn, fail, regression
        ↓
Architecture Office + council review
        ↓
Evaluations → Safety Reviews → Human Approval → production clearance
```

The agent operates in the **Constitutional Plane** AI Fabric — Benchmarks subgraph ([04-system-diagram.md](04-system-diagram.md), §2.2). It governs platform and observatory agents; it does not replace the Quality Review Agent's content-quality role ([13-quality-review-agent.md](13-quality-review-agent.md)).

**Upstream inputs:** Agent Registry entries, OpenTelemetry and Prometheus metrics from agent runtimes, held-out evaluation datasets, agent output samples, canonical architecture documents ([03-canonical-architecture.md](03-canonical-architecture.md)), standards registry ([07-reference-standards.md](07-reference-standards.md)), ADR corpus ([08-decision-record.md](08-decision-record.md)), per-agent benchmark definitions from agent specifications (§AI Fabric Governance in each agent doc).

**Downstream consumers:** Evaluations gate (phase success criteria verification), Safety Reviews (failure triage), Architecture Office (compliance disposition), Implementation and Execution Councils (regression remediation), Grafana benchmark dashboards.

---

## 5. Evaluation Domains

### 5.1 Agent Performance

| Attribute | Specification |
|-----------|---------------|
| **Inputs** | Agent run telemetry (OpenTelemetry traces, Prometheus metrics), job queue statistics, connector health probes, version manifests from Agent Registry |
| **Checks** | SLA compliance (availability, p50/p95 latency, error budget burn); throughput vs. registered capacity; failure rate spikes; resource saturation; connector timeout rates |
| **Output signals** | Performance score (0–100), SLA pass/fail per dimension, regression flags vs. prior agent version baseline |
| **Standards** | OpenTelemetry, Prometheus ([04-system-diagram.md](04-system-diagram.md), §2.1 engineering stack) |

### 5.2 Quality Metrics

| Attribute | Specification |
|-----------|---------------|
| **Inputs** | Per-agent benchmark suites from registered agent specifications; held-out gold datasets; human-validated spot-check samples; steward disposition outcomes |
| **Checks** | Execute domain benchmarks (e.g., mapping coverage for Metadata Agent, link precision/recall for Knowledge Graph Agent, translation BLEU/chrF for Translation Agent); aggregate pass rates against registered thresholds; detect quality regressions on version promotion |
| **Output signals** | Quality metric scorecard by agent and dimension, threshold pass/fail, benchmark run identifier, comparison to prior version |
| **Standards** | Agent-specific benchmarks as declared in §5.4 Registered Canonical Agent Fleet and each agent's §AI Fabric Governance |

### 5.3 Architecture Compliance

| Attribute | Specification |
|-----------|---------------|
| **Inputs** | Agent capability declarations, connector allowlists, output schema samples, dependency manifests, architecture registry ([docs/governance/architecture-registry.md](../../governance/architecture-registry.md)) |
| **Checks** | Conformance to canonical layer boundaries (no unauthorized preservation writes, no publication without gates); schema validation against registered output types; ADR constraint satisfaction; standards registry binding compliance; detection of shadow connectors or undocumented side effects; Evidence Output Profile presence on assertion-making agent outputs ([03-canonical-architecture.md](03-canonical-architecture.md), §6.6) |
| **Output signals** | Compliance status (`compliant`, `drift`, `violation`), finding list with document references, recommended remediation (ADR, registry update, agent scope reduction) |
| **Standards** | Canonical architecture suite, [07-reference-standards.md](07-reference-standards.md), [08-decision-record.md](08-decision-record.md) |

### 5.4 Registered Canonical Agent Fleet

The Benchmark Agent evaluates **every** registered canonical agent specification. Fleet enumeration is authoritative; Agent Registry entries MUST map one-to-one to this list.

| # | Agent | Specification | Plane | Benchmark source |
|---|-------|---------------|-------|------------------|
| 1 | Source Discovery Agent | [09-source-discovery-agent.md](09-source-discovery-agent.md) | Platform | §AI Fabric Governance |
| 2 | Metadata Agent | [10-metadata-agent.md](10-metadata-agent.md) | Platform | §AI Fabric Governance |
| 3 | Preservation Agent | [11-preservation-agent.md](11-preservation-agent.md) | Platform | §AI Fabric Governance |
| 4 | Knowledge Graph Agent | [12-knowledge-graph-agent.md](12-knowledge-graph-agent.md) | Platform | §AI Fabric Governance |
| 5 | Quality Review Agent | [13-quality-review-agent.md](13-quality-review-agent.md) | Platform | §AI Fabric Governance |
| 6 | Translation Agent | [14-translation-agent.md](14-translation-agent.md) | Platform | §AI Fabric Governance |
| 7 | Publishing Agent | [15-publishing-agent.md](15-publishing-agent.md) | Platform | §AI Fabric Governance |
| 8 | Education Agent | [16-education-agent.md](16-education-agent.md) | Experience | §AI Fabric Governance |
| 9 | Biodiversity Observatory Agent | [17-biodiversity-observatory-agent.md](17-biodiversity-observatory-agent.md) | Experience — Observatories | §AI Fabric Governance |
| 10 | Climate Observatory Agent | [18-climate-observatory-agent.md](18-climate-observatory-agent.md) | Experience — Observatories | §AI Fabric Governance |
| 11 | Heritage Observatory Agent | [19-heritage-observatory-agent.md](19-heritage-observatory-agent.md) | Experience — Observatories | §AI Fabric Governance |
| 12 | Tourism Observatory Agent | [20-tourism-observatory-agent.md](20-tourism-observatory-agent.md) | Experience — Observatories | §AI Fabric Governance |
| 13 | Language Observatory Agent | [21-language-observatory-agent.md](21-language-observatory-agent.md) | Experience — Observatories | §AI Fabric Governance |
| 14 | Standards Agent | [22-standards-agent.md](22-standards-agent.md) | Constitutional | §AI Fabric Governance |
| 15 | Benchmark Agent | [23-benchmark-agent.md](23-benchmark-agent.md) | Constitutional | §7 AI Fabric Governance (meta-benchmarks / self-checks) |

**Self-checks:** The Benchmark Agent runs meta-benchmarks against itself before fleet-wide production runs: scoring reproducibility, false-pass rate on injected violations, regression detection latency, and compliance rule coverage across the full fleet enumeration above (§7).

---

## 6. Outputs

### 6.1 Benchmark Reports

Each evaluation run emits **JSON-LD** with:

| Field | Requirement |
|-------|-------------|
| **Agent reference** | Registered agent identifier and version from Agent Registry |
| **Evaluation domain** | `performance`, `quality`, `compliance`, or `composite` |
| **Result** | `pass`, `warn`, `fail`, `regression` |
| **Scores** | Domain scores with threshold comparison |
| **Findings** | Machine- and human-readable deficiency or regression descriptions |
| **Provenance** | Benchmark run identifier, agent version, dataset snapshot hash, benchmark suite version |

Benchmark Reports are **recommendations** until Architecture Office or designated council approves disposition.

### 6.2 Fleet Scorecards

Periodic aggregates across all registered agents:

- Fleet performance health (agents meeting SLA vs. total)
- Quality metric trend lines by agent and phase
- Compliance posture summary (compliant, drift, violation counts)
- Regression watchlist for version promotion holds

### 6.3 Compliance Findings

Architecture compliance failures emit structured findings:

| Severity | Meaning | Typical Action |
|----------|---------|----------------|
| **info** | Non-blocking drift or documentation gap | Track; schedule registry or ADR update |
| **warning** | Threshold miss or undeclared capability | Hold version promotion; require Implementation Council remediation |
| **blocker** | ADR violation, unauthorized write path, or shadow integration | Block production clearance; mandatory Architecture Office review |

### 6.4 Audit Events (approved writes)

After reviewer approval, persisted audit records include:

- Approved benchmark disposition (`accepted`, `remediated`, `scope_reduced`, `withdrawn`)
- Reviewer identity and timestamp (PREMIS-aligned)
- Link to remediation ADR or registry change when applicable

---

## 7. AI Fabric Governance

| Gate | Requirement |
|------|-------------|
| **Agent Registry** | Benchmark suite definitions, gold datasets, SLA baselines, and compliance rule packs registered before production benchmark runs |
| **Benchmarks** | Meta-benchmarks on the Benchmark Agent itself: scoring reproducibility, false-pass rate on injected violations, regression detection latency, compliance rule coverage |
| **Evaluations** | Periodic review against cross-cutting success criteria and constitution AI Fabric completion criteria |
| **Safety Reviews** | Verify agent does not auto-approve agents, alter registry entries, or bypass human approval on production clearance |
| **Human Approval** | Architecture Office approves compliance dispositions; councils approve performance and quality remediation plans |

**Council assignment:** Architecture Council (compliance rules, ADR alignment checks), Research Council (gold datasets, quality metric methodology), Implementation Council (performance telemetry pipelines), Execution Council (scheduled benchmark runs and regression suites).

---

## 8. Phase Alignment

| Phase | Agent Scope |
|-------|-------------|
| **Discovery (Phase 1)** | Register Source Discovery Agent benchmarks; baseline performance telemetry; initial architecture compliance checks for Acquire subgraph |
| **Preservation – Knowledge Graph (Phases 3–5)** | Expand benchmark coverage as Preservation, Metadata, and Knowledge Graph agents register |
| **Quality Platform (Phase 7)** | Coordinate quality metric benchmarks with Quality Review Agent thresholds; verify quality-precedes-experience gates |
| **Research & Translation – Publishing (Phases 8–10)** | Benchmark Translation and Publishing agents; enforce editorial and rights gate compliance checks |
| **Experience (Phases 11–15)** | Benchmark Education and observatory agents; fleet scorecards operational |
| **Permanence (15–100)** | Longitudinal benchmark retention; cross-generation agent version comparison; succession-readiness compliance audits |

---

## 9. Success Criteria

Aligned with AI Fabric governance completion and constitution accountability criteria:

- Benchmark suites registered for 100% of agents in §5.4 Registered Canonical Agent Fleet before clearance
- Agent performance SLAs measured and reported for all registered agents
- Quality metric benchmarks executed on every agent version promotion
- Architecture compliance checks pass before new agents enter Evaluations gate
- Regression detection blocks version promotion when composite benchmark fails
- Benchmark Reports and audit events persisted with PREMIS-aligned provenance
- End-to-end demonstration: agent registers → benchmark runs → report → council disposition → Evaluations clearance

---

## 10. Constraints

- **Measure, do not deploy.** The agent evaluates; councils and Architecture Office decide production clearance.
- **Registry is authoritative.** Benchmark definitions and thresholds come from Agent Registry and per-agent specifications; the Benchmark Agent does not invent ad hoc pass criteria.
- **No canonical side effects.** Benchmark runs use held-out datasets and telemetry; they do not write to Preservation, Knowledge Graph, or public experience without explicit test-environment isolation.
- **Compliance references canonical docs.** Architecture compliance findings must cite specific architecture, standards, or ADR sections — not informal conventions.
- **Distinct from Quality Review Agent.** Content and metadata quality for canonical entities is owned by the Quality Review Agent; the Benchmark Agent evaluates **agent systems**, not collection content.
- **Human approval is final.** Follow Harvard's accountability pattern ([02-reference-models.md](02-reference-models.md), §10): institutional judgment overrides machine pass on significance, risk, or covenant sensitivity.

---

*Previous: [22-standards-agent.md](22-standards-agent.md) · Governance: [docs/governance/architecture-registry.md](../../governance/architecture-registry.md), [docs/governance/agent-checks-registry.md](../../governance/agent-checks-registry.md)*
