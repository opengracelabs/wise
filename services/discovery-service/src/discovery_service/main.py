"""FastAPI application entrypoint — discovery + RC1 propose API."""

from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI

from wise_common.config import ServiceSettings
from wise_common.logging import configure_logging
from discovery_service.routes.rc1 import router as rc1_router
from discovery_service.routes.v1 import router as v1_router

settings = ServiceSettings(service_name="discovery-service")
logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging(settings.log_level)
    logger.info("service_starting", service=settings.service_name, environment=settings.environment)
    yield
    logger.info("service_stopping", service=settings.service_name)


app = FastAPI(
    title="WISE Discovery Service",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(rc1_router)
app.include_router(v1_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": settings.service_name,
        "environment": settings.environment,
    }
