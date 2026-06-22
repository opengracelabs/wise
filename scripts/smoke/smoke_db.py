#!/usr/bin/env python3
"""Deploy-time smoke test: verify database connectivity and required tables.

Env:
  WISE_DATABASE_URL / DATABASE_URL  psycopg3 DSN
    (default: postgresql+psycopg://wise:wise@localhost:5432/wise)

Exit 0 on PASS, 1 on FAIL.
"""
from __future__ import annotations
import os
import sys

DEFAULT = "postgresql+psycopg://wise:wise@localhost:5432/wise"
REQUIRED = ["registry.sources", "discovery.records"]


def main() -> int:
    url = os.environ.get("WISE_DATABASE_URL") or os.environ.get("DATABASE_URL") or DEFAULT
    if url.startswith("postgresql://"):
        # normalize to the installed psycopg3 driver
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)
    try:
        from sqlalchemy import create_engine, text
    except Exception as exc:  # pragma: no cover
        print(f"FAIL  SQLAlchemy not available: {exc}")
        return 1
    try:
        engine = create_engine(url, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            missing = [t for t in REQUIRED
                       if conn.execute(text("SELECT to_regclass(:t)"), {"t": t}).scalar() is None]
        engine.dispose()
    except Exception as exc:
        print(f"FAIL  database connection error: {exc}")
        return 1
    if missing:
        print(f"FAIL  connected, but missing required tables: {missing}")
        return 1
    print(f"PASS  database connectivity + required tables present: {REQUIRED}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
