"""Base service configuration loaded from environment variables."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class ServiceSettings(BaseSettings):
    """Common settings shared by all WISE microservices."""

    model_config = SettingsConfigDict(env_prefix="WISE_", extra="ignore")

    service_name: str = "wise-service"
    log_level: str = "INFO"
    environment: str = "development"

    database_url: str = "postgresql://wise:wise@postgres:5432/wise"
    redis_url: str = "redis://redis:6379/0"
    minio_endpoint: str = "minio:9000"
    minio_access_key: str = "wise"
    minio_secret_key: str = "wise-minio-secret"
    minio_bucket: str = "wise-preservation"
    opensearch_url: str = "http://opensearch:9200"
