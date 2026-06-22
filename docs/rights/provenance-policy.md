# RC17 Provenance Policy

**Status:** Implementation provenance policy draft  
**Boundary:** Does not modify architecture, governance, ADRs, or the Open Grace canonical model.

## Purpose

The provenance registry records how RC14 collection assets entered RC17 rights tracking. It provides traceability from collection drafts to rights review without writing to canonical stores.

## Provenance requirements

Each asset provenance event records:

- provenance ID,
- asset ID,
- event type,
- event date,
- actor,
- source ID,
- derived-from collection names,
- evidence path.

## Event type

RC17 currently uses `collection_asset_registered` for assets extracted from `content/collections/`.

## Evidence

The evidence reference for this prototype is the key asset list in the RC14 collection markdown files.

## Non-canonical boundary

These provenance records are implementation artifacts only. They do not create canonical provenance events or modify platform registries.
