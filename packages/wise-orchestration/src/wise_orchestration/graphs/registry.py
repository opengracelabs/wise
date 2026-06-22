"""Phase 0 stub graphs for all 15 canonical agents."""

from __future__ import annotations

from collections.abc import Callable

from langgraph.graph import END, StateGraph

from wise_orchestration.graphs.approval import await_steward_approval
from wise_orchestration.nodes.legacy_phase0 import (
    CanonicalWriteForbiddenError,
    PipelineState,
    canonical_write_guard,
    governance_report,
    propose_output,
    route_after_approval,
)

GraphFactory = Callable[[], object]

READ_ONLY_GRAPH_IDS = frozenset({"standards", "benchmark"})


def _build_agent_graph(*, read_only: bool) -> StateGraph:
    graph = StateGraph(PipelineState)

    if read_only:
        graph.add_node("governance_report", governance_report)
        graph.set_entry_point("governance_report")
        graph.add_edge("governance_report", END)
        return graph

    graph.add_node("propose_output", propose_output)
    graph.add_node("await_steward_approval", await_steward_approval)
    graph.add_node("canonical_write", canonical_write_guard)

    graph.set_entry_point("propose_output")
    graph.add_edge("propose_output", "await_steward_approval")
    graph.add_conditional_edges(
        "await_steward_approval",
        route_after_approval,
        {
            "approved": "canonical_write",
            "rejected": END,
            "pending": "await_steward_approval",
        },
    )
    graph.add_edge("canonical_write", END)
    return graph


def _compile(read_only: bool):
    return _build_agent_graph(read_only=read_only).compile()


GRAPH_REGISTRY: dict[str, GraphFactory] = {
    "source-discovery": lambda: _compile(read_only=False),
    "metadata": lambda: _compile(read_only=False),
    "preservation": lambda: _compile(read_only=False),
    "knowledge-graph": lambda: _compile(read_only=False),
    "quality-review": lambda: _compile(read_only=False),
    "translation": lambda: _compile(read_only=False),
    "publishing": lambda: _compile(read_only=False),
    "education": lambda: _compile(read_only=False),
    "biodiversity-observatory": lambda: _compile(read_only=False),
    "climate-observatory": lambda: _compile(read_only=False),
    "heritage-observatory": lambda: _compile(read_only=False),
    "tourism-observatory": lambda: _compile(read_only=False),
    "language-observatory": lambda: _compile(read_only=False),
    "standards": lambda: _compile(read_only=True),
    "benchmark": lambda: _compile(read_only=True),
}


def get_compiled_graph(graph_id: str, *, checkpointer=None):
    if graph_id not in GRAPH_REGISTRY:
        raise KeyError(f"Unknown graph_id: {graph_id}")
    if graph_id in READ_ONLY_GRAPH_IDS:
        graph = _build_agent_graph(read_only=True)
        return graph.compile(checkpointer=checkpointer)
    graph = _build_agent_graph(read_only=False)
    return graph.compile(checkpointer=checkpointer)


def assert_graph_has_no_canonical_write_path(graph_id: str) -> None:
    """Governance agents must not expose canonical write nodes."""
    if graph_id not in READ_ONLY_GRAPH_IDS:
        return
    graph = _build_agent_graph(read_only=True)
    node_names = set(graph.nodes.keys())
    if "canonical_write" in node_names:
        raise CanonicalWriteForbiddenError(
            f"Read-only graph {graph_id} must not include canonical_write node"
        )
