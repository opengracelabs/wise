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
COPY packages/wise-reference /deps/wise-reference
COPY data /app/data
COPY apps/demonstration-surface /app/demonstration-surface
RUN pip install /deps/wise-common /deps/wise-contracts /deps/wise-registry /deps/wise-reference

COPY services/api-service/pyproject.toml services/api-service/README.md ./
COPY services/api-service/src ./src

ENV WISE_DEMONSTRATION_SURFACE_PATH=/app/demonstration-surface

RUN pip install .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "wise_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
