# Translation Agent

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Status** | Canonical |
| **Authority** | Open Grace Architecture Office |
| **Date** | 2026-06-22 |
| **Capability** | Translation Fabric ([03-canonical-architecture.md](03-canonical-architecture.md), §4.9) |
| **Phase** | Translation Fabric ([06-build-roadmap.md](06-build-roadmap.md), Phase 9) |

## Document Map

| Document | Purpose |
|----------|---------|
| [01-mission-and-constitutional-charter.md](01-mission-and-constitutional-charter.md) | Mission, charter, and constitutional relationship |
| [02-reference-models.md](02-reference-models.md) | Institutional reference models informing design |
| [03-canonical-architecture.md](03-canonical-architecture.md) | Canonical 100-year logical architecture |
| [04-system-diagram.md](04-system-diagram.md) | Canonical system diagram |
| [05-physical-architecture.md](05-physical-architecture.md) | Physical and geographic architecture |
| [06-build-roadmap.md](06-build-roadmap.md) | Implementation roadmap and founder build order |
| [07-reference-standards.md](07-reference-standards.md) | Standards, protocols, and interoperability |
| [08-decision-record.md](08-decision-record.md) | Architecture decision records |
| [09-source-discovery-agent.md](09-source-discovery-agent.md) | Source Discovery Agent specification |
| [10-metadata-agent.md](10-metadata-agent.md) | Metadata Agent specification |
| [11-preservation-agent.md](11-preservation-agent.md) | Preservation Agent specification |
| [12-knowledge-graph-agent.md](12-knowledge-graph-agent.md) | Knowledge Graph Agent specification |
| [13-quality-review-agent.md](13-quality-review-agent.md) | Quality Review Agent specification |
| [14-translation-agent.md](14-translation-agent.md) | Translation Agent specification |
| [15-publishing-agent.md](15-publishing-agent.md) | Publishing Agent specification |
| [16-education-agent.md](16-education-agent.md) | Education Agent specification |
| [17-biodiversity-observatory-agent.md](17-biodiversity-observatory-agent.md) | Biodiversity Observatory Agent specification |
| [18-climate-observatory-agent.md](18-climate-observatory-agent.md) | Climate Observatory Agent specification |
| [19-heritage-observatory-agent.md](19-heritage-observatory-agent.md) | Heritage Observatory Agent specification |
| [20-tourism-observatory-agent.md](20-tourism-observatory-agent.md) | Tourism Observatory Agent specification |
| [21-language-observatory-agent.md](21-language-observatory-agent.md) | Language Observatory Agent specification |
| [22-standards-agent.md](22-standards-agent.md) | Standards Agent specification |
| [23-benchmark-agent.md](23-benchmark-agent.md) | Benchmark Agent specification |

---

## 1. Purpose

The **Translation Agent** automates the Translation Fabric capability ([03-canonical-architecture.md](03-canonical-architecture.md), §4.9). It translates canonical content — entity labels, descriptions, narratives, and interface strings — into supported locales; maintains institutional terminology and translation memory; and routes indigenous-language and sensitive content through community-governed review workflows, emitting **Translation Proposals** (JSON-LD / XLIFF) with provenance and quality tiers for human approval before localized content enters the Knowledge Graph, Search, or Experience planes.

The agent does not replace source-language content, publish without review for protected locales, or assert community translations without attribution. It proposes localized variants; stewards and community language authorities approve.

---

## 2. Responsibilities

| Responsibility | Description |
|----------------|-------------|
| **Translate content** | Generate machine translations for entity labels, descriptive text, publishing narratives, and UI strings from source-language graph literals; align segments with translation memory; emit locale-tagged proposals with machine/human/community provenance |
| **Manage terminology** | Maintain controlled glossaries for heritage, biodiversity, conservation, and cultural domains per locale; enforce term consistency across graph labels, search facets, and published narratives; surface conflicts to terminology stewards |
| **Indigenous language support** | Apply community consent, attribution, and review policies for indigenous and endangered languages; route proposals to language-steward queues; preserve source-language authority; never auto-publish indigenous-language variants without approved workflow |

---

## 3. Reference Models

The agent synthesizes patterns from two primary reference models ([02-reference-models.md](02-reference-models.md)):

| Model | Pattern Applied | Agent Behavior |
|-------|-----------------|----------------|
| **UNESCO** | Global multilingual mandate, intangible heritage and linguistic diversity, official-language accessibility without erasing source traditions | Prioritize structural multilingualism (graph labels, search, publishing); model language as first-class heritage metadata; enforce source-language preservation; align locale coverage with UNESCO language-commitment patterns |
| **Wikimedia** | Community-governed multilingual corpus, Wikidata multilingual labels, distributed contributor translation, open attribution | Accept community translation contributions with contributor attribution; reuse Wikidata label suggestions as reconciliation hints (not canonical assertions); support translation participation workflows feeding Community platform |

Supporting standards alignment follows [07-reference-standards.md](07-reference-standards.md): XLIFF, TMX, BCP 47, ISO 639-3.

---

## 4. Position in Architecture

```
Knowledge Graph literals (source language) + UI string catalogs + Publishing drafts
        ↓
Translation Memory + Terminology Glossaries + Community submissions
        ↓
Translation Agent
        ↓
Translation Proposals (JSON-LD / XLIFF) — candidate, pending human or steward approval
        ↓
Localized Content Bundles written to Knowledge Graph (approved only)
        ↓
Search, Publishing, Public Experience, Education, Community
```

The agent operates in the **Research & Translation** subgraph of the Platform Plane ([04-system-diagram.md](04-system-diagram.md), §2). All outputs pass through the AI Fabric governance chain before affecting canonical systems ([04-system-diagram.md](04-system-diagram.md), §2.2).

**Upstream inputs:** Knowledge Graph entity literals ([12-knowledge-graph-agent.md](12-knowledge-graph-agent.md)), metadata language tags from the Metadata Agent ([10-metadata-agent.md](10-metadata-agent.md)), quality and completeness signals from the Quality Review Agent ([13-quality-review-agent.md](13-quality-review-agent.md)).

**Downstream consumers:** Search (cross-lingual retrieval), Publishing (multilingual exhibits), Public Experience and Education (locale-aware display), Community (translation contribution loop).

---

## 5. Translation Targets

### 5.1 Knowledge Graph Content

| Attribute | Specification |
|-----------|---------------|
| **Sources** | Entity `skos:prefLabel`, `skos:altLabel`, descriptive literals, place and tradition names, species vernacular names |
| **Processing pattern** | Segment extraction → terminology lookup → machine translation → memory alignment → proposal emission |
| **Output entities** | Locale-tagged label assertions linked to source literal with `prov:wasDerivedFrom` provenance |
| **Standards** | RDF language tags (BCP 47), SKOS, JSON-LD ([07-reference-standards.md](07-reference-standards.md)) |

### 5.2 Publishing and Narrative Content

| Attribute | Specification |
|-----------|---------------|
| **Sources** | Exhibit copy, story packages, educational narratives, caption and alt-text fields |
| **Processing pattern** | XLIFF segment packaging; glossary enforcement; sensitive-content detection for steward routing |
| **Output entities** | Localized narrative segments with quality tier and reviewer attribution |
| **Standards** | XLIFF 2.x, TMX for translation memory exchange ([07-reference-standards.md](07-reference-standards.md)) |

### 5.3 Interface Strings

| Attribute | Specification |
|-----------|---------------|
| **Sources** | Public Experience, Education, and Community UI string catalogs |
| **Processing pattern** | Key-based string extraction; plural and gender rule preservation; locale fallback chain computation |
| **Output entities** | Localized string bundles with `hreflang` metadata for Experience plane consumption |
| **Standards** | BCP 47, WCAG 2.1 locale requirements ([07-reference-standards.md](07-reference-standards.md)) |

### 5.4 Indigenous and Endangered Languages

| Attribute | Specification |
|-----------|---------------|
| **Sources** | Community-submitted translations, covenant-governed language corpora, steward-approved seed glossaries |
| **Processing pattern** | Consent gate → attribution capture → expert or community review queue → approved-only graph write |
| **Output entities** | Community-attributed localized literals with language-steward approval record |
| **Standards** | ISO 639-3 language identification; UNDRIP-aligned consent and attribution metadata ([07-reference-standards.md](07-reference-standards.md)) |

---

## 6. Terminology Management

The agent maintains institutional glossaries; terminology stewards approve canonical term mappings.

### 6.1 Glossary Scope

| Domain | Term Categories |
|--------|-----------------|
| **Heritage** | Site types, conservation status, material and technique vocabulary, intangible heritage categories |
| **Biodiversity** | Taxonomic ranks, habitat types, conservation threat categories, vernacular species names |
| **Culture** | Tradition names, ceremonial object classes, community-preferred place names |
| **Institutional** | Product names, legal and rights terminology, accessibility labels |

### 6.2 Glossary Output

Each glossary entry includes:

| Field | Requirement |
|-------|-------------|
| **Concept URI** | Stable SKOS concept identifier in institutional taxonomy |
| **Source term** | Authoritative source-language preferred label |
| **Locale mappings** | Approved translations per target locale with usage notes |
| **Provenance** | Steward approval, community attribution when applicable, revision history |
| **Usage constraints** | Mandatory, preferred, or deprecated; domain applicability |

Conflicts between machine translation and approved glossary terms route to terminology stewards; the agent does not override approved glossary entries.

---

## 7. Outputs

### 7.1 Translation Proposals

Each candidate localized segment is emitted as a **Translation Proposal** with:

| Field | Requirement |
|-------|-------------|
| **Source segment** | Original literal with BCP 47 language tag and graph or catalog reference |
| **Target locale** | BCP 47 / ISO 639-3 target language identifier |
| **Proposed text** | Translated or community-submitted localized string |
| **Provenance tier** | `machine`, `human-reviewed`, `community`, or `steward-approved` |
| **Attribution** | Translator, reviewer, and community contributor identifiers when applicable |
| **Quality score** | Machine confidence or steward quality rating |
| **Terminology compliance** | Glossary match status and any flagged conflicts |
| **Review requirement** | Auto-approvable, standard review, or indigenous-language / sensitive-content queue |

Translation Proposals are **candidates** until a steward or authorized language authority approves them through the human-approval gate.

### 7.2 Translation Memory Updates

Approved translation pairs are written to institutional translation memory with:

- Segment alignment (source ↔ target)
- Domain and content-type tags
- Reuse count and last-used timestamp
- Provenance linking to approving steward event

### 7.3 Locale Coverage Reports

Each processing run emits a coverage report containing:

- Languages supported vs. targeted
- Entity label translation coverage by entity type
- UI string localization completeness
- Indigenous-language workflow status (pending consent, in review, approved)
- Glossary gaps and terminology conflicts

---

## 8. AI Fabric Governance

| Gate | Requirement |
|------|-------------|
| **Agent Registry** | Agent version, supported locales, MT engine scope, and indigenous-language policy parameters registered before production runs |
| **Benchmarks** | Translation quality (BLEU/chrF+human spot-check), terminology compliance rate, memory reuse rate, indigenous-language review compliance |
| **Evaluations** | Periodic review against Phase 9 Translation Fabric success criteria |
| **Safety Reviews** | Verify agent does not replace source-language content, bypass indigenous-language consent gates, or publish sensitive cultural translations without review |
| **Human Approval** | Stewards and language authorities approve Translation Proposals before canonical localized graph writes; machine translations for protected locales always require review |

**Council assignment:** Implementation Council (pipeline and glossary tooling) and Research Council (locale expansion, endangered-language partnerships). Community Council advises on indigenous-language workflow and attribution policy.

---

## 9. Phase Alignment

| Phase | Agent Scope |
|-------|-------------|
| **Knowledge Graph (Phase 5)** | Readiness only: language-tag inventory on graph literals; locale gap analysis |
| **Translation Fabric (Phase 9)** | Full machine translation pipeline; terminology glossaries; translation memory; UI string localization; community contribution intake |
| **Publishing (Phase 10)** | Multilingual narrative and exhibit segment translation integrated with publishing workflow |
| **Community (Phase 14)** | Community translation contribution loop; indigenous-language steward queues; attribution and consent enforcement |

---

## 10. Success Criteria

Aligned with Translation Fabric phase completion criteria ([06-build-roadmap.md](06-build-roadmap.md)):

- ≥ 10 languages supported for entity labels and UI strings
- Translation memory operational with ≥ 100,000 aligned segments
- Terminology glossaries for ≥ 5 languages covering core domain vocabulary
- Source-language originals never replaced; localized variants persisted with provenance
- Indigenous-language workflow documented with community consent and attribution requirements
- Human review queue operational for sensitive and indigenous-language content
- End-to-end demonstration: source literal → agent translation → terminology check → steward approval → localized graph label → cross-lingual search retrieval

---

## 11. Constraints

- **No source-language replacement.** Translations are additive; source literals remain authoritative ([08-decision-record.md](08-decision-record.md), ADR-008).
- **No canonical localized writes without approval.** The agent proposes; stewards and language authorities approve.
- **Indigenous-language consent required.** Community-governed languages follow covenant-defined consent and attribution before publication.
- **Terminology stewards override machine output.** Approved glossary entries take precedence over machine translation suggestions.
- **Provenance mandatory.** Every localized literal traces to source segment, translation method, and approving event ([03-canonical-architecture.md](03-canonical-architecture.md), Provenance).
- **Wikidata labels are hints, not assertions.** External multilingual labels inform reconciliation; canonical localized content requires institutional approval.
- **Platform capability, not UI afterthought.** The agent serves graph, search, publishing, and experience layers per ADR-008 ([08-decision-record.md](08-decision-record.md)).
