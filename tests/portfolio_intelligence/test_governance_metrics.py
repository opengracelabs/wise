import json

from governance import (
    PORTFOLIO_GOVERNANCE_REPORT_FILENAME,
    concentration_risk_score,
    coverage_score,
    diversity_score,
    generate_portfolio_governance_report,
    load_portfolio_assets,
    portfolio_health_score,
    representation_score,
    write_portfolio_governance_report,
)


def test_balanced_portfolio_scores_high_on_governance_metrics():
    assets = [
        _asset("heritage", "Italy", "Heritage", "family-a", "origins", "Homepage Assets"),
        _asset("bio", "Kenya", "Biodiversity", "family-b", "species recovery", "Collection Candidates"),
        _asset("protected", "Brazil", "Protected Areas", "family-c", "protection", "Series Candidates"),
        _asset("art", "Japan", "Art", "family-d", "craft", "Product Candidates"),
        _asset("maps", "France", "Historical Maps", "family-e", "exploration", "Homepage Assets"),
        _asset("traditions", "Peru", "Cultural Traditions", "family-f", "living memory", "Collection Candidates"),
    ]

    assert diversity_score(assets) > 90
    assert representation_score(assets) > 80
    assert concentration_risk_score(assets) < 5
    assert coverage_score(assets) > 90
    assert portfolio_health_score(assets) > 85


def test_concentrated_portfolio_reports_risks_and_recommendations():
    assets = [
        _asset(f"italy-{index}", "Italy", "Heritage", "family-a", "origins", "Homepage Assets")
        for index in range(5)
    ] + [
        _asset("kenya", "Kenya", "Biodiversity", "family-b", "species recovery", "Product Candidates")
    ]

    report = generate_portfolio_governance_report(assets)

    assert report.concentration_risk_score > 70
    assert any(area["dimension"] == "geographic" and area["value"] == "italy" for area in report.overrepresented_areas)
    assert any(area["dimension"] == "domain" and area["value"] == "heritage" for area in report.concentration_risks)
    assert any(area["value"] == "protected areas" for area in report.underrepresented_areas)
    assert any("Reduce selection weight" in recommendation for recommendation in report.recommended_portfolio_adjustments)
    assert any("Add or promote candidates" in recommendation for recommendation in report.recommended_portfolio_adjustments)


def test_write_portfolio_governance_report_creates_json_output(tmp_path):
    assets = [
        _asset("heritage", "Italy", "Heritage", "family-a", "origins", "Homepage Assets"),
        _asset("bio", "Kenya", "Biodiversity", "family-b", "species recovery", "Collection Candidates"),
    ]

    result = write_portfolio_governance_report(assets, tmp_path)
    payload = json.loads((tmp_path / PORTFOLIO_GOVERNANCE_REPORT_FILENAME).read_text())

    assert payload["asset_count"] == 2
    assert payload["portfolio_health_score"] == result.portfolio_health_score
    assert "geographic" in payload["distributions"]
    assert payload["diversity_metrics"]["method"] == "normalized_entropy_0_to_100"
    assert payload["distributions"]["domain"]["counts"]["heritage"] == 1


def test_load_portfolio_assets_accepts_candidate_output_shape(tmp_path):
    input_file = tmp_path / "portfolio.json"
    input_file.write_text(
        json.dumps(
            {
                "homepage_candidates": [
                    _asset("homepage", "Italy", "Heritage", "family-a", "origins", "Homepage Assets")
                ],
                "collection_candidates": [
                    _asset("collection", "Kenya", "Biodiversity", "family-b", "species recovery", "Collection Candidates")
                ],
            }
        )
    )

    assets = load_portfolio_assets(input_file)

    assert [asset["id"] for asset in assets] == ["homepage", "collection"]


def test_report_reads_portfolio_inputs_from_selected_assets():
    selected_asset = {
        "id": "selected",
        "portfolio_category": "Product Candidates",
        "portfolio_inputs": {
            "domain": "Art",
            "region": "Japan",
            "country": "Japan",
            "collection_family": "ukiyo-e",
        },
        "narrative": "craft",
    }

    report = generate_portfolio_governance_report([selected_asset])

    assert report.distributions["geographic"]["counts"]["japan"] == 1
    assert report.distributions["domain"]["counts"]["art"] == 1
    assert report.distributions["collection_family"]["counts"]["ukiyo e"] == 1
    assert report.distributions["product"]["counts"]["product candidates"] == 1


def _asset(asset_id, country, domain, collection_family, narrative, product):
    return {
        "id": asset_id,
        "country": country,
        "domain": domain,
        "collection_family": collection_family,
        "narrative": narrative,
        "product_category": product,
    }
