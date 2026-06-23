import pytest

from open_grace_governance.system import GovernanceSystem

EXPECTED_ROLES = {
    "Research Agent": "wise.agent.standards",
    "Translation Agent": "wise.agent.translation",
    "Classification Agent": "wise.agent.metadata",
    "Extraction Agent": "wise.agent.source-discovery",
    "Analysis Agent": "wise.agent.knowledge-graph",
    "Preservation Agent": "wise.agent.preservation",
    "Publishing Agent": "wise.agent.publishing",
}

EXPECTED_CAPABILITY_CLASSES = {
    "wise.agent.standards": "wise.capability.class.research",
    "wise.agent.translation": "wise.capability.class.translation",
    "wise.agent.metadata": "wise.capability.class.classification",
    "wise.agent.source-discovery": "wise.capability.class.extraction",
    "wise.agent.knowledge-graph": "wise.capability.class.analysis",
    "wise.agent.preservation": "wise.capability.class.preservation",
    "wise.agent.publishing": "wise.capability.class.publishing",
}


@pytest.fixture
def seeded_system(tmp_path):
    system = GovernanceSystem.create(tmp_path)
    system.seed_all()
    system.register_nature_culture_agents()
    return system


def test_all_seven_nature_culture_agents_mapped_and_registered(tmp_path):
    system = GovernanceSystem.create(tmp_path)
    system.seed_all()
    count = system.register_nature_culture_agents()

    assert count == 7
    bindings = system.nature_culture.list()
    assert len(bindings) == 7

    by_name = {record.display_name: record for record in bindings}
    assert set(by_name) == set(EXPECTED_ROLES)

    for display_name, agent_id in EXPECTED_ROLES.items():
        record = by_name[display_name]
        assert record.agent_id == agent_id
        assert record.role_id.startswith("nature-culture.role.")


def test_nature_culture_capability_bindings_exist(seeded_system):
    for agent_id, capability_class_id in EXPECTED_CAPABILITY_CLASSES.items():
        record = seeded_system.nature_culture.get_by_agent(agent_id)
        assert record is not None
        assert record.capability_class_id == capability_class_id

        bound = seeded_system.capability_framework.bindings_for_agent(agent_id)
        assert capability_class_id in bound


def test_nature_culture_knowledge_links_valid(seeded_system):
    result = seeded_system.validate_nature_culture_registration()
    assert result.valid, result.errors

    for record in seeded_system.nature_culture.list():
        assert record.knowledge_links, f"{record.display_name} has no knowledge links"
        for registry_key, entry_ids in record.knowledge_links.items():
            assert entry_ids, f"{record.display_name}.{registry_key} is empty"


def test_nature_culture_benchmark_refs_valid(seeded_system):
    result = seeded_system.validate_nature_culture_registration()
    assert result.valid, result.errors

    for record in seeded_system.nature_culture.list():
        assert len(record.benchmark_ids) >= 2
        cap_class = seeded_system.capability_framework.get(record.capability_class_id)
        for benchmark_id in record.benchmark_ids:
            benchmark = seeded_system.benchmarks.get(benchmark_id)
            assert benchmark is not None
            assert benchmark_id in cap_class.benchmark_set


def test_nature_culture_audit_hooks_defined(seeded_system):
    result = seeded_system.validate_nature_culture_registration()
    assert result.valid, result.errors

    for record in seeded_system.nature_culture.list():
        assert len(record.audit_hook_ids) == 2
        assert len(record.audit_requirements) == 2
        for hook_id in record.audit_hook_ids:
            audit = seeded_system.audits.get(hook_id)
            assert audit is not None
            assert audit.subject_id == record.agent_id
            assert audit.subject_type == "agent"


def test_register_requires_canonical_agents_seeded(tmp_path):
    system = GovernanceSystem.create(tmp_path)
    with pytest.raises(ValueError, match="canonical agent not registered"):
        system.register_nature_culture_agents()


def test_validate_fails_before_registration(tmp_path):
    system = GovernanceSystem.create(tmp_path)
    system.seed_all()

    result = system.validate_nature_culture_registration()
    assert result.valid is False
    assert "no Nature & Culture agents registered" in result.errors[0]
