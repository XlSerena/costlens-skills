---
name: spend-attribution
description: >-
  Maps vendor seat identities to org teams/cost centers for AI spend rankings
  when vendors have no native team model. Use when building person→team
  attribution, CostLens-style team rank, or reproducible rollups across roster
  changes.
---

# Spend Attribution

Vendors have **seats**, not teams. Keep org mapping **outside** the vendor and version it when rankings must stay reproducible.

```text
person_key → team_id → (optional) cost_center
```

## When to use

- Team rank / cost-center rollups on AI IDE or gateway spend
- Roster emails exist; vendor has no team API
- People change teams mid-cycle and last month’s chart must not silently rewrite
- Multi entry-point rollup needs one human identity

## When not to use

- Vendor already is the system of record for teams **and** product accepts that model
- Splitting one human’s seat cost across N teams without a written allocation rule
- Embedding employer org charts or real emails into a **public** skill repo

## Workflow

```
Attribution progress:
- [ ] 1. Choose person_key (prefer verified email; vendor id secondary)
- [ ] 2. External mapping table with effective dates if needed
- [ ] 3. One active team per person (unless product supports split)
- [ ] 4. Declare ranking population: seat roster vs spend-observed
- [ ] 5. Multi entry_point: same person_key; keep entry_point on facts
```

### Rules

- One active team per person unless product explicitly supports multi-team split
- Attribution changes are **versioned by effective date** when historical rankings must reproduce
- Rankings always state whether they use **seat roster** or **spend-observed persons**
- Leavers: freeze history; do not delete daily facts

### Mapping row (minimum)

```text
person_key | team_id | cost_center | effective_from | effective_to | source
```

## Anti-rationalization

| Excuse | Reality | Required response |
|--------|---------|-------------------|
| “Put team name in the vendor display name field.” | Not durable; breaks on rename. | External mapping table. |
| “Unmapped spenders can be dropped.” | Silent drops bias ranks. | Show “unassigned” bucket or block publish. |
| “Overwrite team on the person row; history will be fine.” | Past team rank rewrites. | Effective-dated mapping when reproducibility matters. |
| “Gateway API keys aren’t people.” | Still need an owner rule. | Document allocation (owner / tagged project / equal split). |
| “Hardcode our org chart in the agent skill.” | Leaks employer structure. | Keep mapping in private config; skill only states the method. |

## Output

1. `person_key` policy  
2. Mapping schema + ownership of updates  
3. Ranking disclaimer text (roster vs observed; per entry point vs summed)

## Fixture

See [../../fixtures/synthetic/attribution.json](../../fixtures/synthetic/attribution.json) and roster join in `scripts/verify_fixtures.py`.

## Related

- `spend-entry-inventory` — identity stability first
- `spend-alerts` — alert keys use person_key or team_id
- `spend-reconciliation` — roster-only vs spend-only identities explained
