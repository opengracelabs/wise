"""Unit tests for rights and source validators."""

from uuid import uuid4

from wise_metadata.enums import ValidationStatus
from wise_metadata.services.rights_validator import validate_rights
from wise_metadata.services.source_validator import validate_source
from wise_registry.enums import TrustLevel
from wise_registry.models.license import License
from wise_registry.models.source import Source


def _make_source(**kwargs) -> Source:
    defaults = {
        "id": uuid4(),
        "canonical_name": "wikidata",
        "display_name": "Wikidata",
        "source_type_id": uuid4(),
        "homepage_url": "https://www.wikidata.org/",
        "api_url": "https://query.wikidata.org/sparql",
        "trust_level": TrustLevel.AUTHORITATIVE,
        "active": True,
    }
    defaults.update(kwargs)
    return Source(**defaults)


def test_validate_source_active_authoritative():
    source = _make_source()
    outcome = validate_source(source, source_registry_ref="https://wise.example/registry/source/x")
    assert outcome.status == ValidationStatus.PASS


def test_validate_source_inactive_fails():
    source = _make_source(active=False)
    outcome = validate_source(source, source_registry_ref="https://wise.example/registry/source/x")
    assert outcome.status == ValidationStatus.FAIL


def test_validate_rights_cc_license():
    license_ = License(
        id=uuid4(),
        code="CC-BY-4.0",
        uri="https://creativecommons.org/licenses/by/4.0/",
        label="CC BY 4.0",
    )
    outcome = validate_rights(
        rights_uri="https://creativecommons.org/licenses/by/4.0/",
        license=license_,
        rights_status=None,
        source_registry_ref="https://wise.example/registry/source/x",
    )
    assert outcome.status == ValidationStatus.PASS


def test_validate_rights_missing_uri_fails():
    outcome = validate_rights(
        rights_uri=None,
        license=None,
        rights_status=None,
        source_registry_ref="https://wise.example/registry/source/x",
    )
    assert outcome.status == ValidationStatus.FAIL
