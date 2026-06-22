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
def test_rc9_top_100_global_assets_dataset():
    output_path = Path("data/portfolio/top_100_global_assets.json")
    assets = json.loads(output_path.read_text(encoding="utf-8"))

    assert len(assets) == 100
    categories = {asset["category"] for asset in assets}
    for source_family in [
        "UNESCO World Heritage",
        "GBIF Flagship Species",
        "Smithsonian Open Access",
        "National Gallery Public Domain",
        "Rijksmuseum Public Domain",
        "Library of Congress",
        "National Geographic Award-Winning Subject",
    ]:
        assert source_family in categories

    allowed_products = {
        "Posters",
        "Framed Prints",
        "Canvas Prints",
        "Puzzles",
        "Calendars",
        "Coffee Table Books",
        "Historic Maps",
    }
    for asset in assets:
        assert set(asset) == {
            "title",
            "category",
            "country",
            "recognition_score",
            "demand_score",
            "commercial_score",
            "product_recommendations",
        }
        assert asset["title"]
        assert asset["category"]
        assert asset["country"]
        for score_field in ["recognition_score", "demand_score", "commercial_score"]:
            assert 0 <= asset[score_field] <= 1
        assert asset["product_recommendations"]
        assert set(asset["product_recommendations"]).issubset(allowed_products)


@pytest.mark.e2e
def test_rc10_top_100_collections_dataset():
    collections = json.loads(Path("data/portfolio/top_100_collections.json").read_text(encoding="utf-8"))
    assets = json.loads(Path("data/portfolio/top_100_global_assets.json").read_text(encoding="utf-8"))
    asset_titles = {asset["title"] for asset in assets}

    assert len(collections) == 100
    assert len({collection["collection_id"] for collection in collections}) == 100
    assert len({collection["geography_region"] for collection in collections}) >= 6
    assert len({collection["domain"] for collection in collections}) >= 5
    assert len({collection["theme"] for collection in collections}) >= 8
    for collection in collections:
        assert collection["primary_asset"] in asset_titles
        assert collection["assets"]
        assert set(collection["assets"]).issubset(asset_titles)
        assert collection["portfolio_diversity_role"]
        assert 0 <= collection["portfolio_score"] <= 1


@pytest.mark.e2e
def test_rc10_top_100_series_dataset():
    collections = json.loads(Path("data/portfolio/top_100_collections.json").read_text(encoding="utf-8"))
    series = json.loads(Path("data/portfolio/top_100_series.json").read_text(encoding="utf-8"))
    collection_ids = {collection["collection_id"] for collection in collections}
    asset_titles = {asset for collection in collections for asset in collection["assets"]}

    assert len(series) == 100
    assert len({item["series_id"] for item in series}) == 100
    for item in series:
        assert item["collections"]
        assert set(item["collections"]).issubset(collection_ids)
        assert item["assets"]
        assert set(item["assets"]).issubset(asset_titles)
        assert len(item["educational_narrative"]) > 120
        assert item["learning_goals"]


@pytest.mark.e2e
def test_rc10_landing_page_experiments():
    experiment = json.loads(Path("data/portfolio/landing_page_experiments.json").read_text(encoding="utf-8"))

    assert experiment["experiment_id"] == "rc10-landing-message"
    variants = {variant["variant_id"]: variant for variant in experiment["variants"]}
    assert variants["A"]["headline"] == "Explore Humanity's Greatest Heritage"
    assert variants["B"]["headline"] == "Discover Nature, Culture, and History"
    assert variants["C"]["headline"] == "Permanent Digital Memory of Humanity"
    for variant in variants.values():
        assert set(variant["measures"]) == {"clicks", "engagement", "product interest"}


@pytest.mark.e2e
def test_rc10_top_50_products_dataset():
    products = json.loads(Path("data/portfolio/top_50_products.json").read_text(encoding="utf-8"))
    collections = json.loads(Path("data/portfolio/top_100_collections.json").read_text(encoding="utf-8"))
    assets = json.loads(Path("data/portfolio/top_100_global_assets.json").read_text(encoding="utf-8"))
    collection_ids = {collection["collection_id"] for collection in collections}
    asset_titles = {asset["title"] for asset in assets}
    source_families = {asset["category"] for asset in assets}
    required_categories = {
        "Posters",
        "Framed Prints",
        "Canvas Prints",
        "Puzzles",
        "Calendars",
        "Coffee Table Books",
        "Historic Maps",
        "Educational Cards",
    }

    assert len(products) == 50
    assert required_categories.issubset({product["category"] for product in products})
    for product in products:
        assert product["asset"] in asset_titles
        assert product["asset_source"] in source_families
        assert product["collection_id"] in collection_ids
        assert product["collection"]
        assert product["demand_rationale"]
        assert product["commercial_rationale"]
        assert 0 <= product["demand_score"] <= 1
        assert 0 <= product["commercial_score"] <= 1


@pytest.mark.e2e
def test_rc11_showcase_datasets():
    collections = json.loads(Path("data/portfolio/top_25_showcase_collections.json").read_text(encoding="utf-8"))
    series = json.loads(Path("data/portfolio/top_25_showcase_series.json").read_text(encoding="utf-8"))
    products = json.loads(Path("data/portfolio/top_25_showcase_products.json").read_text(encoding="utf-8"))
    collection_ids = {collection["collection_id"] for collection in collections}
    product_categories = {product["category"] for product in products}

    assert len(collections) == 25
    assert len(series) == 25
    assert len(products) == 25
    assert len({collection["geography_region"] for collection in collections}) >= 6
    for collection in collections:
        assert collection["visual_appeal_score"] >= 0
        assert collection["educational_value_score"] >= 0
        assert collection["global_representation_role"]
        assert collection["product_potential_score"] >= 0
    for item in series:
        assert item["collections"]
        assert any(collection_id in collection_ids for collection_id in item["collections"])
        assert item["educational_narrative"]
    for category in [
        "Posters",
        "Framed Prints",
        "Canvas Prints",
        "Puzzles",
        "Calendars",
        "Coffee Table Books",
    ]:
        assert category in product_categories


@pytest.mark.e2e
def test_rc11_apps_web_routes_and_analytics_files():
    web_root = Path("apps/web")
    for route_file in [
        "index.html",
        "collections/index.html",
        "series/index.html",
        "species/index.html",
        "places/index.html",
        "shop/index.html",
        "education/index.html",
        "research/index.html",
        "admin/analytics/index.html",
    ]:
        path = web_root / route_file
        assert path.is_file()
        text = path.read_text(encoding="utf-8")
        assert "Nature & Culture" in text
        assert "/static/analytics.js" in text
        assert "/static/app.js" in text

    analytics = (web_root / "static/analytics.js").read_text(encoding="utf-8")
    for event_name in [
        "page_view",
        "collection_view",
        "series_view",
        "product_view",
        "wishlist",
        "buy_intent",
        "outbound_click",
        "search",
        "session_duration",
    ]:
        assert event_name in analytics


@pytest.mark.e2e
def test_rc11_seo_artifacts():
    web_root = Path("apps/web")
    sitemap = (web_root / "sitemap.xml").read_text(encoding="utf-8")
    robots = (web_root / "robots.txt").read_text(encoding="utf-8")
    metadata = json.loads((web_root / "metadata-templates.json").read_text(encoding="utf-8"))
    opengraph = json.loads((web_root / "opengraph-templates.json").read_text(encoding="utf-8"))

    for route in [
        "/",
        "/collections",
        "/series",
        "/species",
        "/places",
        "/shop",
        "/education",
        "/research",
        "/admin/analytics",
    ]:
        assert route in sitemap
    assert "Sitemap:" in robots
    assert metadata["site_name"] == "Nature & Culture"
    assert opengraph["site_name"] == "Nature & Culture"


@pytest.mark.e2e
def test_rc12_pinterest_campaigns_dataset():
    campaigns = json.loads(Path("data/marketing/pinterest_campaigns.json").read_text(encoding="utf-8"))
    pin_groups = campaigns["pin_groups"]

    assert campaigns["platform"] == "Pinterest"
    for group_name in [
        "top_25_collection_pins",
        "top_25_product_pins",
        "top_25_heritage_pins",
        "top_25_wildlife_pins",
    ]:
        pins = pin_groups[group_name]
        assert len(pins) == 25
        for pin in pins:
            assert pin["title"]
            assert pin["description"]
            assert pin["image_requirements"]
            assert pin["target_audience"]
            assert pin["keywords"]


@pytest.mark.e2e
def test_rc12_youtube_campaigns_dataset():
    campaigns = json.loads(Path("data/marketing/youtube_campaigns.json").read_text(encoding="utf-8"))
    videos = campaigns["videos"]

    assert campaigns["platform"] == "YouTube"
    assert len(videos) == 25
    assert {
        "World Heritage",
        "Big Cats",
        "Endangered Species",
        "Ancient Civilizations",
        "Historic Maps",
    }.issubset({video["category"] for video in videos})
    for video in videos:
        assert video["title"]
        assert video["script_outline"]
        assert video["narration_outline"]
        assert video["image_requirements"]
        assert video["CTA"]


@pytest.mark.e2e
def test_rc12_seo_and_launch_selection_datasets():
    seo = json.loads(Path("data/marketing/seo_landing_pages.json").read_text(encoding="utf-8"))
    selections = json.loads(Path("data/marketing/launch_selections.json").read_text(encoding="utf-8"))

    assert len(seo["pages"]) == 100
    for page in seo["pages"]:
        assert page["title"]
        assert page["slug"]
        assert page["keywords"]
        assert page["collections"]
        assert page["products"]

    assert len(selections["top_10_launch_collections"]) == 10
    assert len(selections["top_10_launch_products"]) == 10
    for collection in selections["top_10_launch_collections"]:
        assert collection["selection_factors"]["educational_value"] >= 0
        assert collection["selection_factors"]["visual_appeal"] >= 0
        assert collection["selection_factors"]["commercial_potential"] >= 0
        assert collection["selection_factors"]["audience_size"] >= 0
    for product in selections["top_10_launch_products"]:
        assert product["title"]
        assert product["category"]
        assert product["asset"]
        assert product["collection"]


@pytest.mark.e2e
def test_rc13_content_factory_and_book_pipelines():
    factory = json.loads(Path("data/publishing/content_factory.json").read_text(encoding="utf-8"))
    showcase_assets = json.loads(Path("data/publishing/top_25_showcase_assets.json").read_text(encoding="utf-8"))
    ebooks = json.loads(Path("data/publishing/ebooks.json").read_text(encoding="utf-8"))["ebooks"]
    audiobooks = json.loads(Path("data/publishing/audiobooks.json").read_text(encoding="utf-8"))["audiobooks"]

    assert len(showcase_assets) == 25
    assert {
        "Articles",
        "Collection Pages",
        "Series Pages",
        "Product Pages",
        "Educational Resources",
    } == {pipeline["name"] for pipeline in factory["pipelines"]}
    assert len(ebooks) == 25
    assert len(audiobooks) == 25
    for concept in ebooks:
        assert concept["title"]
        assert concept["audience"]
        assert concept["chapters"]
        assert concept["source_collections"]
        assert concept["source_assets"]
    for concept in audiobooks:
        assert concept["title"]
        assert concept["chapters"]
        assert concept["source_collections"]
        assert concept["source_assets"]


@pytest.mark.e2e
def test_rc13_print_youtube_and_pinterest_production():
    print_products = json.loads(Path("data/publishing/print_products.json").read_text(encoding="utf-8"))
    youtube = json.loads(Path("data/publishing/youtube_production.json").read_text(encoding="utf-8"))
    pinterest = json.loads(Path("data/publishing/pinterest_production.json").read_text(encoding="utf-8"))

    for group in [
        "coffee_table_books",
        "calendars",
        "educational_card_sets",
        "historic_map_collections",
    ]:
        assert print_products[group]
        for item in print_products[group]:
            assert item["title"]
            assert item["source_asset"]
            assert item["source_collection"]
            assert item["format_requirements"]

    assert len(youtube["videos"]) == 25
    for video in youtube["videos"]:
        assert video["script"]
        assert video["narration"]
        assert video["image_requirements"]
        assert video["CTA"]

    for group in ["heritage_pins", "wildlife_pins", "product_pins", "collection_pins"]:
        assert len(pinterest[group]) == 25
        for pin in pinterest[group]:
            assert pin["title"]
            assert pin["description"]
            assert pin["image_requirements"]
            assert pin["CTA"] if "CTA" in pin else pin["production_status"]


@pytest.mark.e2e
def test_rc14_first_publishable_launch_artifacts():
    ebook_dir = Path("content/ebooks/big-cats-of-the-world")
    audiobook_dir = Path("content/audiobooks/big-cats-of-the-world")
    youtube_dir = Path("content/youtube")
    pinterest_dir = Path("content/pinterest")
    product_dir = Path("content/products")

    for path in [
        ebook_dir / "manuscript.md",
        ebook_dir / "outline.md",
        ebook_dir / "product-description.md",
        ebook_dir / "rights-checklist.md",
        audiobook_dir / "narration-script.md",
        audiobook_dir / "chapter-outline.md",
        audiobook_dir / "production-notes.md",
        youtube_dir / "big-cats-of-the-world.md",
        youtube_dir / "the-story-of-stonehenge.md",
        youtube_dir / "endangered-earth.md",
    ]:
        assert path.is_file()
        assert "Source dependencies" in path.read_text(encoding="utf-8")

    manuscript = (ebook_dir / "manuscript.md").read_text(encoding="utf-8")
    assert manuscript.count("## Chapter") >= 3

    for youtube_file in youtube_dir.glob("*.md"):
        text = youtube_file.read_text(encoding="utf-8")
        for section in ["## Hook", "## Narration", "## Visual direction", "## CTA", "## Rights/source notes"]:
            assert section in text

    pin_files = sorted(pinterest_dir.glob("*.md"))
    assert len(pin_files) == 5
    for pin_file in pin_files:
        text = pin_file.read_text(encoding="utf-8")
        for section in ["## Title", "## Description", "## Image requirements", "## Keywords", "## CTA", "## Linked product or collection"]:
            assert section in text

    product_files = sorted(product_dir.glob("*.md"))
    assert len(product_files) == 10
    for product_file in product_files:
        text = product_file.read_text(encoding="utf-8")
        for section in [
            "## Title",
            "## Subtitle",
            "## Short description",
            "## Long description",
            "## Educational value",
            "## Target audience",
            "## Suggested product type",
            "## Rights/source notes",
        ]:
            assert section in text
        assert "No payment processing" in text


@pytest.mark.e2e
def test_rc14_source_references_exist():
    source_paths = [
        Path("data/publishing/ebooks.json"),
        Path("data/publishing/audiobooks.json"),
        Path("data/publishing/youtube_production.json"),
        Path("data/publishing/pinterest_production.json"),
        Path("data/publishing/print_products.json"),
        Path("data/portfolio/top_25_showcase_products.json"),
    ]
    for path in source_paths:
        assert path.is_file()
        json.loads(path.read_text(encoding="utf-8"))

    report = Path("docs/implementation/rc14-launch-artifacts-report.md")
    assert report.is_file()
    text = report.read_text(encoding="utf-8")
    assert "No payment processing" in text
    assert "ADR-011" in text


@pytest.mark.e2e
def test_rc15_publication_quality_review_artifacts():
    report = Path("docs/implementation/rc15-publication-quality-report.md")
    assert report.is_file()
    report_text = report.read_text(encoding="utf-8")
    for section in [
        "Pass/fail by artifact group",
        "Required edits",
        "Rights blockers",
        "Top 10 publishable artifacts",
        "Top 10 not-ready artifacts",
        "ADR-011",
    ]:
        assert section in report_text

    revised_root = Path("content/revised")
    revised_files = sorted(revised_root.glob("**/*.md"))
    assert len(revised_files) >= 20
    for path in [
        revised_root / "ebooks/big-cats-of-the-world/manuscript.md",
        revised_root / "audiobooks/big-cats-of-the-world/narration-script.md",
        revised_root / "youtube/big-cats-of-the-world.md",
        revised_root / "youtube/the-story-of-stonehenge.md",
        revised_root / "youtube/endangered-earth.md",
    ]:
        assert path.is_file()
        text = path.read_text(encoding="utf-8")
        assert "Source dependencies" in text
        assert "rights" in text.lower()

    for product_file in (revised_root / "products").glob("*.md"):
        text = product_file.read_text(encoding="utf-8")
        assert "No payment processing enabled" in text
        assert "Do not remove rights warnings" in text


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
