"""Reference Capability 7 commerce and distribution contracts."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


ProductCategory = Literal["posters", "prints", "puzzles", "calendars", "books"]
ProviderName = Literal["shopify", "printful", "gelato"]
PromotionStageKey = Literal["collection", "script", "narration", "images", "promo_video"]


class IntelligenceSignal(BaseModel):
    """Commercialization signal derived from existing WISE intelligence layers."""

    layer: Literal[
        "Recognition Intelligence",
        "Demand Intelligence",
        "Commercial Intelligence",
        "Portfolio Intelligence",
    ]
    score: float = Field(ge=0, le=1)
    summary: str
    evidence_refs: list[str] = Field(default_factory=list)


class CommerceProduct(BaseModel):
    """Validation-only product catalog entry."""

    sku: str
    slug: str
    title: str
    category: ProductCategory
    source_entity: str
    collection: str
    description: str
    reference_models: list[str]
    intelligence_signals: list[IntelligenceSignal]
    pinterest_asset_ids: list[str]
    provider_targets: list[ProviderName]
    validation_only: bool = True
    payment_processing_enabled: bool = False


class CommerceProviderValidation(BaseModel):
    """Provider capability status without creating checkout or payment flows."""

    provider: ProviderName
    display_name: str
    role: str
    status: Literal["configured_for_validation", "stubbed", "blocked"]
    capabilities: list[str]
    disabled_capabilities: list[str]
    validation_notes: list[str]


class MarketingDashboardMetrics(BaseModel):
    """Prototype marketing metrics for demand validation."""

    pinterest_clicks: int = Field(ge=0)
    product_views: int = Field(ge=0)
    wishlist_rate: float = Field(ge=0, le=1)
    buy_intent: float = Field(ge=0, le=1)
    conversion_estimate: float = Field(ge=0, le=1)
    tracked_surfaces: list[str]
    notes: list[str]


class PromotionPipelineStage(BaseModel):
    """AI promotion pipeline design stage."""

    key: PromotionStageKey
    label: str
    description: str
    inputs: list[str]
    outputs: list[str]
    governance_gate: str


class PinterestAssetSpec(BaseModel):
    """Pinterest-ready validation asset specification."""

    asset_id: str
    asset_type: Literal["pin_1000x1500", "product_pin", "collection_pin"]
    title: str
    size_px: str = "1000x1500"
    target_url: str
    source_product_skus: list[str]
    alt_text: str
    status: Literal["ready_for_generation", "template_only"]


class CommercePrototype(BaseModel):
    """RC7 Commerce & Distribution Prototype aggregate."""

    name: str = "RC7 Commerce & Distribution Prototype"
    shop_routes: list[str]
    providers: list[CommerceProviderValidation]
    catalog: list[CommerceProduct]
    marketing_dashboard: MarketingDashboardMetrics
    promotion_pipeline: list[PromotionPipelineStage]
    pinterest_assets: list[PinterestAssetSpec]
    youtube_promo_route: str
    reference_models: list[str]
    vercel_compatible: bool = True
    payment_processing_enabled: bool = False
