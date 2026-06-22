# WISE — World Institutional Stewardship Engine

Permanent digital memory of humanity's heritage, nature, and culture.

**Architecture:** [architecture-v1.0](docs/architecture/canonical/) (tag `architecture-v1.0`)  
**Reference Capability 1:** One UNESCO heritage object end-to-end (in progress)

## Repository layout

```
wise/
├── apps/                    # Experience-plane applications
│   └── demonstration-surface/   # Founder Demonstration Surface (Phases 1–3)
├── services/                # Platform-plane microservices (FastAPI)
│   ├── api-service/             # API gateway
│   ├── discovery-service/       # Phase 1 — Discovery
│   ├── metadata-service/        # Phase 4 — Knowledge Modeling
│   ├── preservation-service/    # Phase 3 — Preservation
│   └── knowledge-graph-service/ # Phase 5 — Knowledge Graph
├── packages/                # Shared libraries
│   ├── wise-common/             # Config, logging
│   ├── wise-contracts/          # Interface contracts (03 §7)
│   ├── wise-registry/           # Source Registry v1 (Phase A)
│   └── wise-metadata/           # Metadata Agent v1 (Phase B)
├── infrastructure/          # Docker init, migrations, CI
├── data/                    # Reference data and seeds (not bitstreams)
├── tests/                   # Pytest smoke and integration tests
├── docs/                    # Canonical architecture (authority)
├── docker-compose.yml       # Local development stack
└── architecture-overview.md # Implementation map
```

## Engineering stack

Per `docs/architecture/canonical/04-system-diagram.md` §2.1:

| Layer | Technology |
|-------|------------|
| Services | FastAPI, Python 3.12 |
| Database | PostgreSQL 16 + PostGIS + pgvector |
| Object storage | MinIO (T0/T1 preservation tier) |
| Cache | Redis |
| Search | OpenSearch (Phase 6 scaffold) |
| Containers | Docker, docker-compose |
| CI | GitHub Actions |

## Quick start

```bash
# Configure environment
cp .env.example .env

# Start infrastructure and services
docker compose up --build

# Health checks
curl http://localhost:8000/health   # api-service
curl http://localhost:8001/health   # discovery-service
curl http://localhost:8002/health   # metadata-service
curl http://localhost:8003/health   # preservation-service
curl http://localhost:8004/health   # knowledge-graph-service
```

## Development

```bash
# Install shared packages and a service locally
pip install -e packages/wise-common -e packages/wise-contracts
pip install -e services/discovery-service

# Run smoke tests
pytest tests/ -m smoke -v

# Source Registry (unit tests, no database)
pip install -e packages/wise-registry
pytest tests/registry -m "not integration" -v

# Source Registry integration (requires PostgreSQL)
export WISE_TEST_DATABASE_URL=postgresql+psycopg://wise:wise@localhost:5432/wise_test
cd packages/wise-registry && alembic upgrade head && cd ../..
pytest tests/registry -m integration -v

# Metadata Agent (unit tests, no database)
pip install -e packages/wise-registry -e packages/wise-metadata
pytest tests/metadata -m "not integration" -v

# Metadata Agent integration (requires PostgreSQL; apply registry migrations first)
cd packages/wise-metadata && alembic upgrade head && cd ../..
pytest tests/metadata -m integration -v
```

## Architecture authority

| Document | Role |
|----------|------|
| `docs/architecture/canonical/` | **Canonical** — all design decisions |
| `docs/constitution/founder-execution-roadmap.md` | Execution companion only |
| `architecture-overview.md` | Implementation map for this repository |

## License

Institutional — see Open Grace constitutional charter.
