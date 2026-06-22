"""Shared assembly helpers for heritage and species views."""

from __future__ import annotations

from wise_contracts import (
    ApprovalStatus,
    AuthorityLink,
    DiscoveryRecord as DiscoveryContract,
    EntityAssertion as EntityAssertionContract,
    EvidenceOutputProfile,
    ExternalIdentifiers,
    ExternalLink as ExternalLinkContract,
    FixityRecord,
    GraphEntity as GraphEntityContract,
    MetadataRecord as MetadataContract,
    PremisEvent as PremisContract,
    PreservedObjectDescriptor,
    ProvenanceRef,
    QualityDimensionScore,
    QualityReviewRecord,
    SourceRegistryRef,
)
from wise_registry.models import Source
from wise_reference.models import (
    DiscoveryRecord,
    EntityAssertion,
    ExternalLink,
    GraphEntity,
    MetadataRecord,
    PremisEvent,
    PreservationObject,
    QualityReview,
)


def provenance_from_dict(data: dict) -> ProvenanceRef:
    return ProvenanceRef(
        event_id=data["event_id"],
        event_type=data["event_type"],
        agent_version=data["agent_version"],
        event_timestamp=data["event_timestamp"],
        actor_id=data.get("actor_id", "system"),
    )


def source_registry_ref(source: Source) -> SourceRegistryRef:
    stable_id = getattr(source, "stable_id", None) or source.canonical_name
    return SourceRegistryRef(
        stable_id=stable_id,
        name=source.display_name,
        institution_name=None,
        base_uri=source.homepage_url,
        rights_posture_summary=None,
        covenant_status=source.trust_level.value,
    )


def assemble_discovery(discovery: DiscoveryRecord) -> DiscoveryContract:
    discovery_data = discovery.record_data
    return DiscoveryContract(
        id=str(discovery.id),
        stable_id=discovery.stable_id,
        status=ApprovalStatus(discovery.status.value),
        title=discovery.title,
        description=discovery_data.get("description"),
        source_registry_ref=discovery.source_registry_ref,
        rights_uri=discovery.rights_uri,
        ingestion_candidacy_score=discovery.ingestion_candidacy_score,
        external_identifiers=ExternalIdentifiers(**discovery.external_identifiers),
        evidence=EvidenceOutputProfile(**discovery_data["evidence"]),
        provenance=provenance_from_dict(discovery_data["provenance"]),
        discovered_at=discovery_data["discovered_at"],
        json_ld=discovery_data,
    )


def assemble_preservation(
    preservation: PreservationObject,
    discovery_id: str,
) -> tuple[PreservedObjectDescriptor, list[PremisContract]]:
    descriptor = preservation.object_descriptor
    preservation_contract = PreservedObjectDescriptor(
        ark=preservation.ark,
        stable_id=preservation.stable_id,
        status=ApprovalStatus(preservation.status.value),
        format_uri=descriptor.get("format_uri", ""),
        format_label=descriptor.get("format_label", ""),
        fixity=FixityRecord(
            algorithm=descriptor["fixity"]["algorithm"],
            digest=descriptor["fixity"]["digest"],
            verified_at=descriptor["fixity"]["verified_at"],
            result=descriptor["fixity"]["result"],
        ),
        storage_tier=preservation.storage_tier,
        replica_count=descriptor.get("replica_count", 1),
        minio_key=preservation.minio_key,
        rights_uri=preservation.rights_uri,
        provenance=provenance_from_dict(descriptor["provenance"]),
        discovery_record_id=discovery_id,
        ingest_event_id=preservation.ingest_event_id,
    )
    return preservation_contract, []


def assemble_premis_events(
    preservation: PreservationObject,
    premis_events: list[PremisEvent],
) -> list[PremisContract]:
    return [
        PremisContract(
            id=str(event.id),
            event_type=event.event_type,
            event_timestamp=event.event_timestamp,
            agent_version=event.agent_version,
            actor_id=event.actor_id,
            preservation_object_ark=preservation.ark,
            event_detail=event.event_detail,
            evidence_uris=event.evidence_uris or [],
            outcome=event.outcome,
        )
        for event in premis_events
    ]


def assemble_metadata(metadata: MetadataRecord, ark: str) -> MetadataContract:
    metadata_data = metadata.record_data
    return MetadataContract(
        id=str(metadata.id),
        stable_id=metadata.stable_id,
        status=ApprovalStatus(metadata.status.value),
        source_schema=metadata.source_schema,
        source_schema_version=metadata.source_schema_version,
        preserved_object_ark=ark,
        title=metadata.title,
        description=metadata_data.get("description"),
        language=metadata_data.get("language", "en"),
        rights_uri=metadata.rights_uri,
        field_mappings=metadata_data.get("field_mappings", {}),
        original_literals=metadata_data.get("original_literals", {}),
        provenance=provenance_from_dict(metadata_data["provenance"]),
    )


def assemble_assertion(assertion: EntityAssertion, metadata_id: str) -> EntityAssertionContract:
    assertion_data = assertion.assertion_data
    return EntityAssertionContract(
        id=str(assertion.id),
        status=ApprovalStatus(assertion.status.value),
        entity_uri=assertion.entity_uri,
        entity_type=assertion.entity_type,
        pref_label=assertion.pref_label,
        alt_labels=assertion_data.get("alt_labels", []),
        descriptive_overlay=assertion_data.get("descriptive_overlay", {}),
        authority_links=[AuthorityLink(**link) for link in assertion_data.get("authority_links", [])],
        geographic_anchor=assertion_data.get("geographic_anchor"),
        temporal_bounds=assertion_data.get("temporal_bounds"),
        rights_uri=assertion.rights_uri,
        evidence=EvidenceOutputProfile(**assertion_data["evidence"]),
        provenance=provenance_from_dict(assertion_data["provenance"]),
        metadata_record_id=metadata_id,
        rdf_triples=assertion_data.get("rdf_triples", []),
    )


def assemble_graph(
    graph_entity: GraphEntity,
    external_links: list[ExternalLink],
    assertion_id: str,
) -> GraphEntityContract:
    link_contracts = [
        ExternalLinkContract(
            id=str(link.id),
            status=ApprovalStatus(link.status.value),
            external_authority=link.external_authority,
            external_identifier=link.external_identifier,
            link_type=link.link_type,
            evidence=EvidenceOutputProfile(**link.link_data["evidence"]),
        )
        for link in external_links
    ]
    return GraphEntityContract(
        id=str(graph_entity.id),
        entity_uri=graph_entity.entity_uri,
        stable_id=graph_entity.stable_id,
        status=ApprovalStatus(graph_entity.status.value),
        label=graph_entity.label,
        entity_type=graph_entity.entity_type,
        entity_assertion_id=assertion_id,
        external_links=link_contracts,
        relationships=graph_entity.entity_data.get("relationships", []),
    )


def assemble_quality(quality: QualityReview) -> QualityReviewRecord:
    quality_data = quality.review_data
    return QualityReviewRecord(
        id=str(quality.id),
        status=ApprovalStatus(quality.status.value),
        entity_uri=quality.entity_uri,
        preservation_ark=quality.preservation_ark,
        review_domain=quality.review_domain,
        severity=quality.severity,
        finding=quality.finding,
        recommended_action=quality.recommended_action,
        composite_score=quality.composite_score,
        dimension_scores=[
            QualityDimensionScore(**score) for score in quality_data.get("dimension_scores", [])
        ],
        disposition=quality.disposition,
        provenance=provenance_from_dict(quality_data["provenance"]),
        reviewed_at=quality.reviewed_at,
    )


def quality_flags(quality_data: dict) -> tuple[bool, bool, bool]:
    rights_verified = all(
        score["passed"]
        for score in quality_data.get("dimension_scores", [])
        if score["dimension"] == "rights"
    )
    quality_approved = quality_data.get("disposition") == "accepted"
    accessibility_compliant = all(
        score["passed"]
        for score in quality_data.get("dimension_scores", [])
        if score["dimension"] == "accessibility"
    )
    return rights_verified, quality_approved, accessibility_compliant
