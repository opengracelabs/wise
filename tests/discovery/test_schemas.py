"""Unit tests for discovery schemas and evidence profile builder."""

from uuid import uuid4

import pytest
from pydantic import ValidationError

from wise_discovery.evidence import build_evidence_profile, evidence_profile_to_json
from wise_discovery.schemas.discovery_record import DiscoveryRecordCreate
from wise_discovery.enums import ApprovalStatus


def test_build_evidence_profile_requires_uris():
    profile = build_evidence_profile(
        evidence_uris=["https://example.org/record/1"],
        confidence=0.9,
        evidence_summary="Harvest probe succeeded",
        method="harvest-probe",
        source_registry_refs=["wikidata"],
        provenance_event_id=uuid4(),
    )
    assert profile.confidence == 0.9
    assert profile.source_registry_refs == ["wikidata"]


def test_build_evidence_profile_rejects_empty_uris():
    with pytest.raises(ValidationError):
        build_evidence_profile(
            evidence_uris=[],
            confidence=0.5,
            evidence_summary="x",
            method="rule-based",
            source_registry_refs=["wikidata"],
        )


def test_evidence_profile_to_json_serializes_uuid():
    event_id = uuid4()
    profile = build_evidence_profile(
        evidence_uris=["https://example.org/1"],
        confidence=1.0,
        evidence_summary="ok",
        method="rule-based",
        source_registry_refs=["unesco"],
        provenance_event_id=event_id,
    )
    payload = evidence_profile_to_json(profile)
    assert payload["provenance_event_id"] == str(event_id)


def test_discovery_record_create_defaults():
    payload = DiscoveryRecordCreate(
        stable_id="test-record-1",
        source_id=uuid4(),
        source_record_uri="https://example.org/records/1",
        confidence=0.8,
        evidence_uris=["https://example.org/records/1"],
        evidence_summary="Discovered via API",
        method="api-harvest",
    )
    assert payload.approval_status == ApprovalStatus.PROPOSED
