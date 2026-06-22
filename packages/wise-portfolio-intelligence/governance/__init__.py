"""Portfolio governance metrics for WISE Portfolio Intelligence."""

__all__ = [
    "PORTFOLIO_GOVERNANCE_REPORT_FILENAME",
    "PortfolioGovernanceReport",
    "concentration_risk_score",
    "coverage_score",
    "diversity_score",
    "generate_portfolio_governance_report",
    "load_portfolio_assets",
    "portfolio_health_score",
    "representation_score",
    "write_portfolio_governance_report",
]


def __getattr__(name):
    if name not in __all__:
        raise AttributeError(f"module 'governance' has no attribute {name!r}")

    from governance import metrics

    return getattr(metrics, name)
