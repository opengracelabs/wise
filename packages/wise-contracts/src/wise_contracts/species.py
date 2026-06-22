"""Species and biodiversity contracts (10-metadata-agent §5.3, Darwin Core)."""

from __future__ import annotations

from pydantic import BaseModel, Field

from wise_contracts.common import ApprovalStatus, EvidenceOutputProfile, ProvenanceRef
from wise_contracts.discovery import DiscoveryRecord
from wise_contracts.graph import GraphEntity
from wise_contracts.metadata import EntityAssertion, MetadataRecord
from wise_contracts.object_view import SourceRegistryRef
from wise_contracts.preservation import PremisEvent, PreservedObjectDescriptor
from wise_contracts.quality import QualityReviewRecord


class GbifExternalIdentifiers(BaseModel):
    """GBIF and biodiversity authority identifiers."""

    gbif_taxon_key: str | None = None
    gbif_usage_key: str | None = None
    wikidata: str | None = None
    eol: str | None = None
    dwc_scientific_name: str | None = None
    dwc_taxon_rank: str | None = None


class DarwinCoreOverlay(BaseModel):
    """Darwin Core descriptive overlay for a species record."""

    scientific_name: str
    scientific_name_authorship: str | None = None
    taxon_rank: str
    kingdom: str | None = None
    phylum: str | None = None
    class_: str | None = Field(default=None, alias="class")
    order: str | None = None
    family: str | None = None
    genus: str | None = None
    specific_epithet: str | None = None
    taxonomic_status: str = "accepted"
    nomenclatural_code: str = "ICZN"


class SpeciesRegistryEntry(BaseModel):
    """Canonical Species Registry record."""

    id: str
    stable_id: str
    status: ApprovalStatus = ApprovalStatus.PROPOSED
    species_uri: str
    scientific_name: str
    scientific_name_authorship: str | None = None
    taxonomic_rank: str
    gbif_taxon_key: str
    gbif_usage_key: str
    darwin_core: DarwinCoreOverlay
    external_identifiers: GbifExternalIdentifiers
    evidence: EvidenceOutputProfile
    provenance: ProvenanceRef
    source_registry_ref: str


class TaxonomicBackboneNode(BaseModel):
    """GBIF Taxonomic Backbone alignment node."""

    id: str
    gbif_usage_key: str
    scientific_name: str
    taxonomic_rank: str
    parent_usage_key: str | None = None
    status: ApprovalStatus = ApprovalStatus.APPROVED
    kingdom: str | None = None
    phylum: str | None = None
    class_: str | None = Field(default=None, alias="class")
    order: str | None = None
    family: str | None = None
    genus: str | None = None


class SpeciesObjectView(BaseModel):
    """End-to-end Reference Capability 2 species aggregate."""

    stable_id: str
    scientific_name: str
    common_name: str | None = None
    source_registry: SourceRegistryRef
    species_registry: SpeciesRegistryEntry
    taxonomic_backbone: list[TaxonomicBackboneNode] = Field(default_factory=list)
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
