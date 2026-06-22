"""Reference Capability 1 schema tables.

Revision ID: 001_rc1_schemas
Revises:
Create Date: 2026-06-22
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "001_rc1_schemas"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

AUDIT_COLUMNS = [
    sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    sa.Column("created_by", sa.String(length=255), server_default="system", nullable=False),
    sa.Column("updated_by", sa.String(length=255), server_default="system", nullable=False),
    sa.Column("row_version", sa.Integer(), server_default="1", nullable=False),
]

APPROVAL_VALUES = ("proposed", "approved", "rejected", "superseded")


def _approval_enum(schema: str) -> postgresql.ENUM:
    return postgresql.ENUM(
        *APPROVAL_VALUES,
        name="approval_status_enum",
        schema=schema,
        create_type=False,
    )


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        sa.text(
            """
            DO $$ BEGIN
                ALTER TABLE alembic_version_reference ALTER COLUMN version_num TYPE VARCHAR(128);
            EXCEPTION
                WHEN undefined_table THEN NULL;
            END $$;
            """
        )
    )

    for schema in ("discovery", "preservation", "modeling", "graph", "quality"):
        op.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")

    discovery_status = _approval_enum("discovery")
    preservation_status = _approval_enum("preservation")
    modeling_status = _approval_enum("modeling")
    graph_status = _approval_enum("graph")
    quality_status = _approval_enum("quality")

    for enum in (
        discovery_status,
        preservation_status,
        modeling_status,
        graph_status,
        quality_status,
    ):
        enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "records",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("stable_id", sa.String(length=128), nullable=False),
        sa.Column("status", discovery_status, server_default="proposed", nullable=False),
        sa.Column("title", sa.String(length=512), nullable=False),
        sa.Column("source_registry_ref", sa.String(length=128), nullable=False),
        sa.Column("rights_uri", sa.String(length=512), nullable=False),
        sa.Column("ingestion_candidacy_score", sa.Float(), nullable=False),
        sa.Column("external_identifiers", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("record_data", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("provenance_event_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("discovery_event_id", sa.String(length=128), nullable=False),
        *AUDIT_COLUMNS,
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("stable_id", name="uq_discovery_records_stable_id"),
        schema="discovery",
    )

    op.create_table(
        "objects",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("stable_id", sa.String(length=128), nullable=False),
        sa.Column("ark", sa.String(length=255), nullable=False),
        sa.Column("status", preservation_status, server_default="proposed", nullable=False),
        sa.Column("discovery_record_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("object_descriptor", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("fixity_digest", sa.String(length=128), nullable=False),
        sa.Column("fixity_verified_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("storage_tier", sa.String(length=8), server_default="T0", nullable=False),
        sa.Column("minio_key", sa.String(length=512), nullable=True),
        sa.Column("rights_uri", sa.String(length=512), nullable=False),
        sa.Column("ingest_event_id", sa.String(length=128), nullable=False),
        *AUDIT_COLUMNS,
        sa.ForeignKeyConstraint(["discovery_record_id"], ["discovery.records.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("stable_id", name="uq_preservation_objects_stable_id"),
        sa.UniqueConstraint("ark", name="uq_preservation_objects_ark"),
        schema="preservation",
    )

    op.create_table(
        "premis_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("preservation_object_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("event_timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("agent_version", sa.String(length=64), nullable=False),
        sa.Column("actor_id", sa.String(length=255), server_default="system", nullable=False),
        sa.Column("event_detail", sa.Text(), nullable=False),
        sa.Column("evidence_uris", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("outcome", sa.String(length=32), server_default="success", nullable=False),
        sa.Column("event_data", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        *AUDIT_COLUMNS,
        sa.ForeignKeyConstraint(["preservation_object_id"], ["preservation.objects.id"]),
        sa.PrimaryKeyConstraint("id"),
        schema="preservation",
    )

    op.create_table(
        "metadata_records",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("stable_id", sa.String(length=128), nullable=False),
        sa.Column("status", modeling_status, server_default="proposed", nullable=False),
        sa.Column("preservation_object_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("source_schema", sa.String(length=128), nullable=False),
        sa.Column("source_schema_version", sa.String(length=32), nullable=False),
        sa.Column("title", sa.String(length=512), nullable=False),
        sa.Column("rights_uri", sa.String(length=512), nullable=False),
        sa.Column("record_data", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("modeling_event_id", sa.String(length=128), nullable=False),
        *AUDIT_COLUMNS,
        sa.ForeignKeyConstraint(["preservation_object_id"], ["preservation.objects.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("stable_id", name="uq_metadata_records_stable_id"),
        schema="modeling",
    )

    op.create_table(
        "entity_assertions",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("metadata_record_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("status", modeling_status, server_default="proposed", nullable=False),
        sa.Column("entity_uri", sa.String(length=512), nullable=False),
        sa.Column("entity_type", sa.String(length=128), nullable=False),
        sa.Column("pref_label", sa.String(length=512), nullable=False),
        sa.Column("rights_uri", sa.String(length=512), nullable=False),
        sa.Column("assertion_data", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        *AUDIT_COLUMNS,
        sa.ForeignKeyConstraint(["metadata_record_id"], ["modeling.metadata_records.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("entity_uri", name="uq_entity_assertions_entity_uri"),
        schema="modeling",
    )

    op.create_table(
        "entities",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("stable_id", sa.String(length=128), nullable=False),
        sa.Column("entity_uri", sa.String(length=512), nullable=False),
        sa.Column("status", graph_status, server_default="proposed", nullable=False),
        sa.Column("label", sa.String(length=512), nullable=False),
        sa.Column("entity_type", sa.String(length=128), nullable=False),
        sa.Column("entity_assertion_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("entity_data", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        *AUDIT_COLUMNS,
        sa.ForeignKeyConstraint(["entity_assertion_id"], ["modeling.entity_assertions.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("stable_id", name="uq_graph_entities_stable_id"),
        sa.UniqueConstraint("entity_uri", name="uq_graph_entities_entity_uri"),
        schema="graph",
    )

    op.create_table(
        "external_links",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("entity_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("status", graph_status, server_default="proposed", nullable=False),
        sa.Column("external_authority", sa.String(length=64), nullable=False),
        sa.Column("external_identifier", sa.String(length=128), nullable=False),
        sa.Column("link_type", sa.String(length=32), server_default="sameAs", nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("link_data", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        *AUDIT_COLUMNS,
        sa.ForeignKeyConstraint(["entity_id"], ["graph.entities.id"]),
        sa.PrimaryKeyConstraint("id"),
        schema="graph",
    )

    op.create_table(
        "reviews",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("entity_uri", sa.String(length=512), nullable=False),
        sa.Column("preservation_ark", sa.String(length=255), nullable=False),
        sa.Column("graph_entity_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("status", quality_status, server_default="proposed", nullable=False),
        sa.Column("review_domain", sa.String(length=64), nullable=False),
        sa.Column("severity", sa.String(length=32), nullable=False),
        sa.Column("finding", sa.Text(), nullable=False),
        sa.Column("recommended_action", sa.Text(), nullable=False),
        sa.Column("composite_score", sa.Float(), nullable=False),
        sa.Column("disposition", sa.String(length=32), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("review_data", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        *AUDIT_COLUMNS,
        sa.ForeignKeyConstraint(["graph_entity_id"], ["graph.entities.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("entity_uri", name="uq_quality_reviews_entity_uri"),
        schema="quality",
    )


def downgrade() -> None:
    op.drop_table("reviews", schema="quality")
    op.drop_table("external_links", schema="graph")
    op.drop_table("entities", schema="graph")
    op.drop_table("entity_assertions", schema="modeling")
    op.drop_table("metadata_records", schema="modeling")
    op.drop_table("premis_events", schema="preservation")
    op.drop_table("objects", schema="preservation")
    op.drop_table("records", schema="discovery")

    for schema in ("quality", "graph", "modeling", "preservation", "discovery"):
        op.execute(f"DROP TYPE IF EXISTS {schema}.approval_status_enum")

    for schema in ("quality", "graph", "modeling", "preservation", "discovery"):
        op.execute(f"DROP SCHEMA IF EXISTS {schema} CASCADE")
