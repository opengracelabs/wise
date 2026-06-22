"""RC17 publication approval workflow Pydantic schemas."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from wise_registry.enums import ApprovalWorkflowStatus
from wise_registry.schemas.audit import AuditFields, AuditFieldsCreate


class PublicationApprovalBase(BaseModel):
    asset_id: UUID
    approval_status: ApprovalWorkflowStatus = ApprovalWorkflowStatus.PENDING
    requested_by: str = Field(default="system", max_length=255)
    requested_at: datetime | None = None
    approved_by: str | None = Field(default=None, max_length=255)
    approved_at: datetime | None = None
    publication_channel: str | None = Field(default=None, max_length=128)
    publication_uri: str | None = Field(default=None, max_length=512)
    source_verified_snapshot: bool = False
    license_verified_snapshot: bool = False
    provenance_verified_snapshot: bool = False
    rights_approved_snapshot: bool = False
    attribution_snapshot: dict = Field(default_factory=dict)
    decision_notes: str | None = None


class PublicationApprovalCreate(PublicationApprovalBase, AuditFieldsCreate):
    pass


class PublicationApprovalUpdate(BaseModel):
    approval_status: ApprovalWorkflowStatus | None = None
    approved_by: str | None = Field(default=None, max_length=255)
    approved_at: datetime | None = None
    publication_channel: str | None = Field(default=None, max_length=128)
    publication_uri: str | None = Field(default=None, max_length=512)
    source_verified_snapshot: bool | None = None
    license_verified_snapshot: bool | None = None
    provenance_verified_snapshot: bool | None = None
    rights_approved_snapshot: bool | None = None
    attribution_snapshot: dict | None = None
    decision_notes: str | None = None
    updated_by: str = Field(default="system", max_length=255)


class PublicationApprovalRead(PublicationApprovalBase, AuditFields):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    requested_at: datetime
