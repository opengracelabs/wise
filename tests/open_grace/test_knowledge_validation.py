from open_grace_knowledge import KnowledgeSystem, validate_knowledge_cross_registry
from open_grace_knowledge.validation import KnowledgeValidationContext


def test_cross_registry_validates_seed_graph(tmp_path):
    system = KnowledgeSystem.create(tmp_path)
    system.seed_all()
    context = KnowledgeValidationContext(knowledge=system)

    graph = system.knowledge_graphs.get("wise.knowledge.graph.biodiversity-everglades")
    result = validate_knowledge_cross_registry(graph, context)

    assert result.valid, result.errors


def test_cross_registry_rejects_unknown_place(tmp_path):
    system = KnowledgeSystem.create(tmp_path)
    system.seed_all()
    context = KnowledgeValidationContext(knowledge=system)

    species = system.species.get("wise.species.panthera-leo")
    species.place_ids = ["wise.place.nonexistent"]
    result = validate_knowledge_cross_registry(species, context)

    assert not result.valid
    assert any("unknown place_id" in error for error in result.errors)


def test_entity_validation_warns_missing_wikidata_id(tmp_path):
    system = KnowledgeSystem.create(tmp_path)
    system.seed_all()

    entity = system.entities.get("wise.entity.everglades-nps")
    entity.reference_models = ["wikidata"]
    entity.external_ids = {}

    from open_grace_knowledge.validation import validate_knowledge_entry

    result = validate_knowledge_entry(entity)
    assert result.valid
    assert any("wikidata" in warning for warning in result.warnings)
