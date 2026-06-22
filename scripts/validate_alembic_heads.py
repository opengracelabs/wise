#!/usr/bin/env python3
"""Fail CI when Alembic revision graph has more than one head."""

from __future__ import annotations

import sys
from pathlib import Path

from alembic.config import Config
from alembic.script import ScriptDirectory

REGISTRY_ROOT = Path(__file__).resolve().parents[1] / "packages" / "wise-registry"


def main() -> int:
    cfg = Config(str(REGISTRY_ROOT / "alembic.ini"))
    cfg.set_main_option("script_location", str(REGISTRY_ROOT / "migrations"))
    script = ScriptDirectory.from_config(cfg)
    heads = script.get_heads()
    if len(heads) != 1:
        print(f"ERROR: expected 1 Alembic head, found {len(heads)}: {heads}", file=sys.stderr)
        return 1
    print(f"OK: single Alembic head: {heads[0]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
