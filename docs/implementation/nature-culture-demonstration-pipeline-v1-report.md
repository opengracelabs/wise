# Nature & Culture Demonstration Pipeline v1 — Report

## Summary

Implemented the Panthera leo Nature & Culture demonstration pipeline using Open Grace
Runtime v2 gated LangGraph execution. Seven workflow stages run through
`GovernanceSystem.run_agent()` with real gate validation and stub execution.

## Module

- `packages/open-grace-runtime/src/open_grace_runtime/pipelines/nature_culture_demo.py`
- `packages/open-grace-runtime/src/open_grace_runtime/pipelines/__init__.py`

## Workflow

| Stage | Agent | Artifact |
|-------|-------|----------|
| Research | `wise.agent.standards` | `research.md` |
| Metadata | `wise.agent.metadata` | `metadata.json` |
| Classification | `wise.agent.quality-review` | `classification.json` |
| Translation | `wise.agent.translation` | — |
| Knowledge Graph | `wise.agent.knowledge-graph` | `knowledge-graph.json` |
| Preservation | `wise.agent.preservation` | `preservation-record.json` |
| Publishing | `wise.agent.publishing` | `publication-page.md` |

## Content output

Artifacts are written to `content/species/panthera-leo/` using GBIF reference data
(`data/reference/gbif/panthera-leo-5219404.json`) and Open Grace knowledge links.

## Records

Each stage creates:

- **Execution records** — `runtime/execution_records.json`
- **Audit records** — lifecycle audit via `open-grace-audit`
- **Benchmark run records** — `runtime/benchmark_run_records.json`

## Usage

```python
from open_grace_runtime.pipelines import run_panthera_leo_pipeline

result = run_panthera_leo_pipeline()
print(result.execution_count, result.audit_count, result.benchmark_run_count)
```

## Tests

`tests/open_grace/test_nature_culture_demo_pipeline.py`
