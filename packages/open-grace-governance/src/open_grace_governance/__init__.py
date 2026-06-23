"""Open Grace Agent Governance System v1 — shared foundation."""

from open_grace_governance.lifecycle import (
    LIFECYCLE_TRANSITIONS,
    LifecycleStage,
    advance_lifecycle,
    can_transition,
)
from open_grace_governance.reference_models import REFERENCE_MODELS, ReferenceModelProfile
from open_grace_governance.schemas import (
    AgentRegistryRecord,
    AuditRegistryRecord,
    BenchmarkRegistryRecord,
    CapabilityRegistryRecord,
    ModelRegistryRecord,
    RiskRegistryRecord,
    StandardsRegistryRecord,
)
from open_grace_governance.validation import ValidationResult, validate_entry
from open_grace_governance.validation.rules import validate_capability_framework_record

__version__ = "1.0.0"

__all__ = [
    "LIFECYCLE_TRANSITIONS",
    "LifecycleStage",
    "REFERENCE_MODELS",
    "ReferenceModelProfile",
    "AgentRegistryRecord",
    "AuditRegistryRecord",
    "BenchmarkRegistryRecord",
    "CapabilityRegistryRecord",
    "ModelRegistryRecord",
    "RiskRegistryRecord",
    "StandardsRegistryRecord",
    "ValidationResult",
    "advance_lifecycle",
    "can_transition",
    "validate_capability_framework_record",
    "validate_entry",
]
