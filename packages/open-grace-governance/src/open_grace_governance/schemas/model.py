"""Model registry schema."""

from __future__ import annotations

from typing import Literal

from pydantic import Field, field_validator

from open_grace_governance.schemas.common import GovernedRecord, WISE_MODEL_ID


class ModelRegistryRecord(GovernedRecord):
    model_id: str
    provider: Literal["openai", "anthropic", "google", "alibaba", "deepseek", "other"]
    model_name: str = Field(min_length=1)
    council_role: str | None = None
    allowed_planes: list[str] = Field(default_factory=lambda: ["platform"])
    safety_tier: Literal["standard", "elevated", "restricted"] = "standard"

    @field_validator("model_id")
    @classmethod
    def validate_model_id(cls, value: str) -> str:
        if not WISE_MODEL_ID.match(value):
            raise ValueError("model_id must match wise.model.{slug}")
        return value

    @field_validator("allowed_planes")
    @classmethod
    def validate_planes(cls, value: list[str]) -> list[str]:
        allowed = {"platform", "experience", "constitutional"}
        invalid = set(value) - allowed
        if invalid:
            raise ValueError(f"invalid planes: {sorted(invalid)}")
        return value
