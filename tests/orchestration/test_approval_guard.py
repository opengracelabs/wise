"""Unit tests for canonical write guard."""

import pytest

from wise_orchestration.nodes import CanonicalWriteForbiddenError, canonical_write_guard


def test_canonical_write_blocked_without_approval():
    state = {
        "agent_id": "wise.agent.metadata",
        "read_only": False,
        "approval_status": "proposed",
    }
    with pytest.raises(CanonicalWriteForbiddenError, match="steward approval"):
        canonical_write_guard(state)


def test_canonical_write_blocked_for_read_only_agent():
    state = {
        "agent_id": "wise.agent.standards",
        "read_only": True,
        "approval_status": "approved",
    }
    with pytest.raises(CanonicalWriteForbiddenError, match="read-only"):
        canonical_write_guard(state)


def test_canonical_write_allowed_after_approval():
    state = {
        "agent_id": "wise.agent.metadata",
        "read_only": False,
        "approval_status": "approved",
        "thread_id": "test-thread",
    }
    result = canonical_write_guard(state)
    assert result["phase"] == "complete"
    assert result["output_ref"].startswith("canonical://")
