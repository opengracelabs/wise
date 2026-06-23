"""RC12 launch content validation tests."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKETING_DIR = ROOT / "data" / "marketing"
REPORT = ROOT / "docs" / "implementation" / "rc12-launch-content-report.md"


def _load(name: str):
    with (MARKETING_DIR / name).open(encoding="utf-8") as handle:
        return json.load(handle)


def test_rc12_product_catalog_covers_top_25_products() -> None:
    catalog = _load("product_catalog.json")

    assert len(catalog) == 25
    for product in catalog:
        assert {
            "title",
            "subtitle",
            "short_description",
            "long_description",
            "educational_value",
            "target_audience",
            "keywords",
        }.issubset(product)
        assert product["target_audience"]
        assert product["keywords"]


def test_rc12_pinterest_campaigns_cover_assets_collections_products() -> None:
    campaigns = _load("pinterest_campaigns.json")

    assert {"assets", "collections", "products"}.issubset(set(campaigns))
    assert "pin_groups" in campaigns
    assert len(campaigns["assets"]) == 25
    assert len(campaigns["collections"]) == 25
    assert len(campaigns["products"]) == 25

    for group_name in ("assets", "collections", "products"):
        for campaign in campaigns[group_name]:
            assert {"title", "description", "keywords", "CTA"}.issubset(campaign)
            assert campaign["keywords"]


def test_rc12_youtube_campaigns_cover_required_segments() -> None:
    campaigns = _load("youtube_campaigns.json")
    segments = campaigns["segments"]

    assert {campaign["segment"] for campaign in segments} == {
        "Heritage",
        "Species",
        "Collections",
        "Series",
    }
    for campaign in segments:
        assert {"title", "hook", "outline", "CTA"}.issubset(campaign)
        assert len(campaign["outline"]) >= 3


def test_rc12_seo_pages_include_top_100_pages() -> None:
    pages = _load("seo_pages.json")

    assert len(pages) == 100
    assert len({page["slug"] for page in pages}) == 100
    for page in pages:
        assert {"title", "slug", "meta_description", "keywords"}.issubset(page)
        assert page["keywords"]
        assert len(page["meta_description"]) <= 155


def test_rc12_email_campaigns_cover_required_sequences() -> None:
    sequences = _load("email_campaigns.json")

    assert {sequence["sequence"] for sequence in sequences} == {
        "Welcome",
        "Collections",
        "Species",
        "Products",
    }
    for sequence in sequences:
        assert len(sequence["emails"]) >= 3
        for email in sequence["emails"]:
            assert {"subject", "preview", "body", "CTA"}.issubset(email)


def test_rc12_report_declares_inventory_and_frozen_scope() -> None:
    report = REPORT.read_text(encoding="utf-8")

    assert "Architecture v1.0 remains frozen" in report
    assert "No governance changes" in report
    assert "No agents are proposed or added" in report
    assert "Top 10 first-launch products" in report
    assert "100 SEO pages" in report
