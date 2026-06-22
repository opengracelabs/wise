"""RC17 asset registry Pydantic schemas."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from wise_registry.enums import ApprovalWorkflowStatus, VerificationStatus
from wise_registry.schemas.audit import AuditFields, AuditFieldsCreate


class AssetBase(BaseModel):
    stable_id: str = Field(max_length=128)
    title: str = Field(max_length=255)
    asset_type: str = Field(max_length=64)
    source_id: UUID
    source_record_uri: str | None = Field(default=None, max_length=512)
    canonical_uri: str | None = Field(default=None, max_length=512)
    license_id: UUID | None = None
    rights_status_id: UUID | None = None
    provenance_event_id: UUID | None = None
    source_verification_status: VerificationStatus = VerificationStatus.PENDING
    source_verified_at: datetime | None = None
    source_verified_by: str | None = Field(default=None, max_length=255)
    license_verification_status: VerificationStatus = VerificationStatus.PENDING
    license_verified_at: datetime | None = None
    license_verified_by: str | None = Field(default=None, max_length=255)
    provenance_verification_status: VerificationStatus = VerificationStatus.PENDING
    provenance_verified_at: datetime | None = None
    provenance_verified_by: str | None = Field(default=None, max_length=255)
    rights_approval_status: ApprovalWorkflowStatus = ApprovalWorkflowStatus.PENDING
    rights_approved_at: datetime | None = None
    rights_approved_by: str | None = Field(default=None, max_length=255)
    publication_approval_status: ApprovalWorkflowStatus = ApprovalWorkflowStatus.PENDING
    publication_approved_at: datetime | None = None
    publication_approved_by: str | None = Field(default=None, max_length=255)
    notes: str | None = None


class AssetCreate(AssetBase, AuditFieldsCreate):
    pass


class AssetUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=255)
    source_record_uri: str | None = Field(default=None, max_length=512)
    canonical_uri: str | None = Field(default=None, max_length=512)
    license_id: UUID | None = None
    rights_status_id: UUID | None = None
    provenance_event_id: UUID | None = None
    source_verification_status: VerificationStatus | None = None
    source_verified_at: datetime | None = None
    source_verified_by: str | None = Field(default=None, max_length=255)
    license_verification_status: VerificationStatus | None = None
    license_verified_at: datetime | None = None
    license_verified_by: str | None = Field(default=None, max_length=255)
    provenance_verification_status: VerificationStatus | None = None
    provenance_verified_at: datetime | None = None
    provenance_verified_by: str | None = Field(default=None, max_length=255)
    rights_approval_status: ApprovalWorkflowStatus | None = None
    rights_approved_at: datetime | None = None
    rights_approved_by: str | None = Field(default=None, max_length=255)
    publication_approval_status: ApprovalWorkflowStatus | None = None
    publication_approved_at: datetime | None = None
    publication_approved_by: str | None = Field(default=None, max_length=255)
    notes: str | None = None
    updated_by: str = Field(default="system", max_length=255)


class AssetRead(AssetBase, AuditFields):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
