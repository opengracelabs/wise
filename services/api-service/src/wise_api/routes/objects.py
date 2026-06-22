"""Reference Capability 1 object API routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from wise_contracts import HeritageObjectView

from wise_api.database import get_db
from wise_api.repository import ObjectNotFoundError, get_heritage_object

router = APIRouter(prefix="/v1/objects", tags=["objects"])


@router.get("/{stable_id}", response_model=HeritageObjectView)
def get_object(stable_id: str, db: Session = Depends(get_db)) -> HeritageObjectView:
    """Return the end-to-end Reference Capability 1 aggregate for a heritage object."""
    try:
        return get_heritage_object(db, stable_id)
    except ObjectNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
