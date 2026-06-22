"""Quality Review Agent node (13) — metadata-service quality integration."""

from __future__ import annotations

from typing import Any

from wise_contracts.common import ApprovalStatus
from wise_orchestration.clients.rc1 import get_rc1_client
from wise_orchestration.provenance import append_provenance_event
from wise_orchestration.state import PipelineStage, RC1GraphState


def quality_review_node(state: RC1GraphState) -> dict[str, Any]:
    """Propose QualityReviewRecord; disposition remains null until steward approval."""
    stable_id = state["stable_id"]
    graph_entity = state.get("graph_entity")
    if not graph_entity:
        raise ValueError("Quality review requires graph_entity in state")

    entity_uri = graph_entity.get("entity_uri") or graph_entity.get("uri")
    if not entity_uri:
        raise ValueError("Graph entity missing entity_uri")

    client = get_rc1_client()
    result = client.review_quality(stable_id, graph_entity_uri=entity_uri)

    review_data = result["quality_review"]
    quality_event_id = result["quality_event_id"]
    chain = append_provenance_event(state.get("provenance_chain") or [], quality_event_id)

    return {
        "current_stage": PipelineStage.QUALITY_REVIEW.value,
        "next_stage": PipelineStage.COMPLETE.value,
        "quality_review": review_data,
        "provenance_chain": chain,
        "current_provenance_event_id": result["provenance_event_id"],
        "approval_gate": {
            "gate_id": f"approval-quality-{stable_id}",
            "stage": PipelineStage.QUALITY_REVIEW.value,
            "status": ApprovalStatus.PROPOSED.value,
            "artifact_key": "quality_review",
        },
        "pending_interrupt": True,
        "retry_count": 0,
        "errors": [],
    }
