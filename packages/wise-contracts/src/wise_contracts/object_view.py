"""Aggregated Reference Capability 1 object view."""

from __future__ import annotations

from pydantic import BaseModel, Field

from wise_contracts.discovery import DiscoveryRecord
from wise_contracts.graph import GraphEntity
from wise_contracts.metadata import EntityAssertion, MetadataRecord
from wise_contracts.preservation import PremisEvent, PreservedObjectDescriptor
from wise_contracts.quality import QualityReviewRecord


class SourceRegistryRef(BaseModel):
    """Source Registry entry summary for object provenance."""

    stable_id: str
    name: str
    institution_name: str | None = None
    base_uri: str
    rights_posture_summary: str | None = None
    covenant_status: str


class HeritageObjectView(BaseModel):
    """End-to-end Reference Capability 1 object aggregate."""

    stable_id: str
    title: str
    source_registry: SourceRegistryRef
    discovery: DiscoveryRecord
    preservation: PreservedObjectDescriptor
    preservation_events: list[PremisEvent] = Field(default_factory=list)
    metadata: MetadataRecord
    entity_assertion: EntityAssertion
    graph_entity: GraphEntity
    quality_review: QualityReviewRecord
    provenance_chain: list[str] = Field(
        default_factory=list,
        description="Ordered list of provenance event IDs from discovery through quality",
    )
    rights_verified: bool = False
    quality_approved: bool = False
    accessibility_compliant: bool = False
