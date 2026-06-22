"""Integration tests for Source Registry migrations and seed data."""

from __future__ import annotations

import pytest
from sqlalchemy import func, select, text
from sqlalchemy.orm import Session

from wise_registry.enums import ProvenanceEventType, TrustLevel
from wise_registry.models import License, ProvenanceEvent, RightsStatus, Source, SourceType

SEED_CANONICAL_NAMES = (
    "unesco",
    "wikidata",
    "wikimedia-commons",
    "openstreetmap",
    "gbif",
)

SEED_ACTOR = "wise-registry-seed"


@pytest.mark.integration
def test_registry_schema_tables_exist(db_session: Session):
    result = db_session.execute(
        text(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'registry'
            ORDER BY table_name
            """
        )
    )
    tables = {row[0] for row in result}
    assert {
        "sources",
        "source_types",
        "licenses",
        "rights_statuses",
        "provenance_events",
    }.issubset(tables)


@pytest.mark.integration
def test_reference_data_seeded(db_session: Session):
    source_type_count = db_session.scalar(select(func.count()).select_from(SourceType))
    license_count = db_session.scalar(select(func.count()).select_from(License))
    rights_count = db_session.scalar(select(func.count()).select_from(RightsStatus))

    assert source_type_count >= 4
    assert license_count >= 3
    assert rights_count >= 3


@pytest.mark.integration
@pytest.mark.parametrize("canonical_name", SEED_CANONICAL_NAMES)
def test_initial_sources_present(db_session: Session, canonical_name: str):
    source = db_session.scalar(
        select(Source).where(Source.canonical_name == canonical_name)
    )
    assert source is not None, f"Missing seed source: {canonical_name}"
    assert source.active is True
    assert source.trust_level in TrustLevel
    assert source.created_by == SEED_ACTOR
    assert source.updated_by == SEED_ACTOR
    assert source.row_version >= 1
    assert source.homepage_url.startswith("https://")
    assert source.source_type is not None


@pytest.mark.integration
def test_unesco_source(db_session: Session):
    source = db_session.scalar(select(Source).where(Source.canonical_name == "unesco"))
    assert source is not None
    assert source.display_name == "UNESCO World Heritage Centre"
    assert source.trust_level == TrustLevel.AUTHORITATIVE
    assert source.source_type.code == "authority"


@pytest.mark.integration
def test_wikimedia_commons_license(db_session: Session):
    source = db_session.scalar(
        select(Source).where(Source.canonical_name == "wikimedia-commons")
    )
    assert source is not None
    assert source.license is not None
    assert source.license.code == "CC-BY-4.0"


@pytest.mark.integration
def test_openstreetmap_geospatial_type(db_session: Session):
    source = db_session.scalar(
        select(Source).where(Source.canonical_name == "openstreetmap")
    )
    assert source is not None
    assert source.source_type.code == "geospatial"
    assert source.license is not None
    assert source.license.code == "ODbL-1.0"


@pytest.mark.integration
def test_gbif_biodiversity_source(db_session: Session):
    source = db_session.scalar(select(Source).where(Source.canonical_name == "gbif"))
    assert source is not None
    assert source.display_name == "GBIF"
    assert source.source_type.code == "biodiversity"
    assert source.api_url == "https://api.gbif.org/v1/"


@pytest.mark.integration
def test_seed_provenance_events(db_session: Session):
    sources = db_session.scalars(
        select(Source).where(Source.canonical_name.in_(SEED_CANONICAL_NAMES))
    ).all()
    assert len(sources) == len(SEED_CANONICAL_NAMES)

    for source in sources:
        events = db_session.scalars(
            select(ProvenanceEvent).where(
                ProvenanceEvent.source_id == source.id,
                ProvenanceEvent.event_type == ProvenanceEventType.REGISTER,
            )
        ).all()
        assert len(events) >= 1
        event = events[0]
        assert event.created_by == SEED_ACTOR
        assert event.actor == SEED_ACTOR
        assert event.evidence_uri is not None
        assert event.evidence_uri.startswith("https://")
        assert event.notes is not None
