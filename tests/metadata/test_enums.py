"""Unit tests for metadata enums."""

from wise_metadata.enums import (
    AssertionStatus,
    MappingTarget,
    SourceSchema,
    ValidationDomain,
    ValidationStatus,
)


def test_source_schema_values():
    assert SourceSchema.UNESCO_WHC.value == "unesco_whc"
    assert SourceSchema.WIKIDATA.value == "wikidata"


def test_mapping_targets():
    assert MappingTarget.CIDOC_CRM.value == "cidoc_crm"
    assert MappingTarget.DUBLIN_CORE.value == "dublin_core"


def test_assertion_status_proposed_default():
    assert AssertionStatus.PROPOSED.value == "proposed"


def test_validation_domains():
    assert ValidationDomain.SOURCE.value == "source"
    assert ValidationDomain.RIGHTS.value == "rights"


def test_validation_status_pass():
    assert ValidationStatus.PASS.value == "pass"
