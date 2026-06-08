# ADR 0021 · Sprint 0 预算/模型/派单决策

## 状态

✅ **ACCEPTED · 已采纳** (2026-06-08)

> 关联: `docs/adr/0017-子agent预消化便当法.md` · `docs/adr/0018-多agent-git协作规则.md` · `docs/adr/0020-明日议题-4项.md`
> 关联可视化: `explain/21-discussion-summary.html`

---

## 背景

2026-06-08 讨论了 ADR 0020 中的两个核心议题:

- **B3 · 预算 / API key 来源** — 决定系统内置模型、BYOK、部署阶段。
- **B4 · 第一个试点子 agent** — 决定 ADR 0017 / 0018 的第一次压力测试。

同时确认 Sprint 0 回到 ADR 0017 原方案: **第 1 批先写 7 个关键 brief**, 不采用临时提出的 5 个 brief 并行方案。

---

## 决策

### 1. API key 模式: 混合模式

采用 **系统池 + BYOK** 的混合模式:

| 模式 | 用途 |
|------|------|
| 系统池 | 默认体验 / 免费用户 / Sprint 0 本地试跑 |
| BYOK | 用户自带 API key, 适合 Pro / 高级用户 / 隐私敏感场景 |

### 2. 内置模型: MiniMax token plan

系统内置模型走 **MiniMax token plan 套餐**。

已确认:

- 用户已有 MiniMax 订阅。
- MiniMax token plan 支持 **OpenAI 协议**。
- MiniMax token plan 支持 **Anthropic 协议**。

因此 `ai-orchestrator` 可优先把 MiniMax 作为系统池 provider 接入, 同时保留 DeepSeek / Claude / OpenAI / Gemini 等 12 厂商 BYOK 能力。

### 3. Sprint 0 部署: 本地优先

Sprint 0 先在本地运行:

- Docker Desktop / Git Bash
- PostgreSQL 16
- Redis 7
- MinIO
- Backend
- Frontend
- AI Orchestrator

不在 Sprint 0 上云, 不提前 K8s。

### 4. 第一个试点 agent: infra-agent

第一个试点选择:

| 字段 | 决策 |
|------|------|
| Agent | `infra-agent` |
| 任务 | `S0-15 docker-compose.yml` |
| 目的 | 验证 brief → agent → worktree → 产物 → 主控 review 的完整链路 |

理由:

1. 失败代价低。
2. 不碰业务逻辑。
3. 能解锁 backend / frontend / ai 的本地运行环境。
4. 适合测试 ADR 0017 brief 模板和 ADR 0018 git 协作规则。

### 5. Sprint 0 派单节奏: 回到 7 个关键 brief 原方案

不采用临时讨论中的“5 个 brief + 4 agent 并行”方案。

保持 ADR 0017 原方案:

| 批次 | 数量 | 内容 |
|------|------|------|
| 第 1 批 | 7 个 | S0-04 / S0-15 / S0-16 / S0-17 / S0-18 / S0-22 / S0-29 |
| 第 2 批 | 约 15 个 | 主链剩余任务 |
| 第 3 批 | 约 15 个 | 辅助 / 监控 / CI / 收尾 |

---

## 影响

- `providers.json` 后续需要补充 MiniMax provider, 或在 routing-rules 中指定 MiniMax 作为系统池默认 provider。
- 第 1 个正式派单前, 主控需要先写 `briefs/README.md`、`_template.md` 和第 1 批 7 个 brief。
- `infra-agent` 的第一个任务为 S0-15, 但必须先有 S0-04 / init.sh 的 brief 或主控产物。
- Sprint 0 仍以 M1 主链跑通为目标, 不提前做云部署。

---

## 暂不做

- 不写 brief。
- 不改 `harness.config.json`。
- 不派 agent。
- 不复制外部 HTML 原型。
- 不修改 contracts。

---

## 后续

等用户明确说“开干”后, 主控按 ADR 0017 落地顺序执行:

1. 写 `briefs/README.md` + `_template.md`。
2. 写第 1 批 7 个 brief。
3. 补 l3-v4-lite 配置。
4. 派 `infra-agent` 试点 S0-15。
5. 试点复盘后再批量写第 2 批。

---

*提议人: 用户 + 教练 · 2026-06-08*
*拍板人: 用户 · 2026-06-08*
