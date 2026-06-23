"""RC14 flagship content validation tests."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
REPORT = ROOT / "docs" / "implementation" / "rc14-content-readiness-report.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_rc14_collection_drafts_have_required_sections() -> None:
    collection_files = sorted((CONTENT / "collections").glob("*.md"))

    assert len(collection_files) == 10
    for path in collection_files:
        text = _read(path)
        assert "## Introduction" in text
        assert "## Educational narrative" in text
        assert "## Key assets" in text
        assert "## Key facts" in text
        assert "## Product opportunities" in text
        assert "Architecture v1.0 remains frozen" in text


def test_rc14_product_pages_are_launch_ready_drafts() -> None:
    product_files = sorted((CONTENT / "products").glob("*.md"))
    rc14_products = [path for path in product_files if "## Product promise" in _read(path)]

    assert len(product_files) == 30
    assert len(rc14_products) == 20
    for path in rc14_products:
        text = _read(path)
        assert "## Short description" in text
        assert "## Long description" in text
        assert "## Educational value" in text
        assert "## Suggested page modules" in text
        assert "without enabling checkout, payment processing, production, or fulfillment" in text


def test_rc14_seo_pages_have_complete_landing_page_sections() -> None:
    numbered_seo_files = sorted(
        path for path in (CONTENT / "seo").glob("*.md") if path.name[:2].isdigit()
    )

    assert len(numbered_seo_files) == 25
    for path in numbered_seo_files:
        text = _read(path)
        assert "## Meta title" in text
        assert "## Meta description" in text
        assert "## Landing page hero" in text
        assert "## Educational angle" in text
        assert "## Product pathways" in text


def test_rc14_big_cats_ebook_package_is_complete() -> None:
    ebook = CONTENT / "ebooks" / "big-cats-of-the-world"

    expected = {
        "outline.md",
        "chapters.md",
        "educational-notes.md",
        "product-page.md",
        "marketing-copy.md",
    }
    assert expected.issubset({path.name for path in ebook.glob("*.md")})
    assert "## Chapter outline" in _read(ebook / "outline.md")
    assert "## Chapter 1" in _read(ebook / "chapters.md")
    assert "## Learning goals" in _read(ebook / "educational-notes.md")
    assert "## Product headline" in _read(ebook / "product-page.md")


def test_rc14_readiness_report_declares_scores_and_scope() -> None:
    report = _read(REPORT)

    assert "RC14" in report
    assert ("Educational readiness | 92 / 100" in report or "first publishable content" in report.lower())
    assert ("Architecture v1.0 remains frozen" in report or "Does not modify Architecture v1.0" in report)
    assert ("No agents are proposed or added" in report or "Does not modify Architecture v1.0, governance, ADRs, or agents" in report)
