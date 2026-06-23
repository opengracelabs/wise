"""Unit tests for Source Registry Pydantic schemas (no database)."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

import pytest
from pydantic import ValidationError

from wise_registry.enums import ApprovalWorkflowStatus, ProvenanceEventType, TrustLevel, VerificationStatus
from wise_registry.schemas.audit import AuditFields, AuditFieldsCreate
from wise_registry.schemas.asset import AssetCreate
from wise_registry.schemas.attribution import AttributionCreate
from wise_registry.schemas.license import LicenseCreate, LicenseRead
from wise_registry.schemas.provenance_event import ProvenanceEventCreate
from wise_registry.schemas.publication_approval import PublicationApprovalCreate
from wise_registry.schemas.rights_status import RightsStatusCreate
from wise_registry.schemas.source import SourceCreate, SourceUpdate
from wise_registry.schemas.source_type import SourceTypeCreate


def test_audit_fields_create_defaults():
    audit = AuditFieldsCreate()
    assert audit.created_by == "system"
    assert audit.updated_by == "system"


def test_source_create_defaults():
    source = SourceCreate(
        canonical_name="example-source",
        stable_id="example-source",
        display_name="Example Source",
        source_type_id=uuid4(),
        homepage_url="https://example.org/",
    )
    assert source.trust_level == TrustLevel.UNVERIFIED
    assert source.source_verification_status == VerificationStatus.PENDING
    assert source.rights_status_id is None
    assert source.active is True
    assert source.created_by == "system"


def test_source_create_requires_canonical_name():
    with pytest.raises(ValidationError):
        SourceCreate(
            display_name="Missing canonical_name",
            source_type_id=uuid4(),
            homepage_url="https://example.org/",
        )


def test_source_update_partial():
    update = SourceUpdate(display_name="Renamed", trust_level=TrustLevel.AUTHORITATIVE)
    assert update.display_name == "Renamed"
    assert update.api_url is None
    assert update.updated_by == "system"


def test_asset_create_defaults():
    asset = AssetCreate(
        stable_id="asset-1",
        title="Asset One",
        asset_type="image",
        source_id=uuid4(),
    )

    assert asset.source_verification_status == VerificationStatus.PENDING
    assert asset.license_verification_status == VerificationStatus.PENDING
    assert asset.provenance_verification_status == VerificationStatus.PENDING
    assert asset.rights_approval_status == ApprovalWorkflowStatus.PENDING
    assert asset.publication_approval_status == ApprovalWorkflowStatus.PENDING


def test_attribution_create():
    attribution = AttributionCreate(
        asset_id=uuid4(),
        source_id=uuid4(),
        display_text="Credit: Example Institution",
    )

    assert attribution.required is True
    assert attribution.sort_order == 0


def test_publication_approval_create_defaults():
    approval = PublicationApprovalCreate(asset_id=uuid4())

    assert approval.approval_status == ApprovalWorkflowStatus.PENDING
    assert approval.source_verified_snapshot is False
    assert approval.attribution_snapshot == {}


def test_source_type_create():
    st = SourceTypeCreate(code="authority", label="Authority File")
    assert st.code == "authority"
    assert st.description is None


def test_license_create_accepts_uri():
    lic = LicenseCreate(
        code="CC0-1.0",
        uri="https://creativecommons.org/publicdomain/zero/1.0/",
        label="CC0 1.0",
    )
    assert "creativecommons.org" in str(lic.uri)


def test_rights_status_create():
    rs = RightsStatusCreate(
        code="NoC-OKLR",
        uri="http://rightsstatements.org/vocab/NoC-OKLR/1.0/",
        label="No Copyright - Other Known Legal Restrictions",
    )
    assert rs.code == "NoC-OKLR"


def test_provenance_event_create():
    source_id = uuid4()
    event = ProvenanceEventCreate(
        source_id=source_id,
        event_type=ProvenanceEventType.REGISTER,
        actor="steward@opengrace.org",
        evidence_uris=["https://whc.unesco.org/"],
        notes="Initial registration",
    )
    assert event.event_type == ProvenanceEventType.REGISTER
    assert event.source_id == source_id
    assert event.evidence_uris == ["https://whc.unesco.org/"]
    assert event.previous_event_id is None


def test_provenance_event_create_defaults_evidence_uris():
    event = ProvenanceEventCreate(
        source_id=uuid4(),
        event_type=ProvenanceEventType.UPDATE,
    )
    assert event.evidence_uris == []


def test_provenance_event_create_accepts_chain_link():
    previous_id = uuid4()
    event = ProvenanceEventCreate(
        source_id=uuid4(),
        event_type=ProvenanceEventType.UPDATE,
        previous_event_id=previous_id,
    )
    assert event.previous_event_id == previous_id


def test_audit_fields_row_version_minimum():
    now = datetime.now(timezone.utc)
    with pytest.raises(ValidationError):
        AuditFields(
            created_at=now,
            updated_at=now,
            created_by="system",
            updated_by="system",
            row_version=0,
        )


def test_license_read_from_attributes():
    now = datetime.now(timezone.utc)
    lic_id = uuid4()

    class StubLicense:
        id = lic_id
        code = "CC-BY-4.0"
        uri = "https://creativecommons.org/licenses/by/4.0/"
        label = "CC BY 4.0"
        spdx_id = "CC-BY-4.0"
        description = None
        created_at = now
        updated_at = now
        created_by = "system"
        updated_by = "system"
        row_version = 1

    read = LicenseRead.model_validate(StubLicense())
    assert read.id == lic_id
    assert read.code == "CC-BY-4.0"
