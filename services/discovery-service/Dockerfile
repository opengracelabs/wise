FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY packages/wise-common /deps/wise-common
COPY packages/wise-contracts /deps/wise-contracts
COPY packages/wise-registry /deps/wise-registry
COPY packages/wise-discovery /deps/wise-discovery
RUN pip install /deps/wise-common /deps/wise-contracts /deps/wise-registry /deps/wise-discovery

COPY services/discovery-service/pyproject.toml services/discovery-service/README.md ./
COPY services/discovery-service/src ./src

RUN pip install .

EXPOSE 8001

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

CMD ["uvicorn", "discovery_service.main:app", "--host", "0.0.0.0", "--port", "8001"]
