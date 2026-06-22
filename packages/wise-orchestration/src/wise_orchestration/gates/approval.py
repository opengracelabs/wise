"""Steward approval gate with LangGraph human-in-the-loop interrupt."""

from __future__ import annotations

from typing import Any, Literal

from langgraph.types import Command, interrupt

from wise_contracts.common import ApprovalStatus
from wise_orchestration.recovery import route_after_approval
from wise_orchestration.state import PipelineStage, RC1GraphState


def _artifact_snapshot(state: RC1GraphState) -> dict[str, Any] | None:
    """Return the artifact pending steward review."""
    gate = state.get("approval_gate") or {}
    key = gate.get("artifact_key")
    if key == "discovery_record":
        return state.get("discovery_record")
    if key == "preserved_object":
        return state.get("preserved_object")
    if key == "entity_assertion":
        return state.get("entity_assertion")
    if key == "graph_entity":
        return state.get("graph_entity")
    if key == "quality_review":
        return state.get("quality_review")
    return None


def steward_approval_gate(state: RC1GraphState) -> dict[str, Any]:
    """Pause for steward review; resume with approved or rejected decision."""
    gate = dict(state.get("approval_gate") or {})
    if gate.get("status") != ApprovalStatus.PROPOSED.value:
        return {"pending_interrupt": False}

    decision = interrupt(
        {
            "type": "steward_approval",
            "gate_id": gate.get("gate_id"),
            "stage": gate.get("stage"),
            "stable_id": state.get("stable_id"),
            "artifact": _artifact_snapshot(state),
            "provenance_chain": state.get("provenance_chain") or [],
            "message": "Steward review required: approve or reject proposed artifact",
        }
    )

    status = decision.get("decision", ApprovalStatus.REJECTED.value)
    steward_id = decision.get("steward_id")
    rejection_reason = decision.get("rejection_reason")

    gate["status"] = status
    gate["steward_id"] = steward_id
    gate["rejection_reason"] = rejection_reason

    patch: dict[str, Any] = {
        "approval_gate": gate,
        "pending_interrupt": False,
    }

    if status == ApprovalStatus.REJECTED.value:
        patch["current_stage"] = PipelineStage.FAILED.value
        patch["errors"] = [
            {
                "stage": gate.get("stage"),
                "code": "steward_rejected",
                "message": rejection_reason or "Steward rejected proposed artifact",
                "retryable": False,
            }
        ]
        return patch

    artifact_key = gate.get("artifact_key")
    if status == ApprovalStatus.APPROVED.value and artifact_key:
        patch.update(_mark_artifact_approved(state, artifact_key))

    return patch


def _mark_artifact_approved(state: RC1GraphState, artifact_key: str) -> dict[str, Any]:
    """Set artifact status to approved after steward sign-off."""
    approved = ApprovalStatus.APPROVED.value
    if artifact_key == "discovery_record" and state.get("discovery_record"):
        record = dict(state["discovery_record"])
        record["status"] = approved
        return {"discovery_record": record}
    if artifact_key == "preserved_object" and state.get("preserved_object"):
        obj = dict(state["preserved_object"])
        obj["status"] = approved
        return {"preserved_object": obj}
    if artifact_key == "entity_assertion" and state.get("entity_assertion"):
        assertion = dict(state["entity_assertion"])
        assertion["status"] = approved
        metadata = dict(state["metadata_record"]) if state.get("metadata_record") else None
        result: dict[str, Any] = {"entity_assertion": assertion}
        if metadata:
            metadata["status"] = approved
            result["metadata_record"] = metadata
        return result
    if artifact_key == "graph_entity" and state.get("graph_entity"):
        entity = dict(state["graph_entity"])
        entity["status"] = approved
        for link in entity.get("external_links", []):
            link["status"] = approved
        return {"graph_entity": entity}
    if artifact_key == "quality_review" and state.get("quality_review"):
        review = dict(state["quality_review"])
        review["status"] = approved
        review["disposition"] = "accepted"
        return {"quality_review": review}
    return {}


def route_after_steward_gate(state: RC1GraphState) -> str:
    """Conditional edge: advance pipeline, reject, or fail."""
    route = route_after_approval(state)
    if route == "advance":
        return "advance"
    if route == "reject":
        return "reject"
    return "reject"


def resume_with_approval(
    graph: Any,
    config: dict[str, Any],
    *,
    decision: Literal["approved", "rejected"],
    steward_id: str = "steward@wise.example.org",
    rejection_reason: str | None = None,
) -> RC1GraphState:
    """Resume an interrupted graph after steward decision."""
    return graph.invoke(
        Command(
            resume={
                "decision": decision,
                "steward_id": steward_id,
                "rejection_reason": rejection_reason,
            }
        ),
        config,
    )


def advance_stage(state: RC1GraphState) -> dict[str, Any]:
    """Transition current_stage to next_stage after approval."""
    next_stage = state.get("next_stage") or PipelineStage.COMPLETE.value
    return {
        "current_stage": next_stage,
        "approval_gate": None,
    }


def reject_pipeline(state: RC1GraphState) -> dict[str, Any]:
    """Mark pipeline rejected at current stage."""
    gate = state.get("approval_gate") or {}
    return {
        "current_stage": PipelineStage.FAILED.value,
        "pending_interrupt": False,
        "errors": [
            {
                "stage": gate.get("stage"),
                "code": "steward_rejected",
                "message": gate.get("rejection_reason") or "Steward rejected proposed artifact",
                "retryable": False,
            }
        ],
    }
