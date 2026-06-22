"""Unit and integration tests for rights posture and provenance helpers."""

from uuid import uuid4

import pytest
from sqlalchemy import select

from wise_discovery.provenance import append_provenance_event
from wise_discovery.services.agent import propagate_rights_posture
from wise_registry.enums import ProvenanceEventType, TrustLevel
from wise_registry.models.license import License
from wise_registry.models.provenance_event import ProvenanceEvent
from wise_registry.models.source import Source
from wise_registry.provenance import ProvenanceChainError

pytestmark = pytest.mark.integration


def _make_source_with_license() -> Source:
    license_ = License(
        id=uuid4(),
        code="CC-BY-4.0",
        uri="https://creativecommons.org/licenses/by/4.0/",
        label="CC BY 4.0",
    )
    source = Source(
        id=uuid4(),
        canonical_name="wikidata",
        stable_id="wikidata",
        display_name="Wikidata",
        source_type_id=uuid4(),
        homepage_url="https://www.wikidata.org/",
        trust_level=TrustLevel.AUTHORITATIVE,
        active=True,
        license_id=license_.id,
    )
    source.license = license_
    return source


def test_propagate_rights_posture_from_license():
    source = _make_source_with_license()
    posture = propagate_rights_posture(source)
    assert posture.license_code == "CC-BY-4.0"
    assert posture.rights_uri == posture.license_uri
    assert "CC-BY-4.0" in posture.summary


def test_propagate_rights_posture_without_license():
    source = Source(
        id=uuid4(),
        canonical_name="example",
        stable_id="example",
        display_name="Example",
        source_type_id=uuid4(),
        homepage_url="https://example.org/",
        trust_level=TrustLevel.MEDIUM,
        active=True,
    )
    posture = propagate_rights_posture(source)
    assert posture.rights_uri is None
    assert "unknown" in posture.summary.lower()


def test_append_provenance_event_links_previous(db_session):
    source = db_session.scalar(select(Source).where(Source.canonical_name == "wikidata"))
    assert source is not None

    first = ProvenanceEvent(
        source_id=source.id,
        event_type=ProvenanceEventType.REGISTER,
        actor="seed",
        evidence_uris=["https://example.org/register"],
    )
    db_session.add(first)
    db_session.flush()

    second = append_provenance_event(
        db_session,
        source_id=source.id,
        evidence_uris=["https://example.org/harvest"],
    )
    assert second.previous_event_id == first.id
    assert second.event_type == ProvenanceEventType.HARVEST


def test_append_provenance_event_rejects_cross_source_previous(db_session):
    source_a = db_session.scalar(select(Source).where(Source.canonical_name == "wikidata"))
    source_b = db_session.scalar(select(Source).where(Source.canonical_name == "unesco"))
    assert source_a is not None and source_b is not None

    prior = ProvenanceEvent(
        source_id=source_a.id,
        event_type=ProvenanceEventType.REGISTER,
        actor="seed",
        evidence_uris=[],
    )
    db_session.add(prior)
    db_session.flush()

    with pytest.raises(ProvenanceChainError):
        append_provenance_event(
            db_session,
            source_id=source_b.id,
            evidence_uris=["https://example.org/harvest"],
            previous_event_id=prior.id,
        )
