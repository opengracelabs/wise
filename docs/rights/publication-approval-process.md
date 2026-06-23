# RC17 Publication Approval Process

**Status:** Implementation publication process draft  
**Boundary:** Does not modify architecture, governance, ADRs, or the Open Grace canonical model.

## Purpose

This process defines validation-only publication gating for RC14 content assets.

## Approval flow

1. Asset is registered from `content/collections/`.
2. Source and license are assigned.
3. Rights status is assigned.
4. Publication status is assigned.
5. Blockers are recorded when rights status is not approved.
6. Approved assets may proceed to editorial review.
7. Review-required or restricted assets remain blocked from publication.

## Blocking rules

An asset is blocked from publication when:

- rights status is `Restricted`,
- rights status is `Unknown`,
- license is unknown or missing,
- source is missing,
- required partner or sensitivity review has not completed.

## Current RC17 posture

RC17 is a publication-governance prototype. No asset is marked `Published`.
