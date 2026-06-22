"""Source Discovery Agent v1 — Discovery capability for WISE."""

from wise_discovery.evidence import build_evidence_profile, evidence_profile_to_json
from wise_discovery.provenance import append_provenance_event
from wise_discovery.services.agent import (
    check_reachability,
    create_discovery_record,
    lookup_source,
    propagate_rights_posture,
    validate_source,
)

__all__ = [
    "append_provenance_event",
    "build_evidence_profile",
    "check_reachability",
    "create_discovery_record",
    "evidence_profile_to_json",
    "lookup_source",
    "propagate_rights_posture",
    "validate_source",
]
