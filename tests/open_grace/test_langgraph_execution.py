from open_grace_governance.execution.langgraph import (
    build_governance_lifecycle_graph,
    run_lifecycle_to_stage,
)
from open_grace_governance.lifecycle import LifecycleStage


def test_lifecycle_graph_compiles():
    app = build_governance_lifecycle_graph()
    state = app.invoke(
        {
            "entry_id": "wise.agent.test",
            "registry_type": "agent",
            "lifecycle_stage": LifecycleStage.PROPOSAL.value,
            "transition_log": [],
            "halted": False,
        }
    )
    assert state["lifecycle_stage"] == LifecycleStage.RETIREMENT.value
    assert state["transition_log"]


def test_run_lifecycle_to_stage_stops_at_target():
    state = run_lifecycle_to_stage(
        entry_id="wise.agent.test",
        registry_type="agent",
        target=LifecycleStage.APPROVAL,
    )
    assert state["lifecycle_stage"] == LifecycleStage.APPROVAL.value
    assert not state["halted"]
