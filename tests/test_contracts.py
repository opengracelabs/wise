"""Contract model unit tests."""

from datetime import UTC, datetime

from wise_contracts import (
    ApprovalStatus,
    DiscoveryRecord,
    EvidenceOutputProfile,
    ExternalIdentifiers,
    ProvenanceRef,
)


def test_discovery_record_contract():
    record = DiscoveryRecord(
        id="test-id",
        stable_id="stonehenge",
        status=ApprovalStatus.APPROVED,
        title="Stonehenge",
        source_registry_ref="unesco-whc",
        rights_uri="http://rightsstatements.org/vocab/NoC-OKLR/1.0/",
        ingestion_candidacy_score=0.94,
        external_identifiers=ExternalIdentifiers(unesco_whc="373", wikidata="Q39671"),
        evidence=EvidenceOutputProfile(
            confidence=0.97,
            evidence_summary="Test evidence",
            method="test",
            source_registry_refs=["unesco-whc"],
        ),
        provenance=ProvenanceRef(
            event_id="discovery-test",
            event_type="harvest",
            agent_version="test/0.1.0",
            event_timestamp=datetime(2026, 6, 22, tzinfo=UTC),
        ),
        discovered_at=datetime(2026, 6, 22, tzinfo=UTC),
    )
    assert record.status == ApprovalStatus.APPROVED
    assert record.external_identifiers.wikidata == "Q39671"
