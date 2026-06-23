from open_grace_governance.capabilities import CapabilityClass, CapabilityFrameworkRegistry
from open_grace_governance.schemas.capability_framework import CAPABILITY_CLASS_IDS


def test_seed_eight_capability_classes(tmp_path):
    registry = CapabilityFrameworkRegistry(tmp_path / "framework.json")
    count = registry.seed_from_yaml()

    assert count == 8
    classes = {record.capability_class for record in registry.list()}
    assert classes == set(CapabilityClass)
    assert CAPABILITY_CLASS_IDS[CapabilityClass.RESEARCH] == "wise.capability.class.research"


def test_agent_bindings_resolve(tmp_path):
    registry = CapabilityFrameworkRegistry(tmp_path / "framework.json")
    registry.seed_from_yaml()

    translation_classes = registry.bindings_for_agent("wise.agent.translation")
    assert translation_classes == ["wise.capability.class.translation"]

    benchmark_classes = registry.bindings_for_agent("wise.agent.benchmark")
    assert set(benchmark_classes) == {
        "wise.capability.class.coding",
        "wise.capability.class.research",
    }
