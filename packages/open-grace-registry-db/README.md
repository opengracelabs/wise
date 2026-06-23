# open-grace-registry-db

SQLAlchemy persistence layer for Open Grace governed registries. Additive to
`JsonRegistryStore` — YAML seeds and JSON file stores remain the default path.

## Usage

```python
from pathlib import Path
from open_grace_registry_db import RegistryDatabase, seed_all_from_yaml

db = RegistryDatabase.create("sqlite:///:memory:")
db.create_tables()
counts = seed_all_from_yaml(db)
db.export_json(Path("out/registry"))
```

## Migrations

```bash
export OPEN_GRACE_DATABASE_URL=sqlite:///./open-grace.db
cd packages/open-grace-registry-db && alembic upgrade head
```
