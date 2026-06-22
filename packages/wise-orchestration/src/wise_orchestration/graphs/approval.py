"""Human approval gate subgraph (04-system-diagram §2.2)."""

from __future__ import annotations

from langgraph.graph import END, StateGraph
from langgraph.types import interrupt

from wise_orchestration.nodes.legacy_phase0 import PipelineState, route_after_approval


def await_steward_approval(state: PipelineState) -> PipelineState:
    """Interrupt graph until steward submits approve/reject via /runs/{thread_id}/resume."""
    decision = interrupt(
        {
            "type": "steward_approval_required",
            "thread_id": state.get("thread_id"),
            "agent_id": state.get("agent_id"),
            "approval_status": state.get("approval_status", "proposed"),
        }
    )
    if isinstance(decision, dict):
        return {
            **state,
            "approval_status": decision.get("decision", state.get("approval_status")),
            "reviewer_id": decision.get("reviewer_id"),
            "notes": decision.get("notes"),
            "phase": "await_approval",
        }
    return state


def mark_rejected(state: PipelineState) -> PipelineState:
    return {**state, "approval_status": "rejected", "phase": "complete"}


def build_approval_subgraph() -> StateGraph:
    """Reusable approval gate: interrupt → route approved/rejected."""
    graph = StateGraph(PipelineState)
    graph.add_node("await_steward_approval", await_steward_approval)
    graph.add_node("mark_rejected", mark_rejected)
    graph.set_entry_point("await_steward_approval")
    graph.add_conditional_edges(
        "await_steward_approval",
        route_after_approval,
        {
            "approved": END,
            "rejected": "mark_rejected",
            "pending": "await_steward_approval",
        },
    )
    graph.add_edge("mark_rejected", END)
    return graph


def compile_approval_subgraph():
    return build_approval_subgraph().compile()
