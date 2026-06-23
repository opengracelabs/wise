"""Reference models informing Open Grace Agent Runtime v2 design."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeReferenceModel:
    slug: str
    display_name: str
    runtime_use: str


RUNTIME_REFERENCE_MODELS: tuple[RuntimeReferenceModel, ...] = (
    RuntimeReferenceModel(
        slug="unesco",
        display_name="UNESCO",
        runtime_use="Heritage stewardship and covenant-aware execution context",
    ),
    RuntimeReferenceModel(
        slug="wikidata",
        display_name="Wikidata",
        runtime_use="Entity authority validation for knowledge-linked agents",
    ),
    RuntimeReferenceModel(
        slug="gbif",
        display_name="GBIF",
        runtime_use="Biodiversity knowledge context and taxonomic validation",
    ),
    RuntimeReferenceModel(
        slug="nist-ai-rmf",
        display_name="NIST AI RMF",
        runtime_use="Risk gate alignment and mitigated-control verification",
    ),
    RuntimeReferenceModel(
        slug="iso-42001",
        display_name="ISO 42001",
        runtime_use="AI management lifecycle gates before execution",
    ),
    RuntimeReferenceModel(
        slug="langgraph",
        display_name="LangGraph",
        runtime_use="Execution graph infrastructure for gated agent runs",
    ),
)

RUNTIME_REFERENCE_MODEL_BY_SLUG = {model.slug: model for model in RUNTIME_REFERENCE_MODELS}
