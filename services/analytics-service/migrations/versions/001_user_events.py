"""Create anonymous user_events telemetry table.

Revision ID: 001_user_events
Revises:
Create Date: 2026-06-22
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "001_user_events"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_events",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("type", sa.String(length=64), nullable=False),
        sa.Column("entity_id", sa.String(length=256), nullable=False),
        sa.Column("entity_type", sa.String(length=128), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("session_id", sa.String(length=128), nullable=False),
        sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_user_events_type", "user_events", ["type"])
    op.create_index("ix_user_events_entity_id", "user_events", ["entity_id"])
    op.create_index("ix_user_events_entity_type", "user_events", ["entity_type"])
    op.create_index("ix_user_events_timestamp", "user_events", ["timestamp"])
    op.create_index("ix_user_events_session_id", "user_events", ["session_id"])


def downgrade() -> None:
    op.drop_index("ix_user_events_session_id", table_name="user_events")
    op.drop_index("ix_user_events_timestamp", table_name="user_events")
    op.drop_index("ix_user_events_entity_type", table_name="user_events")
    op.drop_index("ix_user_events_entity_id", table_name="user_events")
    op.drop_index("ix_user_events_type", table_name="user_events")
    op.drop_table("user_events")
