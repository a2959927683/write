# Architecture · 系统总览 (主控权威)

> 来源: `docs/MASTER-PROJECT-SPEC.md` 整体
> 最后更新: 2026-06-07

## 1. 主控定位

**主控 (Master Controller) = 前后端契约权威 + 全栈调度中枢**

主控**不实现**产品 UI/UX 本身, 主控**只做**:
- 制定前后端契约 (OpenAPI + JSON Schema + 事件契约)
- 把握项目方向 (Sprint 规划 + ADR)
- 核心调度 (AI 任务 / 蒸馏 / 一致性)
- 跨模块一致性 (5 层校验 + EventBus)

## 2. 7 大子系统

```
┌──────────────────────────────────────────────────────────────────────┐
│  master (主控)                                                          │
│                                                                            │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  frontend/  │  │  backend/   │  │ai-orchestr.  │  │knowledge-    │   │
│  │  (Vue 3)    │  │  (NestJS)   │  │(Python FastAPI)│ │graph/        │   │
│  └──────┬──────┘  └──────┬──────┘  └──────┬───────┘  └──────┬───────┘   │
│         │                │                │                  │           │
│         └────────────────┴────────┬───────┴──────────────────┘           │
│                                  ▼                                        │
│                           ┌──────────┐                                    │
│                           │contracts/│ ← 权威契约 (子项目必须遵守)          │
│                           └──────────┘                                    │
│                                                                            │
│  ┌─────────────┐  ┌─────────────┐                                          │
│  │   infra/    │  │  tests/     │                                          │
│  │ (Docker/K8s)│  │ (E2E/integr.)│                                          │
│  └─────────────┘  └─────────────┘                                          │
└──────────────────────────────────────────────────────────────────────┘
```

## 3. 数据流

### 3.1 用户登录 + 创建项目

```
[Vue 3 Frontend]
  ↓ POST /auth/login
[Node.js Backend]
  ↓ bcrypt 验证
[PostgreSQL] users
  ↓ 返回 JWT
[Frontend] localStorage.setItem('token')
  ↓ POST /projects
[Backend] QuotaGuard.checkProjectCreate
  ↓ INSERT
[PostgreSQL] projects
  ↓ 返回 Project
[Frontend] /projects 列表显示
```

### 3.2 AI 续写 (SSE 流式)

```
[Vue 3] 用户选中片段末尾, 点击"续写"
  ↓ POST /ai/chat/session { messages, options }
[Backend] 返回 { sessionId }
  ↓ GET /ai/chat/stream/:sessionId (EventSource)
[Backend] 代理到 AI Orchestrator
  ↓
[AI Orchestrator] Router.route('续写')
  ↓
[ProviderRegistry].get('deepseek')
  ↓
[DeepSeek API] stream chat
  ↓ 流式 chunk
[AI Orchestrator] transform_chunk → SSE
  ↓
[Backend] 转发 SSE
  ↓ 流式 event: stream.chunk { delta, index }
[Frontend] useAIStream 逐字显示
  ↓ 累积
[Frontend] 用户点击"采纳插入"
  ↓ PUT /chapters/:id { 标题, 内容 }
[Backend] 三重写入 (内容/正文/content) + 哈希检测
  ↓ 哈希变化
[BullMQ] enqueue distill job
  ↓ 30s 后消费
[AI Orchestrator] DistillPipeline.run (3 阶段)
  ↓
[PostgreSQL] chapters.蒸馏状态 = '已完成'
  ↓
[BullMQ] enqueue consistency check (L4)
  ↓
[EventBus] 广播 timeline.event.added
  ↓
[Frontend] UI 实时更新 (EventSource 推送)
```

### 3.3 跨模块一致性 (设定变更传播)

```
[Vue 3] 用户修改 #7 力量体系 (新增境界"神烬")
  ↓ PUT /power-systems/:id { 体系名称, 境界列表: [...] }
[Backend] PowerSystemService.update
  ↓
[PostgreSQL] power_systems (UPDATE)
  ↓ 触发事件
[EventBus] publish('powersystem.realm.changed', { projectId, systemId, realmId, ... })
  ↓
[订阅者 1: AI Orchestrator] 失效相关 AI prompt 缓存, 重新组装上下文
[订阅者 2: Knowledge Graph] 更新知识图谱节点
[订阅者 3: Frontend SSE] 推送给所有打开该项目的客户端
  ↓
[Frontend] UI 标红提示: "已新增境界, 角色境界自动更新"
[自动任务] 重新计算所有引用该境界的角色的战力系数
  ↓
[Cron 每日 6:00] check_power_system_realm 校验 (L1)
```

## 4. 17 World Tab 模块的数据流

```
[Frontend] World Tab 抽屉
  ↓ GET /worldviews/project/:id
[Backend] WorldviewService.get
  ↓
[PostgreSQL] worldviews
  ↓ 返回 Worldview
[Frontend] 显示表单

[Frontend] 用户点击"AI 生成"
  ↓ POST /worldviews/project/:id/generations { prompt, options }
[Backend] 转发到 AI Orchestrator
  ↓
[AI Orchestrator] ProviderRegistry.get
  ↓
[AI Provider] 返回生成内容
  ↓
[Backend] 写 ai_generations 表 + 返回
  ↓
[Frontend] 显示"采纳"按钮

[Frontend] 用户点击"采纳"
  ↓ PUT /worldviews/:id { 世界名称, ... } (含采纳的生成内容)
[Backend] UPDATE
  ↓
[EventBus] publish('worldview.changed')
  ↓
[订阅者] 失效相关 AI 缓存
```

## 5. 关键数字 (主控记录)

| 指标 | 数值 |
|------|------|
| 复刻 API 端点 | 230+ |
| World Tab 模块 | 17 |
| 角色类型 | 24 |
| 伏笔类型 + 埋设模式 | 6 + 10 |
| 势力类型 | 9 |
| 力量体系 (境界/能力) | 11 + 6 |
| AI 厂商 | 12 |
| 鉴权 | JWT HS256 + 30s 心跳 |
| 配额 (free/pro) | 5000/100000 字/天 |
| 项目数配额 (free/pro) | 1/10 |
| 心跳 | 30s |
| 三栏比例 | 18/50/32 |
| SSE 事件类型 | 7 |
| 蒸馏阶段 | 3 (Generator/Extractor/Checker) |
| 一致性层级 | 5 (设定/结构/时间/关系/蒸馏) |
| ADR 总数 | 16 |

## 6. 关键文件指针

| 关注点 | 主控权威文件 |
|--------|------------|
| 完整规格 | `docs/MASTER-PROJECT-SPEC.md` |
| 任务清单 | `feature_list.json` (37 任务) |
| 进度 | `progress.txt` |
| 决策 | `docs/adr/0001..0016.md` |
| API 契约 | `contracts/openapi/*.yaml` |
| 数据模型 | `contracts/schemas/*.json` |
| AI 厂商 | `contracts/ai/providers.json` |
| 事件 | `contracts/events/*.ts` |
| 知识库 | `C:\Users\Administrator\Desktop\claude\write_clone\knowlage\wiki\` |
| 冲突裁决 | `knowlage/wiki/sources/_conflicts/2026-06-03 冲突清单.md` |

## 7. Sprint 0 主链 (验收路径)

```
[用户] 访问 https://localhost:5173
  → [Frontend] Landing Page
[用户] 点击"注册"
  → [Frontend] Register Form
  → POST /auth/register
  → [Backend] bcrypt + INSERT
  → 返回 token
[用户] 跳到 /projects
  → GET /projects
  → [Backend] 列出当前用户项目
  → [Frontend] ProjectList (4 卡片 + 网格 + 搜索)
[用户] 点击"新建项目"
  → [Frontend] ProjectCreate (11 步探讨式, Sprint 2+)
  → Sprint 0: 简单表单 (项目名 + 类型)
  → POST /projects
  → [Backend] QuotaGuard + INSERT
  → 跳到 /editor/:projectId
[用户] 进入编辑器
  → [Frontend] 三栏布局 (250/auto/300)
  → 左侧: Project Tab (大纲树)
  → 中间: TipTap (空白章节)
  → 右侧: AI 助手面板
[用户] 输入 100 字
  → 2s 后 debounce
  → PUT /chapters/:id { 标题, 内容 }
  → [Backend] 三重写入 + 哈希
[用户] 点击"续写"
  → POST /ai/chat/session
  → 返回 sessionId
  → GET /ai/chat/stream/:sessionId (SSE)
  → [AI Orchestrator] DeepSeek 流式
  → 流式 chunk
  → [Frontend] useAIStream 渲染
[用户] 点击"采纳插入"
  → PUT /chapters/:id (合并续写内容)
  → 哈希变化, 触发蒸馏
[完成]
```

---

*最后更新: 2026-06-07 · 主控 v1.0 · 50 个 Opus agent 深度扫描 87 个 knowlage/wiki 页面合成*
