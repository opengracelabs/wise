# Open Grace Agent System — Standards Audit

| Field | Value |
|-------|-------|
| **Version** | 1.0.0 |
| **Date** | 2026-06-23 |
| **Scope** | Open Grace Agent System (`packages/open-grace-*`, `apps/open-grace-registry`, `tests/open_grace/`) |
| **Boundary** | Implementation layer only. Does **not** modify `docs/architecture/canonical/*`. |

## Executive Summary

This audit maps the Open Grace Agent System against fourteen institutional and technical standards. Scores reflect **observed codebase evidence** as of 2026-06-23, including the MIT AI Risk Repository taxonomy extension to `RiskRegistryRecord`, seven governed registries, runtime pre-execution gates, knowledge cross-registry validation, and observability layers.

**Final maturity score: 61 / 100** (weighted average; methodology in [Scoring Methodology](#scoring-methodology)).

Strengths: governed lifecycle FSM, risk/benchmark/audit registries, capability framework cross-validation, OpenTelemetry instrumentation stub, and rich knowledge reference-model bindings (Wikidata, GBIF, CIDOC CRM, Dublin Core, SKOS, PROV-O).

Primary gaps: no production OpenSSF supply-chain controls, incomplete Internet Archive fixity workflows, no automated PROV-O serialization, PostgreSQL persistence not wired for Open Grace registries, and limited UNESCO covenant review automation.

---

## Scoring Methodology

Each standard receives a **0–100 maturity score** based on:

| Criterion | Weight within standard |
|-----------|------------------------|
| Schema / control mapping present | 25% |
| Seed data or registry evidence | 20% |
| Validation rules enforced | 25% |
| Tests demonstrating conformance | 20% |
| Runtime / integration hooks | 10% |

**Final maturity score** = Σ (standard_score × standard_weight). Weights reflect relevance to agent governance:

| Standard group | Weight |
|----------------|--------|
| MIT AI Risk Repository | 12% |
| NIST AI RMF | 12% |
| ISO/IEC 42001 | 10% |
| ISO/IEC 27001 | 10% |
| OpenTelemetry | 8% |
| UNESCO | 6% |
| Wikidata | 6% |
| GBIF | 6% |
| Internet Archive | 5% |
| CIDOC CRM | 6% |
| Dublin Core | 6% |
| SKOS | 6% |
| PROV-O | 5% |
| OpenSSF | 8% |

---

## 1. MIT AI Risk Repository

**Score: 74 / 100**

### Control Mapping

| MIT Taxonomy Dimension | Open Grace Artifact |
|------------------------|---------------------|
| Risk domain (7 domains) | `RiskRegistryRecord.risk_domain` — `packages/open-grace-governance/src/open_grace_governance/schemas/risk.py` |
| Harm type | `RiskRegistryRecord.harm_type` |
| Affected party / entity | `RiskRegistryRecord.affected_party` |
| Causal source | `RiskRegistryRecord.causal_source` |
| Intent | `RiskRegistryRecord.intent` |
| Timing (pre/post deployment) | `RiskRegistryRecord.timing` |
| Severity | `RiskRegistryRecord.severity` (aligned with MIT ordinal scale) |
| Mitigation | `RiskRegistryRecord.mitigation` + runtime gate `validate_risk_gate` |
| Residual risk | `RiskRegistryRecord.residual_risk` (validated ≤ severity) |
| Evidence | `RiskRegistryRecord.evidence` |

### Implementation Evidence

- Schema: `packages/open-grace-governance/src/open_grace_governance/schemas/risk.py`, `schemas/common.py` (`MitRiskDomain`, `MitHarmType`, etc.)
- Seed: `packages/open-grace-governance/src/open_grace_governance/data/seed/risk_registry.yaml` — 5 risks with full MIT fields; 2 MIT-framework examples (`wise.risk.prompt-injection-attack`, `wise.risk.biodiversity-misclassification`)
- Reference model: `mit-ai-risk` in `packages/open-grace-governance/src/open_grace_governance/reference_models.py`
- Validation: `validate_risk_record` in `packages/open-grace-governance/src/open_grace_governance/validation/rules.py`
- Runtime enforcement: `packages/open-grace-runtime/src/open_grace_runtime/gates.py` — `validate_risk_gate`
- Tests: `tests/open_grace/test_risk_mit_taxonomy.py` (8 tests)

### Gaps

| Gap | Risk Rating | Remediation |
|-----|-------------|-------------|
| No automated import/sync from MIT AI Risk Repository corpus | Medium | Add optional YAML import adapter mapping MIT risk IDs to `wise.risk.*` |
| Sub-domain granularity not modeled | Low | Extend schema with optional `risk_subdomain` field |
| No fleet-level MIT risk dashboard | Medium | Expose aggregated risk reports in `apps/open-grace-registry` |

---

## 2. NIST AI RMF

**Score: 68 / 100**

### Control Mapping

| NIST Function / Category | Open Grace Artifact |
|--------------------------|---------------------|
| GOVERN — policies & roles | `CapabilityFrameworkRecord` owner/steward fields; `GovernanceSystem` coordinator |
| MAP — context & risks | `RiskRegistry` with `framework: nist-ai-rmf`, `control_id: MAP-*` |
| MEASURE — benchmarks | `packages/open-grace-benchmarking/` — threshold evaluation |
| MANAGE — mitigations | Runtime gates, lifecycle approval, `mitigation` on risks |
| Documentation / traceability | Audit registry, lifecycle FSM |

### Implementation Evidence

- Risks: `wise.risk.model-hallucination` (MAP-1.1) in `risk_registry.yaml`
- Capability classes reference `nist-ai-rmf` in `capability_framework.yaml`
- Benchmark evaluation: `open_grace_benchmarking.benchmark_registry.evaluate_benchmark`
- Agent approval: `GovernanceSystem.validate_agent_approval` — `packages/open-grace-governance/src/open_grace_governance/system.py`
- Tests: `tests/open_grace/test_agent_approval_gate.py`, `tests/open_grace/test_capability_validation.py`

### Gaps

| Gap | Risk Rating | Remediation |
|-----|-------------|-------------|
| No explicit GOVERN/MAP/MEASURE/MANAGE function tagging on records | Medium | Add `nist_function` optional field to risks and capability classes |
| Impact assessment worksheet not generated | Medium | Add `generate_nist_impact_report()` to governance reports |
| Third-party AI model risk (MAP-2) not fully traced | High | Link `ModelRegistryRecord` safety tiers to NIST impact categories |

---

## 3. ISO/IEC 42001 (AI Management System)

**Score: 66 / 100**

### Control Mapping

| ISO 42001 Theme | Open Grace Artifact |
|-----------------|---------------------|
| AI policy & objectives | Capability framework classes with `owner`, `audit_requirements` |
| Risk treatment (6.1) | `wise.risk.rights-clearance-gap` — `control_id: 6.1.2` |
| Operational planning | Seven-stage lifecycle FSM — `lifecycle.py` |
| Performance evaluation | Benchmark registry + observability metrics |
| Continual improvement | Lifecycle AUDIT → PUBLICATION loop |

### Implementation Evidence

- Lifecycle: `packages/open-grace-governance/src/open_grace_governance/lifecycle.py`
- Rights risk: `risk_registry.yaml` — `framework: iso-42001`
- Capability framework seed with `audit_requirements` — `capability_framework.yaml`
- LangGraph lifecycle wiring: `packages/open-grace-governance/src/open_grace_governance/execution/langgraph.py`
- Tests: `tests/open_grace/test_lifecycle.py`, `tests/open_grace/test_langgraph_execution.py`

### Gaps

| Gap | Risk Rating | Remediation |
|-----|-------------|-------------|
| No documented AI management system scope statement | Medium | Add `docs/governance/iso-42001-scope.md` (non-canonical) |
| No management review cadence metadata | Low | Add `review_cycle` to capability framework records |
| AI system inventory not exportable as 42001 asset register | Medium | Add `export_ai_inventory()` on `GovernanceSystem` |

---

## 4. ISO/IEC 27001 (Information Security)

**Score: 63 / 100**

### Control Mapping

| ISO 27001 Control Area | Open Grace Artifact |
|------------------------|---------------------|
| A.8 Asset management | Governed registries with lifecycle metadata |
| A.8.2 Privileged access | `wise.risk.unauthorized-canonical-write` — `control_id: A.8.2` |
| A.12 Operations security | Runtime pre-execution gates |
| A.18 Compliance | Audit registry with `evidence_ref`, `trace_id` |

### Implementation Evidence

- Security risk: `risk_registry.yaml` — preservation agent, `read_only` constitutional pattern
- Constitutional agent warnings: `validate_agent_record` — `validation/rules.py`
- Audit trail: `packages/open-grace-audit/src/open_grace_audit/audit_registry.py`
- Restricted model plane check: `validate_model_record` — constitutional plane blocked for restricted models
- Tests: `tests/open_grace/test_validation.py`, `tests/open_grace/test_audit_registry.py`

### Gaps

| Gap | Risk Rating | Remediation |
|-----|-------------|-------------|
| No access-control matrix (RBAC) for steward actors | High | Integrate steward identity with WISE auth layer |
| No encryption-at-rest policy on JSON stores | Medium | Document encryption requirements; migrate to PostgreSQL with TDE |
| Incident response playbook not linked to risks | High | Add `incident_playbook_ref` to critical risks |

---

## 5. OpenTelemetry

**Score: 71 / 100**

### Control Mapping

| OTel Requirement | Open Grace Artifact |
|------------------|---------------------|
| Distributed tracing | `layers/opentelemetry.py` — `trace_agent_execution` |
| Trace context propagation | `SpanContext`, `metric_attributes_from_span` |
| Metrics semantic conventions | Prometheus definitions — `data/prometheus/metric_definitions.yaml` |
| Standards binding | `wise.standard.opentelemetry` in `standards_registry.yaml` |

### Implementation Evidence

- Instrumentation: `packages/open-grace-observability/src/open_grace_observability/layers/opentelemetry.py`
- Metric correlation: `GovernanceSystem.record_agent_metric` accepts `trace_id`, `span_id`
- Observability validation warns when `trace_id` set without `opentelemetry` reference model
- Grafana dashboard seed: `data/grafana/dashboards/open-grace-overview.json`
- Tests: `tests/open_grace/test_observability_layers.py`, `test_observability_governance_integration.py`

### Gaps

| Gap | Risk Rating | Remediation |
|-----|-------------|-------------|
| OTel SDK optional — stub tracer used when package absent | Medium | Add `opentelemetry-api` as default dependency |
| No OTLP exporter configuration | Medium | Add exporter config in observability system |
| Logs (Loki) streams defined but not wired to runtime | Low | Connect `log_streams.yaml` to agent execution events |

---

## 6. UNESCO (Heritage Stewardship)

**Score: 57 / 100**

### Control Mapping

| UNESCO Principle | Open Grace Artifact |
|------------------|---------------------|
| Outstanding universal value stewardship | Heritage registry with `unesco_id`, `heritage_type` |
| Covenant / community review | Capability `community_consent_when_required` audit requirement |
| Heritage-risk classification | Reference model `unesco` in governance + knowledge |

### Implementation Evidence

- Reference model: `reference_models.py` — UNESCO profile
- Heritage seed: `packages/open-grace-knowledge/src/open_grace_knowledge/data/seed/heritage_registry.yaml`
- Rights risk references UNESCO: `wise.risk.rights-clearance-gap`
- Capability class Research references `unesco` — `capability_framework.yaml`
- Tests: `tests/open_grace/test_knowledge_registries.py`, `test_nature_culture_agent_registration.py`

### Gaps

| Gap | Risk Rating | Remediation |
|-----|-------------|-------------|
| No automated OUV (outstanding universal value) assessment workflow | Medium | Add heritage compliance report generator |
| Indigenous/community consent not enforced at runtime gate | High | Add consent-check gate for translation capability class |
| UNESCO state-of-conservation monitoring not modeled | Low | Extend heritage schema with `soc_status` field |

---

## 7. Wikidata

**Score: 63 / 100**

### Control Mapping

| Wikidata Practice | Open Grace Artifact |
|-------------------|---------------------|
| Entity authority (QIDs) | `external_ids.wikidata` on entity/heritage/place records |
| Same-as linking | Knowledge graph `external_ids` |
| Schema conformance | `validate_entity_record` warns on missing wikidata ID when model declared |

### Implementation Evidence

- Entity seed: `packages/open-grace-knowledge/src/open_grace_knowledge/data/seed/entity_registry.yaml` — Q7809, Q604659
- Knowledge graph: `knowledge_graph_registry.yaml` — wikidata bindings
- Standard: `wise.standard.schema-org` references wikidata reference model
- WISE metadata crosswalks: `packages/wise-metadata/migrations/versions/002_seed_schema_mappings.py`
- Tests: `tests/open_grace/test_knowledge_validation.py`

### Gaps

| Gap | Risk Rating | Remediation |
|-----|-------------|-------------|
| No live Wikidata SPARQL validation at runtime | Medium | Add optional QID existence check in knowledge validation |
| Label/description sync not automated | Low | Wire metadata pipeline Wikidata fetch to knowledge registries |
| Entity resolution confidence not scored | Medium | Add `authority_confidence` field to entity records |

---

## 8. GBIF (Biodiversity)

**Score: 61 / 100**

### Control Mapping

| GBIF Requirement | Open Grace Artifact |
|------------------|---------------------|
| Taxonomic keys | `SpeciesRegistryRecord.gbif_taxon_key` |
| Darwin Core binding | `wise.standard.darwin-core` in standards registry |
| Occurrence data quality | Species validation rules |

### Implementation Evidence

- Species seed: `packages/open-grace-knowledge/src/open_grace_knowledge/data/seed/species_registry.yaml`
- Validation: `validate_species_record` — warns when GBIF model declared without taxon key
- MIT risk: `wise.risk.biodiversity-misclassification` — ecosystem harm, GBIF evidence path
- Capability classes require `wise.standard.darwin-core`
- Tests: `tests/open_grace/test_knowledge_validation.py`

### Gaps

| Gap | Risk Rating | Remediation |
|-----|-------------|-------------|
| No Darwin Core occurrence record schema in Open Grace knowledge | Medium | Add occurrence registry with dwc:fields |
| GBIF API validation not invoked | Medium | Add optional taxon key lookup in species validation |
| No checklist bank integration | Low | Document GBIF checklist binding in species metadata |

---

## 9. Internet Archive

**Score: 49 / 100**

### Control Mapping

| IA Practice | Open Grace Artifact |
|-------------|---------------------|
| Long-term preservation | Reference model `internet-archive` in governance |
| Fixity / format migration | `knowledge_use` in reference model profile |
| Media access obligations | Media registry with preservation-oriented reference models |

### Implementation Evidence

- Governance reference: `reference_models.py` — Internet Archive profile
- Knowledge reference: `packages/open-grace-knowledge/src/open_grace_knowledge/reference_models.py`
- Media seed: `packages/open-grace-knowledge/src/open_grace_knowledge/data/seed/media_registry.yaml` — `prov-o`, `dublin-core`
- Standard `schema-org` references `internet-archive`

### Gaps

| Gap | Risk Rating | Remediation |
|-----|-------------|-------------|
| No fixity check (checksum) workflow | High | Add `fixity_digest` to media records with validation |
| No IA Wayback / item URI binding | Medium | Add `ia_item_uri` external ID type |
| No format migration policy engine | High | Integrate with `wise-preservation` service patterns |

---

## 10. CIDOC CRM

**Score: 56 / 100**

### Control Mapping

| CIDOC CRM Element | Open Grace Artifact |
|-------------------|---------------------|
| Heritage object typing | `cidoc_class` on heritage records (E22, E27) |
| Standards binding | `wise.standard.cidoc-crm` — `standards_registry.yaml` |
| Museum semantics | Heritage ↔ place ↔ entity linkage |

### Implementation Evidence

- Standard registry entry: `wise.standard.cidoc-crm`, `schema_family: heritage`
- Heritage seed: `heritage_registry.yaml` — `cidoc_class: E22_Human-Made_Object`, `E27_Site`
- Required by Research and Classification capability classes
- WISE metadata CIDOC mappings: `002_seed_schema_mappings.py`

### Gaps

| Gap | Risk Rating | Remediation |
|-----|-------------|-------------|
| No CRMaaS or full CIDOC serialization | Medium | Add optional `cidoc_rdf` export on heritage records |
| Event/provenance chains not CRM-typed | Medium | Map audit events to CIDOC E5/E7 classes |
| No validation against official CIDOC OWL | Low | Add SHACL or SPARQL conformance check (optional) |

---

## 11. Dublin Core

**Score: 59 / 100**

### Control Mapping

| Dublin Core Term | Open Grace Artifact |
|------------------|---------------------|
| dcterms:Dataset / Collection | `CollectionRegistryRecord.dublin_core_profile` |
| Resource description | Entity `description`, collection metadata |
| Identifier / rights | Media and entity external IDs |

### Implementation Evidence

- Knowledge reference model: `dublin-core` in `open_grace_knowledge/reference_models.py`
- Collection seed: `packages/open-grace-knowledge/src/open_grace_knowledge/data/seed/collection_registry.yaml` — `dcterms:Dataset`, `dcterms:Collection`
- Entity records declare `dublin-core` reference model
- WISE metadata Dublin Core crosswalks in migrations

### Gaps

| Gap | Risk Rating | Remediation |
|-----|-------------|-------------|
| Dublin Core terms not enforced as required fields | Medium | Add DC term validation map per `dublin_core_profile` |
| No DCAT export for collections | Low | Add `export_dcat()` on collection registry |
| Rights (`dcterms:rights`) not uniformly populated | Medium | Require rights URI on published media records |

---

## 12. SKOS

**Score: 57 / 100**

### Control Mapping

| SKOS Concept | Open Grace Artifact |
|--------------|---------------------|
| Concept schemes | `KnowledgeGraphRegistryRecord.skos_concept_scheme` |
| Controlled vocabularies | Species/KG reference models include `skos` |
| Authority alignment | WISE metadata `skos_payload` on authority proposals |

### Implementation Evidence

- KG seed: `knowledge_graph_registry.yaml` — `wise.skos.biodiversity-everglades`, etc.
- Species seed references `skos` reference model
- WISE metadata: `authority_proposer.py` emits `skos:prefLabel`, `skos:exactMatch`
- Knowledge validation: reference model slug catalog includes `skos`

### Gaps

| Gap | Risk Rating | Remediation |
|-----|-------------|-------------|
| No broader/narrower relation validation in Open Grace | Medium | Add `skos:broader` / `skos:narrower` to KG schema |
| SKOS payloads not stored in Open Grace knowledge registries | Medium | Mirror metadata SKOS payloads into entity records |
| No SKOS-XL labels for multilingual agents | Low | Extend translation capability with SKOS-XL binding |

---

## 13. PROV-O (Provenance)

**Score: 53 / 100**

### Control Mapping

| PROV-O Class | Open Grace Artifact |
|--------------|---------------------|
| prov:Activity | Agent execution events, audit lifecycle transitions |
| prov:Agent | `steward_actor`, `reviewer_id` on governed records |
| prov:Entity | Knowledge entities, audit `evidence_ref` |
| prov:wasDerivedFrom | Audit evidence linkage, benchmark run records |

### Implementation Evidence

- Reference model: `prov-o` in knowledge `reference_models.py`
- Entity/media seeds declare `prov-o` reference model
- Audit records: `evidence_ref`, `trace_id` — `schemas/audit.py`
- Runtime benchmark run store: `packages/open-grace-runtime/src/open_grace_runtime/stores.py`

### Gaps

| Gap | Risk Rating | Remediation |
|-----|-------------|-------------|
| No PROV-O JSON-LD serialization emitted | High | Add `export_prov_graph()` for agent runs and audits |
| Derivation chains incomplete across registries | Medium | Link audit → benchmark → risk in provenance graph |
| No prov:hadRole for steward actors | Low | Add role typing to audit records |

---

## 14. OpenSSF (Supply Chain Security)

**Score: 34 / 100**

### Control Mapping

| OpenSSF Practice | Open Grace Artifact |
|------------------|---------------------|
| Dependency transparency | Python `pyproject.toml` per package (manual) |
| Secure development | Pre-commit hooks at repo root (WISE monorepo) |
| Provenance / SBOM | Reference model slug `openssf` in governance catalog |

### Implementation Evidence

- Reference model added: `openssf` in `packages/open-grace-governance/src/open_grace_governance/reference_models.py`
- Package isolation: separate `packages/open-grace-*` with independent `pyproject.toml`
- No Open Grace-specific SBOM or sigstore integration

### Gaps

| Gap | Risk Rating | Remediation |
|-----|-------------|-------------|
| No SBOM generation for Open Grace packages | Critical | Add `syft` or `cyclonedx-py` to CI for open-grace packages |
| No dependency vulnerability scanning gate | High | Integrate `pip-audit` or OSV scanner in `tests/open_grace` CI |
| No SLSA provenance attestations | High | Publish build provenance for release artifacts |
| Model weights / HF model provenance not tracked | High | Extend `ModelRegistryRecord` with `supply_chain_ref` |

---

## Score Summary

| Standard | Score | Weight | Weighted |
|----------|------:|-------:|---------:|
| MIT AI Risk Repository | 74 | 12% | 8.88 |
| NIST AI RMF | 68 | 12% | 8.16 |
| ISO/IEC 42001 | 66 | 10% | 6.60 |
| ISO/IEC 27001 | 63 | 10% | 6.30 |
| OpenTelemetry | 71 | 8% | 5.68 |
| UNESCO | 57 | 6% | 3.42 |
| Wikidata | 63 | 6% | 3.78 |
| GBIF | 61 | 6% | 3.66 |
| Internet Archive | 49 | 5% | 2.45 |
| CIDOC CRM | 56 | 6% | 3.36 |
| Dublin Core | 59 | 6% | 3.54 |
| SKOS | 57 | 6% | 3.42 |
| PROV-O | 53 | 5% | 2.65 |
| OpenSSF | 34 | 8% | 2.72 |
| **Total** | | **100%** | **61.42** |

### Final Maturity Score: **61 / 100**

Rounded per audit convention. Maturity tier: **Developing** (51–70 band) — core governance scaffolding is in place with registry-backed evidence, but production hardening (security RBAC, supply chain, provenance serialization, and external standard automation) remains incomplete.

---

## Cross-Cutting Recommendations (Priority Order)

1. **Critical — OpenSSF**: Add SBOM + vulnerability scanning to Open Grace CI pipeline.
2. **High — ISO 27001**: Steward RBAC and incident playbook linkage on critical risks.
3. **High — PROV-O**: Emit provenance graphs for agent runs linking audit, benchmark, and risk evidence.
4. **High — UNESCO / rights**: Runtime consent gate for translation and heritage capabilities.
5. **Medium — MIT / NIST**: Fleet risk dashboard and NIST function tagging.
6. **Medium — Internet Archive**: Fixity digests on media registry records.

---

## Test Coverage Reference

Open Grace test suite (`tests/open_grace/`): **85 tests** after MIT taxonomy addition (including 8 new tests in `test_risk_mit_taxonomy.py`).

```bash
cd /home/nathan/Projects/wise && . .venv/bin/activate && \
  pip install -e packages/open-grace-governance \
              -e packages/open-grace-agent-registry \
              -e packages/open-grace-benchmarking \
              -e packages/open-grace-audit \
              -e packages/open-grace-knowledge \
              -e packages/open-grace-observability \
              -e packages/open-grace-runtime -q && \
  python -m pytest tests/open_grace/ -q
```

---

*Implementation audit. Does not modify Architecture v1.0, canonical governance documents, ADRs, or operational WISE registry manifests.*
