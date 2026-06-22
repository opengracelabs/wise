"""Knowledge Graph contracts (12-knowledge-graph-agent §6)."""

from __future__ import annotations

from pydantic import BaseModel, Field

from wise_contracts.common import ApprovalStatus, EvidenceOutputProfile


class ExternalLink(BaseModel):
    """External authority link proposal (12-knowledge-graph-agent §6.1)."""

    id: str
    status: ApprovalStatus = ApprovalStatus.PROPOSED
    external_authority: str
    external_identifier: str
    link_type: str = "sameAs"
    evidence: EvidenceOutputProfile


class GraphEntity(BaseModel):
    """Canonical graph entity placement."""

    id: str
    entity_uri: str
    stable_id: str
    status: ApprovalStatus = ApprovalStatus.PROPOSED
    label: str
    entity_type: str
    entity_assertion_id: str
    external_links: list[ExternalLink] = Field(default_factory=list)
    relationships: list[dict[str, str]] = Field(default_factory=list)
