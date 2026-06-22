"""Integration test placeholders — require docker-compose up."""

import os

import pytest

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def database_url() -> str:
    url = os.environ.get("DATABASE_URL")
    if not url:
        pytest.skip("DATABASE_URL not set — start docker-compose for integration tests")
    return url


def test_postgres_placeholder(database_url: str) -> None:
    """Placeholder: verify PostgreSQL connectivity in Reference Capability 1."""
    assert database_url.startswith("postgresql://")


def test_minio_placeholder() -> None:
    """Placeholder: verify MinIO bucket exists in Reference Capability 1."""
    pytest.skip("MinIO integration tests not yet implemented")
