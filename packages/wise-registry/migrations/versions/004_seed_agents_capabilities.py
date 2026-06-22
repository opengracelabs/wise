"""Seed canonical agents and capabilities from registry manifests.

Revision ID: 004_seed_agents_capabilities
Revises: 003_agent_capability_registry
Create Date: 2026-06-22

Must stay aligned with data/registry/agents/manifest.yaml and
data/registry/capabilities/manifest.yaml — validated at orchestrator startup.
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "004_seed_agents_capabilities"
down_revision: Union[str, None] = "003_agent_capability_registry"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SEED_ACTOR = "wise-orchestration-seed"

AGENTS = [
    {
        "agent_id": "wise.agent.source-discovery",
        "spec_prefix": "09",
        "spec_path": "docs/architecture/canonical/09-source-discovery-agent.md",
        "display_name": "Source Discovery Agent",
        "plane": "platform",
        "build_phase": 1,
        "service_binding": "discovery-service",
        "langgraph_graph_id": "source-discovery",
        "output_schema_uri": "wise_contracts.discovery.DiscoveryRecord",
        "evidence_profile": False,
        "read_only": False,
    },
    {
        "agent_id": "wise.agent.metadata",
        "spec_prefix": "10",
        "spec_path": "docs/architecture/canonical/10-metadata-agent.md",
        "display_name": "Metadata Agent",
        "plane": "platform",
        "build_phase": 4,
        "service_binding": "metadata-service",
        "langgraph_graph_id": "metadata",
        "output_schema_uri": "wise_contracts.metadata.EntityAssertion",
        "evidence_profile": True,
        "read_only": False,
    },
    {
        "agent_id": "wise.agent.preservation",
        "spec_prefix": "11",
        "spec_path": "docs/architecture/canonical/11-preservation-agent.md",
        "display_name": "Preservation Agent",
        "plane": "platform",
        "build_phase": 3,
        "service_binding": "preservation-service",
        "langgraph_graph_id": "preservation",
        "output_schema_uri": "wise_contracts.preservation.PreservedObjectDescriptor",
        "evidence_profile": False,
        "read_only": False,
    },
    {
        "agent_id": "wise.agent.knowledge-graph",
        "spec_prefix": "12",
        "spec_path": "docs/architecture/canonical/12-knowledge-graph-agent.md",
        "display_name": "Knowledge Graph Agent",
        "plane": "platform",
        "build_phase": 5,
        "service_binding": "knowledge-graph-service",
        "langgraph_graph_id": "knowledge-graph",
        "output_schema_uri": "wise_contracts.graph.GraphEntity",
        "evidence_profile": True,
        "read_only": False,
    },
    {
        "agent_id": "wise.agent.quality-review",
        "spec_prefix": "13",
        "spec_path": "docs/architecture/canonical/13-quality-review-agent.md",
        "display_name": "Quality Review Agent",
        "plane": "platform",
        "build_phase": 7,
        "service_binding": "metadata-service",
        "langgraph_graph_id": "quality-review",
        "output_schema_uri": "wise_contracts.quality.QualityReviewRecord",
        "evidence_profile": False,
        "read_only": False,
    },
    {
        "agent_id": "wise.agent.translation",
        "spec_prefix": "14",
        "spec_path": "docs/architecture/canonical/14-translation-agent.md",
        "display_name": "Translation Agent",
        "plane": "platform",
        "build_phase": 9,
        "service_binding": "orchestrator-service",
        "langgraph_graph_id": "translation",
        "output_schema_uri": "wise_contracts.common.ApprovalStatus",
        "evidence_profile": False,
        "read_only": False,
    },
    {
        "agent_id": "wise.agent.publishing",
        "spec_prefix": "15",
        "spec_path": "docs/architecture/canonical/15-publishing-agent.md",
        "display_name": "Publishing Agent",
        "plane": "platform",
        "build_phase": 10,
        "service_binding": "orchestrator-service",
        "langgraph_graph_id": "publishing",
        "output_schema_uri": "wise_contracts.common.ApprovalStatus",
        "evidence_profile": False,
        "read_only": False,
    },
    {
        "agent_id": "wise.agent.education",
        "spec_prefix": "16",
        "spec_path": "docs/architecture/canonical/16-education-agent.md",
        "display_name": "Education Agent",
        "plane": "experience",
        "build_phase": 13,
        "service_binding": "orchestrator-service",
        "langgraph_graph_id": "education",
        "output_schema_uri": "wise_contracts.common.ApprovalStatus",
        "evidence_profile": False,
        "read_only": False,
    },
    {
        "agent_id": "wise.agent.biodiversity-observatory",
        "spec_prefix": "17",
        "spec_path": "docs/architecture/canonical/17-biodiversity-observatory-agent.md",
        "display_name": "Biodiversity Observatory Agent",
        "plane": "experience",
        "build_phase": 15,
        "service_binding": "orchestrator-service",
        "langgraph_graph_id": "biodiversity-observatory",
        "output_schema_uri": "wise_contracts.common.EvidenceOutputProfile",
        "evidence_profile": True,
        "read_only": False,
    },
    {
        "agent_id": "wise.agent.climate-observatory",
        "spec_prefix": "18",
        "spec_path": "docs/architecture/canonical/18-climate-observatory-agent.md",
        "display_name": "Climate Observatory Agent",
        "plane": "experience",
        "build_phase": 15,
        "service_binding": "orchestrator-service",
        "langgraph_graph_id": "climate-observatory",
        "output_schema_uri": "wise_contracts.common.EvidenceOutputProfile",
        "evidence_profile": True,
        "read_only": False,
    },
    {
        "agent_id": "wise.agent.heritage-observatory",
        "spec_prefix": "19",
        "spec_path": "docs/architecture/canonical/19-heritage-observatory-agent.md",
        "display_name": "Heritage Observatory Agent",
        "plane": "experience",
        "build_phase": 15,
        "service_binding": "orchestrator-service",
        "langgraph_graph_id": "heritage-observatory",
        "output_schema_uri": "wise_contracts.common.EvidenceOutputProfile",
        "evidence_profile": True,
        "read_only": False,
    },
    {
        "agent_id": "wise.agent.tourism-observatory",
        "spec_prefix": "20",
        "spec_path": "docs/architecture/canonical/20-tourism-observatory-agent.md",
        "display_name": "Tourism Observatory Agent",
        "plane": "experience",
        "build_phase": 15,
        "service_binding": "orchestrator-service",
        "langgraph_graph_id": "tourism-observatory",
        "output_schema_uri": "wise_contracts.common.EvidenceOutputProfile",
        "evidence_profile": True,
        "read_only": False,
    },
    {
        "agent_id": "wise.agent.language-observatory",
        "spec_prefix": "21",
        "spec_path": "docs/architecture/canonical/21-language-observatory-agent.md",
        "display_name": "Language Observatory Agent",
        "plane": "experience",
        "build_phase": 15,
        "service_binding": "orchestrator-service",
        "langgraph_graph_id": "language-observatory",
        "output_schema_uri": "wise_contracts.common.EvidenceOutputProfile",
        "evidence_profile": True,
        "read_only": False,
    },
    {
        "agent_id": "wise.agent.standards",
        "spec_prefix": "22",
        "spec_path": "docs/architecture/canonical/22-standards-agent.md",
        "display_name": "Standards Agent",
        "plane": "constitutional",
        "build_phase": None,
        "service_binding": "orchestrator-service",
        "langgraph_graph_id": "standards",
        "output_schema_uri": "wise_contracts.orchestration.StandardsComplianceReport",
        "evidence_profile": False,
        "read_only": True,
    },
    {
        "agent_id": "wise.agent.benchmark",
        "spec_prefix": "23",
        "spec_path": "docs/architecture/canonical/23-benchmark-agent.md",
        "display_name": "Benchmark Agent",
        "plane": "constitutional",
        "build_phase": None,
        "service_binding": "orchestrator-service",
        "langgraph_graph_id": "benchmark",
        "output_schema_uri": "wise_contracts.orchestration.BenchmarkReport",
        "evidence_profile": False,
        "read_only": True,
    },
]

CAPABILITIES = [
    ("wise.capability.discovery", "03 §4.1", "Discovery", 1, "platform", "wise_contracts.discovery.DiscoveryRecord", None),
    ("wise.capability.ingestion", "03 §4.2", "Ingestion", 2, "platform", "wise_contracts.preservation.PreservedObjectDescriptor", "wise_contracts.discovery.DiscoveryRecord"),
    ("wise.capability.preservation", "03 §4.3", "Preservation", 3, "platform", "wise_contracts.preservation.PreservedObjectDescriptor", None),
    ("wise.capability.knowledge-modeling", "03 §4.4", "Knowledge Modeling", 4, "platform", "wise_contracts.metadata.EntityAssertion", "wise_contracts.preservation.PreservedObjectDescriptor"),
    ("wise.capability.knowledge-graph", "03 §4.5", "Knowledge Graph", 5, "platform", "wise_contracts.graph.GraphEntity", "wise_contracts.metadata.EntityAssertion"),
    ("wise.capability.search", "03 §4.6", "Search", 6, "platform", None, "wise_contracts.graph.GraphEntity"),
    ("wise.capability.quality", "03 §4.7", "Quality Platform", 7, "platform", "wise_contracts.quality.QualityReviewRecord", "wise_contracts.graph.GraphEntity"),
    ("wise.capability.research", "03 §4.8", "Research Fabric", 8, "platform", None, "wise_contracts.graph.GraphEntity"),
    ("wise.capability.translation", "03 §4.9", "Translation Fabric", 9, "platform", None, "wise_contracts.graph.GraphEntity"),
    ("wise.capability.publishing", "03 §4.10", "Publishing", 10, "platform", None, "wise_contracts.graph.GraphEntity"),
    ("wise.capability.standards-conformance", "03 §3 Standards Registry", "Standards Conformance", None, "constitutional", "wise_contracts.orchestration.StandardsComplianceReport", None),
    ("wise.capability.benchmarks", "03 §3 Benchmark Program", "Benchmark Program", None, "constitutional", "wise_contracts.orchestration.BenchmarkReport", None),
]

CAPABILITY_AGENTS = [
    ("wise.capability.discovery", "wise.agent.source-discovery", "primary"),
    ("wise.capability.ingestion", "wise.agent.preservation", "primary"),
    ("wise.capability.preservation", "wise.agent.preservation", "primary"),
    ("wise.capability.knowledge-modeling", "wise.agent.metadata", "primary"),
    ("wise.capability.knowledge-graph", "wise.agent.knowledge-graph", "primary"),
    ("wise.capability.quality", "wise.agent.quality-review", "primary"),
    ("wise.capability.quality", "wise.agent.metadata", "supporting"),
    ("wise.capability.translation", "wise.agent.translation", "primary"),
    ("wise.capability.publishing", "wise.agent.publishing", "primary"),
    ("wise.capability.standards-conformance", "wise.agent.standards", "governance"),
    ("wise.capability.benchmarks", "wise.agent.benchmark", "governance"),
]

CAPABILITY_SERVICES = [
    ("wise.capability.discovery", "discovery-service", "DISCOVERY_SERVICE_URL", "/health"),
    ("wise.capability.ingestion", "preservation-service", "PRESERVATION_SERVICE_URL", "/health"),
    ("wise.capability.preservation", "preservation-service", "PRESERVATION_SERVICE_URL", "/health"),
    ("wise.capability.knowledge-modeling", "metadata-service", "METADATA_SERVICE_URL", "/health"),
    ("wise.capability.knowledge-graph", "knowledge-graph-service", "KNOWLEDGE_GRAPH_SERVICE_URL", "/health"),
    ("wise.capability.quality", "metadata-service", "METADATA_SERVICE_URL", "/health"),
    ("wise.capability.standards-conformance", "orchestrator-service", "ORCHESTRATOR_SERVICE_URL", "/health"),
    ("wise.capability.benchmarks", "orchestrator-service", "ORCHESTRATOR_SERVICE_URL", "/health"),
]


def upgrade() -> None:
    conn = op.get_bind()

    for agent in AGENTS:
        conn.execute(
            sa.text(
                """
                INSERT INTO registry.agents (
                    agent_id, spec_prefix, spec_path, display_name, plane,
                    build_phase, service_binding, langgraph_graph_id,
                    output_schema_uri, evidence_profile, read_only,
                    created_by, updated_by
                ) VALUES (
                    :agent_id, :spec_prefix, :spec_path, :display_name,
                    CAST(:plane AS registry.agent_plane_enum),
                    :build_phase, :service_binding, :langgraph_graph_id,
                    :output_schema_uri, :evidence_profile, :read_only,
                    :actor, :actor
                )
                """
            ),
            {**agent, "actor": SEED_ACTOR},
        )

    for cap in CAPABILITIES:
        conn.execute(
            sa.text(
                """
                INSERT INTO registry.capabilities (
                    capability_id, canonical_section, display_name, build_phase,
                    plane, contract_producer, contract_consumer,
                    created_by, updated_by
                ) VALUES (
                    :capability_id, :canonical_section, :display_name, :build_phase,
                    CAST(:plane AS registry.agent_plane_enum),
                    :contract_producer, :contract_consumer,
                    :actor, :actor
                )
                """
            ),
            {
                "capability_id": cap[0],
                "canonical_section": cap[1],
                "display_name": cap[2],
                "build_phase": cap[3],
                "plane": cap[4],
                "contract_producer": cap[5],
                "contract_consumer": cap[6],
                "actor": SEED_ACTOR,
            },
        )

    for link in CAPABILITY_AGENTS:
        conn.execute(
            sa.text(
                """
                INSERT INTO registry.capability_agents (
                    capability_id, agent_id, role, created_by, updated_by
                ) VALUES (
                    :capability_id, :agent_id,
                    CAST(:role AS registry.capability_role_enum),
                    :actor, :actor
                )
                """
            ),
            {
                "capability_id": link[0],
                "agent_id": link[1],
                "role": link[2],
                "actor": SEED_ACTOR,
            },
        )

    for svc in CAPABILITY_SERVICES:
        conn.execute(
            sa.text(
                """
                INSERT INTO registry.capability_services (
                    capability_id, service_name, base_url_env, health_path,
                    created_by, updated_by
                ) VALUES (
                    :capability_id, :service_name, :base_url_env, :health_path,
                    :actor, :actor
                )
                """
            ),
            {
                "capability_id": svc[0],
                "service_name": svc[1],
                "base_url_env": svc[2],
                "health_path": svc[3],
                "actor": SEED_ACTOR,
            },
        )


def downgrade() -> None:
    op.execute("DELETE FROM registry.capability_services")
    op.execute("DELETE FROM registry.capability_agents")
    op.execute("DELETE FROM registry.capabilities")
    op.execute("DELETE FROM registry.agents")
