"""LangGraph execution infrastructure for governance lifecycle only.

No agent reasoning, model calls, or canonical writes — infrastructure wiring
for stage transitions and audit correlation.
"""

from __future__ import annotations

from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from open_grace_governance.lifecycle import LifecycleStage, advance_lifecycle


class GovernanceLifecycleState(TypedDict):
    entry_id: str
    registry_type: str
    lifecycle_stage: str
    transition_log: list[str]
    halted: bool


def _stage_node(stage: LifecycleStage):
    def node(state: GovernanceLifecycleState) -> GovernanceLifecycleState:
        current = LifecycleStage(state["lifecycle_stage"])
        if current == stage:
            return state
        try:
            next_stage = advance_lifecycle(current, stage)
        except Exception as exc:  # noqa: BLE001 — surface in transition log
            log = list(state.get("transition_log", []))
            log.append(f"blocked:{stage.value}:{exc}")
            return {
                **state,
                "transition_log": log,
                "halted": True,
            }
        log = list(state.get("transition_log", []))
        log.append(f"{current.value}->{next_stage.value}")
        return {
            **state,
            "lifecycle_stage": next_stage.value,
            "transition_log": log,
            "halted": False,
        }

    return node


def build_governance_lifecycle_graph():
    """Compile a linear lifecycle graph: proposal through retirement."""
    graph = StateGraph(GovernanceLifecycleState)

    for stage in LifecycleStage:
        graph.add_node(stage.value, _stage_node(stage))

    ordered = list(LifecycleStage)
    graph.add_edge(START, ordered[0].value)
    for index in range(len(ordered) - 1):
        graph.add_edge(ordered[index].value, ordered[index + 1].value)
    graph.add_edge(ordered[-1].value, END)

    return graph.compile()


def run_lifecycle_to_stage(
    *,
    entry_id: str,
    registry_type: str,
    target: LifecycleStage,
) -> GovernanceLifecycleState:
    """Advance an entry along the forward lifecycle path up to target."""
    ordered = list(LifecycleStage)
    if target not in ordered:
        raise ValueError(f"unknown lifecycle stage: {target}")

    state: GovernanceLifecycleState = {
        "entry_id": entry_id,
        "registry_type": registry_type,
        "lifecycle_stage": LifecycleStage.PROPOSAL.value,
        "transition_log": [],
        "halted": False,
    }
    target_index = ordered.index(target)
    for index in range(target_index):
        current = LifecycleStage(state["lifecycle_stage"])
        nxt = ordered[index + 1]
        try:
            advanced = advance_lifecycle(current, nxt)
        except Exception as exc:  # noqa: BLE001
            state["transition_log"].append(f"blocked:{nxt.value}:{exc}")
            state["halted"] = True
            return state
        state["transition_log"].append(f"{current.value}->{advanced.value}")
        state["lifecycle_stage"] = advanced.value
    return state
