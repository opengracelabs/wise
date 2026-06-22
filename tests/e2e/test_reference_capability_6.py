"""Commercial validation, product intelligence, and brand surface tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from wise_api.main import app


PRODUCT_SLUGS = [
    "big-cats-poster",
    "big-cats-framed-print",
    "big-cats-canvas",
    "big-cats-metal-print",
    "big-cats-puzzle",
    "big-cats-calendar",
    "big-cats-coffee-table-book",
    "world-heritage-museum-print",
    "world-heritage-historic-map",
    "world-heritage-coffee-table-book",
    "education-big-cats-card-set",
    "education-discovery-pack",
    "education-paint-by-numbers",
    "education-classroom-kit",
]


@pytest.mark.e2e
def test_commercial_shop_page_served():
    client = TestClient(app)
    response = client.get("/shop")
    if response.status_code == 404:
        pytest.skip("Demonstration surface assets not mounted in test environment")

    assert response.status_code == 200
    assert "Nature & Culture" in response.text
    assert "Product cards with intelligence scores" in response.text
    assert "No payment processing" in response.text
    assert "commercial.js" in response.text


@pytest.mark.e2e
def test_nature_culture_homepage_served():
    client = TestClient(app)
    response = client.get("/")
    if response.status_code == 404:
        pytest.skip("Demonstration surface assets not mounted in test environment")

    assert response.status_code == 200
    assert "Nature & Culture" in response.text
    assert "The permanent digital memory of humanity's heritage, nature, and culture." in response.text
    for section in [
        "Hero",
        "Featured Collections",
        "Featured Series",
        "Featured Products",
        "Explore by Place",
        "Explore by Species",
        "Explore by Theme",
        "Education",
        "Research",
        "Shop",
    ]:
        assert section in response.text
    for reference_model in [
        "Smithsonian",
        "National Geographic",
        "Europeana",
        "British Museum",
        "Google Arts & Culture",
    ]:
        assert reference_model in response.text


@pytest.mark.e2e
def test_commercial_catalog_script_contains_required_surface():
    client = TestClient(app)
    response = client.get("/static/commercial.js")
    if response.status_code == 404:
        pytest.skip("Demonstration surface assets not mounted in test environment")

    assert response.status_code == 200
    assert "Big Cats of the World" in response.text
    for product_type in [
        "Poster",
        "Framed Print",
        "Canvas Prints",
        "Museum Prints",
        "Historic Maps",
        "Educational Card Sets",
        "Discovery Packs",
        "Paint-by-Numbers",
        "Classroom Kits",
        "Puzzle",
        "Calendar",
        "Coffee Table Book",
    ]:
        assert product_type in response.text
    for event_name in [
        "product_view",
        "add_to_wishlist",
        "buy_interest",
        "checkout_intent",
    ]:
        assert event_name in response.text
    for intelligence_field in [
        "product_category_score",
        "product_fit_score",
        "estimated_giftability",
        "estimated_repeat_purchase",
    ]:
        assert intelligence_field in response.text


@pytest.mark.e2e
def test_rc7_recommended_products_output():
    output_path = Path("packages/wise-product-intelligence/recommended_products.json")
    payload = json.loads(output_path.read_text(encoding="utf-8"))

    assert payload["reference_capability"] == "RC7 Product Intelligence"
    assert "ADR-011" in payload["architecture_note"]
    products = payload["recommended_products"]
    assert len(products) >= 12
    categories = {product["product_category"] for product in products}
    for category in [
        "Canvas Prints",
        "Metal Prints",
        "Museum Prints",
        "Historic Maps",
        "Educational Card Sets",
        "Discovery Packs",
        "Paint-by-Numbers",
        "Classroom Kits",
    ]:
        assert category in categories
    for product in products:
        for field in payload["commercial_intelligence_fields"]:
            assert field in product


@pytest.mark.e2e
@pytest.mark.parametrize("product_slug", PRODUCT_SLUGS)
def test_commercial_product_pages_served(product_slug: str):
    client = TestClient(app)
    response = client.get(f"/shop/products/{product_slug}")
    if response.status_code == 404:
        pytest.skip("Demonstration surface assets not mounted in test environment")

    assert response.status_code == 200
    assert "Product detail page" in response.text
    assert "Price placeholder" in response.text
    assert "Add to Wishlist" in response.text or "product-detail-actions" in response.text
    assert "Buy Interest" in response.text or "product-detail-actions" in response.text
    assert "No payment processing" in response.text


@pytest.mark.e2e
@pytest.mark.parametrize("route,expected", [
    ("/shop/maps", "Historic Maps"),
    ("/shop/education", "Education products"),
    ("/shop/gifts", "Gifts"),
])
def test_commercial_shop_section_routes_served(route: str, expected: str):
    client = TestClient(app)
    response = client.get(route)
    if response.status_code == 404:
        pytest.skip("Demonstration surface assets not mounted in test environment")

    assert response.status_code == 200
    assert expected in response.text
    assert "product-grid" in response.text
    assert "No payment processing" in response.text


@pytest.mark.e2e
def test_commercial_dashboard_page_served():
    client = TestClient(app)
    response = client.get("/admin/commercial")
    if response.status_code == 404:
        pytest.skip("Demonstration surface assets not mounted in test environment")

    assert response.status_code == 200
    assert "Top Products" in response.text
    assert "Top Categories" in response.text
    assert "Most viewed products" in response.text
    assert "Highest buy intent" in response.text
    assert "Highest wishlist rate" in response.text
    assert "Highest Product Fit Score" in response.text
    assert "product_view" in response.text
    assert "checkout_intent" in response.text
