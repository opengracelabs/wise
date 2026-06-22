"""FastAPI orchestrator — LangGraph control plane (architecture-v1.0 Phase 0)."""

from __future__ import annotations

from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI

from wise_common.logging import configure_logging
from wise_orchestration.validation import RegistryValidationError, validate_registry_alignment
from wise_orchestrator.database import SessionLocal
from wise_orchestrator.dependencies import clear_run_service, set_rc1_run_service, set_run_service
from wise_orchestrator.routes.rc1 import router as rc1_router
from wise_orchestrator.routes.registry import router as registry_router
from wise_orchestrator.routes.runs import router as runs_router
from wise_orchestrator.rc1_run_service import RC1RunService
from wise_orchestrator.run_service import RunService
from wise_orchestrator.settings import OrchestratorSettings

settings = OrchestratorSettings()
logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging(settings.log_level)
    logger.info("service_starting", service=settings.service_name, environment=settings.environment)

    with SessionLocal() as session:
        try:
            validate_registry_alignment(session)
        except RegistryValidationError as exc:
            logger.error("registry_validation_failed", error=str(exc))
            raise RuntimeError(f"Registry validation failed: {exc}") from exc
    logger.info("registry_validation_passed", agent_count=15, capability_count=12)

    set_run_service(RunService(settings.database_url))
    set_rc1_run_service(RC1RunService(settings.database_url))
    yield

    clear_run_service()
    logger.info("service_stopping", service=settings.service_name)


app = FastAPI(
    title="WISE Orchestrator Service",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(registry_router, prefix="/api/v1")
app.include_router(runs_router, prefix="/api/v1")
app.include_router(rc1_router, prefix="/api/v1")


@app.get("/health")
async def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": settings.service_name,
        "environment": settings.environment,
    }
