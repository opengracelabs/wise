"""FastAPI application entrypoint — Metadata Agent v1 scaffold."""

from contextlib import asynccontextmanager
from typing import Annotated
from uuid import UUID

import structlog
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from wise_common.config import ServiceSettings
from wise_common.logging import configure_logging
from metadata_service.routes.rc1 import router as rc1_router
from wise_metadata.models import EntityAssertionProposal, NormalizedRecord
from wise_metadata.session import create_session_factory
from wise_registry.models.source import Source

settings = ServiceSettings(service_name="metadata-service")
logger = structlog.get_logger()

_session_factory = None


def get_db() -> Session:
    global _session_factory
    if _session_factory is None:
        _session_factory = create_session_factory()
    session = _session_factory()
    try:
        yield session
    finally:
        session.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging(settings.log_level)
    logger.info("service_starting", service=settings.service_name, environment=settings.environment)
    yield
    logger.info("service_stopping", service=settings.service_name)


app = FastAPI(
    title="WISE Metadata Service",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(rc1_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": settings.service_name,
        "environment": settings.environment,
    }


@app.get("/modeling/assertions")
async def list_assertion_proposals(
    db: Annotated[Session, Depends(get_db)],
    limit: int = 50,
) -> dict:
    """List entity assertion proposals (steward-gated; no graph placement)."""
    rows = db.scalars(select(EntityAssertionProposal).limit(limit)).all()
    return {
        "items": [
            {
                "id": str(row.id),
                "subject_uri": row.subject_uri,
                "predicate": row.predicate,
                "object_value": row.object_value,
                "status": row.status.value,
                "evidence": row.evidence,
            }
            for row in rows
        ]
    }


@app.get("/modeling/records/{record_id}")
async def get_normalized_record(
    record_id: str,
    db: Annotated[Session, Depends(get_db)],
) -> dict:
    """Read normalized metadata record by ID."""
    record = db.get(NormalizedRecord, UUID(record_id))
    if record is None:
        raise HTTPException(status_code=404, detail="Normalized record not found")
    source = db.get(Source, record.source_id)
    return {
        "id": str(record.id),
        "source": source.canonical_name if source else None,
        "external_record_id": record.external_record_id,
        "source_schema": record.source_schema.value,
        "normalized_payload": record.normalized_payload,
        "original_literals": record.original_literals,
    }
