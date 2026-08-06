# Trigger self-test (CostLens skills)

Sanitized phrases to confirm agents pick the right skill.
Run after: `npx skills add XlSerena/costlens-skills`

## Pass phrases → expected skill

| Say this | Expect |
|----------|--------|
| “Admin API only returns cycle-to-date spend totals; we need a daily chart.” | `cycle-total-to-daily` |
| “We’re onboarding a new AI IDE seat product — what do we capture from their spend API?” | `spend-entry-inventory` |
| “Vendor has seats, not teams; we need team rank that stays reproducible.” | `spend-attribution` |
| “Every sync re-sends the same spend spike alert to chat.” | `spend-alerts` |
| “Dashboard looks fine but in-cycle dailies don’t sum to the cycle total.” | `spend-reconciliation` |

## Fail / should refuse or redirect

| Say this | Expect |
|----------|--------|
| “Estimate our in-app LLM token bill from prompt logs only.” | Not these skills (no seat Admin API) |
| “Label request counts as USD spend.” | Skill should refuse / anti-rationalization |
| “Missing cycle_id — just use calendar month.” | `cycle-total-to-daily` fail-closed |

## Local check (2026-08-06)

- [x] `npx skills add XlSerena/costlens-skills -g -y` from GitHub succeeded (Cursor + shared `~/.agents/skills/`)
- [x] Five skill folders present under `~/.agents/skills/`
- [x] Description frontmatter contains trigger keywords (see `scripts/check_trigger_phrases.py`)
- [ ] skills.sh search may lag install telemetry — recheck https://skills.sh/ later

```bash
python3 scripts/check_trigger_phrases.py
python3 scripts/verify_fixtures.py
```
