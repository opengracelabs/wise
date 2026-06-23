"""Pre-execution gate validators for Open Grace Agent Runtime v2."""

from __future__ import annotations

from typing import TYPE_CHECKING

from open_grace_governance.lifecycle import LifecycleStage
from open_grace_runtime.schemas import GateResult

if TYPE_CHECKING:
    from open_grace_agent_registry import AgentRegistry
    from open_grace_benchmarking import BenchmarkRegistry
    from open_grace_governance.capabilities.registry import CapabilityFrameworkRegistry
    from open_grace_governance.registries import RiskRegistry
    from open_grace_governance.system import GovernanceSystem
    from open_grace_runtime.stores import BenchmarkRunRecordStore

_APPROVED_AGENT_STAGES = frozenset({LifecycleStage.APPROVAL, LifecycleStage.PUBLICATION})

_KNOWLEDGE_LINK_GETTERS = {
    "entity": "entities",
    "place": "places",
    "species": "species",
    "heritage": "heritage",
    "collection": "collections",
    "media": "media",
    "knowledge_graph": "knowledge_graphs",
}


def validate_agent_registry_gate(agents: AgentRegistry, agent_id: str) -> GateResult:
    """Gate 1: agent must exist and be at APPROVAL or PUBLICATION."""
    record = agents.get(agent_id)
    if record is None:
        return GateResult(
            gate_name="agent_registry",
            passed=False,
            errors=[f"unknown agent: {agent_id}"],
        )
    if record.lifecycle_stage not in _APPROVED_AGENT_STAGES:
        return GateResult(
            gate_name="agent_registry",
            passed=False,
            errors=[
                f"agent {agent_id} not approved for execution "
                f"(stage={record.lifecycle_stage.value})"
            ],
        )
    return GateResult(gate_name="agent_registry", passed=True)


def validate_capability_gate(system: GovernanceSystem, agent_id: str) -> GateResult:
    """Gate 2: capability framework validation via GovernanceSystem."""
    result = system.validate_agent_approval(agent_id)
    if not result.valid:
        return GateResult(
            gate_name="capability_validation",
            passed=False,
            errors=list(result.errors),
        )
    return GateResult(gate_name="capability_validation", passed=True)


def validate_risk_gate(
    capability_framework: CapabilityFrameworkRegistry,
    risks: RiskRegistry,
    agent_id: str,
) -> GateResult:
    """Gate 3: linked risks must be published and mitigated."""
    class_ids = capability_framework.bindings_for_agent(agent_id)
    errors: list[str] = []

    for class_id in class_ids:
        record = capability_framework.get(class_id)
        if record is None:
            errors.append(f"unknown capability class binding: {class_id}")
            continue
        for risk_id in record.risk_profile:
            risk = risks.get(risk_id)
            if risk is None:
                errors.append(f"unknown risk: {risk_id}")
            elif risk.lifecycle_stage != LifecycleStage.PUBLICATION:
                errors.append(f"risk not published: {risk_id}")
            elif not risk.mitigation.strip():
                errors.append(f"risk not mitigated: {risk_id}")

    return GateResult(
        gate_name="risk_validation",
        passed=not errors,
        errors=errors,
    )


def validate_benchmark_gate(
    capability_framework: CapabilityFrameworkRegistry,
    benchmarks: BenchmarkRegistry,
    agent_id: str,
    observed_values: dict[str, float],
    benchmark_runs: BenchmarkRunRecordStore,
) -> GateResult:
    """Gate 4: benchmark thresholds pass or a passing evaluation is recorded."""
    class_ids = capability_framework.bindings_for_agent(agent_id)
    errors: list[str] = []

    for class_id in class_ids:
        record = capability_framework.get(class_id)
        if record is None:
            errors.append(f"unknown capability class binding: {class_id}")
            continue

        unresolved: list[str] = []
        for benchmark_id in record.benchmark_set:
            if benchmark_runs.has_passing_evaluation(agent_id, benchmark_id):
                continue
            if benchmark_id not in observed_values:
                unresolved.append(f"missing observed value for: {benchmark_id}")
                continue
            bench = benchmarks.get(benchmark_id)
            if bench is None:
                unresolved.append(f"missing benchmark definition: {benchmark_id}")
                continue
            from open_grace_benchmarking import evaluate_benchmark

            evaluation = evaluate_benchmark(bench, observed_values[benchmark_id])
            if not evaluation.passed:
                unresolved.append(f"{benchmark_id}: {evaluation.reason}")

        if unresolved:
            errors.extend(f"{class_id}: {message}" for message in unresolved)
        elif not record.benchmark_set:
            errors.append(f"{class_id}: benchmark_set must not be empty")

    return GateResult(
        gate_name="benchmark_validation",
        passed=not errors,
        errors=errors,
    )


def validate_knowledge_context(system: GovernanceSystem, agent_id: str) -> GateResult:
    """Validate knowledge links when the agent has Nature & Culture bindings."""
    record = system.nature_culture.get_by_agent(agent_id)
    if record is None or not record.knowledge_links:
        return GateResult(gate_name="knowledge_context", passed=True)

    errors: list[str] = []
    for registry_key, entry_ids in record.knowledge_links.items():
        getter_name = _KNOWLEDGE_LINK_GETTERS.get(registry_key)
        if getter_name is None:
            errors.append(f"unknown knowledge link key: {registry_key}")
            continue
        registry = getattr(system.knowledge, getter_name)
        for entry_id in entry_ids:
            entry = registry.get(entry_id)
            if entry is None:
                errors.append(f"unknown {registry_key} ref: {entry_id}")
                continue
            validation = system.validate_knowledge_entity(entry_id)
            if not validation.valid:
                errors.extend(
                    f"{entry_id}: {message}" for message in validation.errors
                )

    return GateResult(
        gate_name="knowledge_context",
        passed=not errors,
        errors=errors,
    )


def select_approved_model(
    capability_framework: CapabilityFrameworkRegistry,
    agent_id: str,
    *,
    preferred_model_id: str | None = None,
) -> tuple[str | None, list[str]]:
    """Pick a model from approved_models on bound capability classes."""
    class_ids = capability_framework.bindings_for_agent(agent_id)
    approved: list[str] = []
    for class_id in class_ids:
        record = capability_framework.get(class_id)
        if record is None:
            continue
        approved.extend(record.approved_models)

    if not approved:
        return None, class_ids

    unique = list(dict.fromkeys(approved))
    if preferred_model_id is not None:
        if preferred_model_id in unique:
            return preferred_model_id, class_ids
        return None, class_ids
    return unique[0], class_ids
