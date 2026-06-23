# open-grace-knowledge

Open Grace Knowledge Framework v1 — governed registries for entities, places, species, heritage, collections, media, and knowledge graphs.

## ID conventions

| Registry | Pattern | Example |
|----------|---------|---------|
| Entity | `wise.entity.{slug}` | `wise.entity.unesco` |
| Place | `wise.place.{slug}` | `wise.place.everglades-national-park` |
| Species | `wise.species.{slug}` | `wise.species.panthera-leo` |
| Heritage | `wise.heritage.{slug}` | `wise.heritage.venice-lagoon` |
| Collection | `wise.collection.{slug}` | `wise.collection.gbif-occurrences-everglades` |
| Media | `wise.media.{slug}` | `wise.media.everglades-aerial-1940` |
| Knowledge Graph | `wise.knowledge.graph.{slug}` | `wise.knowledge.graph.biodiversity-everglades` |

## Reference models

Wikidata, GBIF, Europeana, Internet Archive, CIDOC CRM, Dublin Core, SKOS, PROV-O.

## Usage

```python
from pathlib import Path
from open_grace_knowledge import KnowledgeSystem

system = KnowledgeSystem.create(Path(".open-grace-knowledge"))
system.seed_all()
```

Integrate with `GovernanceSystem` via lazy imports:

```python
from open_grace_governance.system import GovernanceSystem

gov = GovernanceSystem.create()
gov.seed_all()
gov.validate_knowledge_entity("wise.entity.unesco")
reports = gov.knowledge_reports()
```
