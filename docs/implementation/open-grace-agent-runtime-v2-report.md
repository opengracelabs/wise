# Open Grace Agent Runtime v2 — Implementation Report

| Field | Value |
|-------|-------|
| **Version** | 2.0.0 |
| **Date** | 2026-06-23 |
| **Boundary** | Implementation layer only. Does **not** modify canonical architecture (`docs/architecture/canonical/*`). |

## Summary

Open Grace Agent Runtime v2 adds gated LangGraph agent execution integrated with the existing Governance, Capability, Knowledge, and Observability frameworks. Execution requires four pre-execute gates (agent registry, capability, risk, benchmark). LangGraph is infrastructure only — v2 records stub execution results without LLM calls.

## Package

| Package | Responsibility |
|---------|----------------|
| `packages/open-grace-runtime/` | `RuntimeSystem`, LangGraph flow, gate validators, JSON record stores, schemas |

## LangGraph Flow

```
select_agent → validate_capability → validate_risk → select_model → execute → evaluate → audit → persist
```

| Node | Responsibility |
|------|----------------|
| `select_agent` | Gate 1 — agent at APPROVAL/PUBLICATION; knowledge context validation |
| `validate_capability` | Gate 2 — `GovernanceSystem.validate_agent_approval` |
| `validate_risk` | Gate 3 — linked risks published and mitigated |
| `select_model` | Gate 4 — benchmark thresholds or recorded passing evaluation; model selection |
| `execute` | Stub execution + agent observability metric |
| `evaluate` | `evaluate_capability_benchmarks` + benchmark observability metrics |
| `audit` | `record_lifecycle_audit` via open-grace-audit |
| `persist` | Write `ExecutionRecord` and `BenchmarkRunRecord` JSON stores |

## Execution Gates

| Gate | Validator | Blocks when |
|------|-----------|-------------|
| Agent Registry | `validate_agent_registry_gate` | Agent missing or lifecycle before APPROVAL |
| Capability | `validate_capability_gate` | `validate_agent_approval` fails (framework cross-registry) |
| Risk | `validate_risk_gate` | Risk in capability `risk_profile` not PUBLICATION or missing mitigation |
| Benchmark | `validate_benchmark_gate` | No passing recorded evaluation and missing/failing observed values |

Knowledge context validation runs in `select_agent` when the agent has Nature & Culture `knowledge_links`.

## Schemas

| Schema | Key fields |
|--------|------------|
| `ExecutionRecord` | `run_id`, `agent_id`, `model_id`, `capability_class_ids`, `status`, `started_at`, `completed_at`, `gate_results`, `output_ref`, `audit_id` |
| `GateResult` | `gate_name`, `passed`, `errors` |
| `BenchmarkRunRecord` | `benchmark_run_id`, `run_id`, `agent_id`, `capability_class_id`, `benchmark_id`, `passed`, `observed_value`, `reason` |

## Reference Models

UNESCO, Wikidata, GBIF, NIST AI RMF, ISO 42001, LangGraph — catalogued in `open_grace_runtime.reference_models`.

## Governance Integration

`GovernanceSystem` (`open_grace_governance.system`) exposes:

- `runtime` — lazy-loaded cached `RuntimeSystem`
- `run_agent(agent_id, observed_values=..., ...)` — executes the LangGraph flow

```python
from open_grace_governance.system import GovernanceSystem

system = GovernanceSystem.create()
system.seed_all()

result = system.run_agent(
    "wise.agent.translation",
    observed_values={
        "wise.benchmark.translation-cost": 0.03,
        "wise.benchmark.translation-quality": 0.85,
    },
)
```

## Record Stores

JSON file stores under `{governance_root}/runtime/`:

- `execution_records.json` — execution trail
- `benchmark_run_records.json` — per-run benchmark evaluations

## Tests

```bash
pip install -e packages/open-grace-governance \
            -e packages/open-grace-agent-registry \
            -e packages/open-grace-benchmarking \
            -e packages/open-grace-audit \
            -e packages/open-grace-knowledge \
            -e packages/open-grace-observability \
            -e packages/open-grace-runtime
pytest tests/open_grace/ -q
```

| Suite | Tests | Coverage |
|-------|-------|----------|
| `test_runtime_gates.py` | 6 | Each gate blocks on failure; recorded benchmark bypass |
| `test_runtime_langgraph.py` | 2 | Graph compiles; full flow via `GovernanceSystem` |
| `test_runtime_records.py` | 2 | Execution, audit, benchmark persistence; blocked runs |
| `test_runtime_governance_integration.py` | 3 | `run_agent`, `RuntimeSystem.create`, observability metrics |

**Total Open Grace suite: 77 passed** (13 new runtime tests).

## Files Added

```
packages/open-grace-runtime/
  pyproject.toml
  README.md
  src/open_grace_runtime/
    __init__.py
    reference_models.py
    gates.py
    langgraph.py
    system.py
    stores.py
    schemas/
      __init__.py
      execution.py
tests/open_grace/
  test_runtime_gates.py
  test_runtime_langgraph.py
  test_runtime_records.py
  test_runtime_governance_integration.py
docs/implementation/
  open-grace-agent-runtime-v2-report.md
```

## Files Modified

- `packages/open-grace-governance/src/open_grace_governance/system.py` — `runtime` property and `run_agent()` with lazy import
