"""Steward approval interrupt and full pipeline tests."""

from __future__ import annotations

from langgraph.checkpoint.memory import MemorySaver

from wise_orchestration import build_rc1_graph, initial_state_for_stonehenge
from wise_orchestration.gates.approval import resume_with_approval
from wise_orchestration.hooks.benchmark import benchmark_evaluation_hook
from wise_orchestration.state import PipelineStage


def test_benchmark_hook_passes_on_discovery():
    base = initial_state_for_stonehenge()
    from wise_orchestration.nodes.source_discovery import source_discovery_node

    patch = source_discovery_node(base)
    merged = {**base, **patch}
    bench = benchmark_evaluation_hook(merged)
    assert bench["benchmark_reports"][0]["result"] in {"pass", "warn"}
    assert bench["benchmark_reports"][0]["agent_id"] == "09-source-discovery"


def test_full_pipeline_auto_approve():
    graph = build_rc1_graph(checkpointer=MemorySaver())
    config = {"configurable": {"thread_id": "test-auto-approve"}}
    state = graph.invoke(initial_state_for_stonehenge(), config)

    for _ in range(5):
        if state.get("current_stage") in {
            PipelineStage.COMPLETE.value,
            PipelineStage.FAILED.value,
        }:
            break
        state = resume_with_approval(
            graph,
            config,
            decision="approved",
            steward_id="test-steward",
        )

    assert state["current_stage"] == PipelineStage.COMPLETE.value
    assert len(state["provenance_chain"]) >= 4
    assert state["quality_review"]["status"] == "approved"
    assert state["quality_review"]["disposition"] == "accepted"
    assert len(state["benchmark_reports"]) >= 5
    assert len(state["standards_reports"]) >= 5
    assert state["pipeline_benchmark_report"] is not None


def test_steward_rejection_stops_pipeline():
    graph = build_rc1_graph(checkpointer=MemorySaver())
    config = {"configurable": {"thread_id": "test-reject"}}
    state = graph.invoke(initial_state_for_stonehenge(), config)

    state = resume_with_approval(
        graph,
        config,
        decision="rejected",
        steward_id="test-steward",
        rejection_reason="Insufficient rights documentation",
    )

    assert state["current_stage"] == PipelineStage.FAILED.value
    assert state["approval_gate"]["status"] == "rejected"
