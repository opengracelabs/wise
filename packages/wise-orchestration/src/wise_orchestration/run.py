"""CLI entry point for RC1 orchestration."""

from __future__ import annotations

import argparse
import json
import sys

from langgraph.checkpoint.memory import MemorySaver

from wise_orchestration import build_rc1_graph, initial_state_for_stonehenge
from wise_orchestration.gates.approval import resume_with_approval
from wise_orchestration.state import PipelineStage


def _run_pipeline(*, auto_approve: bool, thread_id: str) -> dict:
    graph = build_rc1_graph(checkpointer=MemorySaver())
    config = {"configurable": {"thread_id": thread_id}}
    state = graph.invoke(initial_state_for_stonehenge(), config)

    stages = [
        PipelineStage.SOURCE_DISCOVERY.value,
        PipelineStage.PRESERVATION.value,
        PipelineStage.METADATA.value,
        PipelineStage.KNOWLEDGE_GRAPH.value,
        PipelineStage.QUALITY_REVIEW.value,
    ]

    for stage in stages:
        if state.get("current_stage") == PipelineStage.COMPLETE.value:
            break
        if state.get("current_stage") == PipelineStage.FAILED.value:
            break
        if not auto_approve:
            print(json.dumps(state.get("approval_gate"), indent=2))
            print("Pipeline paused at steward approval gate. Re-run with --auto-approve or resume via API.")
            return state

        state = resume_with_approval(
            graph,
            config,
            decision="approved",
            steward_id="cli-auto-steward",
        )

    return state


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Stonehenge RC1 LangGraph orchestration")
    parser.add_argument("--stable-id", default="stonehenge", help="Target stable_id (RC1)")
    parser.add_argument(
        "--auto-approve",
        action="store_true",
        help="Automatically approve all steward gates (dev/demo only)",
    )
    parser.add_argument("--thread-id", default="stonehenge-rc1-cli", help="LangGraph thread id")
    args = parser.parse_args(argv)

    if args.stable_id != "stonehenge":
        print(f"Only stonehenge RC1 is implemented; got {args.stable_id!r}", file=sys.stderr)
        return 1

    final = _run_pipeline(auto_approve=args.auto_approve, thread_id=args.thread_id)
    print(json.dumps({"current_stage": final.get("current_stage"), "provenance_chain": final.get("provenance_chain")}, indent=2))
    return 0 if final.get("current_stage") == PipelineStage.COMPLETE.value else 1


if __name__ == "__main__":
    raise SystemExit(main())
