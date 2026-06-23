from open_grace_knowledge import KnowledgeSystem


def test_seed_all_seven_registries(tmp_path):
    system = KnowledgeSystem.create(tmp_path)
    seeded = system.seed_all()

    assert seeded["entities"] == 3
    assert seeded["places"] == 3
    assert seeded["species"] == 3
    assert seeded["heritage"] == 3
    assert seeded["collections"] == 3
    assert seeded["media"] == 3
    assert seeded["knowledge_graphs"] == 3

    summary = system.summary()
    assert summary["entities"] == 3
    assert summary["knowledge_graphs"] == 3


def test_get_by_id_resolves_entity(tmp_path):
    system = KnowledgeSystem.create(tmp_path)
    system.seed_all()

    record = system.get_by_id("wise.entity.unesco")
    assert record is not None
    assert record.display_name == "UNESCO"
    assert record.external_ids["wikidata"] == "Q7809"


def test_place_has_postgis_backing_store(tmp_path):
    system = KnowledgeSystem.create(tmp_path)
    system.seed_all()

    place = system.places.get("wise.place.everglades-national-park")
    store_kinds = {store.store.value for store in place.backing_stores}
    assert "postgis" in store_kinds
    assert place.geometry_ref is not None
