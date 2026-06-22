"""Phase 0 reusable graph nodes (legacy scaffold)."""

from __future__ import annotations

from typing import Literal, TypedDict


class PipelineState(TypedDict, total=False):
    run_id: str
    thread_id: str
    agent_id: str
    agent_version: str
    graph_id: str
    read_only: bool
    input_ref: str | None
    output_ref: str | None
    approval_status: Literal["proposed", "approved", "rejected", "superseded"]
    steward_task_id: str | None
    reviewer_id: str | None
    notes: str | None
    errors: list[str]
    phase: Literal["propose", "await_approval", "execute", "complete"]


class CanonicalWriteForbiddenError(RuntimeError):
    """Raised when a graph attempts a canonical write without steward approval."""


def propose_output(state: PipelineState) -> PipelineState:
    """Phase 0 stub — mark output as proposed pending steward review."""
    return {
        **state,
        "approval_status": "proposed",
        "phase": "propose",
        "output_ref": state.get("output_ref") or f"proposed://{state.get('agent_id')}/{state.get('thread_id')}",
    }


def governance_report(state: PipelineState) -> PipelineState:
    """Read-only governance agent stub — emits report reference, never canonical writes."""
    return {
        **state,
        "approval_status": "proposed",
        "phase": "complete",
        "output_ref": f"governance-report://{state.get('agent_id')}/{state.get('thread_id')}",
    }


def canonical_write_guard(state: PipelineState) -> PipelineState:
    """Block canonical writes unless steward approval is recorded."""
    if state.get("read_only"):
        raise CanonicalWriteForbiddenError(
            f"Agent {state.get('agent_id')} is read-only and cannot perform canonical writes"
        )
    if state.get("approval_status") != "approved":
        raise CanonicalWriteForbiddenError(
            "Canonical write blocked: steward approval required (architecture-v1.0 §2.2)"
        )
    return {
        **state,
        "phase": "complete",
        "output_ref": state.get("output_ref") or f"canonical://{state.get('agent_id')}/{state.get('thread_id')}",
    }


def route_after_approval(state: PipelineState) -> str:
    if state.get("approval_status") == "approved":
        return "approved"
    if state.get("approval_status") == "rejected":
        return "rejected"
    return "pending"
