---
name: cycle-total-to-daily
description: >-
  Derives trustworthy daily AI spend series from billing-cycle cumulative vendor
  APIs via same-cycle snapshot diffs. Use when Admin APIs return cycle-to-date
  totals only, CostLens-style daily charts are required, or diffs risk crossing
  cycle boundaries.
---

# Cycle-Total → Daily

When spend APIs return only **current cycle cumulative** per person, persist snapshots and diff **inside the same `cycle_id`**.

```text
daily_spend = today_cycle_total - previous_same_cycle_total
```

## When to use

- Vendor Admin API: cycle-to-date cents, no per-day spend array
- Product needs daily person/team charts
- Review finds calendar-month used as fake `cycle_id`
- Negative days / cycle resets confuse the chart

## When not to use

- Vendor already returns native daily spend rows (document “no derivation”)
- Monthly invoice-only billing with no seat cumulatives (use explicit allocation rules instead)
- Inventing dollars from usage counts

## Workflow

```
Cycle→daily progress:
- [ ] 1. Persist each pull: date, person_key, cycle_id, cycle_total_cents
- [ ] 2. Diff only within same cycle_id
- [ ] 3. First snapshot in cycle → daily = full cumulative
- [ ] 4. In-cycle drop → negative daily (correction); do not invent new cycle
- [ ] 5. Missing cycle_id → abort batch
- [ ] 6. Reconcile sum(dailies) ≈ latest cycle total
```

### Hard rules

1. Diff **only inside the same `cycle_id`**
2. First snapshot of a new cycle → `daily_spend = today_cycle_total` (vendor reset)
3. Same-cycle cumulative **drop** → store as **negative** correction; do **not** invent a new cycle
4. Missing `cycle_id` → **abort sync** for that batch
5. People absent from current roster → exclude from *current* cycle active spend; freeze history
6. Money as **integer cents** after documented rounding

### Snapshot schema

| Field | Purpose |
|-------|---------|
| `date` / `pulled_at` | calendar day of snapshot |
| `person_key` | stable identity |
| `cycle_id` | billing period identity from vendor |
| `cycle_total_cents` | cumulative spend in that cycle |
| `source_batch_id` | sync batch for audit |

### Mid-day multiple syncs

Upsert the same date. Daily is vs **previous persisted** same-cycle snapshot for that person — not only “yesterday wall clock.”

## Anti-rationalization

| Excuse | Reality | Required response |
|--------|---------|-------------------|
| “Use calendar month as cycle_id.” | Vendor cycle ≠ month. | Use vendor cycle start / id field only. |
| “Drop negative days so charts look nice.” | Negatives are corrections/refunds. | Keep them; label in UI. |
| “Missing cycle_id — assume this month.” | Unsafe attribution. | Fail the batch closed. |
| “First day of new cycle should diff against last cycle.” | Cross-cycle diff invents spend. | Reset: first daily = today’s cumulative. |
| “We can backfill daily from usage × price later.” | Different problem; model risk. | Do not mix into this derivation path without a versioned price table. |

## Fixture

Run synthetic proofs:

```bash
python3 scripts/verify_fixtures.py
```

See [../../fixtures/synthetic/](../../fixtures/synthetic/) and [../../references/vendor-api-gaps.md](../../references/vendor-api-gaps.md).

## Related

- `spend-entry-inventory` — confirm grain is cycle-total-only first
- `spend-reconciliation` — in-cycle sum checks
- `spend-alerts` — do not re-page on snapshot replay
