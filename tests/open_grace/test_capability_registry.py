from open_grace_agent_registry import CapabilityRegistry


def test_import_canonical_capability_manifest(tmp_path):
    registry = CapabilityRegistry(tmp_path / "capabilities.json")
    count = registry.import_canonical_manifest()

    assert count == 12
    capabilities = registry.list()
    assert all(item.capability_id.startswith("wise.capability.") for item in capabilities)
    bindings = registry.bindings()
    assert bindings
    assert any(binding.role == "governance" for binding in bindings)
