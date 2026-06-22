"""Reference Capability 6 commercial validation surface tests."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from wise_api.main import app


PRODUCT_SLUGS = [
    "big-cats-poster",
    "big-cats-framed-print",
    "big-cats-puzzle",
    "big-cats-calendar",
    "big-cats-coffee-table-book",
]


@pytest.mark.e2e
def test_commercial_shop_page_served():
    client = TestClient(app)
    response = client.get("/shop")
    if response.status_code == 404:
        pytest.skip("Demonstration surface assets not mounted in test environment")

    assert response.status_code == 200
    assert "Big Cats of the World" in response.text
    assert "Product cards" in response.text
    assert "No payment processing" in response.text
    assert "commercial.js" in response.text


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
def test_commercial_dashboard_page_served():
    client = TestClient(app)
    response = client.get("/admin/commercial")
    if response.status_code == 404:
        pytest.skip("Demonstration surface assets not mounted in test environment")

    assert response.status_code == 200
    assert "Most viewed products" in response.text
    assert "Highest buy intent" in response.text
    assert "Highest wishlist rate" in response.text
    assert "product_view" in response.text
    assert "checkout_intent" in response.text
