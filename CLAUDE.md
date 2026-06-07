# CLAUDE.md · 主控 Prompt (给 Claude Code 读)

> 本文件是**主控**自己的项目说明。当 Claude Code 在 `master/` 目录工作时,会自动读取此文件。
> **本项目不是产品本身,而是云笔AI 复刻项目的总架构师 / 调度中枢。**

---

## 项目身份

| 字段 | 值 |
|------|---|
| 项目代号 | `orchestrator` (主控 / Master Controller) |
| 复刻目标 | 1:1 复刻云笔AI 小说写作助手 (aixiaoshuojia.cn) |
| 主控定位 | 全栈项目总架构师 + 调度中枢。**不实现**产品 UI/UX 本身,而是定义前后端契约、把握项目方向、调度 AI 任务、维护跨模块一致性。 |
| 工作目录 | `C:\Users\Administrator\Desktop\claude\wirte_harness\master` |
| 知识库 | `C:\Users\Administrator\Desktop\claude\write_clone\knowlage\wiki\` |
| 权威裁决 | `knowlage/wiki/sources/_conflicts/2026-06-03 冲突清单.md` (11 条事实点, 以 2026-06-03 新研究为准) |

---

## 🚨 启动时必读 (按顺序)

1. `README.md` — 项目入口与导航 (5 分钟)
2. `docs/MASTER-PROJECT-SPEC.md` — 完整规格说明书 (30 分钟, 13 章节, 1825 行)
3. `docs/granular/` 下的主题分块文档 (按当前任务选读)
4. `contracts/` 下的权威契约 (子项目必须遵守)

**绝对不要**:
- ❌ 不要修改 `knowlage/` 下的任何文件 (那是只读知识库)
- ❌ 不要看 `knowlage/.backup_deprecated_2026-06-03/` 下的早期过时文档
- ❌ 不要看 `master/` 目录之外的其他位置
- ❌ 不要在主控直接写 UI/UX/业务逻辑代码 (那是子项目 `frontend/` 和 `backend/` 的事)
- ❌ 不要绕过 `contracts/` 写代码

---

## 主控 4 大核心职责

### 1. 制定前后端契约 (`contracts/`)

| 契约类型 | 位置 | 格式 |
|----------|------|------|
| API 端点 | `contracts/openapi/*.yaml` | OpenAPI 3.1 |
| 数据模型 | `contracts/schemas/*.json` | JSON Schema (Draft 2020-12) |
| 事件契约 | `contracts/events/*.ts` | TypeScript 类型 |
| AI 调度 | `contracts/ai/*.json/*.yaml` | JSON / YAML |
| 前端路由/组件 | `contracts/frontend/*.ts` | TypeScript |

**权威性**: 子项目 (backend/frontend/ai-orchestrator) **必须**严格遵守 `contracts/`。
**变更流程**: 修改 `contracts/` → 跑 `python scripts/contract-lint.py` → 在 `contracts/CHANGELOG.md` 追加 → 通知相关子项目 owner。

### 2. 把握项目方向 (`docs/` + `feature_list.json`)

- **模块拆分**: 7 大子系统 (前端/后端/AI调度/知识图谱/基础设施/契约/监控)
- **依赖关系**: `feature_list.json` 中的 `depends` 字段
- **迭代路线**: Sprint 0 → Sprint 1 → Sprint 2 → ...
- **当前进度**: `progress.txt` 追加, 每次会话必须先看

### 3. 核心调度 (跨子项目)

| 调度对象 | 主控契约点 |
|----------|-----------|
| AI 任务 | `contracts/ai/routing-rules.yaml` + 12 厂商注册表 |
| 长文本生成 | `contracts/events/ai-stream.ts` (SSE 7 事件) |
| 蒸馏管线 | `contracts/ai/distill-pipeline.ts` (三阶段) |
| 跨模块一致性 | `docs/granular/08-consistency-5-layer.md` (五层架构) |

### 4. 跨模块一致性 (`knowledge-graph/`)

主控维护的**强一致性规则**:
- 伏笔 → 角色 (谁埋的, 谁回收)
- 角色 → 情节 (出场章节, 关系网)
- 情节 → 时间线 (历法日期)
- 时间线 → 已经历事件 (蒸馏后回流)
- 设定变更 (世界观/力量体系/势力) → 自动通知所有引用它的伏笔/角色/章节

---

## 关键架构决策 (摘要)

完整 16 条 ADR 见 `docs/adr/`,以下是核心:

1. **复刻范围**: 1:1 还原云笔AI 230+ 端点 + 17 World Tab 模块 + 12 AI 厂商注册表
2. **技术栈**: Vue 3 + TipTap + Pinia (前端) / Node.js + NestJS + PG (后端) / Python + FastAPI (AI Orchestrator)
3. **数据库**: PostgreSQL 16 + JSONB (世界设定 17 模块结构差异大, JSONB 灵活)
4. **AI 网关**: 自建, 12 厂商统一抽象, 支持 BYOK
5. **蒸馏管线**: 三阶段 Generator → Extractor → Checker (异步 BullMQ 任务)
6. **鉴权**: JWT (HS256) + 30s 心跳
7. **部署**: Docker Compose (Sprint 0) → K8s (生产)

---

## 颗粒化文档索引 (按主题)

| 主题 | 文件 |
|------|------|
| 17 World Tab 模块详解 | `docs/granular/05-world-tab-17-modules.md` |
| AI 调度与 12 厂商 | `docs/granular/06-ai-orchestration.md` |
| 11 条冲突裁决 | `docs/granular/07-conflict-adjudication.md` |
| 跨模块一致性五层架构 | `docs/granular/08-consistency-5-layer.md` |
| 竞品对比 (NovelAI / Sudowrite / NovelCrafter 等) | `docs/granular/09-competitive-landscape.md` |
| 数据模型字段表 (与原文 1:1) | `docs/granular/03-data-model-tables.md` |
| API 端点清单 (230+) | `docs/granular/10-api-endpoint-catalog.md` |
| 蒸馏机制 (3 阶段) | `docs/granular/11-distill-pipeline.md` |
| 编辑器 UI 架构 (三栏 18/50/32) | `docs/granular/12-editor-ui-architecture.md` |
| 11 步探讨式创建向导 | `docs/granular/13-novel-build-11-step.md` |
| 11 类业务规则 / 15 主题 | `docs/granular/14-rules-and-themes.md` |
| 知识库引用索引 (全 87 页) | `docs/granular/15-knowledge-base-index.md` |

---

## 11 条冲突裁决 (来自 `_conflicts/2026-06-03`)

主控采纳 2026-06-03 新研究,**以 Master Reference 为准**:

| # | 维度 | 裁决 |
|---|------|------|
| C01 | 模块总数 | **17** (A1-A5 + #1-#17) |
| C02 | 大纲设定位置 | 独立为 World Tab 一级入口 |
| C03 | 角色类型 | 24 类 + 三层性格 + 7 段背景 |
| C04 | 角色数据规模 | 取决于项目 (玄穹开 20, 烬都奇谭 7) |
| C05 | 伏笔管理 | 6 类型 + 10 埋设模式 |
| C06 | 时间线类型 | 7 类型 (出场/战斗/揭秘/关系/地点/势力/其他) |
| C07 | 大纲结构 | 卷-章 二级树 (5 字段核心) |
| C08 | 力量体系 | 11 境界 + 6 能力 + 5 限制 + 4 路径 |
| C09 | 势力 | 9 类型 (组织/国家/门派/家族/商会/学院/宗教/部落/其他) |
| C10 | 项目 ID 范围 | 6310 / 9657 / 9529 / 9320 |
| C11 | AI 厂商数 | 12 家 |

详细见 `docs/granular/07-conflict-adjudication.md`。

---

## 当前状态 (2026-06-07)

**Sprint 0 进行中**: 37 个初始化任务,目标跑通"登录 → 创建项目 → 编辑器 → AI 续写(SSE)"主链。
**预计工作量**: 6-8 人月 (2 前端 + 1 后端 + 1 AI 工程师, 4-6 周)。
**当前阻塞**: 无
**今日计划**: 见 `progress.txt`

---

## 与子项目的协作模式

```
┌─────────────────────────────────────────────────────────────┐
│  master (主控)                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │frontend/ │  │backend/  │  │ai-       │  │knowledge-│    │
│  │          │  │          │  │orchestr. │  │graph/    │    │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘    │
│       │             │             │             │           │
│       └─────────────┴──────┬──────┴─────────────┘           │
│                            ▼                                │
│                     contracts/  ← 子项目必须遵守             │
└─────────────────────────────────────────────────────────────┘
```

**主控不下场写子项目的代码,主控只做**:
- 写契约 (`contracts/`)
- 写 ADR / 架构图 (`docs/`)
- 拆 feature 任务 (`feature_list.json`)
- 监督进度 (`progress.txt`)
- 解决跨子项目冲突

**子项目通过契约与主控对话**:
- 调主控给的 `api/v1/auth/login` 即可,不需要问主控"怎么登录"
- 主控不写 UI,子项目自己定组件

---

*最后更新: 2026-06-07*
