"""Knowledge registry record schemas."""

from open_grace_knowledge.schemas.collection import CollectionRegistryRecord
from open_grace_knowledge.schemas.entity import EntityRegistryRecord
from open_grace_knowledge.schemas.heritage import HeritageRegistryRecord
from open_grace_knowledge.schemas.knowledge_graph import KnowledgeGraphRegistryRecord
from open_grace_knowledge.schemas.media import MediaRegistryRecord
from open_grace_knowledge.schemas.place import PlaceRegistryRecord
from open_grace_knowledge.schemas.species import SpeciesRegistryRecord

__all__ = [
    "CollectionRegistryRecord",
    "EntityRegistryRecord",
    "HeritageRegistryRecord",
    "KnowledgeGraphRegistryRecord",
    "MediaRegistryRecord",
    "PlaceRegistryRecord",
    "SpeciesRegistryRecord",
]
