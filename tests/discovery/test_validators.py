"""Unit tests for source validation and reachability."""

from uuid import uuid4

import httpx

from wise_discovery.enums import ReachabilityStatus, ValidationStatus
from wise_discovery.services.agent import check_reachability, validate_source
from wise_registry.enums import TrustLevel
from wise_registry.models.source import Source


def _make_source(**kwargs) -> Source:
    defaults = {
        "id": uuid4(),
        "canonical_name": "wikidata",
        "stable_id": "wikidata",
        "display_name": "Wikidata",
        "source_type_id": uuid4(),
        "homepage_url": "https://www.wikidata.org/",
        "api_url": "https://query.wikidata.org/sparql",
        "trust_level": TrustLevel.AUTHORITATIVE,
        "active": True,
    }
    defaults.update(kwargs)
    return Source(**defaults)


class _MockResponse:
    def __init__(self, status_code: int):
        self.status_code = status_code


class _MockClient:
    def __init__(self, status_code: int = 200):
        self.status_code = status_code
        self.head_calls: list[str] = []
        self.get_calls: list[str] = []

    def head(self, url: str, *, timeout: float) -> _MockResponse:
        self.head_calls.append(url)
        return _MockResponse(self.status_code)

    def get(self, url: str, *, timeout: float) -> _MockResponse:
        self.get_calls.append(url)
        return _MockResponse(self.status_code)


def test_validate_source_active_authoritative():
    source = _make_source()
    outcome = validate_source(source, source_registry_ref_value="wikidata")
    assert outcome.status == ValidationStatus.PASS.value


def test_validate_source_inactive_fails():
    source = _make_source(active=False)
    outcome = validate_source(source, source_registry_ref_value="wikidata")
    assert outcome.status == ValidationStatus.FAIL.value


def test_validate_source_requires_license_when_configured():
    source = _make_source(license_id=None)
    outcome = validate_source(
        source,
        source_registry_ref_value="wikidata",
        require_license=True,
    )
    assert outcome.status == ValidationStatus.FAIL.value


def test_check_reachability_uses_head_first():
    source = _make_source()
    client = _MockClient(status_code=200)
    result = check_reachability(source, client=client)
    assert result.status == ReachabilityStatus.REACHABLE.value
    assert client.head_calls == ["https://query.wikidata.org/sparql"]
    assert client.get_calls == []


def test_check_reachability_falls_back_to_get_on_head_error_status():
    source = _make_source()

    class _Client:
        def head(self, url: str, *, timeout: float) -> _MockResponse:
            return _MockResponse(404)

        def get(self, url: str, *, timeout: float) -> _MockResponse:
            return _MockResponse(200)

    result = check_reachability(source, client=_Client())
    assert result.status == ReachabilityStatus.REACHABLE.value
    assert result.http_status == 200


def test_check_reachability_unreachable_on_http_error():
    source = _make_source()

    class _FailingClient:
        def head(self, url: str, *, timeout: float) -> _MockResponse:
            raise httpx.ConnectError("connection refused")

        def get(self, url: str, *, timeout: float) -> _MockResponse:
            raise httpx.ConnectError("connection refused")

    result = check_reachability(source, client=_FailingClient())
    assert result.status == ReachabilityStatus.UNREACHABLE.value
