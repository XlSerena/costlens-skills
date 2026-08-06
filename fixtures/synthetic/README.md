# Synthetic spend fixtures

Toy **cycle-total-only** vendor data for proving CostLens method skills.

No real emails, tenants, or API keys — `@example.com` only.

## Layout

| Path | Role |
|------|------|
| `roster.json` | Seat identities |
| `attribution.json` | External person → team map (one person intentionally unmapped) |
| `snapshots/*.json` | Daily Admin pulls (`cycle_total_cents`) |
| `snapshots/*-ABORT.json` | Batches that must fail closed |
| `expected/` | Golden daily ledger, alerts, reconciliation |

## Story encoded

1. **Same-cycle diff** — Mar 1–4 under `cycle_id=2026-03-01`
2. **Negative correction** — Alice 1500 → 1480 on Mar 4 (`spend_cents=-20`)
3. **Cycle reset** — Apr 1 new `cycle_id`; first daily = full cumulative (not diff vs March)
4. **Fail closed** — Mar 5 batch missing `cycle_id` aborts
5. **Unassigned** — `unmapped@example.com` stays visible, not dropped
6. **Alert dedupe** — Alice Mar 2 daily 500¢ vs threshold 400¢ → one key even if replayed

## Verify

```bash
python3 scripts/verify_fixtures.py
```

Exit 0 means derivation, reconciliation, abort, attribution visibility, and alert dedupe match `expected/`.
