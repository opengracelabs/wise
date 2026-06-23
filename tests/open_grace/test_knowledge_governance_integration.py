from open_grace_governance.system import GovernanceSystem


def test_governance_system_knowledge_seed_and_validate(tmp_path):
    system = GovernanceSystem.create(tmp_path)
    seeded = system.seed_all()

    assert seeded["entities"] == 3
    assert seeded["knowledge_graphs"] == 3

    result = system.validate_knowledge_entity("wise.entity.unesco")
    assert result.valid, result.errors

    result = system.validate_knowledge_entity("wise.knowledge.graph.heritage-venice")
    assert result.valid, result.errors


def test_governance_knowledge_reports_with_agent_hooks(tmp_path):
    system = GovernanceSystem.create(tmp_path)
    system.seed_all()

    reports = system.knowledge_reports()
    assert len(reports) == 21
    assert all(report.validation_passed for report in reports)

    summary = system.summary()
    assert summary["entities"] == 3
    assert summary["places"] == 3
