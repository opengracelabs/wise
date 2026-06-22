"""RC1 LangGraph assembly — agents 09–13 with gates, hooks, and recovery."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from wise_orchestration.gates.approval import (
    advance_stage,
    reject_pipeline,
    route_after_steward_gate,
    steward_approval_gate,
)
from wise_orchestration.hooks.benchmark import benchmark_hook_node
from wise_orchestration.hooks.pipeline_benchmark import pipeline_benchmark_node
from wise_orchestration.hooks.standards import standards_hook_node
from wise_orchestration.nodes import (
    knowledge_graph_node,
    metadata_node,
    preservation_node,
    quality_review_node,
    source_discovery_node,
)
from wise_orchestration.recovery import (
    classify_error,
    increment_retry,
    mark_dead_letter,
    mark_steward_escalation,
    route_on_error,
)
from wise_orchestration.state import PipelineStage, RC1GraphState


def _wrap_agent(
    node_fn: Callable[[RC1GraphState], dict[str, Any]],
    stage: PipelineStage,
) -> Callable[[RC1GraphState], dict[str, Any]]:
    """Catch agent failures and record structured errors for recovery routing."""

    def wrapped(state: RC1GraphState) -> dict[str, Any]:
        try:
            return node_fn(state)
        except Exception as exc:  # noqa: BLE001 — orchestration boundary
            return {
                "current_stage": stage.value,
                "errors": [
                    classify_error(stage, code="agent_failure", message=str(exc), retryable=True)
                ],
            }

    return wrapped


def _route_after_agent(state: RC1GraphState) -> str:
    """Route to recovery or benchmark hook after agent execution."""
    errors = state.get("errors") or []
    if errors:
        return "recovery"
    return "benchmark"


def _recovery_node(state: RC1GraphState) -> dict[str, Any]:
    """Apply retry, dead-letter, or steward escalation policy."""
    route = route_on_error(state)
    if route == "retry":
        return increment_retry(state)
    if route == "steward_escalation":
        return mark_steward_escalation(state, "Non-retryable agent failure")
    reason = "Max retries exceeded"
    if state.get("errors"):
        reason = state["errors"][-1].get("message", reason)
    return mark_dead_letter(state, reason)


def _route_after_recovery(state: RC1GraphState) -> str:
    """Route after recovery node: retry agent, dead-letter, or escalate."""
    if state.get("dead_letter"):
        return "dead_letter"
    if state.get("steward_escalation"):
        return "escalate"
    return "retry"


def _complete_node(state: RC1GraphState) -> dict[str, Any]:
    """Terminal node when quality review is approved; run pipeline benchmark."""
    patch: dict[str, Any] = {
        "current_stage": PipelineStage.COMPLETE.value,
        "next_stage": None,
        "pending_interrupt": False,
    }
    merged = {**state, **patch}
    patch.update(pipeline_benchmark_node(merged))
    return patch


def _route_after_standards(state: RC1GraphState) -> str:
    errors = state.get("errors") or []
    if errors and any(e.get("code") == "standards_violation" for e in errors):
        return "recovery"
    return "gate"


def _add_stage(
    builder: StateGraph,
    *,
    agent_name: str,
    agent_node: Callable[[RC1GraphState], dict[str, Any]],
    stage: PipelineStage,
    next_agent: str | None,
) -> None:
    """Wire agent → benchmark → standards → steward gate → next stage."""
    benchmark_name = f"benchmark_{stage.value}"
    standards_name = f"standards_{stage.value}"
    gate_name = f"gate_{stage.value}"
    recovery_name = f"recovery_{stage.value}"
    advance_name = f"advance_{stage.value}"

    builder.add_node(agent_name, _wrap_agent(agent_node, stage))
    builder.add_node(benchmark_name, benchmark_hook_node)
    builder.add_node(standards_name, standards_hook_node)
    builder.add_node(gate_name, steward_approval_gate)
    builder.add_node(recovery_name, _recovery_node)
    builder.add_node(advance_name, advance_stage)

    builder.add_conditional_edges(
        agent_name,
        _route_after_agent,
        {"recovery": recovery_name, "benchmark": benchmark_name},
    )
    builder.add_edge(benchmark_name, standards_name)
    builder.add_conditional_edges(
        standards_name,
        _route_after_standards,
        {"recovery": recovery_name, "gate": gate_name},
    )
    builder.add_conditional_edges(
        gate_name,
        route_after_steward_gate,
        {
            "advance": advance_name,
            "reject": END,
        },
    )

    if next_agent:
        builder.add_edge(advance_name, next_agent)
    else:
        builder.add_node("complete", _complete_node)
        builder.add_edge(advance_name, "complete")
        builder.add_edge("complete", END)

    builder.add_conditional_edges(
        recovery_name,
        _route_after_recovery,
        {
            "retry": agent_name,
            "dead_letter": END,
            "escalate": END,
        },
    )


def build_rc1_graph(
    *,
    checkpointer: BaseCheckpointSaver | None = None,
) -> Any:
    """Build and compile the Reference Capability 1 orchestration graph."""
    builder: StateGraph = StateGraph(RC1GraphState)

    builder.add_node("reject", reject_pipeline)

    _add_stage(
        builder,
        agent_name="source_discovery",
        agent_node=source_discovery_node,
        stage=PipelineStage.SOURCE_DISCOVERY,
        next_agent="preservation",
    )
    _add_stage(
        builder,
        agent_name="preservation",
        agent_node=preservation_node,
        stage=PipelineStage.PRESERVATION,
        next_agent="metadata",
    )
    _add_stage(
        builder,
        agent_name="metadata",
        agent_node=metadata_node,
        stage=PipelineStage.METADATA,
        next_agent="knowledge_graph",
    )
    _add_stage(
        builder,
        agent_name="knowledge_graph",
        agent_node=knowledge_graph_node,
        stage=PipelineStage.KNOWLEDGE_GRAPH,
        next_agent="quality_review",
    )
    _add_stage(
        builder,
        agent_name="quality_review",
        agent_node=quality_review_node,
        stage=PipelineStage.QUALITY_REVIEW,
        next_agent=None,
    )

    builder.add_edge(START, "source_discovery")

    saver = checkpointer or MemorySaver()
    return builder.compile(checkpointer=saver)
