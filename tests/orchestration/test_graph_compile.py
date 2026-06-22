"""Graph compilation tests — no live LLM required."""

from __future__ import annotations

from langgraph.checkpoint.memory import MemorySaver

from wise_orchestration import build_rc1_graph, initial_state_for_stonehenge


def test_rc1_graph_compiles():
    graph = build_rc1_graph(checkpointer=MemorySaver())
    assert graph is not None
    assert hasattr(graph, "invoke")


def test_initial_state_shape():
    state = initial_state_for_stonehenge()
    assert state["stable_id"] == "stonehenge"
    assert state["current_stage"] == "source_discovery"
    assert state["provenance_chain"] == []
    assert state["max_retries"] == 3
