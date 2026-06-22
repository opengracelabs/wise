"""Metadata Agent node (10) — metadata-service integration."""

from __future__ import annotations

from typing import Any

from wise_contracts.common import ApprovalStatus
from wise_orchestration.clients.rc1 import get_rc1_client
from wise_orchestration.provenance import append_provenance_event
from wise_orchestration.state import PipelineStage, RC1GraphState


def metadata_node(state: RC1GraphState) -> dict[str, Any]:
    """Call metadata-service to propose MetadataRecord and EntityAssertion."""
    stable_id = state["stable_id"]
    preserved = state.get("preserved_object")
    if not preserved:
        raise ValueError("Metadata requires preserved_object in state")

    client = get_rc1_client()
    result = client.model_metadata(stable_id, preserved_object_ark=preserved["ark"])

    metadata_data = result["metadata_record"]
    assertion_data = result["entity_assertion"]
    modeling_event_id = result["modeling_event_id"]

    chain = append_provenance_event(
        state.get("provenance_chain") or [],
        modeling_event_id,
    )
    evidence_profiles = dict(state.get("evidence_profiles") or {})
    evidence_profiles["entity_assertion"] = result["evidence"]

    return {
        "current_stage": PipelineStage.METADATA.value,
        "next_stage": PipelineStage.KNOWLEDGE_GRAPH.value,
        "metadata_record": metadata_data,
        "entity_assertion": assertion_data,
        "provenance_chain": chain,
        "current_provenance_event_id": result["provenance_event_id"],
        "evidence_profiles": evidence_profiles,
        "approval_gate": {
            "gate_id": f"approval-metadata-{stable_id}",
            "stage": PipelineStage.METADATA.value,
            "status": ApprovalStatus.PROPOSED.value,
            "artifact_key": "entity_assertion",
        },
        "pending_interrupt": True,
        "retry_count": 0,
        "errors": [],
    }
