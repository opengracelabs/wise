# wise-orchestration

LangGraph orchestration for **Reference Capability 1** — the Stonehenge UNESCO World Heritage pipeline.

Implements the frozen architecture-v1.0 agent chain (09–13) with steward approval gates, Benchmark Agent evaluation hooks, provenance propagation, and error recovery.

Also includes Phase 0 scaffolding: manifest loader (`manifest_loader.py`) and Postgres checkpointer helper (`checkpointer.py`).

## Pipeline

```
Source Discovery (09) → Preservation (11) → Metadata (10) → Knowledge Graph (12) → Quality Review (13)
```

Each stage emits **proposed** outputs, runs a Benchmark evaluation hook, then pauses at a steward approval interrupt before advancing.

## Install

```bash
pip install -e packages/wise-contracts -e packages/wise-reference -e packages/wise-orchestration
```

## Run (Stonehenge RC1)

```python
from langgraph.checkpoint.memory import MemorySaver

from wise_orchestration import build_rc1_graph, initial_state_for_stonehenge
from wise_orchestration.gates.approval import resume_with_approval

graph = build_rc1_graph(checkpointer=MemorySaver())
config = {"configurable": {"thread_id": "stonehenge-rc1-001"}}

state = graph.invoke(initial_state_for_stonehenge(), config)
state = resume_with_approval(graph, config, decision="approved", steward_id="steward@wise.example.org")
```

CLI:

```bash
python -m wise_orchestration.run --stable-id stonehenge --auto-approve
```

## Tests

```bash
pytest tests/orchestration -q
```

## Documentation

Full implementation plan: [`docs/implementation/rc1-langgraph-orchestration.md`](../../docs/implementation/rc1-langgraph-orchestration.md)
