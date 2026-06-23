"""Lifecycle stages for governed registry entries."""

from __future__ import annotations

from enum import StrEnum


class LifecycleStage(StrEnum):
    PROPOSAL = "proposal"
    REVIEW = "review"
    BENCHMARK = "benchmark"
    APPROVAL = "approval"
    PUBLICATION = "publication"
    AUDIT = "audit"
    RETIREMENT = "retirement"


LIFECYCLE_TRANSITIONS: dict[LifecycleStage, tuple[LifecycleStage, ...]] = {
    LifecycleStage.PROPOSAL: (LifecycleStage.REVIEW,),
    LifecycleStage.REVIEW: (LifecycleStage.PROPOSAL, LifecycleStage.BENCHMARK),
    LifecycleStage.BENCHMARK: (LifecycleStage.REVIEW, LifecycleStage.APPROVAL),
    LifecycleStage.APPROVAL: (LifecycleStage.BENCHMARK, LifecycleStage.PUBLICATION),
    LifecycleStage.PUBLICATION: (LifecycleStage.AUDIT, LifecycleStage.RETIREMENT),
    LifecycleStage.AUDIT: (LifecycleStage.PUBLICATION, LifecycleStage.RETIREMENT),
    LifecycleStage.RETIREMENT: (),
}


class LifecycleTransitionError(ValueError):
    """Raised when a lifecycle transition is not permitted."""


def can_transition(
    current: LifecycleStage,
    target: LifecycleStage,
) -> bool:
    return target in LIFECYCLE_TRANSITIONS[current]


def advance_lifecycle(
    current: LifecycleStage,
    target: LifecycleStage,
) -> LifecycleStage:
    if not can_transition(current, target):
        allowed = ", ".join(stage.value for stage in LIFECYCLE_TRANSITIONS[current])
        raise LifecycleTransitionError(
            f"Cannot transition from {current.value} to {target.value}; "
            f"allowed: {allowed or '(terminal)'}"
        )
    return target
