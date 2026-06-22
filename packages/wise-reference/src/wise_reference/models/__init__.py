"""Reference Capability 1 and 2 SQLAlchemy models."""

from wise_reference.models.discovery import DiscoveryRecord
from wise_reference.models.graph import ExternalLink, GraphEntity
from wise_reference.models.modeling import EntityAssertion, MetadataRecord
from wise_reference.models.preservation import PremisEvent, PreservationObject
from wise_reference.models.protected_area import ProtectedArea
from wise_reference.models.quality import QualityReview
from wise_reference.models.species import SpeciesRegistryEntry
from wise_reference.models.taxonomy import SpeciesBackboneLink, TaxonomicBackboneNode

__all__ = [
    "DiscoveryRecord",
    "EntityAssertion",
    "ExternalLink",
    "GraphEntity",
    "MetadataRecord",
    "PremisEvent",
    "PreservationObject",
    "ProtectedArea",
    "QualityReview",
    "SpeciesBackboneLink",
    "SpeciesRegistryEntry",
    "TaxonomicBackboneNode",
]
