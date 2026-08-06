---
name: spend-alerts
description: >-
  Designs deduplicated AI spend and sync-failure alerts so replays and backfills
  do not double-page. Use when wiring chat/email/webhook alerts for CostLens-style
  thresholds, vibe-coding spend spikes, or spend sync health.
---

# Spend Alerts (Deduplicated)

Threshold alerts and sync-health alerts are different streams. Both must survive **re-sync** without duplicate pages.

## When to use

- Chat / email / webhook alerts on person or team daily spend
- Scheduled sync + manual “sync now” both exist
- Backfills re-process historical days
- Users report “same spike alerted three times”

## When not to use

- One-off manual finance review with no automated channel
- Replacing vendor billing emails
- Paging on raw usage metrics labeled as dollars

## Workflow

```
Spend-alerts progress:
- [ ] 1. Split streams: threshold vs sync failure
- [ ] 2. Define metrics + thresholds + threshold_version
- [ ] 3. Dedupe key including date + subject + metric + version
- [ ] 4. Quiet window / coalesce policy
- [ ] 5. Prove replay of same batch does not re-page
```

### Alert key

```text
(date, person_key|team_id, metric, threshold_version)
```

Optional: include `entry_point` when thresholds differ per tool.

### Rules

- Coalesce repeats within a quiet window; never re-page on sync replay alone
- Separate **data sync failure** alerts from **spend threshold** alerts
- Sync safety: idempotent upserts on `(date, entry_point, person_key, cycle_id)`
- Surface last success / last error on the sync job itself

### Matrix template

| metric | threshold | dedupe key | channel |
|--------|-----------|------------|---------|
| person daily spend | configurable cents | `date\|person\|daily_spend\|v1` | chat |
| team daily spend | configurable cents | `date\|team\|daily_spend\|v1` | chat |
| sync failure | any error | `date\|sync\|entry_point` | oncall |

## Anti-rationalization

| Excuse | Reality | Required response |
|--------|---------|-------------------|
| “Alert every time the sync runs if still over threshold.” | That is a pager flood. | Fire once per dedupe key; optional daily digest. |
| “Backfill should notify for every historical breach.” | Noisy; usually unwanted. | Default: no threshold alerts on backfill unless explicitly flagged. |
| “Sync errors can share the spend alert channel with same key.” | Different owners/urgency. | Separate keys and preferably channels. |
| “We’ll dedupe in the chat group manually.” | Doesn’t scale; lost in scroll. | Persistent alert ledger keyed as above. |
| “Usage spike is close enough to spend spike.” | Mislabeled paging. | Only page on `spend_cents` (or versioned priced mapping). |

## Fixture

`fixtures/synthetic/expected/alerts.json` — same breach replayed twice → one alert id.

```bash
python3 scripts/verify_fixtures.py
```

## Related

- `cycle-total-to-daily` — derived dailies feed threshold metrics
- `spend-attribution` — team_id subjects
- `spend-reconciliation` — do not alert on known rounding ±1–2¢ as incidents
