# Education Agent

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Status** | Canonical |
| **Authority** | Open Grace Architecture Office |
| **Date** | 2026-06-22 |
| **Capability** | Education ([03-canonical-architecture.md](03-canonical-architecture.md), §5.3) |
| **Phase** | Education ([06-build-roadmap.md](06-build-roadmap.md), Phase 13) |

## Document Map

| Document | Purpose |
|----------|---------|
| [01-mission.md](01-mission.md) | Mission, charter, and constitutional relationship |
| [02-reference-models.md](02-reference-models.md) | Institutional reference models informing design |
| [03-canonical-architecture.md](03-canonical-architecture.md) | Canonical 100-year logical architecture |
| [04-system-diagram.md](04-system-diagram.md) | Canonical system diagram |
| [05-physical-architecture.md](05-physical-architecture.md) | Physical and geographic architecture |
| [06-build-roadmap.md](06-build-roadmap.md) | Implementation roadmap and founder build order |
| [07-reference-standards.md](07-reference-standards.md) | Standards, protocols, and interoperability |
| [08-decision-record.md](08-decision-record.md) | Architecture decision records |
| [09-source-discovery-agent.md](09-source-discovery-agent.md) | Source Discovery Agent specification |
| [12-knowledge-graph-agent.md](12-knowledge-graph-agent.md) | Knowledge Graph Agent specification |
| [10-metadata-agent.md](10-metadata-agent.md) | Metadata Agent specification |
| [11-preservation-agent.md](11-preservation-agent.md) | Preservation Agent specification |
| [12-knowledge-graph-agent.md](12-knowledge-graph-agent.md) | Knowledge Graph Agent specification |
| [13-quality-review-agent.md](13-quality-review-agent.md) | Quality Review Agent specification |
| [14-translation-agent.md](14-translation-agent.md) | Translation Agent specification |
| [15-education-agent.md](15-education-agent.md) | Education Agent specification |
| [16-heritage-observatory-agent.md](16-heritage-observatory-agent.md) | Heritage Observatory Agent specification |
| [17-language-observatory-agent.md](17-language-observatory-agent.md) | Language Observatory Agent specification |

---

## 1. Purpose

The **Education Agent** automates the Education capability ([03-canonical-architecture.md](03-canonical-architecture.md), §5.3). It generates curriculum-aligned learning resources from canonical collections; maps institutional content to national and international learning standards; and produces teacher guides with activity sequences, assessment rubrics, and differentiation guidance — emitting **Learning Resource Proposals** (JSON-LD / HTML5) for educator and curatorial approval before resources enter the Education portal.

The agent does not publish classroom materials without review, replace curatorial narratives with unsourced claims, or expose restricted or culturally sensitive content in student-facing bundles. It proposes learning artifacts grounded in graph-linked canonical memory; educators and curators approve.

---

## 2. Responsibilities

| Responsibility | Description |
|----------------|-------------|
| **Generate learning resources** | Assemble lesson plans, interactive exploration modules, field-study activities, and multimedia learning sequences from published exhibits, entity pages, and graph neighborhoods; enforce age-appropriate framing, rights clearance, and accessibility requirements; emit structured resource packages with entity provenance |
| **Curriculum mapping** | Align generated and existing resources to UNESCO frameworks, national standards (e.g., NGSS, C3, state frameworks), and institutional learning objectives; maintain crosswalk tables linking graph entities and publishing narratives to standard codes; surface coverage gaps and recommend canonical content for new standard alignments |
| **Teacher guides** | Produce educator-facing guides with learning objectives, prerequisite knowledge, activity timelines, discussion prompts, differentiation strategies, assessment rubrics, and safety or cultural-sensitivity notes; link every guide section to canonical source URIs and rights metadata |

---

## 3. Reference Models

The agent synthesizes patterns from two primary reference models ([02-reference-models.md](02-reference-models.md)):

| Model | Pattern Applied | Agent Behavior |
|-------|-----------------|----------------|
| **Smithsonian** | Public education mission co-equal with research, collection stewardship at scale, interdisciplinary framing across natural history and cultural heritage | Build learning modules from canonical collection objects and cross-domain graph relationships; treat classroom access as a first-class outcome of stewardship; apply institutional trust through systematic educator review and provenance-linked activities |
| **Harvard** | Curatorial authority, linked open data publishing, centuries-scale stewardship of educational materials, tiered access for sensitive collections | Route high-significance and culturally sensitive topics through expert educator and curator queues; link every learning artifact to graph entity URIs with `prov:wasDerivedFrom` provenance; apply tiered classroom access when source objects carry restriction flags; preserve durable resource packaging for long-horizon reuse |

Supporting standards alignment follows [07-reference-standards.md](07-reference-standards.md): HTML5, WCAG 2.1, SCORM (Permitted), JSON-LD, BCP 47 / ISO 639-3 (multilingual education).

---

## 4. Position in Architecture

```
Published exhibits + entity pages + graph neighborhoods + translation bundles
        ↓
Curriculum frameworks + learning objective registry + educator submissions
        ↓
Education Agent
        ↓
Learning Resource Proposals (JSON-LD / HTML5) — candidate, pending educator or curator approval
        ↓
Approved Learning Bundles written to Education catalog
        ↓
Education portal, teacher dashboards, student-safe experiences, Public Experience embeds
```

The agent operates in the **Experience Plane** Education subgraph ([04-system-diagram.md](04-system-diagram.md), §2). All outputs pass through the AI Fabric governance chain before affecting canonical systems ([04-system-diagram.md](04-system-diagram.md), §2.2).

**Upstream inputs:** Knowledge Graph entities and relationships ([12-knowledge-graph-agent.md](12-knowledge-graph-agent.md)), published narratives and exhibits from Publishing, localized content from the Translation Agent ([14-translation-agent.md](14-translation-agent.md)), quality and rights clearance signals from the Quality Review Agent ([13-quality-review-agent.md](13-quality-review-agent.md)).

**Downstream consumers:** Education portal (lesson delivery, teacher dashboards), Public Experience (embedded learning paths), Products (educational kits and API consumers), Community (educator contribution loop).

---

## 5. Resource Domains

### 5.1 Learning Resources

| Attribute | Specification |
|-----------|---------------|
| **Sources** | Published exhibit copy, entity summaries, IIIF manifests, field-guide narratives, observatory datasets cleared for classroom use |
| **Processing pattern** | Learning objective extraction → age-band framing → activity sequence assembly → rights and accessibility gate → proposal emission |
| **Output entities** | Lesson plans, interactive modules, field-study packets, and multimedia sequences with linked canonical entity URIs |
| **Standards** | HTML5, WCAG 2.1 AA, JSON-LD resource descriptors, SCORM packaging where LMS export is required ([07-reference-standards.md](07-reference-standards.md)) |

### 5.2 Curriculum Mapping

| Attribute | Specification |
|-----------|---------------|
| **Sources** | Institutional learning objective registry, UNESCO competency frameworks, national and state standard taxonomies, existing approved resource catalog |
| **Processing pattern** | Standard code ingestion → entity-to-standard alignment → coverage scoring → gap analysis → crosswalk table maintenance |
| **Output entities** | Curriculum crosswalk records linking resource identifiers to standard codes with confidence tier and reviewer attribution |
| **Standards** | SKOS concept schemes for standard vocabularies; JSON-LD alignment assertions with `skos:relatedMatch` and institutional extension properties |

### 5.3 Teacher Guides

| Attribute | Specification |
|-----------|---------------|
| **Sources** | Generated learning resources, curator-authored context, quality review accessibility findings, translation locale bundles |
| **Processing pattern** | Guide template selection by grade band and subject → objective and activity expansion → differentiation and assessment generation → sensitivity and safety annotation → proposal emission |
| **Output entities** | Educator guides with structured sections: objectives, materials, sequence, discussion prompts, differentiation, assessment, provenance appendix |
| **Standards** | HTML5 printable and web formats; WCAG 2.1 AA for educator-facing interfaces; locale-tagged variants per Translation Fabric provenance tiers |

### 5.4 Student-Safe and Sensitive Content

| Attribute | Specification |
|-----------|---------------|
| **Sources** | Quality Review restriction flags, rights metadata, cultural sensitivity annotations, partner covenant constraints |
| **Processing pattern** | Restriction gate → age-band filter → educator-queue routing for sensitive topics → approved-only student bundle assembly |
| **Output entities** | Tiered resource variants (`educator-only`, `classroom-safe`, `restricted-hold`) with disposition audit trail |
| **Standards** | RightsStatements.org and Creative Commons expressions; PREMIS-aligned audit events for disposition ([07-reference-standards.md](07-reference-standards.md)) |

---

## 6. Curriculum Framework Integration

The agent maintains alignment registries; curriculum stewards approve canonical standard mappings.

### 6.1 Framework Scope

| Framework | Alignment Use |
|-----------|---------------|
| **UNESCO** | Global citizenship, intangible heritage literacy, biodiversity education, multilingual learning competencies |
| **Science (e.g., NGSS)** | Species, ecosystem, conservation, and earth-system phenomena linked to nature graph entities |
| **Social studies / history (e.g., C3)** | Heritage sites, cultural traditions, geographic inquiry, primary-source analysis from published collections |
| **Arts and humanities** | Material culture, artistic traditions, interdisciplinary object study across Smithsonian-style collections |
| **Institutional objectives** | Open Grace mission-aligned competencies: stewardship, provenance literacy, rights-aware reuse |

### 6.2 Crosswalk Output

Each alignment record includes:

| Field | Requirement |
|-------|-------------|
| **Resource URI** | Stable identifier for the approved or proposed learning resource |
| **Standard code** | External framework identifier (URI or code literal) |
| **Graph anchors** | Canonical entity URIs supporting the alignment claim |
| **Confidence tier** | `machine-suggested`, `educator-reviewed`, or `steward-approved` |
| **Provenance** | Agent version, source narratives consumed, reviewer attribution when applicable |
| **Coverage notes** | Partial vs. full standard coverage; recommended companion resources |

Machine-suggested alignments route to educator stewards; the agent does not assert steward-approved mappings without human approval.

---

## 7. Outputs

### 7.1 Learning Resource Proposals

Each candidate classroom artifact is emitted as a **Learning Resource Proposal** with:

| Field | Requirement |
|-------|-------------|
| **Title and summary** | Age-band-appropriate title and abstract |
| **Grade band** | Target learner range and reading level |
| **Learning objectives** | Measurable objectives linked to curriculum crosswalk records |
| **Activity sequence** | Ordered steps with duration estimates and required materials |
| **Canonical anchors** | Entity URIs, exhibit references, and IIIF manifest links with `prov:wasDerivedFrom` |
| **Rights posture** | Declared reuse rights for classroom reproduction and adaptation |
| **Accessibility profile** | WCAG compliance status, alt-text coverage, caption and transcript availability |
| **Locale variants** | Available translated bundles with provenance tier per locale |
| **Review requirement** | Auto-approvable, standard educator review, or curator/sensitivity queue |

Learning Resource Proposals are **candidates** until an educator steward or curator approves them through the human-approval gate.

### 7.2 Curriculum Coverage Reports

Each processing run emits a coverage report containing:

- Standards frameworks loaded vs. targeted
- Resource count aligned per standard code and subject area
- Graph entity utilization in approved classroom materials
- Coverage gaps with recommended canonical content for new resource generation
- Grade-band and locale completeness metrics

### 7.3 Teacher Guide Bundles

Approved guides are packaged with:

- Printable and web-renderable HTML5 sections
- Linked assessment rubrics and answer-key segments (educator-only tier when applicable)
- Differentiation pathways (support, core, extension)
- Safety, cultural sensitivity, and rights reuse instructions
- Provenance appendix listing all canonical sources and review events

---

## 8. AI Fabric Governance

| Gate | Requirement |
|------|-------------|
| **Agent Registry** | Agent version, supported grade bands, framework registries, sensitivity routing rules, and SCORM export scope registered before production runs |
| **Benchmarks** | Curriculum alignment accuracy (human spot-check), accessibility compliance rate, rights-gate pass rate, educator approval turnaround impact |
| **Evaluations** | Periodic review against Phase 13 Education success criteria |
| **Safety Reviews** | Verify agent does not publish restricted content to student-facing bundles, fabricate historical or scientific claims without graph anchors, or bypass cultural-sensitivity queues |
| **Human Approval** | Educator stewards and curators approve Learning Resource Proposals before canonical Education catalog writes; sensitive topics always require expert review |

**Council assignment:** Implementation Council (resource generation pipelines, curriculum crosswalk tooling) and Research Council (framework expansion, interdisciplinary module design). Community Council advises on culturally responsive framing and classroom safety policy.

---

## 9. Phase Alignment

| Phase | Agent Scope |
|-------|-------------|
| **Publishing (Phase 10)** | Readiness only: inventory published narratives and exhibits suitable for classroom derivation |
| **Public Experience (Phase 11)** | Embed learning-path hooks on entity pages; consume Public Experience content patterns |
| **Education (Phase 13)** | Full learning resource generation; curriculum mapping registries; teacher guide production; educator review queues; Education portal catalog writes (approved only) |
| **Community (Phase 14)** | Educator contribution loop; community-submitted activity ideas routed through quality and education review |
| **Translation Fabric (Phase 9)** | Multilingual classroom bundles; locale-aware teacher guides |

---

## 10. Success Criteria

Aligned with Education phase completion criteria ([06-build-roadmap.md](06-build-roadmap.md)):

- ≥ 50 approved lesson plans across ≥ 3 subject areas
- ≥ 5 interactive exploration modules linked to canonical graph entities
- Teacher resource hub live with downloadable guides and curriculum crosswalk search
- Curriculum mappings maintained for ≥ 2 national or international frameworks
- 100% of student-facing resources pass rights clearance and WCAG 2.1 AA gates
- Sensitive and culturally restricted topics routed through curator/educator review; zero unapproved restricted content in student bundles
- End-to-end demonstration: published exhibit → agent resource proposal → curriculum alignment → educator approval → classroom module → student-safe delivery with provenance trace

---

## 11. Constraints

- **No student-facing publish without approval.** The agent proposes; educator stewards and curators approve.
- **Canonical anchors mandatory.** Every factual claim in a learning resource links to a graph entity or approved publishing narrative ([03-canonical-architecture.md](03-canonical-architecture.md), Provenance).
- **Rights before classroom reuse.** Ambiguous or restricted rights block student bundle assembly ([08-decision-record.md](08-decision-record.md)).
- **Curatorial authority on sensitive topics.** Expert judgment overrides machine-generated framing on cultural sensitivity, significance, and restricted collections — following Harvard's curatorial workflow pattern ([02-reference-models.md](02-reference-models.md), §10).
- **Research and education co-equal.** Learning resources derive from the same canonical memory as research and public experience — following Smithsonian's dual-mandate pattern ([02-reference-models.md](02-reference-models.md), §4).
- **Accessibility non-negotiable.** Student- and educator-facing outputs meet WCAG 2.1 AA before approval.
- **Free access preserved.** Educational resources must not gate access to underlying canonical public memory ([01-mission.md](01-mission.md)).
