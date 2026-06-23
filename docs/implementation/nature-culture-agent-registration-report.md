# Nature & Culture Agent Registration — Implementation Report

| Field | Value |
|-------|-------|
| **Version** | 1.0.0 |
| **Date** | 2026-06-23 |
| **Boundary** | Implementation layer only. Does **not** modify canonical architecture (`docs/architecture/canonical/*`) or operational `data/registry/` manifests. |

## Summary

Nature & Culture operational agent roles are registered in Open Grace by mapping seven steward-facing roles to canonical `wise.agent.*` IDs, capability framework classes, knowledge registry links, benchmark references, and audit hooks. Cross-registry validation ensures all bindings resolve after `GovernanceSystem.seed_all()`.

## Role Mappings

| Nature & Culture Role | Canonical Agent ID | Capability Class |
|-----------------------|-------------------|------------------|
| Research Agent | `wise.agent.standards` | `wise.capability.class.research` |
| Translation Agent | `wise.agent.translation` | `wise.capability.class.translation` |
| Classification Agent | `wise.agent.metadata` | `wise.capability.class.classification` |
| Extraction Agent | `wise.agent.source-discovery` | `wise.capability.class.extraction` |
| Analysis Agent | `wise.agent.knowledge-graph` | `wise.capability.class.analysis` |
| Preservation Agent | `wise.agent.preservation` | `wise.capability.class.preservation` |
| Publishing Agent | `wise.agent.publishing` | `wise.capability.class.publishing` |

The capability framework also defines **Coding** (`wise.capability.class.coding`), bound to `wise.agent.benchmark` in the base seed. That class is outside the seven Nature & Culture operational roles.

## Registry Connections

Each Nature & Culture role binding includes:

- **Knowledge Registry** — typed links to entity, place, species, heritage, collection, media, and knowledge-graph entries from the Open Grace knowledge seed
- **Capability Registry** — capability class validated via `CapabilityFrameworkRegistry.bindings_for_agent()`
- **Benchmark Registry** — two benchmark IDs per agent, matched to `agent_id` in the benchmark seed
- **Audit Registry** — two `wise.audit.nc-*` hooks per agent, registered at bind time with `subject_type=agent`

## Files Added / Changed

| Path | Change |
|------|--------|
| `packages/open-grace-agent-registry/src/open_grace_agent_registry/data/seed/nature_culture_agents.yaml` | Seed mappings for all seven roles |
| `packages/open-grace-agent-registry/src/open_grace_agent_registry/nature_culture.py` | `NatureCultureAgentRegistry`, `register_nature_culture_agents()` |
| `packages/open-grace-agent-registry/src/open_grace_agent_registry/__init__.py` | Export Nature & Culture registry API |
| `packages/open-grace-governance/src/open_grace_governance/system.py` | `nature_culture` field, `register_nature_culture_agents()`, `validate_nature_culture_registration()` |
| `tests/open_grace/test_nature_culture_agent_registration.py` | Registration and cross-registry validation tests |
| `docs/implementation/nature-culture-agent-registration-report.md` | This report |

## Usage

```python
from open_grace_governance.system import GovernanceSystem

system = GovernanceSystem.create()
system.seed_all()
registered = system.register_nature_culture_agents()  # 7
result = system.validate_nature_culture_registration()
assert result.valid
```

## Tests

```bash
cd /home/nathan/Projects/wise
. .venv/bin/activate
pip install -e packages/open-grace-governance \
            -e packages/open-grace-agent-registry \
            -e packages/open-grace-benchmarking \
            -e packages/open-grace-audit \
            -e packages/open-grace-knowledge -q
python -m pytest tests/open_grace/test_nature_culture_agent_registration.py tests/open_grace/ -q
```

**Result:** 64 passed (7 Nature & Culture registration tests + 57 existing Open Grace tests).

## Design Notes

- Registration is explicit (`register_nature_culture_agents`) and runs after `seed_all()` so canonical agents, capability classes, benchmarks, and knowledge entries exist.
- Audit hooks use stable `wise.audit.nc-{role}-{gate}` IDs and are appended to the Audit Registry at registration time.
- `validate_nature_culture_registration()` checks agent presence, capability bindings, knowledge link resolution, benchmark existence, and audit hook registration in one pass.
