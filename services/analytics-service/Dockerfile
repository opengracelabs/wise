FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY packages/wise-common /deps/wise-common
COPY packages/wise-demand-intelligence /deps/wise-demand-intelligence
RUN pip install /deps/wise-common /deps/wise-demand-intelligence

COPY services/analytics-service/pyproject.toml services/analytics-service/README.md ./
COPY services/analytics-service/src ./src

RUN pip install .

EXPOSE 8006

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8006/health || exit 1

CMD ["uvicorn", "wise_analytics.main:app", "--host", "0.0.0.0", "--port", "8006"]
