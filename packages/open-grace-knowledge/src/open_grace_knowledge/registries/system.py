"""Knowledge system coordinator."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from open_grace_knowledge.registries import (
    CollectionRegistry,
    EntityRegistry,
    HeritageRegistry,
    KnowledgeGraphRegistry,
    MediaRegistry,
    PlaceRegistry,
    SpeciesRegistry,
)


@dataclass
class KnowledgeSystem:
    """Open Grace Knowledge Framework v1 — seven governed registries."""

    entities: EntityRegistry
    places: PlaceRegistry
    species: SpeciesRegistry
    heritage: HeritageRegistry
    collections: CollectionRegistry
    media: MediaRegistry
    knowledge_graphs: KnowledgeGraphRegistry

    @classmethod
    def create(cls, root: Path | None = None) -> KnowledgeSystem:
        base = root or Path.cwd() / ".open-grace-knowledge"
        base.mkdir(parents=True, exist_ok=True)
        return cls(
            entities=EntityRegistry(base / "entity_registry.json"),
            places=PlaceRegistry(base / "place_registry.json"),
            species=SpeciesRegistry(base / "species_registry.json"),
            heritage=HeritageRegistry(base / "heritage_registry.json"),
            collections=CollectionRegistry(base / "collection_registry.json"),
            media=MediaRegistry(base / "media_registry.json"),
            knowledge_graphs=KnowledgeGraphRegistry(base / "knowledge_graph_registry.json"),
        )

    def seed_all(self) -> dict[str, int]:
        return {
            "entities": self.entities.seed_from_yaml(),
            "places": self.places.seed_from_yaml(),
            "species": self.species.seed_from_yaml(),
            "heritage": self.heritage.seed_from_yaml(),
            "collections": self.collections.seed_from_yaml(),
            "media": self.media.seed_from_yaml(),
            "knowledge_graphs": self.knowledge_graphs.seed_from_yaml(),
        }

    def summary(self) -> dict[str, int]:
        return {
            "entities": len(self.entities.list()),
            "places": len(self.places.list()),
            "species": len(self.species.list()),
            "heritage": len(self.heritage.list()),
            "collections": len(self.collections.list()),
            "media": len(self.media.list()),
            "knowledge_graphs": len(self.knowledge_graphs.list()),
        }

    def get_by_id(self, entry_id: str):
        if entry_id.startswith("wise.entity."):
            return self.entities.get(entry_id)
        if entry_id.startswith("wise.place."):
            return self.places.get(entry_id)
        if entry_id.startswith("wise.species."):
            return self.species.get(entry_id)
        if entry_id.startswith("wise.heritage."):
            return self.heritage.get(entry_id)
        if entry_id.startswith("wise.collection."):
            return self.collections.get(entry_id)
        if entry_id.startswith("wise.media."):
            return self.media.get(entry_id)
        if entry_id.startswith("wise.knowledge.graph."):
            return self.knowledge_graphs.get(entry_id)
        return None
