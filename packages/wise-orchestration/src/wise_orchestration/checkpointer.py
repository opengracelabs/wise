"""PostgresSaver configuration for LangGraph checkpoints."""

from __future__ import annotations

from langgraph.checkpoint.postgres import PostgresSaver

from psycopg_pool import ConnectionPool


def create_checkpointer(database_url: str) -> tuple[PostgresSaver, ConnectionPool]:
    """Create a Postgres-backed LangGraph checkpointer and connection pool."""
    pool = ConnectionPool(
        conninfo=database_url,
        min_size=1,
        max_size=10,
        kwargs={"autocommit": True, "prepare_threshold": 0},
    )
    checkpointer = PostgresSaver(pool)
    checkpointer.setup()
    return checkpointer, pool
