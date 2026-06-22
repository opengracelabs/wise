"""Smoke tests — no infrastructure required."""

import importlib

import pytest

SERVICES = [
    ("discovery_service", "discovery-service"),
    ("metadata_service", "metadata-service"),
    ("wise_preservation", "preservation-service"),
    ("wise_knowledge_graph", "knowledge-graph-service"),
    ("wise_api", "api-service"),
]


@pytest.mark.smoke
@pytest.mark.parametrize("module_name,service_name", SERVICES)
def test_service_module_imports(module_name: str, service_name: str) -> None:
    module = importlib.import_module(f"{module_name}.main")
    assert hasattr(module, "app")
    assert module.app.title is not None


@pytest.mark.smoke
def test_wise_common_imports() -> None:
    from wise_common.config import ServiceSettings

    settings = ServiceSettings(service_name="test")
    assert settings.service_name == "test"


@pytest.mark.smoke
def test_wise_contracts_imports() -> None:
    import wise_contracts

    assert wise_contracts.__version__


@pytest.mark.smoke
def test_wise_registry_imports() -> None:
    from wise_registry import Base
    from wise_registry.models import License, ProvenanceEvent, RightsStatus, Source, SourceType

    assert Base.metadata is not None
    assert {Source, SourceType, License, RightsStatus, ProvenanceEvent}


@pytest.mark.smoke
def test_wise_discovery_imports() -> None:
    from wise_discovery import (
        build_evidence_profile,
        check_reachability,
        create_discovery_record,
        lookup_source,
        validate_source,
    )

    assert callable(build_evidence_profile)
    assert callable(check_reachability)
    assert callable(create_discovery_record)
    assert callable(lookup_source)
    assert callable(validate_source)


@pytest.mark.smoke
def test_wise_metadata_imports() -> None:
    from wise_metadata import Base
    from wise_metadata.models import EntityAssertionProposal, NormalizedRecord, SchemaMapping

    assert Base.metadata is not None
    assert {EntityAssertionProposal, NormalizedRecord, SchemaMapping}


@pytest.mark.smoke
def test_wise_recognition_intelligence_imports() -> None:
    from wise_recognition_intelligence import calculate_recognition_score, evaluate_asset

    assert callable(calculate_recognition_score)
    assert callable(evaluate_asset)


@pytest.mark.smoke
def test_wise_commercial_intelligence_imports() -> None:
    from wise_commercial_intelligence import calculate_commercial_score, rank_assets

    assert callable(calculate_commercial_score)
    assert callable(rank_assets)
