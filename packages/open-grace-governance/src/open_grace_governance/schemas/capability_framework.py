"""Open Grace Capability Framework v1 schemas."""

from __future__ import annotations

import re
from enum import StrEnum

from pydantic import Field, field_validator

from open_grace_governance.schemas.common import GovernedRecord

WISE_CAPABILITY_CLASS_ID = re.compile(r"^wise\.capability\.class\.[a-z]+$")


class CapabilityClass(StrEnum):
    RESEARCH = "research"
    TRANSLATION = "translation"
    CLASSIFICATION = "classification"
    EXTRACTION = "extraction"
    ANALYSIS = "analysis"
    CODING = "coding"
    PRESERVATION = "preservation"
    PUBLISHING = "publishing"


CAPABILITY_CLASS_IDS = {
    cls: f"wise.capability.class.{cls.value}" for cls in CapabilityClass
}


class CapabilityFrameworkRecord(GovernedRecord):
    """Governed capability class with cross-registry bindings."""

    id: str
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    owner: str = Field(min_length=1)
    benchmark_set: list[str] = Field(min_length=1)
    risk_profile: list[str] = Field(min_length=1)
    approved_models: list[str] = Field(min_length=1)
    required_standards: list[str] = Field(min_length=1)
    audit_requirements: list[str] = Field(min_length=1)

    @field_validator("id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        if not WISE_CAPABILITY_CLASS_ID.match(value):
            raise ValueError("id must match wise.capability.class.{slug}")
        return value

    @property
    def capability_class(self) -> CapabilityClass:
        slug = self.id.rsplit(".", maxsplit=1)[-1]
        return CapabilityClass(slug)
