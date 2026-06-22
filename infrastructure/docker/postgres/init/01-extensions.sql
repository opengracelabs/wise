-- WISE database initialization
-- Enables PostGIS and pgvector per architecture-v1.0 engineering stack (04-system-diagram §2.1)

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS vector;

-- Application schemas aligned with platform layers (03-canonical-architecture §4)
CREATE SCHEMA IF NOT EXISTS discovery;
CREATE SCHEMA IF NOT EXISTS ingestion;
CREATE SCHEMA IF NOT EXISTS preservation;
CREATE SCHEMA IF NOT EXISTS modeling;
CREATE SCHEMA IF NOT EXISTS graph;
CREATE SCHEMA IF NOT EXISTS quality;
CREATE SCHEMA IF NOT EXISTS registry;
CREATE SCHEMA IF NOT EXISTS orchestration;
CREATE SCHEMA IF NOT EXISTS species;
CREATE SCHEMA IF NOT EXISTS taxonomy;

COMMENT ON SCHEMA orchestration IS 'Orchestration plane — steward tasks, LangGraph checkpoints';
COMMENT ON SCHEMA discovery IS 'Phase 1 — Discovery catalog and Source Registry';
COMMENT ON SCHEMA ingestion IS 'Phase 2 — Ingest workflow state';
COMMENT ON SCHEMA preservation IS 'Phase 3 — ARK registry, fixity, PREMIS events';
COMMENT ON SCHEMA modeling IS 'Phase 4 — Entity assertions pending approval';
COMMENT ON SCHEMA graph IS 'Phase 5 — Canonical knowledge graph store';
COMMENT ON SCHEMA quality IS 'Phase 7 — Quality scores and curation queues';
COMMENT ON SCHEMA registry IS 'Cross-cutting — sources, agents, provenance events';
COMMENT ON SCHEMA species IS 'Biodiversity — Species Registry (RC2)';
COMMENT ON SCHEMA taxonomy IS 'Biodiversity — GBIF Taxonomic Backbone (RC2)';
