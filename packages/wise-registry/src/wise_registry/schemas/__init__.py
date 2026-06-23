"""Pydantic schemas for Source Registry v1."""

from wise_registry.schemas.audit import AuditFields
from wise_registry.schemas.asset import AssetCreate, AssetRead, AssetUpdate
from wise_registry.schemas.attribution import AttributionCreate, AttributionRead, AttributionUpdate
from wise_registry.schemas.license import LicenseCreate, LicenseRead
from wise_registry.schemas.provenance_event import ProvenanceEventCreate, ProvenanceEventRead
from wise_registry.schemas.publication_approval import (
    PublicationApprovalCreate,
    PublicationApprovalRead,
    PublicationApprovalUpdate,
)
from wise_registry.schemas.rights_status import RightsStatusCreate, RightsStatusRead
from wise_registry.schemas.source import SourceCreate, SourceRead, SourceUpdate
from wise_registry.schemas.source_type import SourceTypeCreate, SourceTypeRead

__all__ = [
    "AuditFields",
    "AssetCreate",
    "AssetRead",
    "AssetUpdate",
    "AttributionCreate",
    "AttributionRead",
    "AttributionUpdate",
    "LicenseCreate",
    "LicenseRead",
    "ProvenanceEventCreate",
    "ProvenanceEventRead",
    "PublicationApprovalCreate",
    "PublicationApprovalRead",
    "PublicationApprovalUpdate",
    "RightsStatusCreate",
    "RightsStatusRead",
    "SourceCreate",
    "SourceRead",
    "SourceUpdate",
    "SourceTypeCreate",
    "SourceTypeRead",
]
