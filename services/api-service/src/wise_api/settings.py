"""API service settings."""

from pydantic import AliasChoices, Field
from pydantic_settings import SettingsConfigDict

from wise_common.config import ServiceSettings


class ApiSettings(ServiceSettings):
    model_config = SettingsConfigDict(
        env_prefix="WISE_",
        extra="ignore",
        populate_by_name=True,
    )

    database_url: str = Field(
        default="postgresql+psycopg://wise:wise@postgres:5432/wise",
        validation_alias=AliasChoices("DATABASE_URL", "WISE_DATABASE_URL"),
    )
    demonstration_surface_path: str = Field(
        default="/app/demonstration-surface",
        description="Path to Founder Demonstration Surface static assets",
    )
