"""In-memory RC7 commerce catalog and marketing prototype data."""

from __future__ import annotations

from wise_contracts import (
    CommerceProduct,
    CommercePrototype,
    IntelligenceSignal,
    MarketingDashboardMetrics,
    PinterestAssetSpec,
    PromotionPipelineStage,
)

from wise_api.commerce_providers import get_provider_validations

SHOP_ROUTES = [
    "/shop",
    "/shop/posters",
    "/shop/prints",
    "/shop/puzzles",
    "/shop/calendars",
    "/shop/books",
]

REFERENCE_MODELS = [
    "Smithsonian",
    "National Geographic",
    "British Museum",
    "Shopify Commerce",
]


def _signals(
    *,
    recognition: tuple[float, str],
    demand: tuple[float, str],
    commercial: tuple[float, str],
    portfolio: tuple[float, str],
    evidence_refs: list[str],
) -> list[IntelligenceSignal]:
    return [
        IntelligenceSignal(
            layer="Recognition Intelligence",
            score=recognition[0],
            summary=recognition[1],
            evidence_refs=evidence_refs,
        ),
        IntelligenceSignal(
            layer="Demand Intelligence",
            score=demand[0],
            summary=demand[1],
            evidence_refs=evidence_refs,
        ),
        IntelligenceSignal(
            layer="Commercial Intelligence",
            score=commercial[0],
            summary=commercial[1],
            evidence_refs=evidence_refs,
        ),
        IntelligenceSignal(
            layer="Portfolio Intelligence",
            score=portfolio[0],
            summary=portfolio[1],
            evidence_refs=evidence_refs,
        ),
    ]


CATALOG: list[CommerceProduct] = [
    CommerceProduct(
        sku="RC7-POSTER-STONEHENGE-001",
        slug="stonehenge-ritual-landscape-poster",
        title="Stonehenge Ritual Landscape Poster",
        category="posters",
        source_entity="stonehenge",
        collection="World Heritage Icons",
        description=(
            "Museum-style educational poster for Stonehenge, positioned as an "
            "accessible heritage entry point."
        ),
        reference_models=["British Museum", "Smithsonian", "Shopify Commerce"],
        intelligence_signals=_signals(
            recognition=(0.96, "UNESCO and Wikidata recognition support broad awareness."),
            demand=(0.88, "Strong evergreen Pinterest interest in ancient sites and travel."),
            commercial=(0.82, "Poster format offers simple validation with low fulfillment complexity."),
            portfolio=(0.91, "Anchors the heritage side of the launch collection."),
            evidence_refs=["unesco:373", "wikidata:Q39671", "rc1:stonehenge"],
        ),
        pinterest_asset_ids=["pin-stonehenge-hero", "product-stonehenge-poster"],
        provider_targets=["shopify", "printful", "gelato"],
    ),
    CommerceProduct(
        sku="RC7-PRINT-PANTHERA-001",
        slug="panthera-leo-conservation-print",
        title="Panthera leo Conservation Print",
        category="prints",
        source_entity="panthera-leo",
        collection="Nature & Culture Field Notes",
        description=(
            "Fine-art conservation print presenting Panthera leo as a biodiversity "
            "and stewardship story."
        ),
        reference_models=["National Geographic", "Smithsonian", "Shopify Commerce"],
        intelligence_signals=_signals(
            recognition=(0.94, "GBIF, EOL, and Wikidata identifiers create high entity confidence."),
            demand=(0.86, "Wildlife and conservation visuals map well to social discovery."),
            commercial=(0.79, "Premium print validation tests willingness-to-pay without checkout."),
            portfolio=(0.88, "Balances heritage products with biodiversity-led storytelling."),
            evidence_refs=["gbif:5219404", "eol:328450", "wikidata:Q140", "rc2:panthera-leo"],
        ),
        pinterest_asset_ids=["pin-panthera-field-note", "product-panthera-print"],
        provider_targets=["shopify", "printful", "gelato"],
    ),
    CommerceProduct(
        sku="RC7-PUZZLE-EVERGLADES-001",
        slug="everglades-waterways-puzzle",
        title="Everglades Waterways Puzzle",
        category="puzzles",
        source_entity="everglades-national-park",
        collection="Protected Places",
        description=(
            "Educational puzzle concept built around Everglades geospatial and "
            "conservation metadata."
        ),
        reference_models=["National Geographic", "Smithsonian", "Shopify Commerce"],
        intelligence_signals=_signals(
            recognition=(0.92, "UNESCO, Ramsar, and Wikidata signals validate place recognition."),
            demand=(0.81, "Family learning, maps, and nature puzzles provide testable demand."),
            commercial=(0.74, "Puzzle format needs provider validation before production approval."),
            portfolio=(0.86, "Adds protected-area learning to the RC7 catalog mix."),
            evidence_refs=["unesco:76", "ramsar:374", "wikidata:Q212174", "rc3:everglades"],
        ),
        pinterest_asset_ids=["pin-everglades-map", "product-everglades-puzzle"],
        provider_targets=["shopify", "printful", "gelato"],
    ),
    CommerceProduct(
        sku="RC7-CALENDAR-WISE-001",
        slug="world-institutional-stewardship-calendar",
        title="World Institutional Stewardship Calendar",
        category="calendars",
        source_entity="wise-reference-collection",
        collection="Founder Demonstration Collection",
        description=(
            "Twelve-month calendar concept combining heritage, biodiversity, and "
            "protected-area educational prompts."
        ),
        reference_models=["Smithsonian", "National Geographic", "Shopify Commerce"],
        intelligence_signals=_signals(
            recognition=(0.89, "Uses already approved RC1-RC3 entities for trustworthy curation."),
            demand=(0.77, "Seasonal calendar demand can be measured through wishlist intent."),
            commercial=(0.76, "Calendar production is viable if provider format coverage validates."),
            portfolio=(0.93, "Bundles the prototype into a coherent annual collection."),
            evidence_refs=["rc1:stonehenge", "rc2:panthera-leo", "rc3:everglades"],
        ),
        pinterest_asset_ids=["collection-founder-calendar", "product-wise-calendar"],
        provider_targets=["shopify", "printful", "gelato"],
    ),
    CommerceProduct(
        sku="RC7-BOOK-STEWARDSHIP-001",
        slug="field-guide-to-world-stewardship",
        title="Field Guide to World Stewardship",
        category="books",
        source_entity="wise-reference-collection",
        collection="Founder Demonstration Collection",
        description=(
            "Validation-only book landing concept for editorial packaging of "
            "approved reference capability narratives."
        ),
        reference_models=["British Museum", "Smithsonian", "National Geographic"],
        intelligence_signals=_signals(
            recognition=(0.87, "Draws from recognized public-memory reference entities."),
            demand=(0.72, "Long-form education demand should be validated before production."),
            commercial=(0.68, "Book economics require additional editorial and print validation."),
            portfolio=(0.9, "Creates a deeper educational product in the catalog ladder."),
            evidence_refs=["rc1:stonehenge", "rc2:panthera-leo", "rc3:everglades"],
        ),
        pinterest_asset_ids=["collection-field-guide", "product-stewardship-book"],
        provider_targets=["shopify"],
    ),
]


MARKETING_DASHBOARD = MarketingDashboardMetrics(
    pinterest_clicks=0,
    product_views=0,
    wishlist_rate=0,
    buy_intent=0,
    conversion_estimate=0,
    tracked_surfaces=[
        "/shop",
        "/shop/posters",
        "/shop/prints",
        "/shop/puzzles",
        "/shop/calendars",
        "/shop/books",
        "/marketing/youtube",
    ],
    notes=[
        "Metrics are validation placeholders; no third-party tracking pixel is installed.",
        "Buy intent means click-through to a disabled purchase CTA, not a transaction.",
        "Conversion estimate is modeled from views, wishlists, and buy-intent events only.",
    ],
)


PROMOTION_PIPELINE = [
    PromotionPipelineStage(
        key="collection",
        label="Collection",
        description="Select approved public-memory entities and product groupings.",
        inputs=["Commerce catalog", "Portfolio Intelligence", "rights_verified flags"],
        outputs=["Collection brief", "Audience hypothesis"],
        governance_gate="Rights and portfolio clearance",
    ),
    PromotionPipelineStage(
        key="script",
        label="Script",
        description="Draft short educational promo scripts grounded in approved metadata.",
        inputs=["Collection brief", "Recognition Intelligence", "Commercial Intelligence"],
        outputs=["15s script", "30s script", "Product CTA copy"],
        governance_gate="Factuality and tone review",
    ),
    PromotionPipelineStage(
        key="narration",
        label="Narration",
        description="Prepare narration directions for human or synthetic voice validation.",
        inputs=["Approved script", "Brand voice notes"],
        outputs=["Narration guide", "Caption text"],
        governance_gate="Accessibility and disclosure review",
    ),
    PromotionPipelineStage(
        key="images",
        label="Images",
        description="Generate or assemble rights-cleared image layouts for pins and video.",
        inputs=["Pinterest specs", "Product mockup requirements", "Rights metadata"],
        outputs=["1000x1500 pin layouts", "Product pins", "Collection pins"],
        governance_gate="Rights, sensitivity, and attribution review",
    ),
    PromotionPipelineStage(
        key="promo_video",
        label="Promo Video",
        description="Compose short-form video concepts for YouTube and social validation.",
        inputs=["Narration guide", "Image layouts", "Caption text"],
        outputs=["YouTube promo storyboard", "Short-form cutdown plan"],
        governance_gate="No payment CTA; validation-only launch approval",
    ),
]


PINTEREST_ASSETS = [
    PinterestAssetSpec(
        asset_id="pin-stonehenge-hero",
        asset_type="pin_1000x1500",
        title="Stonehenge: A Ritual Landscape",
        target_url="/shop/posters",
        source_product_skus=["RC7-POSTER-STONEHENGE-001"],
        alt_text="Vertical educational pin layout for a Stonehenge poster concept.",
        status="ready_for_generation",
    ),
    PinterestAssetSpec(
        asset_id="product-panthera-print",
        asset_type="product_pin",
        title="Panthera leo Conservation Print",
        target_url="/shop/prints",
        source_product_skus=["RC7-PRINT-PANTHERA-001"],
        alt_text="Product pin template for a lion conservation print.",
        status="ready_for_generation",
    ),
    PinterestAssetSpec(
        asset_id="collection-founder-calendar",
        asset_type="collection_pin",
        title="Founder Demonstration Collection",
        target_url="/shop/calendars",
        source_product_skus=[
            "RC7-POSTER-STONEHENGE-001",
            "RC7-PRINT-PANTHERA-001",
            "RC7-PUZZLE-EVERGLADES-001",
            "RC7-CALENDAR-WISE-001",
        ],
        alt_text="Collection pin template for heritage, biodiversity, and protected-area products.",
        status="ready_for_generation",
    ),
]


def get_catalog(category: str | None = None) -> list[CommerceProduct]:
    """Return RC7 products, optionally filtered by category."""

    if category is None:
        return CATALOG
    return [product for product in CATALOG if product.category == category]


def get_commerce_prototype() -> CommercePrototype:
    """Return the complete RC7 prototype aggregate."""

    return CommercePrototype(
        shop_routes=SHOP_ROUTES,
        providers=get_provider_validations(),
        catalog=CATALOG,
        marketing_dashboard=MARKETING_DASHBOARD,
        promotion_pipeline=PROMOTION_PIPELINE,
        pinterest_assets=PINTEREST_ASSETS,
        youtube_promo_route="/marketing/youtube",
        reference_models=REFERENCE_MODELS,
    )
