"""Deterministic RC7 commercial product recommendations."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Literal

CollectionName = Literal["Big Cats Collection", "World Heritage Collection", "Education Collection"]


@dataclass(frozen=True)
class ProductRecommendation:
    """Recommendation record for commercial validation scoring."""

    product_slug: str
    product_title: str
    product_category: str
    collection: CollectionName
    product_category_score: float
    product_fit_score: float
    estimated_giftability: float
    estimated_repeat_purchase: float
    rationale: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


_RECOMMENDATIONS: tuple[ProductRecommendation, ...] = (
    ProductRecommendation(
        product_slug="big-cats-poster",
        product_title="Big Cats of the World Field Poster",
        product_category="Poster",
        collection="Big Cats Collection",
        product_category_score=0.92,
        product_fit_score=0.91,
        estimated_giftability=0.88,
        estimated_repeat_purchase=0.42,
        rationale="Strong museum-store wall-chart fit for species education and broad gift appeal.",
    ),
    ProductRecommendation(
        product_slug="big-cats-framed-print",
        product_title="Panthera Portrait Framed Print",
        product_category="Framed Print",
        collection="Big Cats Collection",
        product_category_score=0.90,
        product_fit_score=0.86,
        estimated_giftability=0.84,
        estimated_repeat_purchase=0.36,
        rationale="Premium decor validates member and collector demand without adding checkout.",
    ),
    ProductRecommendation(
        product_slug="big-cats-canvas",
        product_title="Big Cats Habitat Canvas",
        product_category="Canvas Prints",
        collection="Big Cats Collection",
        product_category_score=0.88,
        product_fit_score=0.89,
        estimated_giftability=0.86,
        estimated_repeat_purchase=0.34,
        rationale="Large-format habitat storytelling fits conservation-oriented home display.",
    ),
    ProductRecommendation(
        product_slug="big-cats-metal-print",
        product_title="Big Cats Conservation Metal Print",
        product_category="Metal Prints",
        collection="Big Cats Collection",
        product_category_score=0.87,
        product_fit_score=0.85,
        estimated_giftability=0.83,
        estimated_repeat_purchase=0.31,
        rationale="Contemporary premium material tests gift demand for conservation-led visual impact.",
    ),
    ProductRecommendation(
        product_slug="big-cats-puzzle",
        product_title="Big Cats Range Map Puzzle",
        product_category="Puzzle",
        collection="Big Cats Collection",
        product_category_score=0.84,
        product_fit_score=0.82,
        estimated_giftability=0.78,
        estimated_repeat_purchase=0.57,
        rationale="Hands-on education product supports family repeat engagement.",
    ),
    ProductRecommendation(
        product_slug="big-cats-calendar",
        product_title="Twelve Months of Big Cats Calendar",
        product_category="Calendar",
        collection="Big Cats Collection",
        product_category_score=0.78,
        product_fit_score=0.74,
        estimated_giftability=0.82,
        estimated_repeat_purchase=0.65,
        rationale="Seasonal editorial format has high repeat-purchase potential.",
    ),
    ProductRecommendation(
        product_slug="world-heritage-museum-print",
        product_title="World Heritage Museum Print",
        product_category="Museum Prints",
        collection="World Heritage Collection",
        product_category_score=0.91,
        product_fit_score=0.87,
        estimated_giftability=0.80,
        estimated_repeat_purchase=0.32,
        rationale="Institutional object-label treatment maps well to heritage display demand.",
    ),
    ProductRecommendation(
        product_slug="world-heritage-historic-map",
        product_title="World Heritage Historic Map",
        product_category="Historic Maps",
        collection="World Heritage Collection",
        product_category_score=0.89,
        product_fit_score=0.88,
        estimated_giftability=0.77,
        estimated_repeat_purchase=0.38,
        rationale="Map-led discovery follows British Museum and Europeana collection navigation patterns.",
    ),
    ProductRecommendation(
        product_slug="world-heritage-coffee-table-book",
        product_title="World Heritage Coffee Table Book",
        product_category="Coffee Table Book",
        collection="World Heritage Collection",
        product_category_score=0.86,
        product_fit_score=0.84,
        estimated_giftability=0.92,
        estimated_repeat_purchase=0.29,
        rationale="Premium editorial artifact aligns with exhibition catalog and gift-market behavior.",
    ),
    ProductRecommendation(
        product_slug="education-big-cats-card-set",
        product_title="Big Cats Educational Card Set",
        product_category="Educational Card Sets",
        collection="Education Collection",
        product_category_score=0.82,
        product_fit_score=0.79,
        estimated_giftability=0.70,
        estimated_repeat_purchase=0.71,
        rationale="Portable classroom product reinforces taxonomy, range, and conservation literacy.",
    ),
    ProductRecommendation(
        product_slug="education-discovery-pack",
        product_title="Nature & Culture Discovery Pack",
        product_category="Discovery Packs",
        collection="Education Collection",
        product_category_score=0.80,
        product_fit_score=0.78,
        estimated_giftability=0.75,
        estimated_repeat_purchase=0.68,
        rationale="Bundled activity format supports museum-shop family learning and repeat visits.",
    ),
    ProductRecommendation(
        product_slug="education-paint-by-numbers",
        product_title="Big Cats Paint-by-Numbers",
        product_category="Paint-by-Numbers",
        collection="Education Collection",
        product_category_score=0.74,
        product_fit_score=0.70,
        estimated_giftability=0.81,
        estimated_repeat_purchase=0.52,
        rationale="Creative activity tests accessible entry points into species learning.",
    ),
    ProductRecommendation(
        product_slug="education-classroom-kit",
        product_title="Nature & Culture Classroom Kit",
        product_category="Classroom Kits",
        collection="Education Collection",
        product_category_score=0.85,
        product_fit_score=0.83,
        estimated_giftability=0.58,
        estimated_repeat_purchase=0.76,
        rationale="Educator-oriented bundle has the strongest repeat-use signal for school settings.",
    ),
)


def recommended_products() -> list[ProductRecommendation]:
    """Return product recommendations ordered by product fit score."""

    return sorted(_RECOMMENDATIONS, key=lambda item: item.product_fit_score, reverse=True)


def recommended_products_payload() -> dict[str, object]:
    """Return the serializable RC7 recommendation output."""

    products = [product.to_dict() for product in recommended_products()]
    return {
        "reference_capability": "RC7 Product Intelligence",
        "architecture_note": "Architecture v1.0 remains frozen; ADR-011 followed.",
        "commercial_intelligence_fields": [
            "product_category_score",
            "product_fit_score",
            "estimated_giftability",
            "estimated_repeat_purchase",
        ],
        "recommended_products": products,
    }


def write_recommended_products(path: str | Path) -> None:
    """Write recommended product output as stable, human-readable JSON."""

    destination = Path(path)
    destination.write_text(
        json.dumps(recommended_products_payload(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
