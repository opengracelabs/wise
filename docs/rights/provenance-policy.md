# Nature & Culture Provenance Policy

**Status:** RC17 implementation policy  
**Architecture note:** Architecture v1.0 remains frozen; this policy does not modify governance, architecture, agents, or ADRs.

## 1. Purpose

Every public demo or publishable asset must have a provenance record connecting it to an original source, acquisition method, validation status, and review history.

## 2. Required provenance fields

- `provenance_id`
- `asset_id`
- `original_source`
- `source_id`
- `acquisition_method`
- `validation_status`
- `review_history`

## 3. Validation statuses

Allowed statuses:

- `draft`
- `validated_for_demo_metadata`
- `validated_for_publication`
- `blocked_pending_rights`
- `rejected`

## 4. Review history

Each provenance record must include at least one review entry with:

- date
- reviewer or review process
- finding

## 5. Production rule

Metadata-only demo provenance is not sufficient for production imagery. Production publication requires asset-level source URL, license evidence, and attribution review.
