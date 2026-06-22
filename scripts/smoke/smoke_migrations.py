#!/usr/bin/env python3
"""Deploy-time smoke test: verify each package has a single Alembic head and the
target database is migrated to that head.

Env:
  WISE_DATABASE_URL / DATABASE_URL  psycopg3 DSN
  SMOKE_REQUIRE_MIGRATED            if "1", a missing version table FAILs
                                    (default: WARN — useful when only some
                                    packages are applied to a given DB)

Exit 0 on PASS, 1 on FAIL.
"""
from __future__ import annotations
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT = "postgresql+psycopg://wise:wise@localhost:5432/wise"
# package -> version_table (must match each package's env.py)
PKGS = {
    "wise-registry": "alembic_version_registry",
    "wise-reference": "alembic_version_reference",
    "wise-metadata": "alembic_version",
    "wise-discovery": "alembic_version_discovery",
}


def main() -> int:
    url = os.environ.get("WISE_DATABASE_URL") or os.environ.get("DATABASE_URL") or DEFAULT
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)
    require_migrated = os.environ.get("SMOKE_REQUIRE_MIGRATED") == "1"
    try:
        from alembic.config import Config
        from alembic.script import ScriptDirectory
        from sqlalchemy import create_engine, text
    except Exception as exc:  # pragma: no cover
        print(f"FAIL  dependency missing: {exc}")
        return 1

    engine = create_engine(url, pool_pre_ping=True)
    fail = 0
    for pkg, vtable in PKGS.items():
        cfg = Config(str(ROOT / "packages" / pkg / "alembic.ini"))
        cfg.set_main_option("script_location", str(ROOT / "packages" / pkg / "migrations"))
        heads = ScriptDirectory.from_config(cfg).get_heads()
        if len(heads) != 1:
            print(f"FAIL  {pkg}: expected 1 Alembic head, found {heads}")
            fail = 1
            continue
        head = heads[0]
        try:
            with engine.connect() as conn:
                present = conn.execute(text("SELECT to_regclass(:t)"), {"t": vtable}).scalar()
                current = (conn.execute(text(f"SELECT version_num FROM {vtable}")).scalar()
                           if present else None)
        except Exception as exc:
            print(f"FAIL  {pkg}: error reading {vtable}: {exc}")
            fail = 1
            continue
        if present is None:
            msg = f"{pkg}: version table {vtable} absent (DB not migrated for this package)"
            if require_migrated:
                print(f"FAIL  {msg}")
                fail = 1
            else:
                print(f"WARN  {msg}")
            continue
        if current == head:
            print(f"PASS  {pkg}: at head {head}")
        else:
            print(f"FAIL  {pkg}: db at {current}, head {head}")
            fail = 1
    engine.dispose()
    return fail


if __name__ == "__main__":
    raise SystemExit(main())
