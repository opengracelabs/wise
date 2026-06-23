"""Reference Capability 7 commerce prototype tests."""

from fastapi.testclient import TestClient

from wise_api.commerce_catalog import get_catalog, get_commerce_prototype
from wise_api.main import app


def test_rc7_commerce_prototype_contract() -> None:
    prototype = get_commerce_prototype()

    assert prototype.name == "RC7 Commerce & Distribution Prototype"
    assert prototype.payment_processing_enabled is False
    assert prototype.vercel_compatible is True
    assert set(prototype.shop_routes) == {
        "/shop",
        "/shop/posters",
        "/shop/prints",
        "/shop/puzzles",
        "/shop/calendars",
        "/shop/books",
    }
    assert {provider.provider for provider in prototype.providers} == {
        "shopify",
        "printful",
        "gelato",
    }
    assert {product.category for product in prototype.catalog} == {
        "posters",
        "prints",
        "puzzles",
        "calendars",
        "books",
    }
    assert [stage.key for stage in prototype.promotion_pipeline] == [
        "collection",
        "script",
        "narration",
        "images",
        "promo_video",
    ]
    assert {asset.asset_type for asset in prototype.pinterest_assets} == {
        "pin_1000x1500",
        "product_pin",
        "collection_pin",
    }


def test_rc7_products_include_all_intelligence_layers() -> None:
    expected_layers = {
        "Recognition Intelligence",
        "Demand Intelligence",
        "Commercial Intelligence",
        "Portfolio Intelligence",
    }

    for product in get_catalog():
        assert product.validation_only is True
        assert product.payment_processing_enabled is False
        assert {signal.layer for signal in product.intelligence_signals} == expected_layers


def test_rc7_commerce_api_routes() -> None:
    client = TestClient(app)

    prototype_response = client.get("/v1/commerce/prototype")
    assert prototype_response.status_code == 200
    assert prototype_response.json()["name"] == "RC7 Commerce & Distribution Prototype"

    catalog_response = client.get("/v1/commerce/catalog/posters")
    assert catalog_response.status_code == 200
    assert catalog_response.json()[0]["category"] == "posters"

    dashboard_response = client.get("/v1/commerce/marketing-dashboard")
    assert dashboard_response.status_code == 200
    assert {
        "pinterest_clicks",
        "product_views",
        "wishlist_rate",
        "buy_intent",
        "conversion_estimate",
    }.issubset(dashboard_response.json())


def test_rc7_static_pages_are_routed() -> None:
    client = TestClient(app)

    for route in ["/shop", "/shop/posters", "/admin/marketing", "/marketing/youtube"]:
        response = client.get(route)
        assert response.status_code == 200
        assert "RC7 Commerce" in response.text or "Marketing dashboard" in response.text
