"""Reference Capability 1 seed and schema tests."""

from __future__ import annotations

import pytest
from sqlalchemy import select, text

from wise_reference.models import (
    DiscoveryRecord,
    EntityAssertion,
    ExternalLink,
    GraphEntity,
    MetadataRecord,
    PremisEvent,
    PreservationObject,
    QualityReview,
)


@pytest.mark.integration
def test_stonehenge_discovery_record(rc1_session):
    record = rc1_session.scalars(
        select(DiscoveryRecord).where(DiscoveryRecord.stable_id == "stonehenge")
    ).one()
    assert record.status.value == "approved"
    assert record.source_registry_ref == "unesco"
    assert record.external_identifiers["unesco_whc"] == "373"
    assert record.external_identifiers["wikidata"] == "Q39671"


@pytest.mark.integration
def test_stonehenge_preservation_with_premis(rc1_session):
    obj = rc1_session.scalars(
        select(PreservationObject).where(PreservationObject.stable_id == "stonehenge")
    ).one()
    assert obj.ark == "ark:/99999/373/stonehenge/"
    assert obj.status.value == "approved"
    events = rc1_session.scalars(
        select(PremisEvent).where(PremisEvent.preservation_object_id == obj.id)
    ).all()
    assert len(events) >= 2
    assert {event.event_type for event in events} >= {"ingestion", "fixity"}


@pytest.mark.integration
def test_stonehenge_metadata_and_assertion(rc1_session):
    metadata = rc1_session.scalars(
        select(MetadataRecord).where(MetadataRecord.stable_id == "stonehenge")
    ).one()
    assertion = rc1_session.scalars(
        select(EntityAssertion).where(EntityAssertion.metadata_record_id == metadata.id)
    ).one()
    assert assertion.entity_type == "crm:E27_Site"
    assert assertion.status.value == "approved"


@pytest.mark.integration
def test_stonehenge_graph_entity_with_wikidata_link(rc1_session):
    entity = rc1_session.scalars(
        select(GraphEntity).where(GraphEntity.stable_id == "stonehenge")
    ).one()
    link = rc1_session.scalars(
        select(ExternalLink).where(ExternalLink.entity_id == entity.id)
    ).one()
    assert link.external_authority == "wikidata"
    assert link.external_identifier == "Q39671"
    assert link.status.value == "approved"


@pytest.mark.integration
def test_stonehenge_quality_review_approved(rc1_session):
    review = rc1_session.scalars(
        select(QualityReview).where(QualityReview.entity_uri.like("%stonehenge%"))
    ).one()
    assert review.status.value == "approved"
    assert review.disposition == "accepted"
    assert review.composite_score >= 0.9


@pytest.mark.integration
def test_provenance_chain_tables_linked(rc1_session):
    row = rc1_session.execute(
        text(
            """
            SELECT d.discovery_event_id, p.ingest_event_id, g.entity_uri, q.disposition
            FROM discovery.records d
            JOIN preservation.objects p ON p.discovery_record_id = d.id
            JOIN modeling.metadata_records m ON m.preservation_object_id = p.id
            JOIN modeling.entity_assertions ea ON ea.metadata_record_id = m.id
            JOIN graph.entities g ON g.entity_assertion_id = ea.id
            JOIN quality.reviews q ON q.graph_entity_id = g.id
            WHERE d.stable_id = 'stonehenge'
            """
        )
    ).one()
    assert row.disposition == "accepted"
    assert row.discovery_event_id.startswith("discovery-")
    assert row.ingest_event_id.startswith("ingest-")
