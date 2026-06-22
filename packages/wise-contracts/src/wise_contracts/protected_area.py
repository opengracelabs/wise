"""Protected area and map service contracts (Reference Capability 3)."""

from __future__ import annotations

from pydantic import BaseModel, Field

from wise_contracts.common import ApprovalStatus, EvidenceOutputProfile, ProvenanceRef
from wise_contracts.discovery import DiscoveryRecord
from wise_contracts.graph import GraphEntity
from wise_contracts.metadata import EntityAssertion, MetadataRecord
from wise_contracts.object_view import SourceRegistryRef
from wise_contracts.preservation import PremisEvent, PreservedObjectDescriptor
from wise_contracts.quality import QualityReviewRecord


class ProtectedAreaIdentifiers(BaseModel):
    """Cross-authority identifiers for a protected area."""

    ramsar: str | None = None
    unesco_whc: str | None = None
    unesco_mab: str | None = None
    wikidata: str | None = None
    geonames: str | None = None
    iucn_pid: str | None = None


class ConservationMetadata(BaseModel):
    """Conservation designation metadata for a protected area."""

    iucn_category: str | None = None
    designation_type: str | None = None
    ramsar_criteria: list[str] = Field(default_factory=list)
    designation_date: str | None = None
    area_hectares: float | None = None
    country: str | None = None
    unesco_whc_id: str | None = None
    management_authority: str | None = None


class ProtectedAreaRegistryEntry(BaseModel):
    """Protected area registry record with geospatial anchor."""

    id: str
    stable_id: str
    status: ApprovalStatus = ApprovalStatus.PROPOSED
    pref_label: str
    designation_type: str
    conservation_metadata: ConservationMetadata
    external_identifiers: ProtectedAreaIdentifiers
    boundary_geojson: dict
    centroid_geojson: dict
    evidence: EvidenceOutputProfile
    provenance: ProvenanceRef
    graph_entity_id: str


class MapAreaSummary(BaseModel):
    """Lightweight map feature for search results."""

    stable_id: str
    pref_label: str
    designation_type: str
    centroid_geojson: dict
    boundary_geojson: dict | None = None
    external_identifiers: ProtectedAreaIdentifiers


class MapSearchResult(BaseModel):
    """Bbox or nearby protected area search response."""

    count: int
    bbox: list[float] | None = Field(
        default=None,
        description="[min_lon, min_lat, max_lon, max_lat] when bbox query used",
    )
    areas: list[MapAreaSummary]


class ProtectedAreaObjectView(BaseModel):
    """End-to-end Reference Capability 3 protected area aggregate."""

    stable_id: str
    title: str
    source_registry: SourceRegistryRef
    protected_area: ProtectedAreaRegistryEntry
    discovery: DiscoveryRecord
    preservation: PreservedObjectDescriptor
    preservation_events: list[PremisEvent] = Field(default_factory=list)
    metadata: MetadataRecord
    entity_assertion: EntityAssertion
    graph_entity: GraphEntity
    quality_review: QualityReviewRecord
    provenance_chain: list[str] = Field(default_factory=list)
    rights_verified: bool = False
    quality_approved: bool = False
    accessibility_compliant: bool = False
    geospatial_indexed: bool = False
