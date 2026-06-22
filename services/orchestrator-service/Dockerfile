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
COPY packages/wise-orchestration /deps/wise-orchestration
COPY data/registry /deps/data-registry

RUN pip install /deps/wise-common /deps/wise-contracts /deps/wise-registry /deps/wise-orchestration

COPY services/orchestrator-service/pyproject.toml services/orchestrator-service/README.md ./
COPY services/orchestrator-service/src ./src

ENV WISE_MANIFEST_ROOT=/deps/data-registry

RUN pip install .

EXPOSE 8005

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8005/health || exit 1

CMD ["uvicorn", "wise_orchestrator.main:app", "--host", "0.0.0.0", "--port", "8005"]
