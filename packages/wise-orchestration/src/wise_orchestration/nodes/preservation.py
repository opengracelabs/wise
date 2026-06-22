"""Preservation Agent node (11) — preservation-service integration."""

from __future__ import annotations

from typing import Any

from wise_contracts.common import ApprovalStatus
from wise_orchestration.clients.rc1 import get_rc1_client
from wise_orchestration.provenance import append_provenance_event
from wise_orchestration.state import PipelineStage, RC1GraphState


def preservation_node(state: RC1GraphState) -> dict[str, Any]:
    """Call preservation-service to propose Preserved Object Descriptor + PREMIS."""
    stable_id = state["stable_id"]
    discovery_record = state.get("discovery_record")
    if not discovery_record:
        raise ValueError("Preservation requires approved discovery_record in state")

    client = get_rc1_client()
    result = client.preserve(stable_id, discovery_record_id=discovery_record["id"])

    object_descriptor = result["object_descriptor"]
    premis_events = result["premis_events"]
    ingest_event_id = result["ingest_event_id"]

    chain = list(state.get("provenance_chain") or [])
    chain = append_provenance_event(chain, ingest_event_id)
    for event in premis_events:
        chain = append_provenance_event(chain, event["id"])

    return {
        "current_stage": PipelineStage.PRESERVATION.value,
        "next_stage": PipelineStage.METADATA.value,
        "preserved_object": object_descriptor,
        "premis_events": premis_events,
        "provenance_chain": chain,
        "current_provenance_event_id": result["provenance_event_id"],
        "approval_gate": {
            "gate_id": f"approval-preservation-{stable_id}",
            "stage": PipelineStage.PRESERVATION.value,
            "status": ApprovalStatus.PROPOSED.value,
            "artifact_key": "preserved_object",
        },
        "pending_interrupt": True,
        "retry_count": 0,
        "errors": [],
    }
