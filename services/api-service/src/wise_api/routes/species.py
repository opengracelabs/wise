"""Reference Capability 2 species API routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from wise_contracts import SpeciesObjectView

from wise_api.database import get_db
from wise_api.species_repository import SpeciesNotFoundError, get_species_object

router = APIRouter(prefix="/v1/species", tags=["species"])


@router.get("/{stable_id}", response_model=SpeciesObjectView)
def get_species(stable_id: str, db: Session = Depends(get_db)) -> SpeciesObjectView:
    """Return the end-to-end Reference Capability 2 aggregate for a species."""
    try:
        return get_species_object(db, stable_id)
    except SpeciesNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
