"""Governance consistency checks for the Unified Compliance Model."""

from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
GOVERNANCE_DIR = REPO_ROOT / "docs" / "governance"
CANONICAL_DIR = REPO_ROOT / "docs" / "architecture" / "canonical"
MODEL_PATH = GOVERNANCE_DIR / "unified-compliance-model.md"
CAPABILITY_REGISTRY_PATH = GOVERNANCE_DIR / "capability-registry.md"

MODELED_AGENT_DOCS = {
    "Quality Review Agent": CANONICAL_DIR / "13-quality-review-agent.md",
    "Standards Agent": CANONICAL_DIR / "22-standards-agent.md",
    "Benchmark Agent": CANONICAL_DIR / "23-benchmark-agent.md",
    "Research Agent": CANONICAL_DIR / "25-research-agent.md",
    "Audit Agent": CANONICAL_DIR / "26-audit-agent.md",
}


def read_doc(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_unified_compliance_model_contains_required_sequence_and_diagram() -> None:
    model = read_doc(MODEL_PATH)

    assert "Standards -> Quality -> Benchmark -> Audit -> Human Approval" in model
    assert "flowchart TD" in model
    assert "Standards --> Quality" in model
    assert "Quality --> Benchmark" in model
    assert "Benchmark --> Audit" in model
    assert "Audit --> HumanApproval" in model


def test_unified_compliance_model_contains_boundary_rules() -> None:
    model = read_doc(MODEL_PATH)

    required_rules = [
        "Audit Agent MUST NOT redefine standards. Audit Agent verifies standards were correctly applied.",
        "Benchmark Agent measures performance. Benchmark Agent does not approve publication.",
        "Quality Review Agent validates content. Quality Review Agent does not define standards.",
        "Standards Agent defines correctness. Standards Agent does not audit execution.",
    ]

    for rule in required_rules:
        assert rule in model


def test_unified_compliance_model_preserves_architecture_freeze() -> None:
    model = read_doc(MODEL_PATH)

    required_non_expansion_clauses = [
        "Architecture v1.0 remains frozen.",
        "no new capabilities",
        "no governance changes",
        "no new governance structures",
        "no new agents",
        "requires **no ADR**",
        "This document must not be used to justify new agent capabilities",
    ]

    for clause in required_non_expansion_clauses:
        assert clause in model


def test_modeled_agents_are_registered_or_documented() -> None:
    model = read_doc(MODEL_PATH)
    capability_registry = read_doc(CAPABILITY_REGISTRY_PATH)

    for agent_name, path in MODELED_AGENT_DOCS.items():
        assert agent_name in model
        assert path.exists(), f"Missing modeled agent spec: {path}"

    # Architecture Agent is represented as a Draft capability until a spec exists.
    assert "Architecture Agent (24), as listed in the [Capability Registry]" in model
    assert "`wise.capability.architecture-council` | Architecture Agent" in capability_registry


def test_boundary_rules_have_no_direct_forbidden_claims() -> None:
    docs = {agent: read_doc(path).lower() for agent, path in MODELED_AGENT_DOCS.items()}

    forbidden_claims = {
        "Audit Agent": [
            "audit agent defines correctness",
            "audit agent redefines standards",
            "audit agent approves deployments",
            "audit agent performs canonical writes",
        ],
        "Benchmark Agent": [
            "benchmark agent approves publication",
            "benchmark agent grants production clearance",
            "benchmark agent deploys agents",
        ],
        "Quality Review Agent": [
            "quality review agent defines standards",
            "quality review agent publishes content",
        ],
        "Standards Agent": [
            "standards agent audits execution",
            "standards agent waives required-standard failures",
        ],
        "Research Agent": [
            "research agent writes canonical metadata",
            "research agent publishes research conclusions as canonical fact",
        ],
    }

    for agent_name, phrases in forbidden_claims.items():
        doc = docs[agent_name]
        for phrase in phrases:
            assert phrase not in doc


def test_capability_registry_contains_no_extra_governance_compliance_owner_for_core_model() -> None:
    capability_registry = read_doc(CAPABILITY_REGISTRY_PATH)

    core_capabilities = [
        "`wise.capability.architecture-council`",
        "`wise.capability.research-council`",
        "`wise.capability.governance-audit`",
    ]

    for capability_id in core_capabilities:
        assert capability_id in capability_registry

    assert capability_registry.count("| Audit Agent | AI Fabric") == 1
    assert capability_registry.count("| Research Agent | AI Fabric") == 1
    assert capability_registry.count("| Architecture Agent | AI Fabric") == 1
