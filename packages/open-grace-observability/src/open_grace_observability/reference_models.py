"""Observability-domain reference model profiles."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ObservabilityReferenceModelProfile:
    slug: str
    display_name: str
    domain: str
    observability_use: str


OBSERVABILITY_REFERENCE_MODELS: tuple[ObservabilityReferenceModelProfile, ...] = (
    ObservabilityReferenceModelProfile(
        slug="opentelemetry",
        display_name="OpenTelemetry",
        domain="distributed_tracing",
        observability_use="Trace context propagation, span attributes, and metric correlation",
    ),
    ObservabilityReferenceModelProfile(
        slug="prometheus",
        display_name="Prometheus",
        domain="metrics",
        observability_use="Counter/gauge/histogram exposition and alerting label schemas",
    ),
    ObservabilityReferenceModelProfile(
        slug="grafana",
        display_name="Grafana",
        domain="visualization",
        observability_use="Dashboard panels, datasource bindings, and SLO views",
    ),
    ObservabilityReferenceModelProfile(
        slug="loki",
        display_name="Loki",
        domain="log_aggregation",
        observability_use="Log stream labels, query schemas, and audit trail indexing",
    ),
    ObservabilityReferenceModelProfile(
        slug="langsmith",
        display_name="LangSmith",
        domain="llm_observability",
        observability_use="Agent run tracing, prompt/response logging, and evaluation hooks",
    ),
    ObservabilityReferenceModelProfile(
        slug="nist-ai-rmf",
        display_name="NIST AI RMF",
        domain="ai_risk_management",
        observability_use="Risk signal metrics, impact monitoring, and governance telemetry",
    ),
    ObservabilityReferenceModelProfile(
        slug="iso-42001",
        display_name="ISO 42001",
        domain="ai_management_system",
        observability_use="Continual improvement metrics and management review evidence",
    ),
)

OBSERVABILITY_REFERENCE_MODEL_BY_SLUG = {
    profile.slug: profile for profile in OBSERVABILITY_REFERENCE_MODELS
}
