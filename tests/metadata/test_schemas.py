"""Unit tests for Pydantic schemas."""

from uuid import uuid4

import pytest
from pydantic import ValidationError

from wise_metadata.enums import MappingTarget, SourceSchema
from wise_metadata.schemas.evidence import EvidenceProfile
from wise_metadata.schemas.normalized_record import NormalizedRecordCreate


def _evidence() -> EvidenceProfile:
    return EvidenceProfile(
        evidence_uris=["https://example.org/source"],
        confidence=1.0,
        evidence_summary="Test evidence",
        method="rule-based",
        source_registry_refs=["https://wise.example/registry/source/test"],
    )


def test_evidence_profile_requires_uris():
    with pytest.raises(ValidationError):
        EvidenceProfile(
            evidence_uris=[],
            confidence=1.0,
            evidence_summary="x",
            method="rule-based",
            source_registry_refs=["ref"],
        )


def test_evidence_profile_confidence_bounds():
    data = _evidence().model_dump()
    data["confidence"] = 1.5
    with pytest.raises(ValidationError):
        EvidenceProfile.model_validate(data)


def test_normalized_record_create():
    record = NormalizedRecordCreate(
        source_id=uuid4(),
        external_record_id="Q16476",
        source_schema=SourceSchema.WIKIDATA,
        raw_payload={"id": "Q16476"},
    )
    assert record.source_schema == SourceSchema.WIKIDATA


def test_evidence_profile_json_roundtrip():
    profile = _evidence()
    data = profile.model_dump(mode="json")
    restored = EvidenceProfile.model_validate(data)
    assert restored.confidence == profile.confidence
