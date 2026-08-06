# Examples

## Example A — Design a first ledger (Cursor-like Admin API)

**Input (sanitized):**

- Members: email + vendor user id
- Spend: current cycle cumulative cents only; includes `subscription_cycle_start`
- Usage: per person per day; no dollars
- Org: teams maintained outside the vendor

**Agent output (condensed):**

1. **Inventory**

   | entry_point | identity | spend grain | usage grain | cycle id | history |
   |-------------|----------|-------------|-------------|----------|---------|
   | cursor | email (+ user id) | cycle total | daily | cycle start | usage backfill; spend snapshot-forward |

2. **Ledger PK:** `(date, entry_point, person_key, cycle_id)`

3. **Daily rule:** same-cycle snapshot diff; abort if cycle start missing

4. **Attribution:** `email → team_id` (one team); rankings note “active roster”

5. **Alerts:**

   | metric | threshold | dedupe key |
   |--------|-----------|------------|
   | person daily spend | configurable cents | `date\|person\|daily_spend\|v1` |
   | sync failure | any error | `date\|sync\|entry_point` |

6. **Risks:** schema field rename on spend total; negative correction days; leavers still in history

---

## Example B — Review an existing dashboard

Use this checklist when the user pastes schema / sync code / screenshots:

```
Review:
- [ ] Spend and usage are not conflated in labels
- [ ] Daily dollars state derived vs native
- [ ] Diffs gated on cycle identity
- [ ] Missing cycle id fails closed
- [ ] Team mapping is external and dated if needed
- [ ] Alerts dedupe on replayable keys
- [ ] In-cycle sum of dailies reconciles to cycle total
```

**Good finding format:**

```text
🟡 Suggestion: Person detail chart title says "Spend" but series is request counts.
   Relabel to "Usage (requests)" or join a priced mapping with an explicit version.
```

---

## Example C — Multi-tool rollup

**Ask:** “We have Cursor seats and a second AI gateway billed monthly per API key.”

**Approach:**

1. Two `entry_point` values; separate sync jobs
2. Gateway invoice monthly → allocate with an explicit rule (equal split, key owner, or tagged project). Document the rule; do not hide it in UI.
3. Company overview = sum of entry points after each is normalized to `spend_cents` + `date`
4. Never diff a monthly invoice as if it were a Cursor-style cycle cumulative unless the math is written down
