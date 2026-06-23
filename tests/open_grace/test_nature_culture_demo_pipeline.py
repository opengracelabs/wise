"""Nature & Culture demonstration pipeline tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from open_grace_governance.system import GovernanceSystem
from open_grace_runtime.pipelines.nature_culture_demo import (
    PIPELINE_STAGES,
    _stage_run_id,
    load_reference_species,
    run_panthera_leo_pipeline,
)
from open_grace_runtime.schemas import ExecutionStatus

EXPECTED_ARTIFACTS = (
    "research.md",
    "metadata.json",
    "classification.json",
    "knowledge-graph.json",
    "preservation-record.json",
    "publication-page.md",
)


@pytest.fixture
def pipeline_dirs(tmp_path):
    governance_root = tmp_path / "governance"
    content_root = tmp_path / "content" / "species" / "panthera-leo"
    return governance_root, content_root


def test_load_reference_species_has_panthera_leo():
    species = load_reference_species()
    assert species["slug"] == "panthera-leo"
    assert species["scientific_name"] == "Panthera leo"
    assert species["gbif_taxon_key"] == "5219404"


def test_panthera_leo_pipeline_runs_end_to_end(pipeline_dirs):
    governance_root, content_root = pipeline_dirs
    result = run_panthera_leo_pipeline(
        governance_root=governance_root,
        content_root=content_root,
    )

    assert result.all_completed
    assert len(result.stages) == len(PIPELINE_STAGES)
    assert result.execution_count == len(PIPELINE_STAGES)
    assert result.audit_count == len(PIPELINE_STAGES)
    assert result.benchmark_run_count >= len(PIPELINE_STAGES)

    for stage in result.stages:
        assert stage.run_result.status == ExecutionStatus.COMPLETED
        assert stage.run_result.halted is False
        assert stage.run_result.audit_id is not None
        assert stage.run_result.execution is not None


def test_pipeline_content_artifacts_exist_and_valid(pipeline_dirs):
    governance_root, content_root = pipeline_dirs
    run_panthera_leo_pipeline(
        governance_root=governance_root,
        content_root=content_root,
    )

    for name in EXPECTED_ARTIFACTS:
        path = content_root / name
        assert path.is_file(), f"missing artifact: {name}"

    research = (content_root / "research.md").read_text(encoding="utf-8")
    assert "Panthera leo" in research
    assert _stage_run_id("research") in research

    metadata = json.loads((content_root / "metadata.json").read_text(encoding="utf-8"))
    assert metadata["stable_id"] == "panthera-leo"
    assert metadata["scientific_name"] == "Panthera leo"
    assert metadata["gbif_taxon_key"] == "5219404"
    assert "darwin_core" in metadata
    assert metadata["provenance"]["pipeline"] == "nature-culture-demo-v1"

    classification = json.loads(
        (content_root / "classification.json").read_text(encoding="utf-8")
    )
    assert classification["classification"]["family"] == "Felidae"
    assert classification["classification"]["genus"] == "Panthera"
    assert len(classification["authority_records"]) >= 2

    kg = json.loads((content_root / "knowledge-graph.json").read_text(encoding="utf-8"))
    assert isinstance(kg["nodes"], list) and len(kg["nodes"]) >= 3
    assert isinstance(kg["edges"], list) and len(kg["edges"]) >= 2

    preservation = json.loads(
        (content_root / "preservation-record.json").read_text(encoding="utf-8")
    )
    assert preservation["fixity"]["verified"] is True
    assert len(preservation["premis_events"]) >= 2

    publication = (content_root / "publication-page.md").read_text(encoding="utf-8")
    assert "Panthera leo" in publication
    assert "Editorial gate" in publication


def test_pipeline_persists_runtime_records(pipeline_dirs):
    governance_root, content_root = pipeline_dirs
    run_panthera_leo_pipeline(
        governance_root=governance_root,
        content_root=content_root,
    )

    system = GovernanceSystem.create(governance_root)
    executions = system.runtime.executions.list()
    benchmark_runs = system.runtime.benchmark_runs.list()
    audits = system.audits.list()

    assert len(executions) == len(PIPELINE_STAGES)
    assert len(benchmark_runs) >= len(PIPELINE_STAGES)
    assert len(audits) >= len(PIPELINE_STAGES)

    run_ids = {_stage_run_id(str(stage["stage"])) for stage in PIPELINE_STAGES}
    stored_run_ids = {record.run_id for record in executions}
    assert run_ids <= stored_run_ids

    for record in executions:
        assert record.status == ExecutionStatus.COMPLETED
        assert record.audit_id is not None
        assert record.output_ref is not None
