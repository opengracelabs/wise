"""Shared schema primitives for knowledge registries."""

from __future__ import annotations

import re
from enum import StrEnum

from pydantic import BaseModel, Field

WISE_ENTITY_ID = re.compile(r"^wise\.entity\.[a-z0-9]+(?:-[a-z0-9]+)*$")
WISE_PLACE_ID = re.compile(r"^wise\.place\.[a-z0-9]+(?:-[a-z0-9]+)*$")
WISE_SPECIES_ID = re.compile(r"^wise\.species\.[a-z0-9]+(?:-[a-z0-9]+)*$")
WISE_HERITAGE_ID = re.compile(r"^wise\.heritage\.[a-z0-9]+(?:-[a-z0-9]+)*$")
WISE_COLLECTION_ID = re.compile(r"^wise\.collection\.[a-z0-9]+(?:-[a-z0-9]+)*$")
WISE_MEDIA_ID = re.compile(r"^wise\.media\.[a-z0-9]+(?:-[a-z0-9]+)*$")
WISE_KNOWLEDGE_GRAPH_ID = re.compile(r"^wise\.knowledge\.graph\.[a-z0-9]+(?:-[a-z0-9]+)*$")


class BackingStoreKind(StrEnum):
    POSTGRESQL = "postgresql"
    POSTGIS = "postgis"
    PGVECTOR = "pgvector"
    OPENSEARCH = "opensearch"
    JSON_FILE = "json_file"


class BackingStoreMetadata(BaseModel):
    """Declared backing store for a registry record (v1 metadata only)."""

    store: BackingStoreKind
    schema_ref: str | None = None
    table_or_index: str | None = None
    notes: str | None = None


class ExternalIdentifierMap(BaseModel):
    """External authority identifiers keyed by reference model slug."""

    identifiers: dict[str, str] = Field(default_factory=dict)
