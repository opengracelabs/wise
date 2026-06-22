"""Reference Capability 3 protected area API routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from wise_contracts import ProtectedAreaObjectView

from wise_api.area_repository import ProtectedAreaNotFoundError, get_protected_area_object
from wise_api.database import get_db

router = APIRouter(prefix="/v1/areas", tags=["areas"])


@router.get("/{stable_id}", response_model=ProtectedAreaObjectView)
def get_area(stable_id: str, db: Session = Depends(get_db)) -> ProtectedAreaObjectView:
    """Return the end-to-end Reference Capability 3 aggregate for a protected area."""
    try:
        return get_protected_area_object(db, stable_id)
    except ProtectedAreaNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
