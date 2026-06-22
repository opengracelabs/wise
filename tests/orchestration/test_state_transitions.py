"""State transition tests for RC1 pipeline nodes."""

from __future__ import annotations

from wise_contracts.common import ApprovalStatus
from wise_orchestration.nodes import (
    knowledge_graph_node,
    metadata_node,
    preservation_node,
    quality_review_node,
    source_discovery_node,
)
from wise_orchestration.state import PipelineStage, initial_state_for_stonehenge


def test_source_discovery_emits_proposed_record():
    state = initial_state_for_stonehenge()
    patch = source_discovery_node(state)
    assert patch["discovery_record"]["status"] == ApprovalStatus.PROPOSED.value
    assert patch["current_stage"] == PipelineStage.SOURCE_DISCOVERY.value
    assert patch["pending_interrupt"] is True
    assert len(patch["provenance_chain"]) >= 1


def test_preservation_links_discovery():
    base = initial_state_for_stonehenge()
    discovery = source_discovery_node(base)
    merged = {**base, **discovery}
    patch = preservation_node(merged)
    assert patch["preserved_object"]["status"] == ApprovalStatus.PROPOSED.value
    assert patch["preserved_object"]["discovery_record_id"] == discovery["discovery_record"]["id"]
    assert len(patch["premis_events"]) >= 2


def test_metadata_emits_assertion_with_evidence():
    base = initial_state_for_stonehenge()
    discovery = source_discovery_node(base)
    preservation = preservation_node({**base, **discovery})
    merged = {**base, **discovery, **preservation}
    patch = metadata_node(merged)
    assertion = patch["entity_assertion"]
    assert assertion["status"] == ApprovalStatus.PROPOSED.value
    assert assertion["evidence"]["provenance_event_id"]
    assert assertion["entity_type"] == "crm:E27_Site"


def test_knowledge_graph_external_link():
    base = initial_state_for_stonehenge()
    discovery = source_discovery_node(base)
    preservation = preservation_node({**base, **discovery})
    metadata = metadata_node({**base, **discovery, **preservation})
    merged = {**base, **discovery, **preservation, **metadata}
    patch = knowledge_graph_node(merged)
    links = patch["graph_entity"]["external_links"]
    assert links[0]["external_identifier"] == "Q39671"
    assert links[0]["status"] == ApprovalStatus.PROPOSED.value


def test_quality_review_composite_score():
    base = initial_state_for_stonehenge()
    discovery = source_discovery_node(base)
    preservation = preservation_node({**base, **discovery})
    metadata = metadata_node({**base, **discovery, **preservation})
    graph = knowledge_graph_node({**base, **discovery, **preservation, **metadata})
    merged = {**base, **discovery, **preservation, **metadata, **graph}
    patch = quality_review_node(merged)
    review = patch["quality_review"]
    assert review["composite_score"] >= 0.9
    assert review["status"] == ApprovalStatus.PROPOSED.value
