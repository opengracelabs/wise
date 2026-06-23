# Open Grace Agent Runtime v2

Gated LangGraph agent execution infrastructure integrated with Open Grace Governance.

## Flow

```
select_agent → validate_capability → validate_risk → select_model → execute → evaluate → audit → persist
```

Execution gates (agent registry, capability, risk, benchmark) must pass before the `execute` node runs. LangGraph is infrastructure only — v2 records stub execution results without LLM calls.

## Usage

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

Or via `RuntimeSystem`:

```python
from open_grace_runtime import RuntimeSystem

runtime = RuntimeSystem.create(system)
result = runtime.run_agent("wise.agent.translation", observed_values={...})
```
