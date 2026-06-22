"""Map service routes for protected area geospatial queries."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from wise_contracts import MapAreaSummary, MapSearchResult

from wise_api.area_repository import (
    ProtectedAreaNotFoundError,
    get_map_area,
    search_protected_areas_by_bbox,
)
from wise_api.database import get_db

router = APIRouter(prefix="/v1/map", tags=["map"])


@router.get("/areas/{stable_id}", response_model=MapAreaSummary)
def map_area(stable_id: str, db: Session = Depends(get_db)) -> MapAreaSummary:
    """Return geospatial map feature for a protected area."""
    try:
        return get_map_area(db, stable_id)
    except ProtectedAreaNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/search", response_model=MapSearchResult)
def map_search(
    bbox: str = Query(
        ...,
        description="Bounding box as min_lon,min_lat,max_lon,max_lat (WGS84)",
        examples=["-82.0,25.0,-80.0,26.0"],
    ),
    db: Session = Depends(get_db),
) -> MapSearchResult:
    """Search approved protected areas intersecting a bounding box."""
    try:
        parts = [float(value.strip()) for value in bbox.split(",")]
    except ValueError as exc:
        raise HTTPException(status_code=422, detail="bbox must be four comma-separated floats") from exc

    if len(parts) != 4:
        raise HTTPException(status_code=422, detail="bbox must contain exactly four values")

    min_lon, min_lat, max_lon, max_lat = parts
    if min_lon >= max_lon or min_lat >= max_lat:
        raise HTTPException(status_code=422, detail="bbox min values must be less than max values")

    return search_protected_areas_by_bbox(
        db,
        min_lon=min_lon,
        min_lat=min_lat,
        max_lon=max_lon,
        max_lat=max_lat,
    )
