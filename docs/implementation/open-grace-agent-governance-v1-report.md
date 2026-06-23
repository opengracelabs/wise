# Open Grace Agent Governance System v1 — Implementation Report

| Field | Value |
|-------|-------|
| **Version** | 1.0.0 |
| **Date** | 2026-06-23 |
| **Boundary** | Implementation layer only. Does **not** modify canonical architecture, ADRs, governance Markdown authority, or operational `data/registry/` manifests. |

## Summary

Open Grace Agent Governance System v1 delivers seven governed registries, Pydantic schemas with validation rules, a seven-stage lifecycle finite-state machine, LangGraph execution infrastructure (lifecycle wiring only — no agent reasoning), reference-model alignment, and unit tests across four new packages.

## Packages

| Package | Responsibility |
|---------|----------------|
| `packages/open-grace-governance/` | Lifecycle FSM, schemas, validation, reference models, Standards + Risk registries, LangGraph infrastructure, `GovernanceSystem` coordinator |
| `packages/open-grace-agent-registry/` | Agent, Capability, Model registries; read-only import from canonical WISE manifests |
| `packages/open-grace-benchmarking/` | Benchmark Registry and threshold evaluation |
| `packages/open-grace-audit/` | Audit Registry and lifecycle evidence recording |

## Seven Registries

| Registry | ID pattern | Package | Seed source |
|----------|------------|---------|-------------|
| Agent | `wise.agent.{slug}` | open-grace-agent-registry | `data/registry/agents/manifest.yaml` (import) |
| Capability | `wise.capability.{slug}` | open-grace-agent-registry | `data/registry/capabilities/manifest.yaml` (import) |
| Standards | `wise.standard.{slug}` | open-grace-governance | `data/seed/standards_registry.yaml` |
| Risk | `wise.risk.{slug}` | open-grace-governance | `data/seed/risk_registry.yaml` |
| Benchmark | `wise.benchmark.{slug}` | open-grace-benchmarking | `data/seed/benchmark_registry.yaml` |
| Audit | `wise.audit.{slug}` | open-grace-audit | runtime append |
| Model | `wise.model.{slug}` | open-grace-agent-registry | `data/seed/model_registry.yaml` |

## Lifecycle

```
Proposal → Review → Benchmark → Approval → Publication → Audit → Retirement
```

Backward transitions are permitted at Review, Benchmark, and Approval stages per `open_grace_governance.lifecycle.LIFECYCLE_TRANSITIONS`. Publication requires `steward_actor` on governed records.

LangGraph (`open_grace_governance.execution.langgraph`) compiles a linear lifecycle graph for infrastructure integration. `run_lifecycle_to_stage()` advances entries along the forward path without model calls or canonical writes.

## Reference Models

Governance rules are informed by:

- UNESCO — heritage stewardship
- Wikidata — linked open data authority
- GBIF — biodiversity Darwin Core binding
- Internet Archive — long-term preservation
- NIST AI RMF — risk taxonomy
- ISO 42001 — AI management lifecycle
- ISO 27001 — security controls and audit evidence
- OpenTelemetry — trace/metric correlation

## Validation Rules (v1)

- ID format enforcement per registry (`wise.{domain}.{slug}`)
- Reference model slug must exist in catalog when declared
- Risks must reference `agent_id` or `capability_id`
- Benchmarks require at least one threshold (`threshold_min` / `threshold_max`)
- Audits require `evidence_ref`
- Restricted models cannot serve the constitutional plane
- Publication stage requires `steward_actor`
- Constitutional agents warn when not `read_only`

## Tests

```bash
pip install -e packages/open-grace-governance \
            -e packages/open-grace-agent-registry \
            -e packages/open-grace-benchmarking \
            -e packages/open-grace-audit
pytest tests/open_grace/ -q
```

Suites: lifecycle, validation, each registry, LangGraph execution, `GovernanceSystem` integration.

## Usage

```python
from open_grace_governance.system import GovernanceSystem

system = GovernanceSystem.create()  # writes to ./.open-grace-governance/
counts = system.seed_all()
summary = system.summary()
```

## Non-Goals (v1)

- No changes to `docs/architecture/canonical/*`
- No changes to `data/registry/agents/manifest.yaml` or capability manifest
- No PostgreSQL persistence (JSON file stores; integrates with `wise-registry` in a future revision)
- No LLM or agent reasoning inside LangGraph graphs
- No git push (per task constraint)

## Integration Path (future)

1. Mirror governed rows into `registry.*` tables via `wise-registry` migrations
2. Invoke `validate_registry_alignment()` from orchestrator startup
3. Wire benchmark evaluation hooks to `open-grace-benchmarking.evaluate_benchmark`
4. Emit audit records on steward approval resume in `wise-orchestration`

*Implementation report. Does not modify Architecture v1.0, governance authority documents, ADRs, or the operational Agent Registry manifest.*
