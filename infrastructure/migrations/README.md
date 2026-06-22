# migrations/

Database migrations for WISE platform schemas (`discovery`, `ingestion`, `preservation`, `modeling`, `graph`, `quality`, `registry`).

Migrations are applied after PostgreSQL init scripts in `infrastructure/docker/postgres/init/`.

Reference Capability 1 will add:

- `registry.sources` — Source Registry
- `discovery.records` — Discovery Records (JSON-LD)
- `preservation.objects` — ARK registry and fixity
- `graph.entities` — Knowledge graph entities
- `quality.reviews` — Quality Review Records

Tooling: Alembic (to be configured in implementation phase).
