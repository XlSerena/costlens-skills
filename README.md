# CostLens Skills

Cursor Agent Skills distilled from **CostLens** (AI / vibe-coding spend governance):
method and checklists only — **no company code, keys, or tenant data**.

[Website](https://xlserena.github.io) · Author [XlSerena](https://github.com/XlSerena)

---

### English

**What this is** — Reusable agent instructions for designing or reviewing a trustworthy AI spend ledger when vendors expose uneven API grain (usage vs dollars, daily rows vs billing-cycle totals) and no native team model.

**What’s inside**

| Skill | Use when |
|-------|----------|
| [`ai-spend-governance`](./ai-spend-governance/) | Building or reviewing CostLens-style ingestion, attribution, daily series from cycle totals, rankings, and deduplicated alerts |

**Install (Cursor)**

```bash
# Personal skill (all projects)
git clone https://github.com/XlSerena/costlens-skills.git
cp -R costlens-skills/ai-spend-governance ~/.cursor/skills/ai-spend-governance
```

Or clone this repo and copy the skill folder into a project’s `.cursor/skills/`.

**Not included** — Production services, Admin API credentials, org rosters, or chat-tenant wiring. Those stay private; this repo ships the durable method.

---

### 中文

**这是什么** — 从 **CostLens**（vibe coding / AI 花销治理）脱敏蒸馏出的 Cursor Agent Skill：只含方法与清单，**不含公司代码、密钥或租户数据**。

**何时用** — 厂商 API 粒度不一致（用量 vs 金额、按日明细 vs 仅账期累计）、且没有原生「组」模型时，设计或评审一套可信的 AI 花销台账。

**安装**

```bash
git clone https://github.com/XlSerena/costlens-skills.git
cp -R costlens-skills/ai-spend-governance ~/.cursor/skills/ai-spend-governance
```

也可克隆后拷入项目的 `.cursor/skills/`。

---

### License

MIT — see [LICENSE](./LICENSE).
