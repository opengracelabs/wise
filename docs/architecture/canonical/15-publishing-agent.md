# Publishing Agent

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Status** | Canonical |
| **Authority** | Open Grace Architecture Office |
| **Date** | 2026-06-22 |
| **Capability** | Publishing ([03-canonical-architecture.md](03-canonical-architecture.md), §4.10) |
| **Phase** | Publishing ([06-build-roadmap.md](06-build-roadmap.md), Phase 10) |

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
| [10-metadata-agent.md](10-metadata-agent.md) | Metadata Agent specification |
| [11-preservation-agent.md](11-preservation-agent.md) | Preservation Agent specification |
| [12-knowledge-graph-agent.md](12-knowledge-graph-agent.md) | Knowledge Graph Agent specification |
| [13-quality-review-agent.md](13-quality-review-agent.md) | Quality Review Agent specification |
| [14-translation-agent.md](14-translation-agent.md) | Translation Agent specification |
| [15-publishing-agent.md](15-publishing-agent.md) | Publishing Agent specification |

---

## 1. Purpose

The **Publishing Agent** automates the Publishing capability ([03-canonical-architecture.md](03-canonical-architecture.md), §4.10). It assembles curated institutional publications — encyclopedias, field guides, books, and reports — from canonical knowledge under editorial authority; generates IIIF manifests and structured publication packages; and routes drafts through quality and editorial gates, emitting **Publication Proposals** (JSON-LD) for steward approval before release to Public Experience, Education, and Products.

The agent does not bypass quality clearance, override curatorial narrative decisions, or publish restricted content. It composes, packages, and proposes; editors and curators approve.

---

## 2. Responsibilities

| Responsibility | Description |
|----------------|-------------|
| **Encyclopedias** | Assemble structured encyclopedia articles from knowledge-graph entities with inline entity linking, citations, media placement, and multilingual edition packaging |
| **Field guides** | Produce species and site field guides with identification keys, distribution maps, media linkage, and taxonomic authority reconciliation building on biodiversity foundations |
| **Books** | Compile long-form institutional books from curated article and guide selections with chapter structure, visual narrative layout, and export-ready publication manifests |
| **Reports** | Generate institutional and thematic reports with underlying data packages, visualization embeds, citation blocks, and Research Registry linkage |

---

## 3. Reference Models

The agent synthesizes patterns from one primary reference model ([02-reference-models.md](02-reference-models.md)):

| Model | Pattern Applied | Agent Behavior |
|-------|-----------------|----------------|
| **National Geographic** | Public science storytelling, visual-first narrative, exploration ethos, media-rich publishing, global contributor attribution | Lead with visual narrative structure; compose accessible science storytelling from canonical facts; prioritize maps, images, and media as primary carriers; attribute explorers, photographers, scientists, and community contributors; package publications for global exploration and discovery experiences |

Supporting standards alignment follows [07-reference-standards.md](07-reference-standards.md): IIIF Presentation API, IIIF Image API, EDM, HTML5, JSON-LD.

---

## 4. Position in Architecture

```
Knowledge Graph selections + preserved media + localized narratives
        ↓
Quality Review clearance + Translation Fabric locale bundles
        ↓
Publishing Agent
        ↓
Publication Proposals (JSON-LD) + IIIF manifests + editorial drafts — pending steward approval
        ↓
Published Collection Manifests written to Publishing store (approved only)
        ↓
Public Experience, Education, Products, Research Fabric
```

The agent operates in the **Publishing & Product Platform** subgraph of the Platform Plane ([04-system-diagram.md](04-system-diagram.md), §2). All outputs pass through the AI Fabric governance chain before affecting public-facing systems ([04-system-diagram.md](04-system-diagram.md), §2.2).

**Upstream inputs:** Knowledge Graph entities and relationships ([12-knowledge-graph-agent.md](12-knowledge-graph-agent.md)), quality clearance signals from the Quality Review Agent ([13-quality-review-agent.md](13-quality-review-agent.md)), localized content from the Translation Agent ([14-translation-agent.md](14-translation-agent.md)), preserved media surrogates and IIIF Image API endpoints.

**Downstream consumers:** Public Experience (entity pages, visual narratives), Education (curriculum-aligned publications), Products (API collections, embeddable packages), Research Fabric (report data packages and DOI-linked exports).

---

## 5. Publication Targets

### 5.1 Encyclopedias

| Attribute | Specification |
|-----------|---------------|
| **Sources** | Heritage, biodiversity, and culture entities with cleared quality scores; descriptive narratives; authority-linked citations |
| **Processing pattern** | Entity selection → article assembly with inline `schema:mentions` links → citation block generation → media placement → locale edition packaging |
| **Output entities** | Encyclopedia article records with entity graph backlinks, citation manifest, and publication-readiness tier |
| **Standards** | JSON-LD, schema.org, SKOS, Dublin Core ([07-reference-standards.md](07-reference-standards.md)) |

### 5.2 Field Guides

| Attribute | Specification |
|-----------|---------------|
| **Sources** | Species Registry entries, occurrence and distribution data, identification key structures, site heritage entities, preserved media |
| **Processing pattern** | Taxon or site selection → descriptive assembly → distribution map layer binding → identification key rendering → media surrogate linkage via IIIF |
| **Output entities** | Field guide entries with taxonomic authority, media provenance, geographic anchors, and identification key markup |
| **Standards** | Darwin Core, IIIF Presentation API, GeoJSON / PostGIS layer references ([07-reference-standards.md](07-reference-standards.md)) |

### 5.3 Books

| Attribute | Specification |
|-----------|---------------|
| **Sources** | Curated encyclopedia articles, field guide compilations, editorial narrative arcs, cover and chapter media |
| **Processing pattern** | Collection curation → chapter sequencing → visual narrative layout → table of contents and index generation → export manifest (web, print-ready, ebook) |
| **Output entities** | Book publication records with chapter graph, contributor attribution, and edition metadata |
| **Standards** | JSON-LD, HTML5, IIIF, EDM ([07-reference-standards.md](07-reference-standards.md)) |

### 5.4 Reports

| Attribute | Specification |
|-----------|---------------|
| **Sources** | Aggregated datasets, observatory metrics, research query snapshots, thematic entity collections |
| **Processing pattern** | Scope definition → data package assembly → visualization embed generation → narrative summary with citations → Research Registry deposit linkage |
| **Output entities** | Report publication records with underlying data package URI, DOI candidate, and reproducible query snapshot reference |
| **Standards** | JSON-LD, Dublin Core, DataCite metadata patterns, open dataset packaging ([07-reference-standards.md](07-reference-standards.md)) |

---

## 6. Editorial Workflow

The agent supports but does not replace institutional editorial authority.

### 6.1 Publication States

| State | Description |
|-------|-------------|
| `draft` | Agent-assembled proposal; not eligible for public release |
| `editorial_review` | Routed to curator or editor queue |
| `quality_blocked` | Quality Review Agent clearance missing or expired |
| `approved` | Steward approved; ready for scheduled or immediate release |
| `published` | Released to Publishing store and downstream consumers |
| `withdrawn` | Previously published; removed from public channels per steward disposition |

### 6.2 Editorial Gates

| Gate | Requirement |
|------|-------------|
| **Quality clearance** | No publication proposal advances past `draft` without cleared Quality Review Record from [13-quality-review-agent.md](13-quality-review-agent.md) |
| **Rights clearance** | All embedded media and excerpts carry parseable rights metadata; restricted items excluded or redacted |
| **Accessibility** | Alt text, captions, transcripts, and heading structure present for published-facing content (WCAG 2.1 AA) |
| **Locale completeness** | Multilingual editions meet institutional locale coverage thresholds before `approved` |
| **Curatorial sign-off** | High-significance and culturally sensitive publications require explicit curator approval |

---

## 7. Outputs

### 7.1 Publication Proposals

Each candidate publication is emitted as a **Publication Proposal** with:

| Field | Requirement |
|-------|-------------|
| **Publication type** | `encyclopedia`, `field_guide`, `book`, or `report` |
| **Title and slug** | Locale-tagged title, URL-safe identifier, edition label |
| **Content graph** | Ordered content nodes with entity URIs, narrative segments, and media references |
| **IIIF manifest** | Presentation API 3.0 manifest URI when image-rich (required for field guides and visual books) |
| **Citation block** | Structured references to canonical entities, preserved objects, and external sources |
| **Contributor attribution** | Authors, photographers, scientists, translators, and community contributors |
| **Quality clearance** | Link to approved Quality Review Record |
| **Locale editions** | Available and pending locale variants with translation provenance tiers |
| **Review requirement** | Auto-approvable (pre-registered profiles only), standard editorial review, or high-significance curator queue |

Publication Proposals are **candidates** until an editor or curator approves them through the human-approval gate.

### 7.2 IIIF Presentation Manifests

For image-rich publications, the agent generates:

- Canvas and range structure aligned to publication sections
- Image service references to preserved surrogates (IIIF Image API)
- Metadata labels in all approved locales
- Rights expressions per canvas
- Linking identifiers back to canonical entity URIs

### 7.3 Published Collection Manifests

After steward approval, persisted manifests include:

- Stable publication URI and edition identifier
- Publication type, release timestamp, and scheduling metadata
- Content graph snapshot hash for reproducibility
- Downstream API collection endpoints for Experience and Products planes
- PREMIS-aligned audit event linking to approving steward

### 7.4 Publication Coverage Reports

Each processing run emits a coverage report containing:

- Publications by type (encyclopedia, field guide, book, report) and state
- Quality-blocked and rights-blocked draft counts
- Locale edition completeness by publication
- IIIF manifest generation success rate
- Editorial queue depth and median turnaround impact

---

## 8. AI Fabric Governance

| Gate | Requirement |
|------|-------------|
| **Agent Registry** | Agent version, publication type profiles, editorial gate rules, and auto-approval thresholds registered before production runs |
| **Benchmarks** | Proposal assembly accuracy, IIIF manifest validity, citation completeness, editorial gate compliance, time-to-publish for approved workflows |
| **Evaluations** | Periodic review against Phase 10 Publishing success criteria |
| **Safety Reviews** | Verify agent does not publish without quality clearance, bypass rights restrictions, or release culturally sensitive content without curator approval |
| **Human Approval** | Editors and curators approve Publication Proposals before canonical Publishing store writes |

**Council assignment:** Implementation Council (assembly pipelines, IIIF tooling, export formats) and Execution Council (scheduled publication releases, edition updates). Research Council advises on report data packaging and reproducibility metadata.

---

## 9. Phase Alignment

| Phase | Agent Scope |
|-------|-------------|
| **Knowledge Graph (Phase 5)** | Readiness only: entity selection queries and publication candidacy inventory |
| **Quality Platform (Phase 7)** | Consume clearance signals; enforce quality gates on all publication proposals |
| **Translation Fabric (Phase 9)** | Integrate localized narrative bundles; package multilingual editions |
| **Publishing (Phase 10)** | Full encyclopedia, field guide, book, and report assembly; IIIF manifest generation; editorial workflow operational |
| **Public Experience (Phase 11)** | Release approved publications to entity pages, visual narratives, and browse surfaces |
| **Education (Phase 13)** | Supply curriculum-aligned publications and teacher resource packages |

---

## 10. Success Criteria

Aligned with Publishing phase completion criteria ([06-build-roadmap.md](06-build-roadmap.md)) and constitution Publishing Platform criteria:

- Encyclopedia contains ≥ 500 published articles with entity links and citations
- Field guide catalog ≥ 200 species/site guides with identification keys and IIIF media
- ≥ 5 institutional books published with chapter structure and export manifests
- ≥ 5 institutional reports published with underlying data packages in Research Registry
- Editorial workflow enforces Quality Platform gates before every publication
- IIIF Presentation manifests operational for all image-rich publications
- End-to-end demonstration: graph selection → agent assembly → quality clearance → editorial approval → published manifest → Public Experience delivery

---

## 11. Constraints

- **No publication without clearance.** Quality Review Agent clearance is mandatory; the agent enforces gates, editors grant release.
- **Curatorial authority is final.** Follow National Geographic's contributor-attribution and editorial narrative patterns ([02-reference-models.md](02-reference-models.md), §13): institutional editors shape public-facing story; the agent assembles, it does not invent.
- **Visual-first, fact-grounded.** Narrative structure leads with media and maps; every factual assertion traces to a canonical entity or cited source.
- **Rights before reuse.** Embedded media and excerpts require cleared rights metadata; ambiguous rights block publication.
- **Provenance mandatory.** Every published artifact traces to content graph snapshot, agent version, quality clearance, and approving steward event ([03-canonical-architecture.md](03-canonical-architecture.md), Provenance).
- **Experience Plane isolation.** Public-facing components consume Publishing APIs; they do not write directly to canonical storage (ADR-003, [08-decision-record.md](08-decision-record.md)).
- **Canonical memory is not gated.** Publications are curated views on open canonical memory; Products must not restrict access to underlying public entities ([01-mission.md](01-mission.md)).
