---
name: ai-spend-governance
description: >-
  Designs and reviews AI / vibe-coding spend ledgers across vendor entry points:
  ingestion, person/team attribution, daily series from cycle-total-only APIs,
  rankings, and deduplicated alerts. Use when building CostLens-style governance,
  AI IDE or gateway spend sync, cost dashboards, spend attribution, or when the
  user mentions cycle totals, daily spend snapshots, or AI spend alerts.
---

# AI Spend Governance

Build a trustworthy ledger for AI tool spend when vendors expose **different grain**
(usage vs dollars, daily rows vs billing-cycle totals) and **no native team model**.

This skill encodes method, not a product codebase. Prefer checklists and schemas over
guessing vendor semantics.

## When to apply

- Unifying spend across AI IDEs, coding agents, gateways, and other entry points
- Vendor API returns **cycle-to-date totals** but product needs **daily series**
- Need person → team attribution the vendor does not provide
- Designing rankings, drill-downs, or chat/ops alerts without double-firing

## Non-goals

- Do not invent dollar amounts the API never returns
- Do not treat usage metrics (lines, requests, tabs) as spend unless a priced mapping exists
- Do not hardcode employer org charts, emails, or chat tenant IDs into shared code

## Workflow

Copy and track:

```
Spend governance progress:
- [ ] 1. Inventory entry points and API grain
- [ ] 2. Define ledger grain + identity keys
- [ ] 3. Model cycle-total → daily (if needed)
- [ ] 4. Add org attribution above vendor identity
- [ ] 5. Ship rankings / drill-down contracts
- [ ] 6. Add deduplicated alerts + sync safety
- [ ] 7. Validate with reconciliation checks
```

### 1. Inventory entry points and API grain

For each vendor / entry point, record:

| Field | Capture |
|-------|---------|
| Identity | email, user id, seat id — which is stable? |
| Spend grain | daily row / cycle total only / invoice only |
| Usage grain | daily / none |
| Cycle identity | field that marks billing period start |
| Currency unit | cents vs dollars; integer vs fractional |
| History | backfill possible? or snapshot-only going forward? |

**Rule:** usage endpoints and spend endpoints are separate truths. Join on identity + date,
never assume one implies the other.

### 2. Define ledger grain + identity keys

Canonical row (minimum):

```text
date | entry_point | person_key | cycle_id | spend_cents | usage_json | source_batch_id
```

- `person_key`: prefer verified email; keep vendor user id as secondary
- `cycle_id`: opaque billing-period key from vendor (e.g. cycle start date)
- Store money as **integer cents** after documented rounding
- Keep raw vendor payload (or hash) for audit when feasible

### 3. Cycle-total → daily series

When the spend API returns only **current cycle cumulative** per person:

```text
daily_spend = today_cycle_total - previous_same_cycle_total
```

Hard rules:

1. Diff **only inside the same `cycle_id`**
2. First snapshot of a new cycle → `daily_spend = today_cycle_total` (vendor reset)
3. Same-cycle cumulative **drop** → store as negative correction; do **not** invent a new cycle
4. Missing `cycle_id` → **abort sync** for that batch (unsafe to attribute)
5. People absent from current roster → exclude from *current* cycle active spend; freeze history

See [vendor-api-gaps.md](vendor-api-gaps.md) for edge cases and schema drift.

### 4. Org attribution above vendor identity

Vendors often have seats, not teams. Maintain a separate mapping:

```text
person_key → team_id → (optional) cost_center
```

Rules:

- One active team per person unless product explicitly supports multi-team split
- Attribution changes are versioned by effective date when rankings must stay reproducible
- Rankings always state whether they use **seat roster** or **spend-observed persons**

### 5. Rankings and drill-down contracts

Minimum surfaces:

1. **Overview** — period total, per-person average, top spenders, team comparison
2. **Team rank** — team sum → expand to members
3. **Person rank** — searchable; day / month rollups
4. **Person detail** — daily spend series + usage series (labeled as non-dollar)

UI/API copy must say when a series is **derived** (snapshot diff) vs **vendor-native daily**.

### 6. Deduplicated alerts + sync safety

Alerts (chat / email / webhook):

- Key alerts by `(date, person_key|team_id, metric, threshold_version)`
- Coalesce repeats within a quiet window; never re-page on sync replay
- Separate **data sync failure** alerts from **spend threshold** alerts

Sync safety:

- Idempotent upserts on `(date, entry_point, person_key, cycle_id)`
- Manual backfill for usage history; spend backfill only if vendor supports it
- Prefer scheduled sync + explicit “sync now”; surface last success / last error

### 7. Reconciliation checks

Before calling a ledger “trustworthy”:

- [ ] Sum of derived daily spend in-cycle ≈ current cycle total (within rounding)
- [ ] No daily rows span two `cycle_id`s via a single diff
- [ ] Roster-only and spend-only identities are explained, not silently dropped
- [ ] Usage charts never labeled as USD
- [ ] Alert keys survive re-sync without duplicates

## Output templates

When designing or reviewing a system, produce:

1. **Entry-point inventory table** (grain + identity + history)
2. **Ledger schema** (fields + primary key)
3. **Daily derivation rules** (or “native daily — no derivation”)
4. **Attribution model** (person → team)
5. **Alert matrix** (metric, threshold, dedupe key, channel)
6. **Open risks** (schema drift, missing cycle id, partial roster)

For a worked walkthrough, see [examples.md](examples.md).

## Implementation defaults

| Concern | Default |
|---------|---------|
| API shape drift | Prefer richer spend field; fall back only with tests |
| Money | Integer cents in DB; document rounding |
| Scheduler | Daily snapshot at least once per day per entry point |
| Storage | SQLite is fine for <1k seats; keep sync logic storage-agnostic |
| Secrets | API keys in env / secret store only |

## Additional resources

- [vendor-api-gaps.md](vendor-api-gaps.md) — cycle totals, schema drift, freeze rules
- [examples.md](examples.md) — design walkthrough and review checklist
