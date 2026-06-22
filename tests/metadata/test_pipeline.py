"""Integration tests for metadata pipeline."""

from uuid import UUID

import pytest
from sqlalchemy import select

from wise_metadata.enums import AssertionStatus, SourceSchema
from wise_metadata.models import (
    AuthorityRecordProposal,
    EntityAssertionProposal,
    NormalizedRecord,
    ValidationResult,
)
from wise_metadata.schemas.normalized_record import NormalizedRecordCreate
from wise_metadata.services.pipeline import process_record, source_schema_for_canonical_name
from wise_registry.models.source import Source

pytestmark = pytest.mark.integration


@pytest.fixture
def wikidata_source(db_session) -> Source:
    source = db_session.scalars(
        select(Source).where(Source.canonical_name == "wikidata")
    ).first()
    assert source is not None
    return source


def test_pipeline_processes_wikidata_record(db_session, wikidata_source):
    record = NormalizedRecordCreate(
        source_id=wikidata_source.id,
        external_record_id="Q16476",
        source_schema=SourceSchema.WIKIDATA,
        raw_payload={
            "id": "Q16476",
            "labels": {"en": {"value": "Stonehenge"}},
            "descriptions": {"en": {"value": "Prehistoric monument in England"}},
        },
    )
    summary = process_record(
        db_session,
        source=wikidata_source,
        record=record,
        rights_uri="https://creativecommons.org/publicdomain/zero/1.0/",
        license=wikidata_source.license,
    )
    db_session.commit()

    assert summary["assertion_proposals"] >= 1

    normalized = db_session.get(NormalizedRecord, UUID(summary["normalized_record_id"]))
    assert normalized is not None
    assert normalized.normalized_payload["dcterms:title"] == "Stonehenge"
    assert normalized.normalization_event_id is not None

    validations = db_session.scalars(
        select(ValidationResult).where(
            ValidationResult.normalized_record_id == normalized.id
        )
    ).all()
    assert len(validations) >= 2

    assertions = db_session.scalars(
        select(EntityAssertionProposal).where(
            EntityAssertionProposal.normalized_record_id == normalized.id
        )
    ).all()
    assert all(a.status == AssertionStatus.PROPOSED for a in assertions)
    assert all("evidence_uris" in a.evidence for a in assertions)

    authorities = db_session.scalars(
        select(AuthorityRecordProposal).where(
            AuthorityRecordProposal.normalized_record_id == normalized.id
        )
    ).all()
    assert len(authorities) >= 1


def test_source_schema_mapping():
    assert source_schema_for_canonical_name("unesco") == SourceSchema.UNESCO_WHC
    assert source_schema_for_canonical_name("openstreetmap") == SourceSchema.OPENSTREETMAP
