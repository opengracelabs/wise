"""Integration tests for discovery agent record creation."""

import pytest
from sqlalchemy import select, text

from wise_discovery.enums import ApprovalStatus
from wise_discovery.models.discovery_record import DiscoveryRecord
from wise_discovery.schemas.discovery_record import DiscoveryRecordCreate
from wise_discovery.services.agent import create_discovery_record, lookup_source
from wise_registry.enums import ProvenanceEventType
from wise_registry.models.provenance_event import ProvenanceEvent
from wise_registry.models.source import Source

pytestmark = pytest.mark.integration


class _ReachableClient:
    def head(self, url: str, *, timeout: float):
        class _Response:
            status_code = 200

        return _Response()

    def get(self, url: str, *, timeout: float):
        return self.head(url, timeout=timeout)


def test_discovery_v1_columns_exist(db_session):
    columns = {
        row[0]
        for row in db_session.execute(
            text(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema = 'discovery' AND table_name = 'records'
                """
            )
        )
    }
    assert {
        "source_id",
        "source_record_uri",
        "raw_payload_ref",
        "discovery_timestamp",
        "confidence",
        "approval_status",
        "evidence_uris",
    }.issubset(columns)


def test_create_discovery_record_persists_chain(db_session):
    source = db_session.scalar(select(Source).where(Source.canonical_name == "wikidata"))
    assert source is not None

    prior_count = db_session.scalar(
        select(ProvenanceEvent).where(ProvenanceEvent.source_id == source.id)
    )
    _ = prior_count

    payload = DiscoveryRecordCreate(
        stable_id="integration-test-wikidata-1",
        source_id=source.id,
        source_record_uri="https://www.wikidata.org/wiki/Q39671",
        raw_payload_ref="s3://wise-discovery/test/wikidata-q39671.json",
        confidence=0.85,
        evidence_uris=["https://www.wikidata.org/wiki/Q39671"],
        evidence_summary="Wikidata entity page reachable",
        method="harvest-probe",
        title="Integration test record",
    )

    record = create_discovery_record(
        db_session,
        payload=payload,
        source=source,
        http_client=_ReachableClient(),
    )
    db_session.commit()

    stored = db_session.scalar(
        select(DiscoveryRecord).where(DiscoveryRecord.stable_id == payload.stable_id)
    )
    assert stored is not None
    assert stored.source_id == source.id
    assert stored.approval_status == ApprovalStatus.PROPOSED
    assert stored.provenance_event_id == record.provenance_event_id

    event = db_session.get(ProvenanceEvent, stored.provenance_event_id)
    assert event is not None
    assert event.event_type == ProvenanceEventType.HARVEST
    assert event.evidence_uris == payload.evidence_uris


def test_lookup_source_by_canonical_name(db_session):
    source = lookup_source(db_session, canonical_name="unesco")
    assert source.stable_id == "unesco-whc"
