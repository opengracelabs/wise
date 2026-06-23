"""Initial Open Grace registry tables."""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "open_grace_agents",
        sa.Column("agent_id", sa.String(128), primary_key=True),
        sa.Column("lifecycle_stage", sa.String(32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("steward_actor", sa.String(128), nullable=True),
        sa.Column("reference_models", sa.JSON(), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
    )
    op.create_table(
        "open_grace_capabilities",
        sa.Column("id", sa.String(128), primary_key=True),
        sa.Column("lifecycle_stage", sa.String(32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("steward_actor", sa.String(128), nullable=True),
        sa.Column("reference_models", sa.JSON(), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
    )
    op.create_table(
        "open_grace_agent_capability_bindings",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("agent_id", sa.String(128), nullable=False),
        sa.Column("capability_class_id", sa.String(128), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("agent_id", "capability_class_id"),
    )
    op.create_index("ix_open_grace_agent_capability_bindings_agent_id", "open_grace_agent_capability_bindings", ["agent_id"])
    op.create_index("ix_open_grace_agent_capability_bindings_capability_class_id", "open_grace_agent_capability_bindings", ["capability_class_id"])
    op.create_table(
        "open_grace_knowledge",
        sa.Column("entry_id", sa.String(128), primary_key=True),
        sa.Column("knowledge_type", sa.String(32), nullable=False),
        sa.Column("lifecycle_stage", sa.String(32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("steward_actor", sa.String(128), nullable=True),
        sa.Column("reference_models", sa.JSON(), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
    )
    op.create_index("ix_open_grace_knowledge_knowledge_type", "open_grace_knowledge", ["knowledge_type"])
    op.create_table(
        "open_grace_risks",
        sa.Column("risk_id", sa.String(128), primary_key=True),
        sa.Column("lifecycle_stage", sa.String(32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("steward_actor", sa.String(128), nullable=True),
        sa.Column("reference_models", sa.JSON(), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
    )
    op.create_table(
        "open_grace_benchmarks",
        sa.Column("benchmark_id", sa.String(128), primary_key=True),
        sa.Column("lifecycle_stage", sa.String(32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("steward_actor", sa.String(128), nullable=True),
        sa.Column("reference_models", sa.JSON(), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
    )
    op.create_table(
        "open_grace_audits",
        sa.Column("audit_id", sa.String(128), primary_key=True),
        sa.Column("lifecycle_stage", sa.String(32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("steward_actor", sa.String(128), nullable=True),
        sa.Column("reference_models", sa.JSON(), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
    )
    op.create_table(
        "open_grace_standards",
        sa.Column("standard_id", sa.String(128), primary_key=True),
        sa.Column("lifecycle_stage", sa.String(32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("steward_actor", sa.String(128), nullable=True),
        sa.Column("reference_models", sa.JSON(), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
    )
    op.create_table(
        "open_grace_models",
        sa.Column("model_id", sa.String(128), primary_key=True),
        sa.Column("lifecycle_stage", sa.String(32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("steward_actor", sa.String(128), nullable=True),
        sa.Column("reference_models", sa.JSON(), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
    )
    op.create_table(
        "open_grace_executions",
        sa.Column("run_id", sa.String(128), primary_key=True),
        sa.Column("agent_id", sa.String(128), nullable=False),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
    )
    op.create_index("ix_open_grace_executions_agent_id", "open_grace_executions", ["agent_id"])
    op.create_index("ix_open_grace_executions_status", "open_grace_executions", ["status"])


def downgrade() -> None:
    op.drop_table("open_grace_executions")
    op.drop_table("open_grace_models")
    op.drop_table("open_grace_standards")
    op.drop_table("open_grace_audits")
    op.drop_table("open_grace_benchmarks")
    op.drop_table("open_grace_risks")
    op.drop_table("open_grace_knowledge")
    op.drop_table("open_grace_agent_capability_bindings")
    op.drop_table("open_grace_capabilities")
    op.drop_table("open_grace_agents")
