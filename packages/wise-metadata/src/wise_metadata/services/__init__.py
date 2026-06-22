"""Metadata Agent v1 service modules."""

from wise_metadata.services.authority_proposer import propose_from_normalized, propose_place_authority
from wise_metadata.services.mapper import apply_schema_mappings
from wise_metadata.services.normalizer import normalize_metadata
from wise_metadata.services.pipeline import process_record, source_schema_for_canonical_name
from wise_metadata.services.rights_validator import validate_rights
from wise_metadata.services.source_validator import validate_source

__all__ = [
    "normalize_metadata",
    "apply_schema_mappings",
    "validate_source",
    "validate_rights",
    "propose_place_authority",
    "propose_from_normalized",
    "process_record",
    "source_schema_for_canonical_name",
]
