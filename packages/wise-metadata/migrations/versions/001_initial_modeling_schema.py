"""Initial Metadata Agent modeling schema.

Revision ID: 001_initial_modeling_schema
Revises:
Create Date: 2026-06-22

Requires registry schema from wise-registry migration 001.
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "001_initial_modeling_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
# NOTE: The registry schema (wise-registry migration 001_initial_source_registry)
# must be applied before this migration — the modeling tables declare foreign keys
# into registry.sources / registry.provenance_events. This ordering is enforced
# operationally (registry → metadata) and by those FK constraints at DDL time.
# A cross-package Alembic ``depends_on`` cannot be used here because the registry
# revision lives in a separate version directory and is not on this package's
# revision path (resolving it raises KeyError during revision-map construction).
depends_on: Union[str, Sequence[str], None] = None

AUDIT_COLUMNS = [
    sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    sa.Column("created_by", sa.String(length=255), server_default="metadata-agent@1.0.0", nullable=False),
    sa.Column("updated_by", sa.String(length=255), server_default="metadata-agent@1.0.0", nullable=False),
    sa.Column("row_version", sa.Integer(), server_default="1", nullable=False),
]


def _create_enum(name: str, values: list[str]) -> None:
    vals = ", ".join(f"'{v}'" for v in values)
    op.execute(
        f"""
        DO $$ BEGIN
            CREATE TYPE modeling.{name} AS ENUM ({vals});
        EXCEPTION WHEN duplicate_object THEN NULL; END $$;
        """
    )


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS modeling")

    _create_enum("source_schema_enum", ["unesco_whc", "wikidata", "wikimedia_commons", "openstreetmap"])
    _create_enum("mapping_target_enum", ["cidoc_crm", "dublin_core", "skos", "darwin_core"])
    _create_enum("assertion_status_enum", ["proposed", "steward_approved", "steward_rejected"])
    _create_enum("validation_status_enum", ["pass", "warn", "fail"])
    _create_enum("validation_domain_enum", ["source", "rights", "schema_cidoc", "schema_dc", "schema_dwc"])
    _create_enum(
        "modeling_event_type_enum",
        ["normalize", "map", "validate", "authority_propose", "steward_approve", "steward_reject"],
    )
    _create_enum("authority_entity_type_enum", ["place", "species", "person", "organization"])
    _create_enum(
        "authority_match_method_enum",
        ["exact", "fuzzy", "coordinate_proximity", "taxonomic_synonym"],
    )
    _create_enum("mapping_run_status_enum", ["pending", "running", "completed", "failed"])

    modeling_event_type = postgresql.ENUM(name="modeling_event_type_enum", schema="modeling", create_type=False)

    op.create_table(
        "provenance_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("event_type", modeling_event_type, nullable=False),
        sa.Column("linked_entity_type", sa.String(length=64), nullable=False),
        sa.Column("linked_entity_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("source_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("registry.sources.id"), nullable=False),
        sa.Column(
            "registry_provenance_event_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("registry.provenance_events.id"),
            nullable=True,
        ),
        sa.Column("actor", sa.String(length=255), nullable=False),
        sa.Column("agent_version", sa.String(length=64), nullable=False),
        sa.Column("evidence_uris", postgresql.ARRAY(sa.Text()), server_default="{}", nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("occurred_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        *AUDIT_COLUMNS,
        sa.PrimaryKeyConstraint("id"),
        schema="modeling",
    )

    source_schema = postgresql.ENUM(name="source_schema_enum", schema="modeling", create_type=False)

    op.create_table(
        "normalized_records",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("source_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("registry.sources.id"), nullable=False),
        sa.Column("external_record_id", sa.String(length=512), nullable=False),
        sa.Column("source_schema", source_schema, nullable=False),
        sa.Column("source_schema_version", sa.String(length=32), server_default="1.0", nullable=False),
        sa.Column("raw_payload", postgresql.JSONB(), nullable=False),
        sa.Column("normalized_payload", postgresql.JSONB(), server_default="{}", nullable=False),
        sa.Column("original_literals", postgresql.JSONB(), server_default="{}", nullable=False),
        sa.Column("language", sa.String(length=16), nullable=True),
        sa.Column(
            "registry_provenance_event_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("registry.provenance_events.id"),
            nullable=True,
        ),
        sa.Column(
            "normalization_event_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("modeling.provenance_events.id"),
            nullable=True,
        ),
        *AUDIT_COLUMNS,
        sa.PrimaryKeyConstraint("id"),
        schema="modeling",
    )

    mapping_target = postgresql.ENUM(name="mapping_target_enum", schema="modeling", create_type=False)

    op.create_table(
        "schema_mappings",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("source_canonical_name", sa.String(length=128), nullable=False),
        sa.Column("source_field_path", sa.String(length=512), nullable=False),
        sa.Column("mapping_target", mapping_target, nullable=False),
        sa.Column("target_term", sa.String(length=256), nullable=False),
        sa.Column("crm_class", sa.String(length=64), nullable=True),
        sa.Column("transform_rule", sa.String(length=64), server_default="direct", nullable=False),
        sa.Column("priority", sa.Integer(), server_default="100", nullable=False),
        sa.Column("active", sa.Boolean(), server_default="true", nullable=False),
        *AUDIT_COLUMNS,
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "source_canonical_name",
            "source_field_path",
            "mapping_target",
            "target_term",
            name="uq_schema_mappings_crosswalk",
        ),
        schema="modeling",
    )

    mapping_run_status = postgresql.ENUM(name="mapping_run_status_enum", schema="modeling", create_type=False)

    op.create_table(
        "mapping_runs",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column(
            "normalized_record_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("modeling.normalized_records.id"),
            nullable=False,
        ),
        sa.Column("source_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("registry.sources.id"), nullable=False),
        sa.Column("agent_version", sa.String(length=64), nullable=False),
        sa.Column("status", mapping_run_status, server_default="pending", nullable=False),
        sa.Column("mappings_applied", sa.Integer(), server_default="0", nullable=False),
        sa.Column("unmapped_fields", postgresql.JSONB(), server_default="[]", nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        *AUDIT_COLUMNS,
        sa.PrimaryKeyConstraint("id"),
        schema="modeling",
    )

    assertion_status = postgresql.ENUM(name="assertion_status_enum", schema="modeling", create_type=False)

    op.create_table(
        "entity_assertion_proposals",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column(
            "mapping_run_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("modeling.mapping_runs.id"),
            nullable=False,
        ),
        sa.Column(
            "normalized_record_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("modeling.normalized_records.id"),
            nullable=False,
        ),
        sa.Column("subject_uri", sa.String(length=512), nullable=False),
        sa.Column("predicate", sa.String(length=256), nullable=False),
        sa.Column("object_value", sa.Text(), nullable=False),
        sa.Column("object_type", sa.String(length=32), server_default="literal", nullable=False),
        sa.Column("language", sa.String(length=16), nullable=True),
        sa.Column("entity_type", sa.String(length=64), nullable=False),
        sa.Column("mapping_target", mapping_target, nullable=False),
        sa.Column("status", assertion_status, server_default="proposed", nullable=False),
        sa.Column("rights_uri", sa.String(length=512), nullable=True),
        sa.Column("evidence", postgresql.JSONB(), nullable=False),
        *AUDIT_COLUMNS,
        sa.PrimaryKeyConstraint("id"),
        schema="modeling",
    )

    authority_entity_type = postgresql.ENUM(name="authority_entity_type_enum", schema="modeling", create_type=False)
    authority_match_method = postgresql.ENUM(name="authority_match_method_enum", schema="modeling", create_type=False)

    op.create_table(
        "authority_record_proposals",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column(
            "normalized_record_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("modeling.normalized_records.id"),
            nullable=False,
        ),
        sa.Column("entity_type", authority_entity_type, nullable=False),
        sa.Column("provisional_uri", sa.String(length=512), nullable=False),
        sa.Column("pref_label", sa.String(length=512), nullable=False),
        sa.Column("alt_labels", postgresql.JSONB(), server_default="[]", nullable=False),
        sa.Column("external_scheme", sa.String(length=64), nullable=False),
        sa.Column("external_id", sa.String(length=128), nullable=False),
        sa.Column("link_type", sa.String(length=32), server_default="exactMatch", nullable=False),
        sa.Column("match_confidence", sa.Float(), nullable=False),
        sa.Column("match_method", authority_match_method, nullable=False),
        sa.Column("status", assertion_status, server_default="proposed", nullable=False),
        sa.Column("skos_payload", postgresql.JSONB(), server_default="{}", nullable=False),
        sa.Column("evidence", postgresql.JSONB(), nullable=False),
        *AUDIT_COLUMNS,
        sa.PrimaryKeyConstraint("id"),
        schema="modeling",
    )

    validation_status = postgresql.ENUM(name="validation_status_enum", schema="modeling", create_type=False)
    validation_domain = postgresql.ENUM(name="validation_domain_enum", schema="modeling", create_type=False)

    op.create_table(
        "validation_results",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column(
            "normalized_record_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("modeling.normalized_records.id"),
            nullable=False,
        ),
        sa.Column("source_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("registry.sources.id"), nullable=False),
        sa.Column(
            "mapping_run_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("modeling.mapping_runs.id"),
            nullable=True,
        ),
        sa.Column("validation_domain", validation_domain, nullable=False),
        sa.Column("status", validation_status, nullable=False),
        sa.Column("severity", sa.String(length=16), server_default="info", nullable=False),
        sa.Column("findings", postgresql.JSONB(), server_default="[]", nullable=False),
        sa.Column(
            "rights_status_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("registry.rights_statuses.id"),
            nullable=True,
        ),
        sa.Column(
            "license_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("registry.licenses.id"),
            nullable=True,
        ),
        sa.Column("evidence", postgresql.JSONB(), nullable=False),
        *AUDIT_COLUMNS,
        sa.PrimaryKeyConstraint("id"),
        schema="modeling",
    )


def downgrade() -> None:
    op.execute("DROP SCHEMA IF EXISTS modeling CASCADE")
