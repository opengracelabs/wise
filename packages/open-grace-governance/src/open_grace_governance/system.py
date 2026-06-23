"""Governance system coordinator (lazy imports to avoid package cycles)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from open_grace_governance.lifecycle import LifecycleStage
from open_grace_governance.validation import ValidationResult

if TYPE_CHECKING:
    from open_grace_agent_registry import (
        AgentRegistry,
        CapabilityRegistry,
        ModelRegistry,
        NatureCultureAgentRegistry,
    )
    from open_grace_audit import AuditRegistry
    from open_grace_benchmarking import BenchmarkRegistry
    from open_grace_governance.capabilities import CapabilityFrameworkRegistry
    from open_grace_governance.capabilities.reports import CapabilityComplianceReport
    from open_grace_governance.registries import RiskRegistry, StandardsRegistry
    from open_grace_governance.schemas import AgentRegistryRecord
    from open_grace_knowledge import KnowledgeSystem
    from open_grace_knowledge.reports import KnowledgeComplianceReport
    from open_grace_observability import ObservabilitySystem
    from open_grace_observability.reports import ObservabilityComplianceReport
    from open_grace_observability.schemas import AgentExecutionMetric
    from open_grace_runtime.system import AgentRunResult, RuntimeSystem


@dataclass
class GovernanceSystem:
    """Open Grace Agent Governance System v1 — registries and capability framework."""

    agents: AgentRegistry
    capabilities: CapabilityRegistry
    capability_framework: CapabilityFrameworkRegistry
    standards: StandardsRegistry
    risks: RiskRegistry
    benchmarks: BenchmarkRegistry
    audits: AuditRegistry
    models: ModelRegistry
    knowledge: KnowledgeSystem
    observability: ObservabilitySystem
    nature_culture: NatureCultureAgentRegistry

    @classmethod
    def create(cls, root: Path | None = None) -> GovernanceSystem:
        from open_grace_agent_registry import (
            AgentRegistry,
            CapabilityRegistry,
            ModelRegistry,
            NatureCultureAgentRegistry,
        )
        from open_grace_audit import AuditRegistry
        from open_grace_benchmarking import BenchmarkRegistry
        from open_grace_governance.capabilities import CapabilityFrameworkRegistry
        from open_grace_governance.registries import RiskRegistry, StandardsRegistry
        from open_grace_knowledge import KnowledgeSystem
        from open_grace_observability import ObservabilitySystem

        base = root or Path.cwd() / ".open-grace-governance"
        base.mkdir(parents=True, exist_ok=True)
        knowledge_root = base / "knowledge"
        knowledge_root.mkdir(parents=True, exist_ok=True)
        observability_root = base / "observability"
        observability_root.mkdir(parents=True, exist_ok=True)
        return cls(
            agents=AgentRegistry(base / "agent_registry.json"),
            capabilities=CapabilityRegistry(base / "capability_registry.json"),
            capability_framework=CapabilityFrameworkRegistry(
                base / "capability_framework.json"
            ),
            standards=StandardsRegistry(base / "standards_registry.json"),
            risks=RiskRegistry(base / "risk_registry.json"),
            benchmarks=BenchmarkRegistry(base / "benchmark_registry.json"),
            audits=AuditRegistry(base / "audit_registry.json"),
            models=ModelRegistry(base / "model_registry.json"),
            knowledge=KnowledgeSystem.create(knowledge_root),
            observability=ObservabilitySystem.create(observability_root),
            nature_culture=NatureCultureAgentRegistry(base / "nature_culture_agents.json"),
        )

    def seed_all(self) -> dict[str, int]:
        return {
            "agents": self.agents.import_canonical_manifest(),
            "capabilities": self.capabilities.import_canonical_manifest(),
            "capability_classes": self.capability_framework.seed_from_yaml(),
            "standards": self.standards.seed_from_yaml(),
            "risks": self.risks.seed_from_yaml(),
            "benchmarks": self.benchmarks.seed_from_yaml(),
            "models": self.models.seed_from_yaml(),
            "audits": 0,
            **self.knowledge.seed_all(),
            **self.observability.seed_all(),
        }

    def summary(self) -> dict[str, int]:
        return {
            "agents": len(self.agents.list()),
            "capabilities": len(self.capabilities.list()),
            "capability_classes": len(self.capability_framework.list()),
            "standards": len(self.standards.list()),
            "risks": len(self.risks.list()),
            "benchmarks": len(self.benchmarks.list()),
            "audits": len(self.audits.list()),
            "models": len(self.models.list()),
            "nature_culture_agents": len(self.nature_culture.list()),
            **self.knowledge.summary(),
            **self.observability.summary(),
        }

    def capability_validation_context(self):
        from open_grace_governance.capabilities.validation import CapabilityValidationContext

        return CapabilityValidationContext(
            benchmarks=self.benchmarks,
            models=self.models,
            standards=self.standards,
            risks=self.risks,
        )

    def validate_agent_approval(self, agent_id: str) -> ValidationResult:
        """Ensure linked capability classes pass cross-registry validation."""
        from open_grace_governance.capabilities.validation import validate_capability_framework

        if self.agents.get(agent_id) is None:
            return ValidationResult(valid=False, errors=[f"unknown agent: {agent_id}"])

        class_ids = self.capability_framework.bindings_for_agent(agent_id)
        if not class_ids:
            return ValidationResult(
                valid=True,
                warnings=[f"no capability class bindings for {agent_id}"],
            )

        context = self.capability_validation_context()
        errors: list[str] = []
        warnings: list[str] = []

        for class_id in class_ids:
            record = self.capability_framework.get(class_id)
            if record is None:
                errors.append(f"unknown capability class binding: {class_id}")
                continue
            result = validate_capability_framework(record, context)
            if not result.valid:
                errors.extend(
                    f"{class_id}: {message}" for message in result.errors
                )
            warnings.extend(
                f"{class_id}: {message}" for message in result.warnings
            )

        return ValidationResult(valid=not errors, errors=errors, warnings=warnings)

    def advance_agent(
        self,
        agent_id: str,
        target: LifecycleStage,
        *,
        steward_actor: str | None = None,
    ) -> AgentRegistryRecord:
        if target == LifecycleStage.APPROVAL:
            approval = self.validate_agent_approval(agent_id)
            if not approval.valid:
                raise ValueError(
                    "capability validation failed before approval: "
                    + "; ".join(approval.errors)
                )
        return self.agents.advance(agent_id, target, steward_actor=steward_actor)

    def capability_reports(
        self,
        observed_values_by_capability: dict[str, dict[str, float]] | None = None,
    ) -> list[CapabilityComplianceReport]:
        from open_grace_governance.capabilities.reports import generate_fleet_capability_reports

        return generate_fleet_capability_reports(
            self.capability_framework,
            context=self.capability_validation_context(),
            benchmark_registry=self.benchmarks,
            observed_values_by_capability=observed_values_by_capability,
        )

    def knowledge_validation_context(self):
        from open_grace_knowledge.validation import KnowledgeValidationContext

        return KnowledgeValidationContext(
            knowledge=self.knowledge,
            agents=self.agents,
            capabilities=self.capabilities,
            audits=self.audits,
            benchmarks=self.benchmarks,
        )

    def validate_knowledge_entity(self, entity_id: str) -> ValidationResult:
        """Validate a knowledge registry entry with cross-registry checks."""
        from open_grace_knowledge.validation import validate_knowledge_cross_registry

        record = self.knowledge.get_by_id(entity_id)
        if record is None:
            return ValidationResult(valid=False, errors=[f"unknown knowledge entry: {entity_id}"])

        return validate_knowledge_cross_registry(
            record,
            context=self.knowledge_validation_context(),
        )

    def knowledge_reports(self) -> list[KnowledgeComplianceReport]:
        from open_grace_knowledge.reports import generate_fleet_knowledge_reports

        return generate_fleet_knowledge_reports(
            self.knowledge,
            context=self.knowledge_validation_context(),
        )

    def metric_validation_context(self):
        from open_grace_observability.validation import MetricValidationContext

        return MetricValidationContext(
            observability=self.observability,
            agents=self.agents,
            capabilities=self.capabilities,
            benchmarks=self.benchmarks,
            audits=self.audits,
        )

    def validate_metric_context(self, metric_id: str) -> ValidationResult:
        """Validate a metric record with cross-registry checks."""
        from open_grace_observability.validation import validate_metric_cross_registry

        record = self.observability.get_by_id(metric_id)
        if record is None:
            return ValidationResult(valid=False, errors=[f"unknown metric: {metric_id}"])

        return validate_metric_cross_registry(
            record,
            context=self.metric_validation_context(),
        )

    def record_agent_metric(
        self,
        *,
        agent_id: str,
        metric_kind: str,
        value: float,
        unit: str,
        display_name: str | None = None,
        execution_id: str | None = None,
        trace_id: str | None = None,
        span_id: str | None = None,
        steward_actor: str | None = None,
    ) -> AgentExecutionMetric:
        if self.agents.get(agent_id) is None:
            raise ValueError(f"unknown agent: {agent_id}")
        return self.observability.record_agent_execution(
            agent_id=agent_id,
            metric_kind=metric_kind,
            value=value,
            unit=unit,
            display_name=display_name,
            execution_id=execution_id,
            trace_id=trace_id,
            span_id=span_id,
            steward_actor=steward_actor,
        )

    def observability_reports(self) -> list[ObservabilityComplianceReport]:
        from open_grace_observability.reports import generate_fleet_observability_reports

        return generate_fleet_observability_reports(
            self.observability,
            context=self.metric_validation_context(),
        )

    def register_nature_culture_agents(self) -> int:
        """Register Nature & Culture agent role bindings and audit hooks."""
        return self.nature_culture.register_from_seed(self)

    def validate_nature_culture_registration(self) -> ValidationResult:
        """Cross-registry validation for Nature & Culture agent bindings."""
        return self.nature_culture.validate_cross_registry(self)

    @property
    def runtime(self) -> RuntimeSystem:
        """Lazy-loaded Open Grace Agent Runtime v2."""
        cached = getattr(self, "_runtime_system", None)
        if cached is not None:
            return cached
        from open_grace_runtime import RuntimeSystem

        root = self.agents._store.path.parent / "runtime"
        cached = RuntimeSystem.create(self, root=root)
        self._runtime_system = cached
        return cached

    def run_agent(
        self,
        agent_id: str,
        *,
        observed_values: dict[str, float] | None = None,
        preferred_model_id: str | None = None,
        steward_actor: str | None = None,
        run_id: str | None = None,
    ) -> AgentRunResult:
        """Execute an agent through the gated LangGraph runtime flow."""
        return self.runtime.run_agent(
            agent_id,
            observed_values=observed_values,
            preferred_model_id=preferred_model_id,
            steward_actor=steward_actor,
            run_id=run_id,
        )
