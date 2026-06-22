"""Error recovery routing for RC1 orchestration."""

from __future__ import annotations

from typing import Literal

from wise_orchestration.state import ErrorRecord, PipelineStage, RC1GraphState

RecoveryRoute = Literal["retry", "dead_letter", "steward_escalation", "continue", "fail"]


def classify_error(stage: PipelineStage, code: str, message: str, *, retryable: bool = True) -> dict:
    """Build a structured error record for graph state."""
    record = ErrorRecord(stage=stage, code=code, message=message, retryable=retryable)
    return record.model_dump(mode="json")


def should_retry(state: RC1GraphState) -> bool:
    """Return True when retry budget remains and last error is retryable."""
    retry_count = state.get("retry_count", 0)
    max_retries = state.get("max_retries", 3)
    errors = state.get("errors") or []
    if retry_count >= max_retries:
        return False
    if not errors:
        return False
    last = errors[-1]
    return bool(last.get("retryable", True))


def route_on_error(state: RC1GraphState) -> RecoveryRoute:
    """Determine recovery path after an agent node failure."""
    if state.get("dead_letter"):
        return "dead_letter"
    if should_retry(state):
        return "retry"
    if state.get("steward_escalation"):
        return "steward_escalation"
    errors = state.get("errors") or []
    if errors and not errors[-1].get("retryable", True):
        return "steward_escalation"
    return "dead_letter"


def increment_retry(state: RC1GraphState) -> dict:
    """Return state patch incrementing retry counter and clearing last error."""
    return {"retry_count": state.get("retry_count", 0) + 1, "errors": []}


def mark_dead_letter(state: RC1GraphState, reason: str) -> dict:
    """Return state patch marking pipeline as dead-lettered."""
    error = classify_error(
        PipelineStage(state.get("current_stage", PipelineStage.FAILED.value)),
        code="dead_letter",
        message=reason,
        retryable=False,
    )
    return {
        "dead_letter": True,
        "current_stage": PipelineStage.DEAD_LETTER.value,
        "errors": [error],
    }


def mark_steward_escalation(state: RC1GraphState, reason: str) -> dict:
    """Return state patch flagging steward escalation."""
    error = classify_error(
        PipelineStage(state.get("current_stage", PipelineStage.FAILED.value)),
        code="steward_escalation",
        message=reason,
        retryable=False,
    )
    return {
        "steward_escalation": True,
        "current_stage": PipelineStage.FAILED.value,
        "errors": [error],
    }


def route_after_approval(state: RC1GraphState) -> str:
    """Route after steward approval gate: advance, reject, or escalate."""
    gate = state.get("approval_gate") or {}
    status = gate.get("status", "proposed")
    if status == "approved":
        return "advance"
    if status == "rejected":
        return "reject"
    return "wait"
