"""Analytics service settings."""

from __future__ import annotations

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AnalyticsSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="WISE_", extra="ignore")

    service_name: str = "analytics-service"
    environment: str = "development"
    log_level: str = "INFO"
    database_url: str = "postgresql+psycopg://wise:wise@localhost:5432/wise"
    cors_origins: str = "*"

    @field_validator("database_url")
    @classmethod
    def normalize_postgres_driver(cls, value: str) -> str:
        if value.startswith("postgresql://"):
            return value.replace("postgresql://", "postgresql+psycopg://", 1)
        return value
