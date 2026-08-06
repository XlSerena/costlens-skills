# When the daily chart lied (and the pager wouldn’t shut up)

*Desensitized notes from building CostLens-style AI / vibe-coding spend governance.
No vendor names, no tenant IDs, no real emails — only the failure mode and the method.*

---

## The failure

We needed a **per-person daily spend** chart for AI IDE seats.

The Admin API did not offer daily dollars. It offered a **billing-cycle cumulative** total per seat — “how much this person has spent in the current cycle so far.”

The first sync job did the obvious thing: treat “today’s cumulative” as “today’s spend,” or diff against **yesterday’s wall-clock** row without checking whether the vendor had **rolled the billing cycle**.

Two symptoms showed up within a week:

1. **Chart lies** — On cycle-reset day, spend looked enormous (full new cumulative counted as one day) or jagged in ways nobody could reconcile to the vendor portal.
2. **Pager spam** — A threshold alert on “daily spend” fired again every time the sync job re-ran the same day. Backfills were worse: historical breaches re-paged the chat channel.

Neither bug was a missing dashboard widget. Both were **wrong contracts** with the vendor grain.

## What actually fixes it

### 1. Same-cycle snapshot diff (`cycle-total-to-daily`)

Persist each successful pull:

```text
date | person_key | cycle_id | cycle_total_cents
```

Derive:

```text
daily = today_total - previous_total_in_the_same_cycle_id
```

Hard rules that stop the lies:

- Diff **only** inside the same `cycle_id`
- First snapshot of a new cycle → daily = full cumulative (reset), never subtract last cycle
- Cumulative **drop** in-cycle → keep a **negative** daily (correction); do not invent a new cycle
- Missing `cycle_id` → **abort the batch** (fail closed)

If you catch yourself saying “just use calendar month as the cycle,” that is the bug wearing a costume.

### 2. Deduped alerts (`spend-alerts`)

Key threshold pages by:

```text
(date, person_key|team_id, metric, threshold_version)
```

Replaying the same sync batch must not create a new page. Backfills default to **no** historical threshold noise unless explicitly flagged. Sync failures use a **different** key (and preferably channel) from spend spikes.

### 3. Prove it with toys before production

Synthetic fixtures in this repo encode cycle reset, negative correction, abort-on-missing-cycle, unassigned spenders, and alert dedupe:

```bash
npx skills add XlSerena/costlens-skills
python3 scripts/verify_fixtures.py
```

CI runs the same script on every push.

## Skills map (install what you need)

| Symptom | Skill |
|---------|--------|
| Don’t know what the API grain is | `spend-entry-inventory` |
| Cycle totals only, need dailies | `cycle-total-to-daily` |
| Seats ≠ teams | `spend-attribution` |
| Alert fires on every sync | `spend-alerts` |
| Chart “looks fine” but math doesn’t | `spend-reconciliation` |

```bash
npx skills add XlSerena/costlens-skills
```

## What this is not

- Not a dump of company code or org charts  
- Not FinOps for EC2  
- Not “label usage counts as USD”

Method only — the kind you can hand an agent so it stops rationalizing the shortcuts that already burned you.

---

*Lan Xu — [costlens-skills](https://github.com/XlSerena/costlens-skills) · [site](https://xlserena.github.io)*
