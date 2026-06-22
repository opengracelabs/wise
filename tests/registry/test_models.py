"""SQLAlchemy model and audit field tests."""

from __future__ import annotations

import pytest
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError

from wise_registry.base import AuditMixin, Base
from wise_registry.enums import ProvenanceEventType, TrustLevel
from wise_registry.models import License, ProvenanceEvent, RightsStatus, Source, SourceType


EXPECTED_TABLES = {
    "registry.source_types",
    "registry.licenses",
    "registry.rights_statuses",
    "registry.sources",
    "registry.provenance_events",
}


def test_all_registry_tables_registered():
    table_keys = {f"{table.schema}.{table.name}" for table in Base.metadata.sorted_tables}
    assert EXPECTED_TABLES.issubset(table_keys)


@pytest.mark.parametrize(
    "model",
    [SourceType, License, RightsStatus, Source, ProvenanceEvent],
)
def test_models_include_audit_mixin(model):
    assert issubclass(model, AuditMixin)
    mapper = inspect(model)
    column_names = {col.key for col in mapper.columns}
    assert {"created_at", "updated_at", "created_by", "updated_by", "row_version"}.issubset(
        column_names
    )


def test_source_required_columns():
    mapper = inspect(Source)
    column_names = {col.key for col in mapper.columns}
    assert {
        "id",
        "canonical_name",
        "display_name",
        "source_type_id",
        "homepage_url",
        "api_url",
        "license_id",
        "trust_level",
        "active",
        "created_at",
        "updated_at",
    }.issubset(column_names)


def test_provenance_event_required_columns():
    mapper = inspect(ProvenanceEvent)
    column_names = {col.key for col in mapper.columns}
    assert {
        "id",
        "source_id",
        "event_type",
        "event_timestamp",
        "actor",
        "evidence_uri",
        "notes",
        "created_at",
        "updated_at",
    }.issubset(column_names)


@pytest.mark.integration
def test_source_canonical_name_unique(db_session):
    source_type = SourceType(
        code="test-authority",
        label="Test Authority",
        created_by="test",
        updated_by="test",
    )
    db_session.add(source_type)
    db_session.flush()

    first = Source(
        canonical_name="duplicate-test",
        display_name="First",
        source_type_id=source_type.id,
        homepage_url="https://example.org/",
        trust_level=TrustLevel.AUTHORITATIVE,
        created_by="test",
        updated_by="test",
    )
    second = Source(
        canonical_name="duplicate-test",
        display_name="Second",
        source_type_id=source_type.id,
        homepage_url="https://example.org/",
        trust_level=TrustLevel.AUTHORITATIVE,
        created_by="test",
        updated_by="test",
    )
    db_session.add(first)
    db_session.flush()
    db_session.add(second)
    with pytest.raises(IntegrityError):
        db_session.flush()


@pytest.mark.integration
def test_provenance_event_links_source(db_session):
    source_type = SourceType(
        code="test-media",
        label="Test Media",
        created_by="test",
        updated_by="test",
    )
    db_session.add(source_type)
    db_session.flush()

    source = Source(
        canonical_name="test-source",
        display_name="Test Source",
        source_type_id=source_type.id,
        homepage_url="https://example.org/",
        trust_level=TrustLevel.HIGH,
        created_by="test",
        updated_by="test",
    )
    db_session.add(source)
    db_session.flush()

    event = ProvenanceEvent(
        source_id=source.id,
        event_type=ProvenanceEventType.REGISTER,
        actor="test",
        notes="Test registration",
        created_by="test",
        updated_by="test",
    )
    db_session.add(event)
    db_session.flush()

    assert event.id is not None
    assert event.source_id == source.id
    assert event.source.canonical_name == "test-source"
