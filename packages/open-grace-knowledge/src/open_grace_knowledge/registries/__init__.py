"""Knowledge framework registries."""

from __future__ import annotations

from pathlib import Path

from open_grace_knowledge.registries.base import KnowledgeRegistry
from open_grace_knowledge.schemas import (
    CollectionRegistryRecord,
    EntityRegistryRecord,
    HeritageRegistryRecord,
    KnowledgeGraphRegistryRecord,
    MediaRegistryRecord,
    PlaceRegistryRecord,
    SpeciesRegistryRecord,
)


class EntityRegistry(KnowledgeRegistry[EntityRegistryRecord]):
    def __init__(self, store_path: Path | None = None) -> None:
        default = Path(__file__).resolve().parents[1] / "data" / "entity_registry.json"
        super().__init__(
            store_path=store_path or default,
            model=EntityRegistryRecord,
            id_field="entity_id",
            seed_filename="entity_registry.yaml",
            seed_key="entities",
        )


class PlaceRegistry(KnowledgeRegistry[PlaceRegistryRecord]):
    def __init__(self, store_path: Path | None = None) -> None:
        default = Path(__file__).resolve().parents[1] / "data" / "place_registry.json"
        super().__init__(
            store_path=store_path or default,
            model=PlaceRegistryRecord,
            id_field="place_id",
            seed_filename="place_registry.yaml",
            seed_key="places",
        )


class SpeciesRegistry(KnowledgeRegistry[SpeciesRegistryRecord]):
    def __init__(self, store_path: Path | None = None) -> None:
        default = Path(__file__).resolve().parents[1] / "data" / "species_registry.json"
        super().__init__(
            store_path=store_path or default,
            model=SpeciesRegistryRecord,
            id_field="species_id",
            seed_filename="species_registry.yaml",
            seed_key="species",
        )


class HeritageRegistry(KnowledgeRegistry[HeritageRegistryRecord]):
    def __init__(self, store_path: Path | None = None) -> None:
        default = Path(__file__).resolve().parents[1] / "data" / "heritage_registry.json"
        super().__init__(
            store_path=store_path or default,
            model=HeritageRegistryRecord,
            id_field="heritage_id",
            seed_filename="heritage_registry.yaml",
            seed_key="heritage",
        )


class CollectionRegistry(KnowledgeRegistry[CollectionRegistryRecord]):
    def __init__(self, store_path: Path | None = None) -> None:
        default = Path(__file__).resolve().parents[1] / "data" / "collection_registry.json"
        super().__init__(
            store_path=store_path or default,
            model=CollectionRegistryRecord,
            id_field="collection_id",
            seed_filename="collection_registry.yaml",
            seed_key="collections",
        )


class MediaRegistry(KnowledgeRegistry[MediaRegistryRecord]):
    def __init__(self, store_path: Path | None = None) -> None:
        default = Path(__file__).resolve().parents[1] / "data" / "media_registry.json"
        super().__init__(
            store_path=store_path or default,
            model=MediaRegistryRecord,
            id_field="media_id",
            seed_filename="media_registry.yaml",
            seed_key="media",
        )


class KnowledgeGraphRegistry(KnowledgeRegistry[KnowledgeGraphRegistryRecord]):
    def __init__(self, store_path: Path | None = None) -> None:
        default = Path(__file__).resolve().parents[1] / "data" / "knowledge_graph_registry.json"
        super().__init__(
            store_path=store_path or default,
            model=KnowledgeGraphRegistryRecord,
            id_field="graph_id",
            seed_filename="knowledge_graph_registry.yaml",
            seed_key="knowledge_graphs",
        )
