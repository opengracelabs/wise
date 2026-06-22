"""Knowledge Graph Agent node (12) — knowledge-graph-service integration."""

from __future__ import annotations

from typing import Any

from wise_contracts.common import ApprovalStatus
from wise_orchestration.clients.rc1 import get_rc1_client
from wise_orchestration.provenance import append_provenance_event
from wise_orchestration.state import PipelineStage, RC1GraphState


def knowledge_graph_node(state: RC1GraphState) -> dict[str, Any]:
    """Call knowledge-graph-service to propose GraphEntity placement."""
    stable_id = state["stable_id"]
    assertion = state.get("entity_assertion")
    if not assertion:
        raise ValueError("Knowledge graph placement requires entity_assertion in state")

    client = get_rc1_client()
    result = client.place_graph(stable_id, entity_assertion_id=assertion["id"])

    graph_data = result["graph_entity"]
    graph_event_id = result["graph_event_id"]
    chain = append_provenance_event(state.get("provenance_chain") or [], graph_event_id)

    evidence_profiles = dict(state.get("evidence_profiles") or {})
    if result.get("evidence"):
        evidence_profiles["graph_entity"] = result["evidence"]

    return {
        "current_stage": PipelineStage.KNOWLEDGE_GRAPH.value,
        "next_stage": PipelineStage.QUALITY_REVIEW.value,
        "graph_entity": graph_data,
        "provenance_chain": chain,
        "current_provenance_event_id": result["provenance_event_id"],
        "evidence_profiles": evidence_profiles,
        "approval_gate": {
            "gate_id": f"approval-graph-{stable_id}",
            "stage": PipelineStage.KNOWLEDGE_GRAPH.value,
            "status": ApprovalStatus.PROPOSED.value,
            "artifact_key": "graph_entity",
        },
        "pending_interrupt": True,
        "retry_count": 0,
        "errors": [],
    }
