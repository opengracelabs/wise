"""Source Discovery Agent node (09) — discovery-service integration."""

from __future__ import annotations

from typing import Any

from wise_contracts.common import ApprovalStatus
from wise_orchestration.clients.rc1 import get_rc1_client
from wise_orchestration.provenance import append_provenance_event
from wise_orchestration.state import PipelineStage, RC1GraphState


def source_discovery_node(state: RC1GraphState) -> dict[str, Any]:
    """Call discovery-service to propose a Discovery Record from Source Registry."""
    stable_id = state["stable_id"]
    client = get_rc1_client()
    result = client.discover(stable_id)

    record_data = result["record"]
    event_id = result["discovery_event_id"]
    chain = append_provenance_event(state.get("provenance_chain") or [], event_id)
    evidence_profiles = dict(state.get("evidence_profiles") or {})
    evidence_profiles["discovery_record"] = record_data["evidence"]

    return {
        "current_stage": PipelineStage.SOURCE_DISCOVERY.value,
        "next_stage": PipelineStage.PRESERVATION.value,
        "discovery_record": record_data,
        "provenance_chain": chain,
        "current_provenance_event_id": result["provenance_event_id"],
        "source_registry_refs": result.get("source_registry_refs", []),
        "evidence_profiles": evidence_profiles,
        "approval_gate": {
            "gate_id": f"approval-discovery-{stable_id}",
            "stage": PipelineStage.SOURCE_DISCOVERY.value,
            "status": ApprovalStatus.PROPOSED.value,
            "artifact_key": "discovery_record",
        },
        "pending_interrupt": True,
        "retry_count": 0,
        "errors": [],
    }
