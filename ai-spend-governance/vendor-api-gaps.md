# Vendor API gaps (spend grain)

Companion to `ai-spend-governance`. Read when the vendor’s spend API is not daily-native.

## Cycle-total-only spend

**Symptom:** endpoint returns per-person **billing-cycle cumulative** dollars; no per-day spend array.

**Method:** persist each successful pull as a snapshot:

| snapshot field | purpose |
|----------------|---------|
| `pulled_at` / `date` | calendar day of the snapshot |
| `person_key` | stable identity |
| `cycle_id` | billing period identity from vendor |
| `cycle_total_cents` | cumulative spend in that cycle |

Derive:

```text
if no prior snapshot for (person_key, cycle_id):
    daily = cycle_total_cents
else:
    daily = cycle_total_cents - prior.cycle_total_cents
```

### Edge cases

| Case | Handling |
|------|----------|
| New billing cycle | Vendor resets cumulative; first snapshot daily = full cumulative that day |
| Cumulative decreases in-cycle | Keep negative daily (correction / refund / adjustment). Do not flip `cycle_id` |
| Missing cycle identity | Fail the batch; do not guess from calendar month |
| Mid-day multiple syncs | Upsert same date; daily is vs **previous persisted** same-cycle snapshot, not vs “yesterday wall clock” only |
| Person left roster | Stop updating current-cycle active views; retain historical daily rows |
| Days before current cycle start | Freeze; do not overwrite with diffs from the new cycle |

### Reconciliation

For an open cycle:

```text
sum(daily_spend where cycle_id = C) ≈ latest cycle_total_cents
```

Allow ±1–2 cents per person from rounding. Larger gaps → investigate missed sync days or identity joins.

## Usage without dollars

**Symptom:** rich daily usage (requests, lines, tabs, models) but **no money field**.

**Method:**

- Store usage in a parallel series or `usage_json`
- Never label usage as spend
- Optional: apply an explicit price table versioned by date — only if product owners accept model risk

## Schema drift

Vendors change field names. Pattern:

1. Prefer the most complete total field when present
2. Else compute from documented parts (e.g. on-demand + included)
3. Cover both shapes with tests
4. Log which branch ran per sync batch

## Multi entry-point joins

When Cursor + another tool both bill the same human:

- Normalize to one `person_key` (usually email)
- Keep `entry_point` on every fact row
- Team rankings should declare: **sum across entry points** vs **per entry point tabs**

## What not to do

- Infer daily spend from usage volume without a priced mapping
- Use calendar month as `cycle_id` when vendor has its own cycle start
- Re-send threshold alerts on every historical backfill
- Drop negative dailies to “keep charts pretty”
