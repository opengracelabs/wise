"""Merge RC3 conservation branch with v1.1 provenance hardening.

Revision ID: 006_merge_rc3_and_v1_1
Revises: 003_rc3_conservation_sources, 005_registry_v1_1_provenance_hardening
Create Date: 2026-06-22
"""

from __future__ import annotations

from typing import Sequence, Union

revision: str = "006_merge_rc3_and_v1_1"
down_revision: Union[str, tuple[str, ...], None] = (
    "003_rc3_conservation_sources",
    "005_registry_v1_1_provenance_hardening",
)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
