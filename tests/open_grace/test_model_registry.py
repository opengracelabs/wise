from open_grace_agent_registry import ModelRegistry


def test_seed_model_registry(tmp_path):
    registry = ModelRegistry(tmp_path / "models.json")
    count = registry.seed_from_yaml()
    models = registry.list()

    assert count == 5
    assert registry.get("wise.model.claude-sonnet").council_role == "architecture"
    assert all(model.model_id.startswith("wise.model.") for model in models)
