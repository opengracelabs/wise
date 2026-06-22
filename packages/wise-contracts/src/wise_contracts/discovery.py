"""Discovery Record contract (09-source-discovery-agent §6.2)."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from wise_contracts.common import ApprovalStatus, EvidenceOutputProfile, ProvenanceRef


class ExternalIdentifiers(BaseModel):
    """Cross-authority identifiers for a discovered asset."""

    unesco_whc: str | None = None
    ramsar: str | None = None
    unesco_mab: str | None = None
    wikidata: str | None = None
    geonames: str | None = None
    gbif_taxon_key: str | None = None
    gbif_usage_key: str | None = None
    eol: str | None = None
    provider_local: str | None = None


class DiscoveryRecord(BaseModel):
    """JSON-LD Discovery Record emitted by discovery-service."""

    model_config = {"populate_by_name": True}

    id: str
    stable_id: str
    status: ApprovalStatus = ApprovalStatus.PROPOSED
    type: str = Field(default="wise:DiscoveryRecord", alias="@type")
    context: str = Field(
        default="https://wise.example.org/context/discovery/v1",
        alias="@context",
    )

    title: str
    description: str | None = None
    source_registry_ref: str
    rights_uri: str
    ingestion_candidacy_score: float = Field(ge=0.0, le=1.0)
    external_identifiers: ExternalIdentifiers
    evidence: EvidenceOutputProfile
    provenance: ProvenanceRef
    discovered_at: datetime
    json_ld: dict | None = Field(default=None, description="Full JSON-LD payload")
