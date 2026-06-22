# Nature & Culture Attribution Policy

**Status:** RC17 implementation policy  
**Architecture note:** Architecture v1.0 remains frozen; this policy does not modify governance, architecture, agents, or ADRs.

## 1. Purpose

Attribution preserves public trust, source transparency, and license compliance.

## 2. Required attribution fields

- `attribution_id`
- `asset_id`
- `display_title`
- `source_authority`
- `source_url`
- `required_credit_line`
- `license_id`
- `attribution_required`
- `attribution_status`

## 3. Credit line rule

Every public artifact should display or store a credit line even when attribution is not legally required.

Minimum credit line:

```text
Source: {source_authority}. Individual asset URL required before production publication.
```

## 4. Missing attribution

If source URL or credit line is missing, the asset remains blocked for production publication and may only be used for metadata/text demonstration.

## 5. Product rule

No product page, print product, video, pin, ebook, or audiobook cover may be production-published without attribution review.
