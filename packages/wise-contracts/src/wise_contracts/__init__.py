"""WISE canonical interface contracts."""

from wise_contracts.common import ApprovalStatus, EvidenceOutputProfile, ProvenanceRef
from wise_contracts.commerce import (
    CommerceProduct,
    CommercePrototype,
    CommerceProviderValidation,
    IntelligenceSignal,
    MarketingDashboardMetrics,
    PinterestAssetSpec,
    PromotionPipelineStage,
)
from wise_contracts.discovery import DiscoveryRecord, ExternalIdentifiers
from wise_contracts.graph import ExternalLink, GraphEntity
from wise_contracts.metadata import AuthorityLink, EntityAssertion, MetadataRecord
from wise_contracts.object_view import HeritageObjectView, SourceRegistryRef
from wise_contracts.preservation import FixityRecord, PremisEvent, PreservedObjectDescriptor
from wise_contracts.quality import QualityDimensionScore, QualityReviewRecord
from wise_contracts.protected_area import (
    ConservationMetadata,
    MapAreaSummary,
    MapSearchResult,
    ProtectedAreaIdentifiers,
    ProtectedAreaObjectView,
    ProtectedAreaRegistryEntry,
)
from wise_contracts.orchestration import (
    AgentPlane,
    AgentRegistryEntry,
    AgentRunRecord,
    AgentStatus,
    BenchmarkReport,
    CapabilityAgentLink,
    CapabilityRegistryEntry,
    CapabilityRole,
    RunResumeRequest,
    RunStartRequest,
    RunStatus,
    RC1RunResumeRequest,
    RC1RunStartRequest,
    StandardsComplianceReport,
    StewardApprovalRequest,
)
from wise_contracts.species import (
    DarwinCoreOverlay,
    GbifExternalIdentifiers,
    SpeciesObjectView,
    SpeciesRegistryEntry,
    TaxonomicBackboneNode,
)

__version__ = "0.1.0"

__all__ = [
    "AgentPlane",
    "AgentRegistryEntry",
    "AgentRunRecord",
    "AgentStatus",
    "BenchmarkReport",
    "CapabilityAgentLink",
    "CapabilityRegistryEntry",
    "CapabilityRole",
    "ApprovalStatus",
    "AuthorityLink",
    "CommerceProduct",
    "CommercePrototype",
    "CommerceProviderValidation",
    "DarwinCoreOverlay",
    "DiscoveryRecord",
    "EntityAssertion",
    "EvidenceOutputProfile",
    "ExternalIdentifiers",
    "ExternalLink",
    "FixityRecord",
    "GbifExternalIdentifiers",
    "GraphEntity",
    "ConservationMetadata",
    "HeritageObjectView",
    "IntelligenceSignal",
    "MapAreaSummary",
    "MapSearchResult",
    "MarketingDashboardMetrics",
    "MetadataRecord",
    "PinterestAssetSpec",
    "ProtectedAreaIdentifiers",
    "ProtectedAreaObjectView",
    "ProtectedAreaRegistryEntry",
    "PremisEvent",
    "PromotionPipelineStage",
    "PreservedObjectDescriptor",
    "ProvenanceRef",
    "QualityDimensionScore",
    "QualityReviewRecord",
    "RC1RunResumeRequest",
    "RC1RunStartRequest",
    "RunResumeRequest",
    "RunStartRequest",
    "RunStatus",
    "SourceRegistryRef",
    "SpeciesObjectView",
    "SpeciesRegistryEntry",
    "StandardsComplianceReport",
    "StewardApprovalRequest",
    "TaxonomicBackboneNode",
]
