"""Integration tests for RC1 service propose endpoints."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from discovery_service.main import app as discovery_app
from wise_knowledge_graph.main import app as graph_app
from wise_preservation.main import app as preservation_app
from metadata_service.main import app as metadata_app


@pytest.mark.integration
def test_discovery_propose_stonehenge(orchestration_db_session):
    client = TestClient(discovery_app)
    response = client.post(
        "/v1/rc1/discovery/propose",
        json={"stable_id": "stonehenge"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["record"]["stable_id"] == "stonehenge"
    assert body["record"]["status"] == "proposed"
    assert "unesco" in body["source_registry_refs"]
    assert body["provenance_event_id"]


@pytest.mark.integration
def test_preservation_propose_stonehenge():
    client = TestClient(preservation_app)
    response = client.post(
        "/v1/rc1/preservation/propose",
        json={"stable_id": "stonehenge", "discovery_record_id": "test-id"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["object_descriptor"]["stable_id"] == "stonehenge"
    assert body["provenance_event_id"]


@pytest.mark.integration
def test_metadata_and_quality_propose_stonehenge():
    meta = TestClient(metadata_app)
    md = meta.post(
        "/v1/rc1/metadata/propose",
        json={"stable_id": "stonehenge", "preserved_object_ark": "ark:/99999/373/stonehenge/"},
    )
    assert md.status_code == 200
    assert md.json()["entity_assertion"]["evidence"]["provenance_event_id"]

    qr = meta.post(
        "/v1/rc1/quality/propose",
        json={
            "stable_id": "stonehenge",
            "graph_entity_uri": "https://wise.example.org/entity/stonehenge",
        },
    )
    assert qr.status_code == 200
    assert qr.json()["quality_review"]["disposition"] is None


@pytest.mark.integration
def test_graph_propose_stonehenge():
    client = TestClient(graph_app)
    response = client.post(
        "/v1/rc1/graph/propose",
        json={"stable_id": "stonehenge", "entity_assertion_id": "test-assertion"},
    )
    assert response.status_code == 200
    assert response.json()["graph_entity"]["status"] == "proposed"
