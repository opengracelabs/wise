"""Knowledge graph registry schema."""

from __future__ import annotations

from pydantic import Field, field_validator

from open_grace_governance.schemas.common import GovernedRecord
from open_grace_knowledge.schemas.common import (
    BackingStoreMetadata,
    WISE_KNOWLEDGE_GRAPH_ID,
)


class KnowledgeGraphRegistryRecord(GovernedRecord):
    graph_id: str
    display_name: str = Field(min_length=1)
    graph_type: str = Field(min_length=1)
    description: str | None = None
    node_registry_refs: dict[str, list[str]] = Field(default_factory=dict)
    skos_concept_scheme: str | None = None
    opensearch_index: str | None = None
    steward_agent_id: str | None = None
    capability_id: str | None = None
    audit_requirement_ids: list[str] = Field(default_factory=list)
    benchmark_ids: list[str] = Field(default_factory=list)
    backing_stores: list[BackingStoreMetadata] = Field(min_length=1)

    @field_validator("graph_id")
    @classmethod
    def validate_graph_id(cls, value: str) -> str:
        if not WISE_KNOWLEDGE_GRAPH_ID.match(value):
            raise ValueError("graph_id must match wise.knowledge.graph.{slug}")
        return value
