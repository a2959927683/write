# Master Project · 云笔AI 复刻主控

> **主控定位**: 全栈项目总架构师 + 调度中枢 (Orchestrator/Controller)。
> **复刻目标**: 1:1 复刻云笔AI 小说写作助手 (aixiaoshuojia.cn) 的 17 模块世界设定系统 + 编辑器 + AI 调度 + 蒸馏管线。
> **对标产品**: 云笔AI 小说写作助手 (Project ID 9657 玄穹开 / 6310 烬都奇谭)
> **权威知识库**: `C:\Users\Administrator\Desktop\claude\write_clone\knowlage\wiki\`
> **权威裁决**: `wiki/sources/_conflicts/2026-06-03 冲突清单.md` (11 条事实点, 以 2026-06-03 新研究为准)

---

## ⭐ 项目北极星 (必读)

> 📍 **任何时候迷路, 回来看这两份文档:**
>
> - 🗺️ **[`docs/ROADMAP.md`](docs/ROADMAP.md)** — 整个项目执行路线图 (4 Sprint + 5 里程碑 + 风险)
> - 🟢 **[`docs/sprints/sprint-0.md`](docs/sprints/sprint-0.md)** — 当前 Sprint 0 完整细节 (37 任务 / 5 阶段 / 6 周排期)
>
> 🎨 可视化版本: [`explain/13-整个项目执行规划-路线图.html`](explain/13-整个项目执行规划-路线图.html) (双击浏览器打开)

**当前状态:** Sprint 0 第 1 周 · 主控阶段 · 整体进度 6% · 24% Sprint 0 内进度
**下一里程碑:** M1 · 主链跑通 (2026-07-19)

---

## ⚡ 快速导航

| 你要做什么 | 看哪里 |
|------------|--------|
| 🗺️ **整个项目执行规划 (推荐先看)** | [`docs/ROADMAP.md`](docs/ROADMAP.md) (4 Sprint + 5 里程碑) |
| 🟢 **当前 Sprint 0 细节 (推荐先看)** | [`docs/sprints/sprint-0.md`](docs/sprints/sprint-0.md) (37 任务 / 6 周排期) |
| 了解整个项目的全貌 | [`docs/MASTER-PROJECT-SPEC.md`](docs/MASTER-PROJECT-SPEC.md) (1825 行,13 章节) |
| 找前后端契约 (权威) | [`contracts/openapi/`](contracts/openapi/), [`contracts/schemas/`](contracts/schemas/) |
| 看主控规划的目录结构 | [`docs/granular/02-master-repo-layout.md`](docs/granular/02-master-repo-layout.md) |
| 看 Sprint 0 要做什么 | [`docs/granular/04-sprint-0-tasks.md`](docs/granular/04-sprint-0-tasks.md) |
| 了解 17 个 World Tab 模块 | [`docs/granular/05-world-tab-17-modules.md`](docs/granular/05-world-tab-17-modules.md) |
| 了解 AI 调度机制 (12 厂商) | [`docs/granular/06-ai-orchestration.md`](docs/granular/06-ai-orchestration.md) |
| 了解 11 条冲突裁决 | [`docs/granular/07-conflict-adjudication.md`](docs/granular/07-conflict-adjudication.md) |
| 看架构决策 | [`docs/adr/`](docs/adr/) (22 个 ADR · 20 已定 + 2 新决策) |
| 看 Sprint 0 预算/派单决策 | [`docs/adr/0021-sprint0-agent-dispatch-and-budget.md`](docs/adr/0021-sprint0-agent-dispatch-and-budget.md) |
| 看前端 HTML 原型权威来源 | [`docs/adr/0022-frontend-html-prototypes-authoritative.md`](docs/adr/0022-frontend-html-prototypes-authoritative.md) |
| 看讨论稿 (子 agent/git 规则) | [`docs/discussions/`](docs/discussions/) |
| 童话版可视化 (小白友好) | [`explain/index.html`](explain/index.html) (13 个 HTML 故事) |

---

## 🎯 主控做什么 / 不做什么

### 主控 (本项目) 负责
1. **前后端契约** — 定义 API (OpenAPI 3.1) + 数据模型 (JSON Schema) + 事件契约
2. **项目方向** — 模块拆分、依赖关系、迭代路线、Sprint 规划
3. **核心调度** — AI 任务调度 (12 厂商路由) / 长文本一致性调度 / 蒸馏管线调度
4. **跨模块一致性** — 伏笔 ↔ 角色 ↔ 情节 ↔ 时间线 ↔ 已经历事件 的强一致性
5. **状态监控** — Sprint 进度 / 配额 / 蒸馏状态 / 设定变更传播

### 主控不负责
- ❌ 不直接写前端 UI (那是 `frontend/` 子项目)
- ❌ 不直接写后端业务逻辑 (那是 `backend/` 子项目)
- ❌ 不直接调 AI (那是 `ai-orchestrator/` 子项目)
- ✅ 但所有子项目必须**遵守** `contracts/` 下的契约

---

## 📦 目录结构 (主控布局)

```
master/
├── README.md                       ← 你正在读
├── CLAUDE.md                       ← 给 Claude Code 读的主控 Prompt
├── harness.config.json             ← harness-l3-v4 配置
├── feature_list.json               ← feature 任务清单 (Sprint 0: 37 任务)
├── progress.txt                    ← Sprint 进度日志
├── init.sh                         ← 一键启动 (Windows + Linux/Mac)
├── docker-compose.yml              ← 全栈编排 (PG+Redis+MinIO+API+FE)
│
├── contracts/                      ★ 主控权威契约 (子项目必须遵守)
│   ├── openapi/                    OpenAPI 3.1 端点契约 (按模块)
│   ├── schemas/                    JSON Schema (TS/Python 共享)
│   ├── events/                     事件契约 (SSE / 蒸馏 / 一致性)
│   ├── ai/                         AI 调度契约 (12 厂商注册表 / 路由规则)
│   └── frontend/                   前端路由 / 17 模块清单 / 主题
│
├── backend/                        后端子项目 (Node.js + Fastify/NestJS)
├── frontend/                       前端子项目 (Vue 3 + TipTap + Pinia)
├── ai-orchestrator/                AI 调度子项目 (Python + FastAPI)
├── knowledge-graph/                知识图谱 (伏笔-角色-情节-时间线 一致性)
├── infra/                          Docker / K8s / CI / 监控
├── tests/                          E2E + 集成测试
│
├── docs/                           主控权威文档
│   ├── MASTER-PROJECT-SPEC.md      完整规格说明书 (1825 行)
│   ├── adr/                        架构决策记录 (16 个 ADR)
│   ├── architecture/               系统架构图 / 数据流
│   └── granular/                   颗粒化文档 (按主题拆分, 可被 sub-agent 快速读)
│
├── features/                       单 feature PRD 与设计稿
├── progress/                       Sprint / 复盘 / 决策日志
├── scripts/                        工具脚本 (契约 lint / 种子数据)
└── .claude/                        Claude Code 技能与命令
```

---

## 🧬 核心技术决策 (摘要)

| 维度 | 决策 | 理由 |
|------|------|------|
| 复刻目标 | 1:1 还原云笔AI 230+ 端点 + 17 World Tab 模块 | 用户明确要求"复刻" |
| 前端 | Vue 3 + Vite + TipTap + Pinia + Tailwind | 与原版完全一致,迁移成本最低 |
| 后端 | Node.js + NestJS/Fastify + PostgreSQL + JSONB | 长文本存储 + 灵活 schema |
| AI 调度 | 自建 AI Proxy (12 厂商统一抽象) + BullMQ 任务队列 | 蒸馏 / 长文本生成需要强队列 |
| AI 厂商 | DeepSeek (默认) / Claude / GPT / Gemini / 智谱 / 通义 / 文心 / Kimi 等 12 家 | BYOK 模式, 用户可选 |
| 部署 | Docker Compose (Sprint 0) → K8s (生产) | 渐进式,降低 Sprint 0 复杂度 |
| 鉴权 | JWT (HS256) + 30s 心跳 | 1:1 还原 |
| 知识库 | 沿用原 `knowlage/` (三层 wiki 架构, Karpathy LLM Wiki 方法论) | 用户已投入深度研究 |

详细 ADR 见 [`docs/adr/`](docs/adr/)。

---

## 🚀 快速开始

### 1. 阅读入口
```bash
# 必读 (按顺序)
cat README.md                                   # 5 分钟
cat docs/MASTER-PROJECT-SPEC.md                 # 30 分钟
cat docs/granular/04-sprint-0-tasks.md          # 5 分钟
cat docs/granular/05-world-tab-17-modules.md    # 10 分钟
```

### 2. 启动主链 (Sprint 0 完成后)
```bash
# Windows (Git Bash)
./init.sh dev

# Linux / Mac
bash init.sh dev
```

`init.sh` 会启动:
- PostgreSQL (项目/章节/世界设定数据)
- Redis (会话/配额/AI 响应缓存/BullMQ)
- MinIO (头像/导出/封面, S3 兼容)
- Backend (Node.js API)
- Frontend (Vue 3 SPA)
- AI Orchestrator (Python FastAPI)

### 3. 跑契约一致性检查
```bash
python scripts/contract-lint.py
```

---

## 📊 核心数字 (从 knowlage 提取)

| 指标 | 数值 |
|------|------|
| 累计创作者 | 100万+ |
| 累计生成字数 | 5000万+ |
| 复刻 API 端点数 | 230+ |
| World Tab 模块 | 17 |
| 角色类型 | 24 |
| 伏笔类型 | 6 |
| 伏笔埋设模式 | 10 |
| 势力类型 | 9 |
| 货币/物品/功法 | 3/86/60 |
| AI 厂商数 | 12 |
| 自由创作额度 | 5000字/天 |
| 专业版额度 | 100000字/天 |
| 创建模板 | 2000+ (60 精品) |
| 流派标签 | 13 类型 55 流派 |
| 11 步探讨式构建 | ✓ |
| 创建模式 | 3 (探讨式/抽卡式/剧情式) |
| 心跳间隔 | 30s |
| 三栏布局比例 | 18% / 50% / 32% |

---

## 🔄 主控调度的工作流

1. **新建需求** → 写入 `feature_list.json`,加 ID
2. **契约先行** → 修改 `contracts/openapi/*.yaml` + `contracts/schemas/*.json`
3. **拆子任务** → 在 `feature_list.json` 中加子任务,标明所属子项目
4. **子项目执行** → 调用 `harness-l3-v4` 让子 agent 实现
5. **契约一致性检查** → 跑 `scripts/contract-lint.py`
6. **更新进度** → `progress.txt` 追加
7. **决策记录** → 重要决策加 ADR

---

## 📚 关键文件指针 (相对路径)

- 完整规格: [`docs/MASTER-PROJECT-SPEC.md`](docs/MASTER-PROJECT-SPEC.md)
- 数据模型: [`docs/MASTER-PROJECT-SPEC.md#3-数据模型契约主控权威`](docs/MASTER-PROJECT-SPEC.md)
- API 契约: [`docs/MASTER-PROJECT-SPEC.md#4-前后端-api-契约`](docs/MASTER-PROJECT-SPEC.md)
- AI 调度: [`docs/MASTER-PROJECT-SPEC.md#6-ai-调度契约`](docs/MASTER-PROJECT-SPEC.md)
- 跨模块一致性: [`docs/MASTER-PROJECT-SPEC.md#9-跨模块一致性约束`](docs/MASTER-PROJECT-SPEC.md)
- Sprint 0 任务: [`docs/MASTER-PROJECT-SPEC.md#11-sprint-0-主控初始化任务清单`](docs/MASTER-PROJECT-SPEC.md)
- 11 条冲突裁决: [`docs/granular/07-conflict-adjudication.md`](docs/granular/07-conflict-adjudication.md)
- 16 个 ADR: [`docs/adr/`](docs/adr/)

---

*最后更新: 2026-06-07 · 主控 v1.0 · 由 50 个 Opus agent 在 128 万 token 消耗下深度扫描 87 个 knowlage/wiki 页面合成*
