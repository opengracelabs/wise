"""Open Grace Knowledge Framework v1."""

from open_grace_knowledge.reference_models import (
    KNOWLEDGE_REFERENCE_MODELS,
    KNOWLEDGE_REFERENCE_MODEL_BY_SLUG,
    KnowledgeReferenceModelProfile,
)
from open_grace_knowledge.registries import (
    CollectionRegistry,
    EntityRegistry,
    HeritageRegistry,
    KnowledgeGraphRegistry,
    MediaRegistry,
    PlaceRegistry,
    SpeciesRegistry,
)
from open_grace_knowledge.registries.system import KnowledgeSystem
from open_grace_knowledge.reports import KnowledgeComplianceReport, generate_fleet_knowledge_reports
from open_grace_knowledge.schemas import (
    CollectionRegistryRecord,
    EntityRegistryRecord,
    HeritageRegistryRecord,
    KnowledgeGraphRegistryRecord,
    MediaRegistryRecord,
    PlaceRegistryRecord,
    SpeciesRegistryRecord,
)
from open_grace_knowledge.validation import (
    KnowledgeValidationContext,
    validate_knowledge_cross_registry,
    validate_knowledge_entry,
)

__version__ = "1.0.0"

__all__ = [
    "KNOWLEDGE_REFERENCE_MODELS",
    "KNOWLEDGE_REFERENCE_MODEL_BY_SLUG",
    "KnowledgeComplianceReport",
    "KnowledgeReferenceModelProfile",
    "KnowledgeSystem",
    "KnowledgeValidationContext",
    "CollectionRegistry",
    "CollectionRegistryRecord",
    "EntityRegistry",
    "EntityRegistryRecord",
    "HeritageRegistry",
    "HeritageRegistryRecord",
    "KnowledgeGraphRegistry",
    "KnowledgeGraphRegistryRecord",
    "MediaRegistry",
    "MediaRegistryRecord",
    "PlaceRegistry",
    "PlaceRegistryRecord",
    "SpeciesRegistry",
    "SpeciesRegistryRecord",
    "generate_fleet_knowledge_reports",
    "validate_knowledge_cross_registry",
    "validate_knowledge_entry",
]
