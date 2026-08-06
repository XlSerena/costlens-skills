# CostLens Skills

Agent Skills distilled from **CostLens** (AI / vibe-coding spend governance):
method and checklists only — **no company code, keys, or tenant data**.

Works with any agent that can load skill markdown (Cursor, Claude Code, Codex, etc.).
Cursor install path below is one common option, not a product lock-in.

[Website](https://xlserena.github.io) · Author [XlSerena](https://github.com/XlSerena)

---

### English

**What this is** — Reusable agent instructions for designing or reviewing a trustworthy AI spend ledger when vendors expose uneven API grain (usage vs dollars, daily rows vs billing-cycle totals) and no native team model.

**What’s inside**

| Skill | Use when |
|-------|----------|
| [`ai-spend-governance`](./ai-spend-governance/) | Building or reviewing CostLens-style ingestion, attribution, daily series from cycle totals, rankings, and deduplicated alerts |

**Install**

Clone, then copy the skill folder into your agent’s skills directory:

```bash
git clone https://github.com/XlSerena/costlens-skills.git
```

Examples:

| Agent | Typical path |
|-------|----------------|
| Cursor | `~/.cursor/skills/ai-spend-governance` or project `.cursor/skills/` |
| Other agents | Follow that product’s skill / instruction-pack convention; point it at `ai-spend-governance/SKILL.md` |

```bash
# Cursor (personal, all projects)
cp -R costlens-skills/ai-spend-governance ~/.cursor/skills/ai-spend-governance
```

**Not included** — Production services, vendor API credentials, org rosters, or chat-tenant wiring. Those stay private; this repo ships the durable method.

---

### 中文

**这是什么** — 从 **CostLens**（vibe coding / AI 花销治理）脱敏蒸馏出的 Agent Skill：只含方法与清单，**不含公司代码、密钥或租户数据**。

方法本身不绑定某一家 AI IDE；凡能加载 skill / 指令包的 agent 都可用。下文 Cursor 路径只是常见安装示例。

**何时用** — 厂商 API 粒度不一致（用量 vs 金额、按日明细 vs 仅账期累计）、且没有原生「组」模型时，设计或评审一套可信的 AI 花销台账。

**安装**

```bash
git clone https://github.com/XlSerena/costlens-skills.git
# Cursor 示例（个人全局）
cp -R costlens-skills/ai-spend-governance ~/.cursor/skills/ai-spend-governance
```

其他 agent：按其 skill / 指令包约定，指向 `ai-spend-governance/SKILL.md` 即可。

---

### License

MIT — see [LICENSE](./LICENSE).
