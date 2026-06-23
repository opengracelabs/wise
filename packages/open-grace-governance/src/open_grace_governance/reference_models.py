"""Reference model profiles informing Open Grace governance design."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceModelProfile:
    """Institutional or standards reference informing governance rules."""

    slug: str
    display_name: str
    domain: str
    governance_use: str


REFERENCE_MODELS: tuple[ReferenceModelProfile, ...] = (
    ReferenceModelProfile(
        slug="unesco",
        display_name="UNESCO",
        domain="heritage_preservation",
        governance_use="Stewardship, covenant review, and heritage-risk classification",
    ),
    ReferenceModelProfile(
        slug="wikidata",
        display_name="Wikidata",
        domain="linked_open_data",
        governance_use="Entity authority, provenance, and schema conformance checks",
    ),
    ReferenceModelProfile(
        slug="gbif",
        display_name="GBIF",
        domain="biodiversity",
        governance_use="Occurrence data quality, Darwin Core binding, and taxonomic validation",
    ),
    ReferenceModelProfile(
        slug="internet-archive",
        display_name="Internet Archive",
        domain="digital_preservation",
        governance_use="Fixity, format migration, and long-term access obligations",
    ),
    ReferenceModelProfile(
        slug="mit-ai-risk",
        display_name="MIT AI Risk Repository",
        domain="ai_risk_taxonomy",
        governance_use="Harm taxonomy, causal attribution, timing, and residual risk classification",
    ),
    ReferenceModelProfile(
        slug="nist-ai-rmf",
        display_name="NIST AI RMF",
        domain="ai_risk_management",
        governance_use="Risk registry taxonomy, impact assessment, and mitigation mapping",
    ),
    ReferenceModelProfile(
        slug="openssf",
        display_name="OpenSSF",
        domain="software_supply_chain",
        governance_use="Dependency provenance, secure development practices, and package integrity",
    ),
    ReferenceModelProfile(
        slug="iso-42001",
        display_name="ISO 42001",
        domain="ai_management_system",
        governance_use="Agent lifecycle controls, approval gates, and continual improvement",
    ),
    ReferenceModelProfile(
        slug="iso-27001",
        display_name="ISO 27001",
        domain="information_security",
        governance_use="Access control, audit evidence, and security risk treatment",
    ),
    ReferenceModelProfile(
        slug="opentelemetry",
        display_name="OpenTelemetry",
        domain="observability",
        governance_use="Trace context, metric dimensions, and audit telemetry correlation",
    ),
)

REFERENCE_MODEL_BY_SLUG = {profile.slug: profile for profile in REFERENCE_MODELS}
