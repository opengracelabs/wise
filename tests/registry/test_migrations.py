"""Integration tests for Source Registry migrations and seed data."""

from __future__ import annotations

import pytest
from alembic import command
from sqlalchemy import func, select, text
from sqlalchemy.orm import Session

from wise_registry.enums import ProvenanceEventType, TrustLevel
from wise_registry.models import License, ProvenanceEvent, RightsStatus, Source, SourceType
from wise_registry.provenance import ProvenanceChainError, validate_chain, validate_event_link

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
        "assets",
        "attributions",
        "publication_approvals",
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
        assert event.evidence_uris
        assert event.evidence_uris[0].startswith("https://")
        assert event.notes is not None
        assert event.previous_event_id is None


@pytest.mark.integration
def test_v1_1_migration_columns_exist(db_session: Session):
    result = db_session.execute(
        text(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'registry'
              AND table_name = 'provenance_events'
            """
        )
    )
    columns = {row[0] for row in result}
    assert "evidence_uris" in columns
    assert "previous_event_id" in columns
    assert "evidence_uri" not in columns


@pytest.mark.integration
def test_rc17_migration_columns_exist(db_session: Session):
    source_columns = {
        row[0]
        for row in db_session.execute(
            text(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema = 'registry'
                  AND table_name = 'sources'
                """
            )
        )
    }
    assert {
        "rights_status_id",
        "source_verification_status",
        "source_verified_at",
        "source_verified_by",
    }.issubset(source_columns)

    asset_columns = {
        row[0]
        for row in db_session.execute(
            text(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema = 'registry'
                  AND table_name = 'assets'
                """
            )
        )
    }
    assert {
        "stable_id",
        "source_verification_status",
        "license_verification_status",
        "provenance_verification_status",
        "rights_approval_status",
        "publication_approval_status",
    }.issubset(asset_columns)


@pytest.mark.integration
def test_v1_1_migration_upgrade_downgrade(alembic_config, registry_database_url: str):
    from sqlalchemy import create_engine

    engine = create_engine(registry_database_url, pool_pre_ping=True)
    with Session(engine) as session:
        assert session.execute(
            text(
                """
                SELECT 1 FROM information_schema.columns
                WHERE table_schema = 'registry'
                  AND table_name = 'provenance_events'
                  AND column_name = 'previous_event_id'
                """
            )
        ).first() is not None

    command.downgrade(alembic_config, "005_registry_v1_1_provenance_hardening")

    with Session(engine) as session:
        columns = {
            row[0]
            for row in session.execute(
                text(
                    """
                    SELECT column_name
                    FROM information_schema.columns
                    WHERE table_schema = 'registry'
                      AND table_name = 'provenance_events'
                      AND column_name IN ('previous_event_id', 'evidence_uris')
                    """
                )
            )
        }
        assert "evidence_uris" in columns
        assert "previous_event_id" not in columns

    command.upgrade(alembic_config, "head")
    engine.dispose()


@pytest.mark.integration
@pytest.mark.parametrize("canonical_name,expected_stable_id", [
    ("unesco", "unesco-whc"),
    ("wikidata", "wikidata"),
    ("gbif", "gbif"),
])
def test_seed_sources_have_stable_id(db_session: Session, canonical_name: str, expected_stable_id: str):
    source = db_session.scalar(
        select(Source).where(Source.canonical_name == canonical_name)
    )
    assert source is not None
    assert source.stable_id == expected_stable_id


@pytest.mark.integration
def test_provenance_chain_linking(db_session: Session):
    source = db_session.scalar(select(Source).where(Source.canonical_name == "unesco"))
    assert source is not None

    register_event = db_session.scalar(
        select(ProvenanceEvent).where(
            ProvenanceEvent.source_id == source.id,
            ProvenanceEvent.event_type == ProvenanceEventType.REGISTER,
        )
    )
    assert register_event is not None

    update_event = ProvenanceEvent(
        source_id=source.id,
        event_type=ProvenanceEventType.UPDATE,
        actor="test",
        evidence_uris=["https://whc.unesco.org/updated"],
        notes="Metadata refresh",
        previous_event_id=register_event.id,
        created_by="test",
        updated_by="test",
    )
    validate_event_link(
        source.id,
        None,
        register_event.id,
        register_event,
    )
    db_session.add(update_event)
    db_session.flush()

    chain = db_session.scalars(
        select(ProvenanceEvent)
        .where(ProvenanceEvent.source_id == source.id)
        .order_by(ProvenanceEvent.event_timestamp)
    ).all()
    validate_chain(chain)
    assert update_event.previous_event_id == register_event.id
    assert update_event.previous_event.id == register_event.id


@pytest.mark.integration
def test_provenance_chain_rejects_cross_source_link(db_session: Session):
    unesco = db_session.scalar(select(Source).where(Source.canonical_name == "unesco"))
    wikidata = db_session.scalar(select(Source).where(Source.canonical_name == "wikidata"))
    assert unesco is not None and wikidata is not None

    register_event = db_session.scalar(
        select(ProvenanceEvent).where(
            ProvenanceEvent.source_id == unesco.id,
            ProvenanceEvent.event_type == ProvenanceEventType.REGISTER,
        )
    )
    assert register_event is not None

    with pytest.raises(ProvenanceChainError, match="same source_id"):
        validate_event_link(
            wikidata.id,
            None,
            register_event.id,
            register_event,
        )
