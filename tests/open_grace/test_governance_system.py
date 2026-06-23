from open_grace_governance.system import GovernanceSystem


def test_governance_system_seed_and_summary(tmp_path):
    system = GovernanceSystem.create(tmp_path)
    seeded = system.seed_all()
    summary = system.summary()

    assert seeded["agents"] == 15
    assert seeded["capabilities"] == 12
    assert seeded["capability_classes"] == 8
    assert seeded["standards"] == 4
    assert seeded["risks"] == 5
    assert seeded["benchmarks"] == 13
    assert seeded["models"] == 5
    assert seeded["entities"] == 3
    assert seeded["knowledge_graphs"] == 3
    assert summary["agents"] == 15
    assert summary["capabilities"] == 12
    assert summary["capability_classes"] == 8
