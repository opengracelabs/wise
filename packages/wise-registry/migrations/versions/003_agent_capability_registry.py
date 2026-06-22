"""Agent and Capability Registry + orchestration schema.

Revision ID: 003_agent_capability_registry
Revises: 002_seed_initial_sources
Create Date: 2026-06-22

"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "003_agent_capability_registry"
down_revision: Union[str, None] = "002_seed_initial_sources"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

AUDIT_COLUMNS = [
    sa.Column(
        "created_at",
        sa.DateTime(timezone=True),
        server_default=sa.text("now()"),
        nullable=False,
    ),
    sa.Column(
        "updated_at",
        sa.DateTime(timezone=True),
        server_default=sa.text("now()"),
        nullable=False,
    ),
    sa.Column(
        "created_by",
        sa.String(length=255),
        server_default="system",
        nullable=False,
    ),
    sa.Column(
        "updated_by",
        sa.String(length=255),
        server_default="system",
        nullable=False,
    ),
    sa.Column(
        "row_version",
        sa.Integer(),
        server_default="1",
        nullable=False,
    ),
]


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS orchestration")

    op.execute(
        """
        DO $$ BEGIN
            CREATE TYPE registry.agent_plane_enum AS ENUM (
                'platform', 'experience', 'constitutional'
            );
        EXCEPTION WHEN duplicate_object THEN NULL; END $$;
        """
    )
    op.execute(
        """
        DO $$ BEGIN
            CREATE TYPE registry.agent_status_enum AS ENUM (
                'registered', 'candidate', 'production', 'suspended', 'withdrawn'
            );
        EXCEPTION WHEN duplicate_object THEN NULL; END $$;
        """
    )
    op.execute(
        """
        DO $$ BEGIN
            CREATE TYPE registry.capability_role_enum AS ENUM (
                'primary', 'supporting', 'governance'
            );
        EXCEPTION WHEN duplicate_object THEN NULL; END $$;
        """
    )
    op.execute(
        """
        DO $$ BEGIN
            CREATE TYPE registry.run_status_enum AS ENUM (
                'running', 'interrupted', 'completed', 'failed'
            );
        EXCEPTION WHEN duplicate_object THEN NULL; END $$;
        """
    )
    op.execute(
        """
        DO $$ BEGIN
            CREATE TYPE orchestration.steward_task_status_enum AS ENUM (
                'pending', 'approved', 'rejected', 'expired'
            );
        EXCEPTION WHEN duplicate_object THEN NULL; END $$;
        """
    )

    agent_plane = postgresql.ENUM(
        "platform",
        "experience",
        "constitutional",
        name="agent_plane_enum",
        schema="registry",
        create_type=False,
    )
    agent_status = postgresql.ENUM(
        "registered",
        "candidate",
        "production",
        "suspended",
        "withdrawn",
        name="agent_status_enum",
        schema="registry",
        create_type=False,
    )
    capability_role = postgresql.ENUM(
        "primary",
        "supporting",
        "governance",
        name="capability_role_enum",
        schema="registry",
        create_type=False,
    )
    run_status = postgresql.ENUM(
        "running",
        "interrupted",
        "completed",
        "failed",
        name="run_status_enum",
        schema="registry",
        create_type=False,
    )
    steward_task_status = postgresql.ENUM(
        "pending",
        "approved",
        "rejected",
        "expired",
        name="steward_task_status_enum",
        schema="orchestration",
        create_type=False,
    )

    op.create_table(
        "agents",
        sa.Column("agent_id", sa.String(length=128), nullable=False),
        sa.Column("spec_prefix", sa.String(length=8), nullable=False),
        sa.Column("spec_path", sa.Text(), nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=False),
        sa.Column("plane", agent_plane, nullable=False),
        sa.Column("build_phase", sa.Integer(), nullable=True),
        sa.Column("service_binding", sa.String(length=128), nullable=True),
        sa.Column("langgraph_graph_id", sa.String(length=128), nullable=False),
        sa.Column("output_schema_uri", sa.String(length=512), nullable=False),
        sa.Column("evidence_profile", sa.Boolean(), server_default="false", nullable=False),
        sa.Column("read_only", sa.Boolean(), server_default="false", nullable=False),
        sa.Column(
            "status",
            agent_status,
            server_default="registered",
            nullable=False,
        ),
        *AUDIT_COLUMNS,
        sa.PrimaryKeyConstraint("agent_id"),
        sa.UniqueConstraint("spec_prefix", name="uq_agents_spec_prefix"),
        sa.UniqueConstraint("langgraph_graph_id", name="uq_agents_langgraph_graph_id"),
        schema="registry",
    )

    op.create_table(
        "capabilities",
        sa.Column("capability_id", sa.String(length=128), nullable=False),
        sa.Column("canonical_section", sa.String(length=64), nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=False),
        sa.Column("build_phase", sa.Integer(), nullable=True),
        sa.Column("plane", agent_plane, nullable=False),
        sa.Column("contract_producer", sa.String(length=512), nullable=True),
        sa.Column("contract_consumer", sa.String(length=512), nullable=True),
        sa.Column("status", sa.String(length=32), server_default="active", nullable=False),
        *AUDIT_COLUMNS,
        sa.PrimaryKeyConstraint("capability_id"),
        schema="registry",
    )

    op.create_table(
        "capability_agents",
        sa.Column("capability_id", sa.String(length=128), nullable=False),
        sa.Column("agent_id", sa.String(length=128), nullable=False),
        sa.Column("role", capability_role, nullable=False),
        *AUDIT_COLUMNS,
        sa.ForeignKeyConstraint(["capability_id"], ["registry.capabilities.capability_id"]),
        sa.ForeignKeyConstraint(["agent_id"], ["registry.agents.agent_id"]),
        sa.PrimaryKeyConstraint("capability_id", "agent_id"),
        schema="registry",
    )

    op.create_table(
        "capability_services",
        sa.Column("capability_id", sa.String(length=128), nullable=False),
        sa.Column("service_name", sa.String(length=128), nullable=False),
        sa.Column("base_url_env", sa.String(length=128), nullable=False),
        sa.Column("health_path", sa.String(length=64), server_default="/health", nullable=False),
        *AUDIT_COLUMNS,
        sa.ForeignKeyConstraint(["capability_id"], ["registry.capabilities.capability_id"]),
        sa.PrimaryKeyConstraint("capability_id", "service_name"),
        schema="registry",
    )

    op.create_table(
        "agent_runs",
        sa.Column(
            "run_id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("agent_id", sa.String(length=128), nullable=False),
        sa.Column("agent_version", sa.String(length=64), server_default="0.1.0", nullable=False),
        sa.Column("graph_thread_id", sa.String(length=128), nullable=False),
        sa.Column("trigger_source", sa.String(length=32), nullable=False),
        sa.Column("input_ref", sa.Text(), nullable=True),
        sa.Column("output_ref", sa.Text(), nullable=True),
        sa.Column("status", run_status, nullable=False),
        sa.Column("provenance_event_id", sa.String(length=128), nullable=True),
        sa.Column(
            "started_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        *AUDIT_COLUMNS,
        sa.ForeignKeyConstraint(["agent_id"], ["registry.agents.agent_id"]),
        sa.PrimaryKeyConstraint("run_id"),
        sa.UniqueConstraint("graph_thread_id", name="uq_agent_runs_graph_thread_id"),
        schema="registry",
    )
    op.create_index("ix_agent_runs_agent_id", "agent_runs", ["agent_id"], schema="registry")

    op.create_table(
        "steward_tasks",
        sa.Column(
            "task_id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("run_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("thread_id", sa.String(length=128), nullable=False),
        sa.Column("agent_id", sa.String(length=128), nullable=False),
        sa.Column(
            "status",
            steward_task_status,
            server_default="pending",
            nullable=False,
        ),
        sa.Column("reviewer_id", sa.String(length=255), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        *AUDIT_COLUMNS,
        sa.ForeignKeyConstraint(["run_id"], ["registry.agent_runs.run_id"]),
        sa.PrimaryKeyConstraint("task_id"),
        schema="orchestration",
    )
    op.create_index(
        "ix_steward_tasks_thread_id",
        "steward_tasks",
        ["thread_id"],
        schema="orchestration",
    )


def downgrade() -> None:
    op.drop_index("ix_steward_tasks_thread_id", table_name="steward_tasks", schema="orchestration")
    op.drop_table("steward_tasks", schema="orchestration")
    op.drop_index("ix_agent_runs_agent_id", table_name="agent_runs", schema="registry")
    op.drop_table("agent_runs", schema="registry")
    op.drop_table("capability_services", schema="registry")
    op.drop_table("capability_agents", schema="registry")
    op.drop_table("capabilities", schema="registry")
    op.drop_table("agents", schema="registry")

    op.execute("DROP TYPE IF EXISTS orchestration.steward_task_status_enum")
    op.execute("DROP TYPE IF EXISTS registry.run_status_enum")
    op.execute("DROP TYPE IF EXISTS registry.capability_role_enum")
    op.execute("DROP TYPE IF EXISTS registry.agent_status_enum")
    op.execute("DROP TYPE IF EXISTS registry.agent_plane_enum")
    op.execute("DROP SCHEMA IF EXISTS orchestration CASCADE")
