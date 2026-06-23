"""SQLAlchemy model and audit field tests."""

from __future__ import annotations

from uuid import uuid4

import pytest
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError

from wise_registry.base import AuditMixin, Base
from wise_registry.enums import ApprovalWorkflowStatus, ProvenanceEventType, TrustLevel, VerificationStatus
from wise_registry.models import (
    Asset,
    Attribution,
    License,
    ProvenanceEvent,
    PublicationApproval,
    RightsStatus,
    Source,
    SourceType,
)


EXPECTED_TABLES = {
    "registry.source_types",
    "registry.licenses",
    "registry.rights_statuses",
    "registry.sources",
    "registry.provenance_events",
    "registry.assets",
    "registry.attributions",
    "registry.publication_approvals",
}


def test_all_registry_tables_registered():
    table_keys = {f"{table.schema}.{table.name}" for table in Base.metadata.sorted_tables}
    assert EXPECTED_TABLES.issubset(table_keys)


@pytest.mark.parametrize(
    "model",
    [
        SourceType,
        License,
        RightsStatus,
        Source,
        ProvenanceEvent,
        Asset,
        Attribution,
        PublicationApproval,
    ],
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
        "stable_id",
        "display_name",
        "source_type_id",
        "homepage_url",
        "api_url",
        "license_id",
        "rights_status_id",
        "trust_level",
        "source_verification_status",
        "source_verified_at",
        "source_verified_by",
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
        "evidence_uris",
        "previous_event_id",
        "notes",
        "created_at",
        "updated_at",
    }.issubset(column_names)


def test_asset_required_columns():
    mapper = inspect(Asset)
    column_names = {col.key for col in mapper.columns}
    assert {
        "id",
        "stable_id",
        "title",
        "asset_type",
        "source_id",
        "license_id",
        "rights_status_id",
        "provenance_event_id",
        "source_verification_status",
        "license_verification_status",
        "provenance_verification_status",
        "rights_approval_status",
        "publication_approval_status",
        "created_at",
        "updated_at",
    }.issubset(column_names)


def test_asset_publishable_requires_full_rc17_sequence():
    asset = Asset(
        stable_id="asset-1",
        title="Asset",
        asset_type="image",
        source_id=uuid4(),
        source_verification_status=VerificationStatus.VERIFIED,
        license_verification_status=VerificationStatus.VERIFIED,
        provenance_verification_status=VerificationStatus.VERIFIED,
        rights_approval_status=ApprovalWorkflowStatus.APPROVED,
        publication_approval_status=ApprovalWorkflowStatus.PENDING,
    )

    assert asset.rc17_sequence_complete is True
    assert asset.publishable is False

    asset.publication_approval_status = ApprovalWorkflowStatus.APPROVED
    assert asset.publishable is True


def test_publication_approval_required_columns():
    mapper = inspect(PublicationApproval)
    column_names = {col.key for col in mapper.columns}
    assert {
        "id",
        "asset_id",
        "approval_status",
        "requested_by",
        "requested_at",
        "approved_by",
        "approved_at",
        "source_verified_snapshot",
        "license_verified_snapshot",
        "provenance_verified_snapshot",
        "rights_approved_snapshot",
        "attribution_snapshot",
        "decision_notes",
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
        stable_id="duplicate-test-a",
        display_name="First",
        source_type_id=source_type.id,
        homepage_url="https://example.org/",
        trust_level=TrustLevel.AUTHORITATIVE,
        created_by="test",
        updated_by="test",
    )
    second = Source(
        canonical_name="duplicate-test",
        stable_id="duplicate-test-b",
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
        stable_id="test-source",
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
