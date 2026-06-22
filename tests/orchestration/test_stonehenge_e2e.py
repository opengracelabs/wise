"""End-to-end Stonehenge RC1 orchestration test."""

from __future__ import annotations

import json
import os

import pytest
from langgraph.checkpoint.memory import MemorySaver

from wise_contracts.orchestration import RC1RunResumeRequest, RC1RunStartRequest
from wise_orchestration import build_rc1_graph, initial_state_for_stonehenge
from wise_orchestration.gates.approval import resume_with_approval
from wise_orchestration.state import PipelineStage
from wise_orchestrator.rc1_run_service import RC1RunService


@pytest.mark.integration
def test_stonehenge_rc1_graph_end_to_end():
    """Full RC1 pipeline with inline clients, standards, benchmark, and steward gates."""
    os.environ["WISE_ORCHESTRATION_INLINE"] = "1"
    graph = build_rc1_graph(checkpointer=MemorySaver())
    config = {"configurable": {"thread_id": "e2e-stonehenge"}}
    state = graph.invoke(initial_state_for_stonehenge(thread_id="e2e-stonehenge"), config)

    approvals = 0
    while state.get("current_stage") not in {
        PipelineStage.COMPLETE.value,
        PipelineStage.FAILED.value,
        PipelineStage.DEAD_LETTER.value,
    }:
        assert state.get("approval_gate") is not None
        assert len(state.get("standards_reports") or []) >= approvals + 1
        state = resume_with_approval(
            graph,
            config,
            decision="approved",
            steward_id="steward-stonehenge",
        )
        approvals += 1
        assert approvals <= 5

    assert state["current_stage"] == PipelineStage.COMPLETE.value
    assert state["quality_review"]["disposition"] == "accepted"
    assert state["quality_review"]["status"] == "approved"
    assert state["pipeline_benchmark_report"] is not None
    assert state["pipeline_benchmark_report"]["result"] in {"pass", "warn"}
    assert len(state["provenance_chain"]) >= 4
    assert state["current_provenance_event_id"]
    assert "discovery_record" in state["evidence_profiles"]
    assert "entity_assertion" in state["evidence_profiles"]


@pytest.mark.integration
def test_stonehenge_rc1_orchestrator_persists_agent_run(
    orchestration_db_session, registry_database_url: str
):
    """RC1RunService persists registry.agent_runs and steward tasks."""
    os.environ["WISE_ORCHESTRATION_INLINE"] = "1"
    service = RC1RunService(registry_database_url)
    session = orchestration_db_session
    try:
        run = service.start_run(session, RC1RunStartRequest(stable_id="stonehenge"))
        assert run.status.value == "interrupted"
        assert run.input_ref == "stable_id:stonehenge"
        assert run.provenance_event_id

        for _ in range(5):
            if run.status.value == "completed":
                break
            run = service.resume_run(
                session,
                run.graph_thread_id,
                RC1RunResumeRequest(decision="approved", steward_id="steward-1"),
            )

        assert run.status.value == "completed"
        assert run.provenance_event_id
        output = json.loads(run.output_ref)
        assert output["stable_id"] == "stonehenge"
        assert output["pipeline_benchmark"] is not None
    finally:
        service.close()


@pytest.mark.integration
def test_quality_disposition_requires_steward_approval():
    """Quality Review disposition must be null before steward gate."""
    os.environ["WISE_ORCHESTRATION_INLINE"] = "1"
    graph = build_rc1_graph(checkpointer=MemorySaver())
    config = {"configurable": {"thread_id": "e2e-quality-gate"}}
    state = graph.invoke(initial_state_for_stonehenge(), config)

    for _ in range(4):
        if state.get("current_stage") == PipelineStage.QUALITY_REVIEW.value:
            break
        state = resume_with_approval(graph, config, decision="approved", steward_id="s")

    assert state["current_stage"] == PipelineStage.QUALITY_REVIEW.value
    assert state["quality_review"]["disposition"] is None
