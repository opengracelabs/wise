"""Metadata Agent enumerations aligned with architecture-v1.0."""

from __future__ import annotations

import enum


class SourceSchema(str, enum.Enum):
    """Registered upstream metadata schema identifiers."""

    UNESCO_WHC = "unesco_whc"
    WIKIDATA = "wikidata"
    WIKIMEDIA_COMMONS = "wikimedia_commons"
    OPENSTREETMAP = "openstreetmap"


class MappingTarget(str, enum.Enum):
    """Ontology layer for schema crosswalk targets."""

    CIDOC_CRM = "cidoc_crm"
    DUBLIN_CORE = "dublin_core"
    SKOS = "skos"
    DARWIN_CORE = "darwin_core"


class AssertionStatus(str, enum.Enum):
    """Steward gate status for proposals (no canonical graph writes)."""

    PROPOSED = "proposed"
    STEWARD_APPROVED = "steward_approved"
    STEWARD_REJECTED = "steward_rejected"


class ValidationStatus(str, enum.Enum):
    """Validation outcome for source, rights, and schema checks."""

    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"


class ValidationDomain(str, enum.Enum):
    """Validation check category."""

    SOURCE = "source"
    RIGHTS = "rights"
    SCHEMA_CIDOC = "schema_cidoc"
    SCHEMA_DC = "schema_dc"
    SCHEMA_DWC = "schema_dwc"


class ModelingEventType(str, enum.Enum):
    """Modeling-layer provenance event types."""

    NORMALIZE = "normalize"
    MAP = "map"
    VALIDATE = "validate"
    AUTHORITY_PROPOSE = "authority_propose"
    STEWARD_APPROVE = "steward_approve"
    STEWARD_REJECT = "steward_reject"


class AuthorityEntityType(str, enum.Enum):
    """Authority reconciliation entity categories."""

    PLACE = "place"
    SPECIES = "species"
    PERSON = "person"
    ORGANIZATION = "organization"


class AuthorityMatchMethod(str, enum.Enum):
    """Authority match derivation method."""

    EXACT = "exact"
    FUZZY = "fuzzy"
    COORDINATE_PROXIMITY = "coordinate_proximity"
    TAXONOMIC_SYNONYM = "taxonomic_synonym"


class MappingRunStatus(str, enum.Enum):
    """Mapping pipeline execution status."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
