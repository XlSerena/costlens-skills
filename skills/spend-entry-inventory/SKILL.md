---
name: spend-entry-inventory
description: >-
  Inventories AI / vibe-coding spend entry points and vendor API grain (identity,
  daily vs cycle-total spend, usage, cycle id, currency, history). Use when
  starting CostLens-style governance, onboarding a new AI IDE/gateway vendor,
  or when spend and usage endpoints disagree.
---

# Spend Entry Inventory

Map every AI spend **entry point** before writing sync code. Wrong grain → wrong ledger.

Method only — do not invent vendor field names you have not seen in docs or payloads.

## When to use

- Adding Cursor / Claude / Codex / gateway / other AI seats to a spend product
- Vendor has both “usage” and “spend” APIs and nobody documented which is money
- Multi-tool rollup (“IDE + API gateway”) with unclear join keys
- User asks “what do we need from this Admin API?”

## When not to use

- Pure model-token cost estimation inside one app (no vendor seat billing)
- General cloud FinOps (EC2/S3) without AI seat / agent entry points
- Replacing finance invoice reconciliation for legal books

## Workflow

```
Entry-inventory progress:
- [ ] 1. List entry points (product surfaces humans actually use)
- [ ] 2. Per entry point: identity, spend grain, usage grain, cycle id
- [ ] 3. Currency unit + rounding policy
- [ ] 4. History: backfill vs snapshot-forward only
- [ ] 5. Mark spend vs usage as separate truths
```

### Capture table

| Field | Capture |
|-------|---------|
| `entry_point` | Stable slug (`ai_ide`, `api_gateway`, …) |
| Identity | email / user id / seat id — which is stable? |
| Spend grain | daily row / **cycle total only** / invoice only |
| Usage grain | daily / none |
| Cycle identity | field that marks billing period start |
| Currency unit | cents vs dollars; integer vs fractional |
| History | backfill possible? or snapshot-only going forward? |

**Rule:** usage endpoints and spend endpoints are separate truths. Join on identity + date; never assume one implies the other.

## Anti-rationalization

| Excuse | Reality | Required response |
|--------|---------|-------------------|
| “Usage looks like spend enough for a dashboard.” | Usage is not money. | Separate series; never label usage as USD. |
| “We’ll figure out cycle id later.” | Diffing without cycle id corrupts history. | Block sync design until cycle identity is named or N/A documented. |
| “Email and user id are interchangeable.” | Seats get rebound; emails change. | Pick primary `person_key`; store secondary ids. |
| “One sync job can treat IDE and gateway the same.” | Grains differ. | One inventory row per entry point; separate sync contracts. |
| “Finance already has invoices.” | Invoices ≠ per-seat daily governance. | Inventory seat APIs anyway if product needs person/team rank. |

## Output

Produce a filled inventory table + open questions (missing fields, unstable identity).

Canonical ledger row to aim for later:

```text
date | entry_point | person_key | cycle_id | spend_cents | usage_json | source_batch_id
```

## Related

- `cycle-total-to-daily` — when spend grain is cycle-total-only
- `spend-attribution` — person → team above vendor seats
- `spend-alerts` — deduped threshold + sync-failure alerts
- `spend-reconciliation` — trust checks before calling the ledger done

See [../../references/vendor-api-gaps.md](../../references/vendor-api-gaps.md) and [../../fixtures/synthetic/](../../fixtures/synthetic/).
