---
name: spend-reconciliation
description: >-
  Validates AI spend ledgers before calling them trustworthy: in-cycle daily sums,
  cycle boundaries, roster gaps, usage-vs-spend labels, alert replay safety. Use
  when reviewing CostLens-style dashboards, sync jobs, or before production cutover.
---

# Spend Reconciliation

A ledger is not “done” when the chart renders. Run trust checks.

## When to use

- Before calling a CostLens-style dashboard production
- After changing derivation, attribution, or alert code
- User pastes schema / sync code / screenshots for review
- In-cycle totals drift from sum of dailies

## When not to use

- Greenfield brainstorm before any schema exists (use `spend-entry-inventory`)
- Legal/statutory accounting close (this is product governance, not GL)

## Workflow

```
Reconciliation progress:
- [ ] 1. Sum derived dailies in-cycle ≈ latest cycle total (± rounding)
- [ ] 2. No daily row from a cross-cycle diff
- [ ] 3. Roster-only and spend-only identities explained
- [ ] 4. Usage charts never labeled as USD
- [ ] 5. Alert keys survive re-sync without duplicates
- [ ] 6. Entry-point inventory still matches shipped sync
```

### Checks

| Check | Pass criteria |
|-------|----------------|
| In-cycle sum | `sum(daily_spend where cycle_id=C) ≈ latest cycle_total_cents` (±1–2¢/person) |
| Cycle gate | Every derived daily has a `cycle_id`; abort batches leave no partial silent rows |
| Labels | Derived vs vendor-native daily stated in UI/API copy |
| Usage | Non-dollar series named as usage |
| Attribution | Unassigned spend visible or blocked |
| Alerts | Replaying `source_batch_id` does not create new threshold pages |

### Review finding format

```text
🔴 Critical: diffs across cycle_id / missing cycle fails open / usage labeled USD
🟡 Suggestion: ranking population undocumented / unassigned spenders dropped
🟢 OK: in-cycle sum matches; alert ledger idempotent on replay
```

## Anti-rationalization

| Excuse | Reality | Required response |
|--------|---------|-------------------|
| “It’s only a few cents off.” | Can hide missed sync days. | Bound ±1–2¢; investigate larger gaps. |
| “QA clicked around; good enough.” | Charts hide grain bugs. | Run the checklist against data, not vibes. |
| “We’ll reconcile after launch.” | Wrong dailies become muscle memory. | Block “trusted” badge until checks pass. |
| “Negative days break the sum story.” | They are required for corrections. | Include negatives in the sum. |
| “Fixtures are toy data; skip them.” | Fixtures encode the contract. | `python3 scripts/verify_fixtures.py` must pass in CI or pre-merge. |

## Output

When reviewing, produce:

1. Pass/fail on each check  
2. Open risks (schema drift, partial roster, priced-usage temptation)  
3. Whether series are **derived** or **vendor-native**

## Fixture

```bash
python3 scripts/verify_fixtures.py
```

See [../../fixtures/synthetic/expected/reconciliation.json](../../fixtures/synthetic/expected/reconciliation.json).

## Related

- Full design walkthrough: [../../references/examples.md](../../references/examples.md)
- Gaps: [../../references/vendor-api-gaps.md](../../references/vendor-api-gaps.md)
