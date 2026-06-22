"""Species repository — aggregates RC2 pipeline records."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from wise_contracts import SpeciesObjectView
from wise_api.source_lookup import resolve_source
from wise_reference.models import (
    DiscoveryRecord,
    EntityAssertion,
    ExternalLink,
    GraphEntity,
    MetadataRecord,
    PremisEvent,
    PreservationObject,
    QualityReview,
    SpeciesBackboneLink,
    SpeciesRegistryEntry,
    TaxonomicBackboneNode,
)

from wise_api.species_assembler import assemble_species_view


class SpeciesNotFoundError(LookupError):
    """Raised when no approved RC2 species exists for the stable identifier."""


def get_species_object(session: Session, stable_id: str) -> SpeciesObjectView:
    species_registry = session.scalars(
        select(SpeciesRegistryEntry).where(SpeciesRegistryEntry.stable_id == stable_id)
    ).one_or_none()
    if species_registry is None:
        raise SpeciesNotFoundError(f"Species not found: {stable_id}")

    discovery = session.scalars(
        select(DiscoveryRecord).where(DiscoveryRecord.stable_id == stable_id)
    ).one()

    preservation = session.scalars(
        select(PreservationObject).where(PreservationObject.stable_id == stable_id)
    ).one()

    metadata = session.scalars(
        select(MetadataRecord).where(MetadataRecord.stable_id == stable_id)
    ).one()

    assertion = session.scalars(
        select(EntityAssertion).where(EntityAssertion.metadata_record_id == metadata.id)
    ).one()

    graph_entity = session.scalars(
        select(GraphEntity).where(GraphEntity.stable_id == stable_id)
    ).one()

    quality = session.scalars(
        select(QualityReview).where(QualityReview.graph_entity_id == graph_entity.id)
    ).one()

    source = resolve_source(session, discovery.source_registry_ref)

    premis_events = session.scalars(
        select(PremisEvent)
        .where(PremisEvent.preservation_object_id == preservation.id)
        .order_by(PremisEvent.event_timestamp)
    ).all()

    external_links = session.scalars(
        select(ExternalLink).where(ExternalLink.entity_id == graph_entity.id)
    ).all()

    backbone_ids = session.scalars(
        select(SpeciesBackboneLink.backbone_node_id).where(
            SpeciesBackboneLink.species_registry_id == species_registry.id
        )
    ).all()

    backbone_nodes = session.scalars(
        select(TaxonomicBackboneNode).where(TaxonomicBackboneNode.id.in_(backbone_ids))
    ).all()

    return assemble_species_view(
        source=source,
        species_registry=species_registry,
        backbone_nodes=list(backbone_nodes),
        discovery=discovery,
        preservation=preservation,
        premis_events=premis_events,
        metadata=metadata,
        assertion=assertion,
        graph_entity=graph_entity,
        external_links=external_links,
        quality=quality,
    )
