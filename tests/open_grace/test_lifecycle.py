import pytest

from open_grace_governance.lifecycle import LifecycleStage, LifecycleTransitionError, advance_lifecycle


def test_forward_lifecycle_chain():
    stage = LifecycleStage.PROPOSAL
    for target in (
        LifecycleStage.REVIEW,
        LifecycleStage.BENCHMARK,
        LifecycleStage.APPROVAL,
        LifecycleStage.PUBLICATION,
    ):
        stage = advance_lifecycle(stage, target)
    assert stage == LifecycleStage.PUBLICATION


def test_review_can_return_to_proposal():
    stage = advance_lifecycle(LifecycleStage.REVIEW, LifecycleStage.PROPOSAL)
    assert stage == LifecycleStage.PROPOSAL


def test_retirement_is_terminal():
    with pytest.raises(LifecycleTransitionError):
        advance_lifecycle(LifecycleStage.RETIREMENT, LifecycleStage.PUBLICATION)
