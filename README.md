# CostLens Skills

**Stop vibe-coding spend from becoming an untrusted spreadsheet.**

Agent Skills for **AI / vibe-coding spend governance** (CostLens method):
entry-point inventory, cycle-total → daily derivation, org attribution,
deduplicated alerts, and reconciliation — **method + synthetic fixtures only**.

No company code, API keys, org rosters, or chat tenants.

[Website](https://xlserena.github.io) · Author [XlSerena](https://github.com/XlSerena) · Related: [agent-tool-safety](https://github.com/XlSerena/agent-tool-safety)

[![skills.sh](https://skills.sh/b/XlSerena/costlens-skills)](https://skills.sh/XlSerena/costlens-skills)

---

## Promise

Vendors expose uneven grain (usage vs dollars, daily rows vs **billing-cycle totals**) and usually **no team model**. These skills encode how to build a ledger you can defend in review — including the excuses teams use to skip the hard parts.

## Skills

| Skill | Trigger when | Not for |
|-------|----------------|---------|
| [`spend-entry-inventory`](./skills/spend-entry-inventory/) | Onboarding an AI IDE/gateway/vendor; spend vs usage APIs unclear | General AWS FinOps without AI seats |
| [`cycle-total-to-daily`](./skills/cycle-total-to-daily/) | Admin API is cycle-cumulative only; need daily charts | Native daily spend APIs (document “no derivation”) |
| [`spend-attribution`](./skills/spend-attribution/) | Team/cost-center rank; vendor has seats not teams | Hardcoding a real org chart into a public skill |
| [`spend-alerts`](./skills/spend-alerts/) | Chat/email alerts on spikes or sync failure; backfills re-run | Paging on usage labeled as USD |
| [`spend-reconciliation`](./skills/spend-reconciliation/) | Pre-prod review; chart “looks fine” but totals drift | Legal GL close |

Each skill has an **anti-rationalization** table: common excuses → required response.

## Install

### Fast path — [skills CLI](https://github.com/vercel-labs/skills) (Cursor, Claude Code, Codex, …)

```bash
npx skills add XlSerena/costlens-skills
npx skills add XlSerena/costlens-skills --list
npx skills add XlSerena/costlens-skills --skill cycle-total-to-daily
```

### Manual

```bash
git clone https://github.com/XlSerena/costlens-skills.git
# Cursor example (personal)
cp -R costlens-skills/skills/cycle-total-to-daily ~/.cursor/skills/cycle-total-to-daily
```

| Agent | Typical skills path |
|-------|---------------------|
| Cursor | `~/.cursor/skills/<name>` or project `.cursor/skills/` |
| Claude Code | `.claude/skills/` or plugin install |
| Codex | `.agents/skills/` / `.codex/skills/` |

## Synthetic fixtures

Prove the math without production data:

```bash
python3 scripts/verify_fixtures.py
python3 scripts/check_trigger_phrases.py
```

See [`fixtures/synthetic/`](./fixtures/synthetic/) — cycle reset, negative correction, missing `cycle_id` abort, unassigned spender, alert dedupe.

## Docs

- [`docs/story-when-the-daily-chart-lied.md`](./docs/story-when-the-daily-chart-lied.md) — desensitized launch note (chart lies + pager spam)
- [`docs/trigger-self-test.md`](./docs/trigger-self-test.md) — phrases to verify skill routing
- [`references/vendor-api-gaps.md`](./references/vendor-api-gaps.md) — edge cases
- [`references/examples.md`](./references/examples.md) — design + review walkthroughs

## Who this is for

- Platform / data engineers building AI seat spend dashboards
- Teams unifying Cursor / Claude / gateway bills into one ledger
- Reviewers who need a checklist when sync code is already messy

## Who this is not for

- Estimating in-app LLM token cost with no vendor seat API
- Replacing finance systems of record
- Copy-pasting employer emails, teams, or API keys into skills

## 中文摘要

从 **CostLens**（vibe coding / AI 花销治理）脱敏蒸馏的 Agent Skills：入口盘点、账期累计→按日、组织归因、去重告警、对账。含合成 fixture 与反合理化表。**不含公司代码与租户数据。**

```bash
npx skills add XlSerena/costlens-skills
python3 scripts/verify_fixtures.py
```

## License

MIT — see [LICENSE](./LICENSE).
