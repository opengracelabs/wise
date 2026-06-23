"""Reference Capability 7 commerce and distribution API routes."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from wise_contracts import (
    CommerceProduct,
    CommercePrototype,
    CommerceProviderValidation,
    MarketingDashboardMetrics,
    PinterestAssetSpec,
    PromotionPipelineStage,
)

from wise_api.commerce_catalog import (
    MARKETING_DASHBOARD,
    PINTEREST_ASSETS,
    PROMOTION_PIPELINE,
    get_catalog,
    get_commerce_prototype,
)
from wise_api.commerce_providers import get_provider_validations

router = APIRouter(prefix="/v1/commerce", tags=["commerce"])

VALID_CATEGORIES = {"posters", "prints", "puzzles", "calendars", "books"}


@router.get("/prototype", response_model=CommercePrototype)
def get_rc7_prototype() -> CommercePrototype:
    """Return the complete RC7 Commerce & Distribution Prototype."""

    return get_commerce_prototype()


@router.get("/catalog", response_model=list[CommerceProduct])
def list_catalog() -> list[CommerceProduct]:
    """Return the validation-only product catalog."""

    return get_catalog()


@router.get("/catalog/{category}", response_model=list[CommerceProduct])
def list_catalog_by_category(category: str) -> list[CommerceProduct]:
    """Return products for a shop category."""

    if category not in VALID_CATEGORIES:
        raise HTTPException(status_code=404, detail=f"Unknown commerce category: {category}")
    return get_catalog(category)


@router.get("/providers", response_model=list[CommerceProviderValidation])
def list_providers() -> list[CommerceProviderValidation]:
    """Return validation status for Shopify, Printful, and Gelato."""

    return get_provider_validations()


@router.get("/marketing-dashboard", response_model=MarketingDashboardMetrics)
def get_marketing_dashboard() -> MarketingDashboardMetrics:
    """Return validation-only marketing dashboard metrics."""

    return MARKETING_DASHBOARD


@router.get("/promotion-pipeline", response_model=list[PromotionPipelineStage])
def get_promotion_pipeline() -> list[PromotionPipelineStage]:
    """Return the AI promotion pipeline design."""

    return PROMOTION_PIPELINE


@router.get("/pinterest-assets", response_model=list[PinterestAssetSpec])
def get_pinterest_assets() -> list[PinterestAssetSpec]:
    """Return Pinterest-ready asset specifications."""

    return PINTEREST_ASSETS
