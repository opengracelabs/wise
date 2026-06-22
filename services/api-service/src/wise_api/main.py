"""FastAPI application entrypoint — Reference Capability 1 gateway."""

from contextlib import asynccontextmanager
from pathlib import Path

import structlog
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from wise_common.logging import configure_logging

from wise_api.routes.areas import router as areas_router
from wise_api.routes.commerce import router as commerce_router
from wise_api.routes.map import router as map_router
from wise_api.routes.objects import router as objects_router
from wise_api.routes.species import router as species_router
from wise_api.settings import ApiSettings

settings = ApiSettings()
logger = structlog.get_logger()

surface_path = Path(settings.demonstration_surface_path)
if not surface_path.is_dir():
    local_surface = Path(__file__).resolve().parents[4] / "apps" / "demonstration-surface"
    if local_surface.is_dir():
        surface_path = local_surface


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging(settings.log_level)
    logger.info("service_starting", service=settings.service_name, environment=settings.environment)
    yield
    logger.info("service_stopping", service=settings.service_name)


app = FastAPI(
    title="WISE Api Service",
    version="0.1.0",
    description="Reference Capability gateway — architecture-v1.0",
    lifespan=lifespan,
)

app.include_router(objects_router)
app.include_router(species_router)
app.include_router(areas_router)
app.include_router(map_router)
app.include_router(commerce_router)

if surface_path.is_dir():
    app.mount("/static", StaticFiles(directory=str(surface_path)), name="static")


@app.get("/health")
async def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": settings.service_name,
        "environment": settings.environment,
    }


@app.get("/areas/{stable_id}")
async def public_area_page(stable_id: str):
    """Public protected area page for Reference Capability 3 demonstration."""
    page = surface_path / "areas" / stable_id / "index.html"
    if not page.is_file():
        raise HTTPException(status_code=404, detail=f"Area page not found: {stable_id}")
    return FileResponse(page, media_type="text/html")


@app.get("/objects/{stable_id}")
async def public_object_page(stable_id: str):
    """Public object page for Reference Capability 1 demonstration."""
    page = surface_path / "objects" / stable_id / "index.html"
    if not page.is_file():
        raise HTTPException(status_code=404, detail=f"Object page not found: {stable_id}")
    return FileResponse(page, media_type="text/html")


def _surface_page(*segments: str) -> FileResponse:
    page = surface_path.joinpath(*segments, "index.html")
    if not page.is_file():
        route = "/" + "/".join(segments)
        raise HTTPException(status_code=404, detail=f"Surface page not found: {route}")
    return FileResponse(page, media_type="text/html")


@app.get("/shop")
async def shop_page():
    """RC7 shop landing page."""

    return _surface_page("shop")


@app.get("/shop/{category}")
async def shop_category_page(category: str):
    """RC7 shop category page."""

    if category not in {"posters", "prints", "puzzles", "calendars", "books"}:
        raise HTTPException(status_code=404, detail=f"Shop category not found: {category}")
    return _surface_page("shop", category)


@app.get("/admin/marketing")
async def marketing_dashboard_page():
    """RC7 marketing dashboard page."""

    return _surface_page("admin", "marketing")


@app.get("/marketing/youtube")
async def youtube_promo_page():
    """RC7 YouTube promo validation page."""

    return _surface_page("marketing", "youtube")
