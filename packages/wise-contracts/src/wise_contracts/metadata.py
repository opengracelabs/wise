"""Knowledge Modeling contracts (10-metadata-agent §7)."""

from __future__ import annotations

from pydantic import BaseModel, Field

from wise_contracts.common import ApprovalStatus, EvidenceOutputProfile, ProvenanceRef


class AuthorityLink(BaseModel):
    """Proposed external authority match."""

    registry: str
    identifier: str
    link_type: str = "exactMatch"
    confidence: float = Field(ge=0.0, le=1.0)
    method: str


class MetadataRecord(BaseModel):
    """Normalized metadata record (10-metadata-agent §7.1)."""

    id: str
    stable_id: str
    status: ApprovalStatus = ApprovalStatus.PROPOSED
    source_schema: str
    source_schema_version: str
    preserved_object_ark: str
    title: str
    description: str | None = None
    language: str = "en"
    rights_uri: str
    field_mappings: dict[str, str] = Field(default_factory=dict)
    original_literals: dict[str, str] = Field(default_factory=dict)
    provenance: ProvenanceRef


class EntityAssertion(BaseModel):
    """RDF entity assertion candidate (10-metadata-agent §7.2)."""

    id: str
    status: ApprovalStatus = ApprovalStatus.PROPOSED
    entity_uri: str
    entity_type: str
    pref_label: str
    alt_labels: list[str] = Field(default_factory=list)
    descriptive_overlay: dict[str, str] = Field(default_factory=dict)
    authority_links: list[AuthorityLink] = Field(default_factory=list)
    geographic_anchor: dict | None = None
    temporal_bounds: dict | None = None
    rights_uri: str
    evidence: EvidenceOutputProfile
    provenance: ProvenanceRef
    metadata_record_id: str
    rdf_triples: list[dict[str, str]] = Field(default_factory=list)
