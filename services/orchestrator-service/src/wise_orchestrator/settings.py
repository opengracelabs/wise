"""Orchestrator service settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class OrchestratorSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="WISE_", extra="ignore")

    service_name: str = "orchestrator-service"
    log_level: str = "INFO"
    environment: str = "development"
    database_url: str = "postgresql://wise:wise@postgres:5432/wise"
    n8n_webhook_url: str | None = None
