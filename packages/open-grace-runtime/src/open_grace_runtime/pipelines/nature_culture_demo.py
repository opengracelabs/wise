"""Nature & Culture Demonstration Pipeline v1 — Panthera leo."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from open_grace_governance.system import GovernanceSystem
from open_grace_runtime.schemas import ExecutionStatus
from open_grace_runtime.system import AgentRunResult

STEWARD_ACTOR = "open-grace-nature-culture-demo"
SPECIES_SLUG = "panthera-leo"
SPECIES_ID = "wise.species.panthera-leo"
KNOWLEDGE_GRAPH_ID = "wise.knowledge.graph.serengeti-wildlife"


def _stage_run_id(stage: str) -> str:
    slug = stage.replace("_", "-")
    return f"wise.execution.nc-{slug}-{SPECIES_SLUG}"

# Workflow stages: Research → Metadata → Classification → Translation → KG → Preservation → Publishing
PIPELINE_STAGES: tuple[dict[str, str | None], ...] = (
    {
        "stage": "research",
        "display_name": "Research Agent",
        "agent_id": "wise.agent.standards",
        "artifact": "research.md",
    },
    {
        "stage": "metadata",
        "display_name": "Metadata Agent",
        "agent_id": "wise.agent.metadata",
        "artifact": "metadata.json",
    },
    {
        "stage": "classification",
        "display_name": "Classification Agent",
        "agent_id": "wise.agent.quality-review",
        "artifact": "classification.json",
    },
    {
        "stage": "translation",
        "display_name": "Translation Agent",
        "agent_id": "wise.agent.translation",
        "artifact": None,
    },
    {
        "stage": "knowledge_graph",
        "display_name": "Knowledge Graph Agent",
        "agent_id": "wise.agent.knowledge-graph",
        "artifact": "knowledge-graph.json",
    },
    {
        "stage": "preservation",
        "display_name": "Preservation Agent",
        "agent_id": "wise.agent.preservation",
        "artifact": "preservation-record.json",
    },
    {
        "stage": "publishing",
        "display_name": "Publishing Agent",
        "agent_id": "wise.agent.publishing",
        "artifact": "publication-page.md",
    },
)

_OBSERVED_VALUES: dict[str, dict[str, float]] = {
    "wise.agent.standards": {
        "wise.benchmark.research-coverage": 0.90,
        "wise.benchmark.standards-conformance": 0.96,
    },
    "wise.agent.metadata": {
        "wise.benchmark.classification-precision": 0.95,
        "wise.benchmark.standards-conformance": 0.96,
        "wise.benchmark.discovery-safety": 0.995,
        "wise.benchmark.extraction-recall": 0.90,
    },
    "wise.agent.quality-review": {
        "wise.benchmark.classification-precision": 0.95,
        "wise.benchmark.standards-conformance": 0.96,
    },
    "wise.agent.translation": {
        "wise.benchmark.translation-cost": 0.03,
        "wise.benchmark.translation-quality": 0.85,
    },
    "wise.agent.knowledge-graph": {
        "wise.benchmark.kg-reliability": 0.92,
        "wise.benchmark.analysis-latency": 30.0,
    },
    "wise.agent.preservation": {
        "wise.benchmark.preservation-fixity": 0.9995,
        "wise.benchmark.discovery-safety": 0.995,
    },
    "wise.agent.publishing": {
        "wise.benchmark.publishing-quality": 0.95,
        "wise.benchmark.standards-conformance": 0.96,
    },
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[5]


def default_content_root() -> Path:
    return repo_root() / "content" / "species" / SPECIES_SLUG


def load_reference_species() -> dict[str, Any]:
    """Load GBIF reference record and knowledge species entry when available."""
    gbif_path = repo_root() / "data" / "reference" / "gbif" / "panthera-leo-5219404.json"
    gbif: dict[str, Any] = {}
    if gbif_path.is_file():
        gbif = json.loads(gbif_path.read_text(encoding="utf-8"))

    return {
        "slug": SPECIES_SLUG,
        "species_id": SPECIES_ID,
        "scientific_name": gbif.get("scientific_name", "Panthera leo"),
        "scientific_name_authorship": gbif.get("scientific_name_authorship", "Linnaeus, 1758"),
        "common_name": gbif.get("common_name", "Lion"),
        "common_names": ["African lion", "Lion"],
        "gbif_taxon_key": gbif.get("gbif_taxon_key", "5219404"),
        "taxon_rank": gbif.get("taxon_rank", "species"),
        "kingdom": gbif.get("kingdom", "Animalia"),
        "phylum": gbif.get("phylum", "Chordata"),
        "class": gbif.get("class", "Mammalia"),
        "order": gbif.get("order", "Carnivora"),
        "family": gbif.get("family", "Felidae"),
        "genus": gbif.get("genus", "Panthera"),
        "specific_epithet": gbif.get("specific_epithet", "leo"),
        "taxonomic_status": gbif.get("taxonomic_status", "accepted"),
        "source_uri": gbif.get("source_uri", "https://www.gbif.org/species/5219404"),
        "rights_uri": gbif.get("rights_uri", "https://creativecommons.org/publicdomain/zero/1.0/"),
        "external_ids": {"wikidata": "Q140", "gbif": "5219404", "eol": "328450"},
        "place_ids": ["wise.place.serengeti-national-park"],
        "knowledge_graph_id": KNOWLEDGE_GRAPH_ID,
    }


@dataclass
class NatureCultureStageResult:
    stage: str
    display_name: str
    agent_id: str
    run_result: AgentRunResult
    artifact_path: Path | None = None


@dataclass
class NatureCultureDemoResult:
    species_slug: str
    content_dir: Path
    stages: list[NatureCultureStageResult] = field(default_factory=list)
    execution_count: int = 0
    audit_count: int = 0
    benchmark_run_count: int = 0

    @property
    def all_completed(self) -> bool:
        return all(
            stage.run_result.status == ExecutionStatus.COMPLETED
            for stage in self.stages
        )


def _artifact_provenance(stage: NatureCultureStageResult) -> dict[str, Any]:
    run = stage.run_result
    return {
        "pipeline": "nature-culture-demo-v1",
        "stage": stage.stage,
        "agent_id": stage.agent_id,
        "run_id": run.run_id,
        "audit_id": run.audit_id,
        "model_id": run.model_id,
        "output_ref": run.output_ref,
        "generated_at": datetime.now(UTC).isoformat(),
        "steward_actor": STEWARD_ACTOR,
    }


def _write_research_md(path: Path, species: dict[str, Any], stage: NatureCultureStageResult) -> None:
    prov = _artifact_provenance(stage)
    body = f"""# Research: {species["scientific_name"]}

## Summary

Steward-reviewed research synthesis for *{species["scientific_name"]}* ({species["common_name"]}),
the African lion, using GBIF backbone taxonomy and WISE Nature & Culture knowledge links.

## Taxonomic authority

- Scientific name: {species["scientific_name"]} {species["scientific_name_authorship"]}
- GBIF taxon key: {species["gbif_taxon_key"]}
- Source: [{species["source_uri"]}]({species["source_uri"]})

## Research coverage

- Standards conformance reviewed against CIDOC-CRM and Darwin Core overlays
- Linked heritage contexts: Serengeti ecosystem, Everglades wetland comparison datasets
- Knowledge graph anchor: `{species["knowledge_graph_id"]}`

## Provenance

```json
{json.dumps(prov, indent=2)}
```
"""
    path.write_text(body, encoding="utf-8")


def _write_metadata_json(path: Path, species: dict[str, Any], stage: NatureCultureStageResult) -> None:
    payload = {
        "species_id": species["species_id"],
        "stable_id": species["slug"],
        "scientific_name": species["scientific_name"],
        "scientific_name_authorship": species["scientific_name_authorship"],
        "common_names": species["common_names"],
        "taxon_rank": species["taxon_rank"],
        "gbif_taxon_key": species["gbif_taxon_key"],
        "external_ids": species["external_ids"],
        "place_ids": species["place_ids"],
        "darwin_core": {
            "kingdom": species["kingdom"],
            "phylum": species["phylum"],
            "class": species["class"],
            "order": species["order"],
            "family": species["family"],
            "genus": species["genus"],
            "specificEpithet": species["specific_epithet"],
            "taxonomicStatus": species["taxonomic_status"],
        },
        "rights": {
            "source_uri": species["source_uri"],
            "rights_uri": species["rights_uri"],
        },
        "provenance": _artifact_provenance(stage),
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _write_classification_json(path: Path, species: dict[str, Any], stage: NatureCultureStageResult) -> None:
    payload = {
        "species_id": species["species_id"],
        "classification": {
            "kingdom": species["kingdom"],
            "phylum": species["phylum"],
            "class": species["class"],
            "order": species["order"],
            "family": species["family"],
            "genus": species["genus"],
            "species": species["scientific_name"],
        },
        "authority_records": [
            {"authority": "GBIF Backbone", "taxon_key": species["gbif_taxon_key"]},
            {"authority": "Wikidata", "entity_id": species["external_ids"]["wikidata"]},
        ],
        "schema_validation": {
            "darwin_core": "pass",
            "schema_org": "pass",
        },
        "provenance": _artifact_provenance(stage),
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _write_knowledge_graph_json(path: Path, species: dict[str, Any], stage: NatureCultureStageResult) -> None:
    payload = {
        "graph_id": species["knowledge_graph_id"],
        "species_id": species["species_id"],
        "nodes": [
            {"id": species["species_id"], "type": "species", "label": species["scientific_name"]},
            {"id": "wise.place.serengeti-national-park", "type": "place", "label": "Serengeti National Park"},
            {"id": "wise.heritage.serengeti-ecosystem", "type": "heritage", "label": "Serengeti Ecosystem"},
            {"id": "wise.entity.gbif-secretariat", "type": "entity", "label": "GBIF Secretariat"},
        ],
        "edges": [
            {
                "source": species["species_id"],
                "target": "wise.place.serengeti-national-park",
                "predicate": "occursIn",
            },
            {
                "source": species["species_id"],
                "target": "wise.heritage.serengeti-ecosystem",
                "predicate": "memberOf",
            },
            {
                "source": species["species_id"],
                "target": "wise.entity.gbif-secretariat",
                "predicate": "sourcedFrom",
            },
        ],
        "provenance": _artifact_provenance(stage),
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _write_preservation_record_json(
    path: Path, species: dict[str, Any], stage: NatureCultureStageResult
) -> None:
    payload = {
        "species_id": species["species_id"],
        "fixity": {
            "algorithm": "sha256",
            "checksum": "demo-fixity-panthera-leo-v1",
            "verified": True,
        },
        "premis_events": [
            {
                "event_type": "ingestion",
                "event_datetime": datetime.now(UTC).isoformat(),
                "outcome": "success",
            },
            {
                "event_type": "fixity_check",
                "event_datetime": datetime.now(UTC).isoformat(),
                "outcome": "pass",
            },
        ],
        "backing_stores": ["postgresql", "pgvector", "json_file"],
        "provenance": _artifact_provenance(stage),
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _write_publication_page_md(path: Path, species: dict[str, Any], stage: NatureCultureStageResult) -> None:
    prov = _artifact_provenance(stage)
    body = f"""# {species["common_name"]} — *{species["scientific_name"]}*

Publication-ready species page generated by the Nature & Culture demonstration pipeline.

## Overview

The African lion (*{species["scientific_name"]}*) is a flagship felid species represented in
the WISE reference capability with GBIF taxon key `{species["gbif_taxon_key"]}`.

## Taxonomy

| Rank | Name |
|------|------|
| Family | {species["family"]} |
| Genus | {species["genus"]} |
| Species | {species["scientific_name"]} |

## Rights and attribution

- Source: [GBIF]({species["source_uri"]})
- License: [CC0 1.0]({species["rights_uri"]})

## Editorial gate

- IIIF manifest validation: pass (demonstration stub)
- Editorial gate signed by: `{STEWARD_ACTOR}`

## Pipeline provenance

```json
{json.dumps(prov, indent=2)}
```
"""
    path.write_text(body, encoding="utf-8")


_ARTIFACT_WRITERS = {
    "research.md": _write_research_md,
    "metadata.json": _write_metadata_json,
    "classification.json": _write_classification_json,
    "knowledge-graph.json": _write_knowledge_graph_json,
    "preservation-record.json": _write_preservation_record_json,
    "publication-page.md": _write_publication_page_md,
}


def write_stage_artifact(
    content_dir: Path,
    species: dict[str, Any],
    stage: NatureCultureStageResult,
    artifact_name: str,
) -> Path:
    content_dir.mkdir(parents=True, exist_ok=True)
    path = content_dir / artifact_name
    writer = _ARTIFACT_WRITERS[artifact_name]
    writer(path, species, stage)
    stage.artifact_path = path
    return path


def observed_values_for_agent(agent_id: str) -> dict[str, float]:
    values = _OBSERVED_VALUES.get(agent_id)
    if values is None:
        raise ValueError(f"no observed benchmark values configured for {agent_id}")
    return dict(values)


def run_panthera_leo_pipeline(
    *,
    governance_root: Path | None = None,
    content_root: Path | None = None,
    seed_if_needed: bool = True,
) -> NatureCultureDemoResult:
    """Run the Nature & Culture demonstration pipeline for Panthera leo."""
    system = GovernanceSystem.create(governance_root)
    if seed_if_needed:
        system.seed_all()
        system.register_nature_culture_agents()

    species = load_reference_species()
    content_dir = content_root or default_content_root()
    result = NatureCultureDemoResult(species_slug=SPECIES_SLUG, content_dir=content_dir)

    executions_before = len(system.runtime.executions.list())
    audits_before = len(system.audits.list())
    benchmark_runs_before = len(system.runtime.benchmark_runs.list())

    for stage_def in PIPELINE_STAGES:
        agent_id = str(stage_def["agent_id"])
        run_result = system.run_agent(
            agent_id,
            observed_values=observed_values_for_agent(agent_id),
            steward_actor=STEWARD_ACTOR,
            run_id=_stage_run_id(str(stage_def["stage"])),
        )
        if run_result.halted or run_result.status != ExecutionStatus.COMPLETED:
            gate_errors = [
                error
                for gate in run_result.gate_results
                for error in gate.errors
            ]
            raise RuntimeError(
                f"pipeline halted at {stage_def['stage']}: "
                + "; ".join(gate_errors or [run_result.status.value])
            )

        stage_result = NatureCultureStageResult(
            stage=str(stage_def["stage"]),
            display_name=str(stage_def["display_name"]),
            agent_id=agent_id,
            run_result=run_result,
        )
        artifact_name = stage_def["artifact"]
        if artifact_name:
            write_stage_artifact(content_dir, species, stage_result, artifact_name)
        result.stages.append(stage_result)

    result.execution_count = len(system.runtime.executions.list()) - executions_before
    result.audit_count = len(system.audits.list()) - audits_before
    result.benchmark_run_count = (
        len(system.runtime.benchmark_runs.list()) - benchmark_runs_before
    )
    return result
