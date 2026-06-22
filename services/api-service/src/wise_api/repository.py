"""Heritage object repository — aggregates RC1 pipeline records."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from wise_contracts import HeritageObjectView
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
)
from wise_api.assembler import assemble_object_view


class ObjectNotFoundError(LookupError):
    """Raised when no approved RC1 object exists for the stable identifier."""


def get_heritage_object(session: Session, stable_id: str) -> HeritageObjectView:
    discovery = session.scalars(
        select(DiscoveryRecord).where(DiscoveryRecord.stable_id == stable_id)
    ).one_or_none()
    if discovery is None:
        raise ObjectNotFoundError(f"Object not found: {stable_id}")

    preservation = session.scalars(
        select(PreservationObject)
        .where(PreservationObject.stable_id == stable_id)
        .options(joinedload(PreservationObject.premis_events))
    ).unique().one()

    metadata = session.scalars(
        select(MetadataRecord).where(MetadataRecord.stable_id == stable_id)
    ).one()

    assertion = session.scalars(
        select(EntityAssertion).where(EntityAssertion.metadata_record_id == metadata.id)
    ).one()

    graph_entity = session.scalars(
        select(GraphEntity)
        .where(GraphEntity.stable_id == stable_id)
        .options(joinedload(GraphEntity.external_links))
    ).unique().one()

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

    return assemble_object_view(
        source=source,
        discovery=discovery,
        preservation=preservation,
        premis_events=premis_events,
        metadata=metadata,
        assertion=assertion,
        graph_entity=graph_entity,
        external_links=external_links,
        quality=quality,
    )
