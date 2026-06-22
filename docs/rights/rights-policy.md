# RC17 Rights Policy

**Status:** Implementation rights policy draft  
**Scope:** RC14 content assets converted into publication-governed assets  
**Boundary:** Does not modify architecture, governance, ADRs, or the Open Grace canonical model.

## Purpose

This policy defines how RC17 content assets are classified before publication. It applies to the implementation registries under `rights/` and the content drafts under `content/`.

## Rights statuses

- **Approved**: Rights source and license are sufficient for internal publication planning; editorial review may still be required.
- **Review Required**: Source is known, but item-level rights, image rights, or data/design rights must be reviewed before publication.
- **Restricted**: Partner permission, cultural sensitivity review, or other restrictions block publication until cleared.
- **Unknown**: Not allowed for publication. Validation fails when an asset has this status.

## Publication statuses

- **Draft**: Content exists but has not entered review.
- **Editorial Review**: Content and attribution can proceed to editorial review.
- **Rights Review**: Rights clearance is required before publication.
- **Approved**: Cleared for publication planning.
- **Published**: Released by an approved publication process.

## Required asset fields

Every collection asset must include:

- Asset ID
- Source
- License
- Rights Status
- Publication Status

## Validation rules

Validation fails when:

- source is missing,
- license is unknown or missing,
- rights status is unknown or missing.
