# Nature & Culture Rights Policy

**Status:** RC17 implementation policy  
**Scope:** Rights classification and publication safety for Nature & Culture public demonstration and publishing artifacts.  
**Architecture note:** Architecture v1.0 remains frozen; this policy does not modify governance, architecture, agents, or ADRs.

## 1. Rights status classes

Nature & Culture uses the following rights classes:

- Public Domain
- CC0
- CC-BY
- CC-BY-SA
- Rights Restricted
- Unknown

## 2. Validation rule

Publication validation fails when a publishable asset has `rights_status: "Unknown"`.

Unknown rights may exist as a license class in `rights/license-registry.json`, but Unknown must not be used for approved public demo assets.

## 3. Demonstration use

Assets may be approved for metadata/text/placeholder demonstration without being approved for final image or product use.

Allowed demo uses:

- Metadata display
- Textual educational reference
- Placeholder product copy
- Internal editorial review

Blocked until item-level clearance:

- Final product mockups
- Commercial image publication
- Paid advertising
- Print-on-demand production
- Ebook/audiobook cover art
- YouTube thumbnails and final visuals

## 4. Commercial use

Commercial-use approval requires:

1. Asset-level source URL.
2. License or public-domain evidence.
3. Required credit line.
4. Jurisdiction review.
5. Publication approval record.

No payment processing, checkout, order creation, fulfillment, or customer data collection is enabled by this policy.
