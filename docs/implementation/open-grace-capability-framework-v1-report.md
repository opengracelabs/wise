# Open Grace Capability Framework v1 — Implementation Report

| Field | Value |
|-------|-------|
| **Version** | 1.0.0 |
| **Date** | 2026-06-23 |
| **Boundary** | Implementation layer only. Does **not** modify canonical architecture, ADRs, or operational `data/registry/` manifests. |

## Summary

Open Grace Capability Framework v1 adds eight governed capability classes (Research, Translation, Classification, Extraction, Analysis, Coding, Preservation, Publishing) with full cross-registry metadata, validation, benchmarking, compliance reports, and an agent approval gate in `GovernanceSystem`.

## Capability Classes

| Class | ID | Owner (seed) |
|-------|-----|--------------|
| Research | `wise.capability.class.research` | Open Grace Architecture Office |
| Translation | `wise.capability.class.translation` | Translation Fabric Steward |
| Classification | `wise.capability.class.classification` | Knowledge Modeling Steward |
| Extraction | `wise.capability.class.extraction` | Discovery Steward |
| Analysis | `wise.capability.class.analysis` | Knowledge Graph Steward |
| Coding | `wise.capability.class.coding` | Platform Engineering Council |
| Preservation | `wise.capability.class.preservation` | Preservation Steward |
| Publishing | `wise.capability.class.publishing` | Publishing Steward |

Each record includes: `id`, `name`, `description`, `owner`, `benchmark_set`, `risk_profile`, `approved_models`, `required_standards`, `audit_requirements`.

## Reference Models

UNESCO, GBIF, Wikidata, NIST AI RMF, ISO 42001 — referenced per capability class in seed data.

## Modules

| Module | Path | Role |
|--------|------|------|
| Schema | `open_grace_governance/schemas/capability_framework.py` | `CapabilityClass`, `CapabilityFrameworkRecord` |
| Registry | `open_grace_governance/capabilities/registry.py` | `CapabilityFrameworkRegistry`, agent bindings |
| Validation | `open_grace_governance/capabilities/validation.py` | Cross-registry validation |
| Benchmarking | `open_grace_governance/capabilities/benchmarking.py` | `evaluate_capability_benchmarks` |
| Reports | `open_grace_governance/capabilities/reports.py` | `CapabilityComplianceReport`, JSON output |
| Coordinator | `open_grace_governance/system.py` | `validate_agent_approval`, `advance_agent`, `capability_reports` |

## Seed Data

- `open_grace_governance/data/seed/capability_framework.yaml` — 8 classes + 11 agent bindings
- `open_grace_benchmarking/data/seed/benchmark_registry.yaml` — extended to 13 benchmarks (8 capability-specific)

## Agent Approval Gate

`GovernanceSystem.validate_agent_approval(agent_id)` validates all linked capability classes against benchmarks, models, standards, and risks before an agent may advance to **Approval**.

`GovernanceSystem.advance_agent(..., target=APPROVAL)` enforces this gate and raises `ValueError` on failure.

## Tests

```bash
. .venv/bin/activate
pip install -e packages/open-grace-governance \
            -e packages/open-grace-agent-registry \
            -e packages/open-grace-benchmarking \
            -e packages/open-grace-audit
python -m pytest tests/open_grace/ -q
```

New suites: `test_capability_framework.py`, `test_capability_validation.py`, `test_capability_benchmarking.py`, `test_capability_reports.py`, `test_agent_approval_gate.py`.

## Non-Goals (v1)

- No changes to `docs/architecture/canonical/*`
- No changes to operational capability manifest (`data/registry/capabilities/manifest.yaml`)
- No PostgreSQL persistence for capability framework rows
- No git push

*Implementation report. Does not modify Architecture v1.0 or canonical governance authority documents.*
