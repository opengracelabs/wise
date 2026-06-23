"""Registry enumerations aligned with architecture-v1.0."""

from __future__ import annotations

import enum


class TrustLevel(str, enum.Enum):
    """Institutional trust tier for registered sources."""

    AUTHORITATIVE = "authoritative"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNVERIFIED = "unverified"


class ProvenanceEventType(str, enum.Enum):
    """PREMIS-aligned registry event types."""

    REGISTER = "register"
    UPDATE = "update"
    HARVEST = "harvest"
    APPROVE = "approve"
    DEPRECATE = "deprecate"
    LINK = "link"


class VerificationStatus(str, enum.Enum):
    """RC17 verification gate state for source, license, and provenance checks."""

    PENDING = "pending"
    VERIFIED = "verified"
    FAILED = "failed"


class ApprovalWorkflowStatus(str, enum.Enum):
    """RC17 human approval workflow state."""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    REVOKED = "revoked"


class AgentPlane(str, enum.Enum):
    PLATFORM = "platform"
    EXPERIENCE = "experience"
    CONSTITUTIONAL = "constitutional"


class AgentStatus(str, enum.Enum):
    REGISTERED = "registered"
    CANDIDATE = "candidate"
    PRODUCTION = "production"
    SUSPENDED = "suspended"
    WITHDRAWN = "withdrawn"


class CapabilityRole(str, enum.Enum):
    PRIMARY = "primary"
    SUPPORTING = "supporting"
    GOVERNANCE = "governance"


class RunStatus(str, enum.Enum):
    RUNNING = "running"
    INTERRUPTED = "interrupted"
    COMPLETED = "completed"
    FAILED = "failed"


class StewardTaskStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"
