#!/usr/bin/env python3
"""Generate identical service scaffolding for WISE platform services."""

from pathlib import Path

ROOT = Path("/home/nathan/Projects/wise/services")

SERVICES = [
    {
        "name": "discovery-service",
        "module": "discovery_service",
        "port": 8001,
        "phase": "1 — Discovery",
        "agent": "09-source-discovery-agent",
        "capability": "Discovery (03 §4.1)",
    },
    {
        "name": "metadata-service",
        "module": "wise_metadata",
        "port": 8002,
        "phase": "4 — Knowledge Modeling",
        "agent": "10-metadata-agent",
        "capability": "Knowledge Modeling (03 §4.4)",
    },
    {
        "name": "preservation-service",
        "module": "wise_preservation",
        "port": 8003,
        "phase": "3 — Preservation",
        "agent": "11-preservation-agent",
        "capability": "Preservation (03 §4.3)",
    },
    {
        "name": "knowledge-graph-service",
        "module": "wise_knowledge_graph",
        "port": 8004,
        "phase": "5 — Knowledge Graph",
        "agent": "12-knowledge-graph-agent",
        "capability": "Knowledge Graph (03 §4.5)",
    },
    {
        "name": "api-service",
        "module": "wise_api",
        "port": 8000,
        "phase": "Gateway",
        "agent": "—",
        "capability": "Platform API gateway and Founder Demonstration Surface backend",
    },
]

DOCKERFILE = """\
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \\
    PYTHONUNBUFFERED=1 \\
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl \\
    && rm -rf /var/lib/apt/lists/*

COPY packages/wise-common /deps/wise-common
COPY packages/wise-contracts /deps/wise-contracts
RUN pip install /deps/wise-common /deps/wise-contracts

COPY services/{name}/pyproject.toml services/{name}/README.md ./
COPY services/{name}/src ./src

RUN pip install .

EXPOSE {port}

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \\
    CMD curl -f http://localhost:{port}/health || exit 1

CMD ["uvicorn", "{module}.main:app", "--host", "0.0.0.0", "--port", "{port}"]
"""

PYPROJECT = """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{name}"
version = "0.1.0"
description = "WISE {name} — architecture-v1.0 scaffold"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "wise-common",
    "wise-contracts",
    "fastapi>=0.115",
    "uvicorn[standard]>=0.30",
    "pydantic-settings>=2.0",
]

[tool.hatch.build.targets.wheel]
packages = ["src/{module}"]

[tool.uvicorn]
factory = false
"""

DOCKERIGNORE = """\
__pycache__
*.pyc
.pytest_cache
.venv
.env
"""

README = """\
# {name}

WISE platform service scaffold for **{capability}**.

| Field | Value |
|-------|-------|
| **Architecture** | architecture-v1.0 |
| **Build phase** | {phase} |
| **Agent spec** | `{agent}` |
| **Port** | `{port}` |

## Endpoints (scaffold)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Liveness and readiness probe |

Business logic is implemented in Reference Capability 1 phases. See repository root `architecture-overview.md`.

## Local development

```bash
export WISE_SERVICE_NAME={name}
export WISE_LOG_LEVEL=INFO
uvicorn {module}.main:app --reload --port {port}
```

## Docker

Built from repository root:

```bash
docker compose build {name}
docker compose up {name}
```
"""

INIT = """\
\"\"\"WISE {name}.\"\"\"

__version__ = "0.1.0"
"""

MAIN = """\
\"\"\"FastAPI application entrypoint — health checks only (scaffold).\"\"\"

from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI

from wise_common.config import ServiceSettings
from wise_common.logging import configure_logging

settings = ServiceSettings(service_name="{name}")
logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging(settings.log_level)
    logger.info("service_starting", service=settings.service_name, environment=settings.environment)
    yield
    logger.info("service_stopping", service=settings.service_name)


app = FastAPI(
    title="WISE {title}",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {{
        "status": "ok",
        "service": settings.service_name,
        "environment": settings.environment,
    }}
"""

for svc in SERVICES:
    svc_dir = ROOT / svc["name"]
    mod_dir = svc_dir / "src" / svc["module"]
    mod_dir.mkdir(parents=True, exist_ok=True)

    title = svc["name"].replace("-", " ").title()
    (svc_dir / "Dockerfile").write_text(DOCKERFILE.format(**svc))
    (svc_dir / "pyproject.toml").write_text(PYPROJECT.format(**svc))
    (svc_dir / ".dockerignore").write_text(DOCKERIGNORE)
    (svc_dir / "README.md").write_text(README.format(title=title, **svc))
    (mod_dir / "__init__.py").write_text(INIT.format(**svc))
    (mod_dir / "main.py").write_text(MAIN.format(title=title, **svc))

print("Generated", len(SERVICES), "services")
