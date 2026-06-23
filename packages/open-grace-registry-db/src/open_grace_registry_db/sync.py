"""YAML seed import, JSON export, and JSON store sync utilities."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

import yaml

if TYPE_CHECKING:
    from open_grace_registry_db.database import RegistryDatabase

_PACKAGE_ROOTS = {
    "capability_framework": Path(__file__).resolve().parents[2].parent
    / "open-grace-governance"
    / "src"
    / "open_grace_governance"
    / "data"
    / "seed"
    / "capability_framework.yaml",
    "risk_registry": Path(__file__).resolve().parents[2].parent
    / "open-grace-governance"
    / "src"
    / "open_grace_governance"
    / "data"
    / "seed"
    / "risk_registry.yaml",
    "standards_registry": Path(__file__).resolve().parents[2].parent
    / "open-grace-governance"
    / "src"
    / "open_grace_governance"
    / "data"
    / "seed"
    / "standards_registry.yaml",
    "benchmark_registry": Path(__file__).resolve().parents[2].parent
    / "open-grace-benchmarking"
    / "src"
    / "open_grace_benchmarking"
    / "data"
    / "seed"
    / "benchmark_registry.yaml",
    "model_registry": Path(__file__).resolve().parents[2].parent
    / "open-grace-agent-registry"
    / "src"
    / "open_grace_agent_registry"
    / "data"
    / "seed"
    / "model_registry.yaml",
}

_KNOWLEDGE_SEEDS = {
    "entity": "entity_registry.yaml",
    "species": "species_registry.yaml",
    "place": "place_registry.yaml",
    "heritage": "heritage_registry.yaml",
    "collection": "collection_registry.yaml",
    "media": "media_registry.yaml",
    "knowledge_graph": "knowledge_graph_registry.yaml",
}


def _knowledge_seed_dir() -> Path:
    return (
        Path(__file__).resolve().parents[2].parent
        / "open-grace-knowledge"
        / "src"
        / "open_grace_knowledge"
        / "data"
        / "seed"
    )


def _load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def seed_all_from_yaml(db: RegistryDatabase) -> dict[str, int]:
    """Import all package YAML seeds into the database."""
    from open_grace_agent_registry.manifest_paths import agents_manifest_path
    from open_grace_governance.lifecycle import LifecycleStage
    from open_grace_governance.schemas import (
        AgentRegistryRecord,
        CapabilityFrameworkRecord,
        RiskRegistryRecord,
        StandardsRegistryRecord,
    )
    from open_grace_governance.schemas import BenchmarkRegistryRecord, ModelRegistryRecord
    from open_grace_registry_db.models import (
        AgentEntry,
        BenchmarkEntry,
        CapabilityEntry,
        ModelEntry,
        RiskEntry,
        StandardEntry,
    )
    from open_grace_registry_db.repositories import BindingRepository, GovernedRepository, KnowledgeRepository

    counts: dict[str, int] = {}

    with db.session() as session:
        agents_repo = GovernedRepository(session, AgentEntry, AgentRegistryRecord, "agent_id")
        manifest = _load_yaml(agents_manifest_path())
        for row in manifest["agents"]:
            record = AgentRegistryRecord(
                lifecycle_stage=LifecycleStage.PUBLICATION,
                steward_actor="open-grace-db-seed",
                reference_models=["iso-42001", "nist-ai-rmf"],
                **row,
            )
            agents_repo.upsert(record)
        counts["agents"] = len(agents_repo.list())

        cap_yaml = _load_yaml(_PACKAGE_ROOTS["capability_framework"])
        caps_repo = GovernedRepository(
            session, CapabilityEntry, CapabilityFrameworkRecord, "id"
        )
        for row in cap_yaml["capability_classes"]:
            record = CapabilityFrameworkRecord.model_validate(row)
            caps_repo.upsert(record)
        counts["capabilities"] = len(caps_repo.list())

        bindings_repo = BindingRepository(session)
        bindings_repo.replace_all(cap_yaml.get("agent_bindings", []))
        counts["agent_bindings"] = len(bindings_repo.list())

        risk_yaml = _load_yaml(_PACKAGE_ROOTS["risk_registry"])
        risks_repo = GovernedRepository(session, RiskEntry, RiskRegistryRecord, "risk_id")
        for row in risk_yaml["risks"]:
            risks_repo.upsert(RiskRegistryRecord.model_validate(row))
        counts["risks"] = len(risks_repo.list())

        std_yaml = _load_yaml(_PACKAGE_ROOTS["standards_registry"])
        std_repo = GovernedRepository(session, StandardEntry, StandardsRegistryRecord, "standard_id")
        for row in std_yaml["standards"]:
            std_repo.upsert(StandardsRegistryRecord.model_validate(row))
        counts["standards"] = len(std_repo.list())

        bench_yaml = _load_yaml(_PACKAGE_ROOTS["benchmark_registry"])
        bench_repo = GovernedRepository(
            session, BenchmarkEntry, BenchmarkRegistryRecord, "benchmark_id"
        )
        for row in bench_yaml["benchmarks"]:
            bench_repo.upsert(BenchmarkRegistryRecord.model_validate(row))
        counts["benchmarks"] = len(bench_repo.list())

        model_yaml = _load_yaml(_PACKAGE_ROOTS["model_registry"])
        model_repo = GovernedRepository(session, ModelEntry, ModelRegistryRecord, "model_id")
        for row in model_yaml["models"]:
            model_repo.upsert(ModelRegistryRecord.model_validate(row))
        counts["models"] = len(model_repo.list())

        knowledge_repo = KnowledgeRepository(session)
        knowledge_dir = _knowledge_seed_dir()
        knowledge_counts: dict[str, int] = {}
        from open_grace_knowledge.schemas import (
            CollectionRegistryRecord,
            EntityRegistryRecord,
            HeritageRegistryRecord,
            KnowledgeGraphRegistryRecord,
            MediaRegistryRecord,
            PlaceRegistryRecord,
            SpeciesRegistryRecord,
        )

        type_models = {
            "entity": (EntityRegistryRecord, "entities"),
            "species": (SpeciesRegistryRecord, "species"),
            "place": (PlaceRegistryRecord, "places"),
            "heritage": (HeritageRegistryRecord, "heritage"),
            "collection": (CollectionRegistryRecord, "collections"),
            "media": (MediaRegistryRecord, "media"),
            "knowledge_graph": (KnowledgeGraphRegistryRecord, "knowledge_graphs"),
        }
        for ktype, (model, key) in type_models.items():
            seed_path = knowledge_dir / _KNOWLEDGE_SEEDS[ktype]
            if not seed_path.is_file():
                continue
            data = _load_yaml(seed_path)
            rows = data.get(key, [])
            for row in rows:
                record = model.model_validate(row)
                knowledge_repo.upsert(ktype, record)
            knowledge_counts[ktype] = len(rows)
        counts["knowledge"] = sum(knowledge_counts.values())

    return counts


def export_all_json(db: RegistryDatabase, out_dir: Path) -> dict[str, Path]:
    """Export all registry tables to JSON files matching JsonRegistryStore format."""
    from open_grace_governance.schemas import (
        AgentRegistryRecord,
        CapabilityFrameworkRecord,
        RiskRegistryRecord,
        StandardsRegistryRecord,
    )
    from open_grace_governance.schemas import BenchmarkRegistryRecord, ModelRegistryRecord
    from open_grace_registry_db.models import (
        AgentEntry,
        BenchmarkEntry,
        CapabilityEntry,
        ModelEntry,
        RiskEntry,
        StandardEntry,
    )
    from open_grace_registry_db.repositories import BindingRepository, GovernedRepository, KnowledgeRepository

    out_dir.mkdir(parents=True, exist_ok=True)
    written: dict[str, Path] = {}

    with db.session() as session:
        exports = [
            ("agents", GovernedRepository(session, AgentEntry, AgentRegistryRecord, "agent_id"), "agent_registry.json"),
            (
                "capabilities",
                GovernedRepository(session, CapabilityEntry, CapabilityFrameworkRecord, "id"),
                "capability_framework.json",
            ),
            ("risks", GovernedRepository(session, RiskEntry, RiskRegistryRecord, "risk_id"), "risk_registry.json"),
            (
                "standards",
                GovernedRepository(session, StandardEntry, StandardsRegistryRecord, "standard_id"),
                "standards_registry.json",
            ),
            (
                "benchmarks",
                GovernedRepository(session, BenchmarkEntry, BenchmarkRegistryRecord, "benchmark_id"),
                "benchmark_registry.json",
            ),
            ("models", GovernedRepository(session, ModelEntry, ModelRegistryRecord, "model_id"), "model_registry.json"),
        ]
        for name, repo, filename in exports:
            entries = [record.model_dump(mode="json") for record in repo.list()]
            path = out_dir / filename
            path.write_text(
                json.dumps({"version": "1.0", "entries": entries}, indent=2),
                encoding="utf-8",
            )
            written[name] = path

        bindings = BindingRepository(session).list()
        bindings_path = out_dir / "agent_bindings.json"
        bindings_path.write_text(json.dumps(bindings, indent=2), encoding="utf-8")
        written["agent_bindings"] = bindings_path

        knowledge_repo = KnowledgeRepository(session)
        knowledge_entries = [
            record.model_dump(mode="json") for record in knowledge_repo.list()
        ]
        knowledge_path = out_dir / "knowledge_registry.json"
        knowledge_path.write_text(
            json.dumps({"version": "1.0", "entries": knowledge_entries}, indent=2),
            encoding="utf-8",
        )
        written["knowledge"] = knowledge_path

    return written


def sync_json_store(db: RegistryDatabase, json_dir: Path) -> dict[str, int]:
    """Import from existing JsonRegistryStore JSON files into the database."""
    from open_grace_governance.schemas import (
        AgentRegistryRecord,
        CapabilityFrameworkRecord,
        RiskRegistryRecord,
        StandardsRegistryRecord,
    )
    from open_grace_governance.schemas import BenchmarkRegistryRecord, ModelRegistryRecord
    from open_grace_registry_db.models import (
        AgentEntry,
        BenchmarkEntry,
        CapabilityEntry,
        ModelEntry,
        RiskEntry,
        StandardEntry,
    )
    from open_grace_registry_db.repositories import GovernedRepository

    counts: dict[str, int] = {}
    mapping = [
        ("agent_registry.json", AgentEntry, AgentRegistryRecord, "agent_id", "agents"),
        ("capability_framework.json", CapabilityEntry, CapabilityFrameworkRecord, "id", "capabilities"),
        ("risk_registry.json", RiskEntry, RiskRegistryRecord, "risk_id", "risks"),
        ("standards_registry.json", StandardEntry, StandardsRegistryRecord, "standard_id", "standards"),
        ("benchmark_registry.json", BenchmarkEntry, BenchmarkRegistryRecord, "benchmark_id", "benchmarks"),
        ("model_registry.json", ModelEntry, ModelRegistryRecord, "model_id", "models"),
    ]

    with db.session() as session:
        for filename, model, record_model, id_field, key in mapping:
            path = json_dir / filename
            if not path.is_file():
                continue
            payload = json.loads(path.read_text(encoding="utf-8"))
            repo = GovernedRepository(session, model, record_model, id_field)
            for row in payload.get("entries", []):
                repo.upsert(record_model.model_validate(row))
            counts[key] = len(repo.list())

    return counts
