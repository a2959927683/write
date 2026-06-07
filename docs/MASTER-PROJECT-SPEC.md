# Master Project Spec · 云笔AI 复刻主控项目

> 文档版本: v1.0 · 编制日期: 2026-06-07
> 主控定位: Orchestrator / Controller (非产品本身)
> 对标产品: 云笔AI小说写作助手 (`https://aixiaoshuojia.cn`)
> 知识库: `C:\Users\Administrator\Desktop\claude\write_clone\knowlage\wiki`
> 编制依据: knowlage 全量 87 个 wiki 页(2 overview + 71 sources + 6 entities + 5 concepts + 3 comparisons)
> 权威裁决: `wiki/sources/_conflicts/2026-06-03 冲突清单.md` (11 条事实点, 以 2026-06-03 新研究为准)

---

## 1. 项目元数据

| 字段 | 值 |
|------|---|
| 项目代号 | `orchestrator` (主控 / Orchestrator) |
| 主控定位 | 全栈项目总架构师 + 调度中枢。**不实现**产品 UI/UX 本身,而是定义前后端契约、把握项目方向、调度 AI 任务、维护跨模块一致性。 |
| 复刻目标 | 1:1 复刻云笔AI 小说写作助手的 17 模块世界设定系统 + 编辑器 + AI 调度 + 蒸馏管线 |
| 目标用户 | 中文网文创作者(男频/女频/全年龄/青少年向) |
| 对标产品 | 云笔AI小说写作助手 (Project ID 9657 玄穹开 / 6310 烬都奇谭) |
| 复刻范围 | P0: 认证/项目/章节/角色/大纲/AI 续写/世界 17 模块/伏笔/时间线/蒸馏/管理后台/AI 网关/订阅/导出 |
| 复刻非范围 | 站外内容发布集成、EPUB/PDF 排版深度优化、网文平台账号对接、阅文集团签约链路 |
| 工作目录 | `C:\Users\Administrator\Desktop\claude\wirte_harness\master` |
| 核心数据(对标) | 100万+ 创作者 · 5000万+ 累计生成字 · 230+ API 端点 · 17 世界模块 · 12 AI 厂商 · Freemium(免费 5000 字/天, 专业 100000 字/天) |
| 预估工作量 | 28-36 人月 (3-5 人核心团队, 4 阶段) |

### 1.1 复刻技术栈(主控推荐,源自 knowlage 复刻指南 § 8.1 + 技术选型)

| 层面 | 选型 | 理由 |
|------|------|------|
| 前端框架 | Vue 3 + Vite | 与原版一致,生态成熟,迁移成本最低 |
| 富文本编辑器 | TipTap (ProseMirror) | 原版使用,适合长文本 + 自定义格式 |
| UI 组件 | 自研 + Headless UI + Tailwind CSS | 原版自研,深色主题,无第三方 UI 库锁定 |
| 图标 | Remix Icon | 原版使用 (`ri-robot-line` 等) |
| 状态管理 | Pinia (按模块分 store) | Vue 3 官方推荐,与 17 模块一一对应 |
| Canvas | 原生 Canvas API + Konva.js | 地理/势力/关系图三类模块需要 |
| 拖拽 | vuedraggable / SortableJS | 大纲树/列表 |
| API 通信 | Axios (RESTful) + EventSource (SSE) | 与原版一致 |
| 后端 | Node.js (Fastify 或 NestJS) | SSE 原生支持,API 结构清晰 |
| 数据库 | PostgreSQL + JSONB | 世界观 17 模块结构差异大,JSONB 灵活 |
| 缓存 | Redis | 会话、配额、AI 响应缓存、热点 context |
| 消息队列 | BullMQ (Redis) | 蒸馏任务、AI 长任务调度 |
| AI 网关 | 自建 AI Proxy | 12 厂商统一抽象,支持 BYOK |
| 对象存储 | S3 兼容 (MinIO) | 头像/导出/封面 |
| 部署 | Docker + Docker Compose (Sprint 0) → K8s (生产) | 渐进式 |
| 监控 | Prometheus + Grafana / OpenTelemetry | 可观测性 |
| 鉴权 | JWT (HS256) + 30s 心跳 | 1:1 还原 |

### 1.2 主控项目与子项目映射

| 子项目 | 路径 | 职责 |
|--------|------|------|
| `contracts/` | 主控根 | API/数据模型/事件契约的**唯一权威源** (OpenAPI 3.1 + JSON Schema) |
| `frontend/` | 主控根 | Vue 3 SPA,实现 17 模块 UI + 编辑器 + AI 协作面板 |
| `backend/` | 主控根 | Node.js API 服务,实现 230+ 端点 |
| `ai-orchestrator/` | 主控根 | AI 任务调度 (模型路由/上下文组装/蒸馏) |
| `knowledge-graph/` | 主控根 | 知识图谱(伏笔↔角色↔情节↔时间线↔已经历事件 强一致性) |
| `infra/` | 主控根 | Docker / K8s / CI / 监控 / 备份 |
| `docs/` | 主控根 | 架构决策记录 (ADR) / 流程图 / 知识库快照 |
| `features/` | 主控根 | feature_list.json / 单 feature PRD |
| `progress/` | 主控根 | progress.txt / Sprint 进度 |

---

## 2. 模块清单(全栈视图)

主控将整个系统拆为 **7 大子系统**。每个子系统在主控契约 (contracts/) 中有对应的 OpenAPI tag 和 JSON Schema 命名空间。

### 2.1 前端子系统 (`frontend/`)

| 模块名 | 职责 | 关键类/接口 | 依赖 | 与主控契约点 |
|--------|------|-------------|------|--------------|
| `app-shell` | 顶层 SPA 框架、登录态、全局错误边界 | `App.vue`, `router/index.ts` | 无 | `contracts/frontend/routes.ts` |
| `auth-ui` | 登录/注册/拼图验证/找回密码 | `LoginForm.vue`, `useAuthStore` | `auth-api` | `contracts/api/auth.yaml` |
| `project-list` | 项目管理页(网格/列表/搜索/分页 12/24/48/96) | `ProjectCard.vue`, `ProjectGrid.vue` | `project-api` | `contracts/api/project.yaml` |
| `project-create` | 11 步探讨式创建向导 / 抽卡式 / 剧情式 3 模式 | `NovelBuildWizard.vue` | `novel-build-api` | `contracts/api/novel-build.yaml` |
| `editor` | TipTap 富文本 + 卷-章大纲 + 自动保存 + 状态栏 | `Editor.vue`, `OutlineTree.vue` | `chapter-api`, `outline-api` | `contracts/api/chapter.yaml`, `contracts/frontend/editor-events.ts` |
| `left-panel` | 左侧 3 Tab(项目/角色/世界) | `LeftPanel.vue` | 多个 store | `contracts/frontend/world-tabs.ts` |
| `world-tab` | 17 模块统一抽屉(`ModuleDrawer.vue` 容器) | `WorldviewEditor.vue` ... `EventLineEditor.vue` | 17 个 store | `contracts/api/world-tab/*.yaml` |
| `right-panel` | 右侧 3 Tab(AI 助手/工具箱/统计) | `RightPanel.vue` | `ai-api`, `stats-api` | `contracts/api/ai.yaml` |
| `ai-assistant` | 6 按钮(续写/润色/对话/查漏/修正/展开)+ SSE 流式渲染 | `AIPanel.vue`, `useAIStream` | `ai-api` | `contracts/frontend/sse-events.ts` |
| `theme-system` | 15 种主题 + 暗色优先 + 中文 CSS 变量 | `useTheme.ts` | `user-config-api` | `contracts/frontend/themes.ts` |
| `tutorial` | 新手引导弹窗(3 步) | `OnboardingModal.vue` | `localStorage` | — |
| `admin` | 管理后台(需 `最高角色等级 >= 80`) | `AdminDashboard.vue` | `admin-api` | `contracts/api/admin.yaml` |

### 2.2 后端子系统 (`backend/`)

| 模块名 | 职责 | 关键类/接口 | 依赖 | 与主控契约点 |
|--------|------|-------------|------|--------------|
| `api-gateway` | 路由、JWT 校验、CORS、`Origin` 校验、限流 | `gateway.ts`, `auth-middleware.ts` | `auth-svc` | `contracts/api/*.yaml` |
| `auth-svc` | 注册/登录/JWT 签发/心跳 | `auth.controller.ts` | PostgreSQL | `auth.yaml` |
| `project-svc` | 项目 CRUD + 配额 + 导出 | `project.controller.ts` | PostgreSQL, S3 | `project.yaml` |
| `chapter-svc` | 章节 CRUD + 批量导入 + 自动保存 + 三重冗余 | `chapter.controller.ts` | PostgreSQL | `chapter.yaml` |
| `outline-svc` | 大纲树 (volume/chapter) + 22 端点 + AI 上下文 | `outline.controller.ts` | PostgreSQL | `outline.yaml` |
| `world-svc` | 17 模块子服务 (`worldview-svc`, `geo-map-svc`, ... `event-line-svc`) | 17 个 controller | PostgreSQL, RAG | `world-tab/*.yaml` |
| `character-svc` | 角色/关系/物品/境界/突破 | `character.controller.ts` | PostgreSQL | `character.yaml` |
| `foreshadow-svc` | 伏笔 + 回响 + 章节查找 + 自动爽约 | `foreshadow.controller.ts` | PG, RAG | `foreshadow.yaml` |
| `timeline-svc` | 历法 + 事件 + 章节时序 + 校验 | `timeline.controller.ts` | PG | `timeline.yaml` |
| `plot-svc` | 情节脉络 + 事件线 + 事件流 + 元素绑定 | `plot.controller.ts` | PG | `plot.yaml` |
| `ai-svc` | AI 状态/配置/对话/SSE/本地代理 | `ai.controller.ts` | `ai-orchestrator` | `ai.yaml` |
| `distill-svc` | 蒸馏状态/保存/时间线/异常重置 | `distill.controller.ts` | `ai-orchestrator`, BullMQ | `distill.yaml` |
| `rules-svc` | 规则 CRUD + 规则广场 + 启用/禁用 + 场景规则 | `rules.controller.ts` | PG | `rules.yaml` |
| `community-svc` | 规则广场 + 文笔广场 + 点赞/收藏/官方标记 | `community.controller.ts` | PG, Redis | `plaza.yaml` |
| `stats-svc` | 今日/周/月/项目/Token 统计 | `stats.controller.ts` | PG, ClickHouse(可选) | `stats.yaml` |
| `admin-svc` | 用户/角色/权限/项目管理/内容管理/AI 管理/日志 | `admin.controller.ts` | PG | `admin.yaml` |
| `conversation-svc` | AI 会话 + 消息 + 标题 | `conversation.controller.ts` | PG | `conversation.yaml` |
| `tts-svc` | TTS 合成/流式/导出 (19 音色) | `tts.controller.ts` | TTS 厂商 | `tts.yaml` |
| `novel-build-svc` | 11 步构建向导持久化 | `novel-build.controller.ts` | PG | `novel-build.yaml` |
| `export-svc` | 项目/章节/统计导出 | `export.controller.ts` | S3 | `export.yaml` |

### 2.3 AI 调度子系统 (`ai-orchestrator/`)

| 模块名 | 职责 | 关键类/接口 | 依赖 | 与主控契约点 |
|--------|------|-------------|------|--------------|
| `provider-registry` | 12 厂商注册/健康检查/默认参数 | `ProviderRegistry.ts` | 各厂商 SDK | `contracts/ai/providers.json` |
| `model-router` | 按任务类型+成本+可用性路由模型 | `ModelRouter.ts` | `provider-registry` | `contracts/ai/routing-rules.yaml` |
| `context-assembler` | 从多个 `/context` 端点拉取,组装 prompt | `ContextAssembler.ts` | `backend` 各 `*_svc` | `contracts/ai/context-schema.json` |
| `token-cache` | 跨请求 prompt 缓存 (Anthropic/OpenAI cache_control) | `TokenCache.ts` | Redis | `contracts/ai/cache-policy.yaml` |
| `sse-gateway` | SSE 流式输出到前端,断点续传 | `SSEGatway.ts` | `provider-registry` | `contracts/ai/sse-events.ts` |
| `distill-pipeline` | 章节完成 → AI 摘要 → 写回 | `DistillJob.ts` | `provider-registry`, `distill-svc` | `contracts/ai/distill-pipeline.ts` |
| `thinking-mode` | 推理模型 deepseek-reasoner / o1 系列 thinking 处理 | `ThinkingModeAdapter.ts` | `provider-registry` | `contracts/ai/thinking-modes.yaml` |
| `quota-throttler` | 按用户/项目/全局配额 + 节流 | `QuotaThrottler.ts` | Redis | `contracts/ai/quota-rules.yaml` |
| `local-proxy` | BYOK 用户本地模型代理 (`/ai/local/chat`) | `LocalProxy.ts` | — | `contracts/ai/local-proxy-schema.json` |
| `generation-store` | 统一 `/{module}/generations` 历史 | `GenerationStore.ts` | PG | `contracts/ai/generation-record.json` |

### 2.4 知识图谱 / 一致性子系统 (`knowledge-graph/`)

| 模块名 | 职责 | 关键类/接口 | 依赖 | 与主控契约点 |
|--------|------|-------------|------|--------------|
| `entity-extractor` | 从章节正文/大纲提取实体(角色/物品/势力/伏笔) | `EntityExtractor.ts` | `ai-orchestrator` | `contracts/kg/entity-schema.json` |
| `relation-mapper` | 实体-实体关系(从属/对立/师徒/亲属) | `RelationMapper.ts` | Neo4j/PG | `contracts/kg/relation-types.yaml` |
| `consistency-checker` | 五层一致性检查(结构化世界/上下文/约束生成/后审计/人工) | `ConsistencyChecker.ts` | 全部 17 模块 | `contracts/kg/consistency-rules.yaml` |
| `foreshadow-tracker` | 伏笔埋设 → 状态 → 回收 生命周期 | `ForeshadowTracker.ts` | `foreshadow-svc` | `contracts/kg/foreshadow-lifecycle.yaml` |
| `timeline-validator` | 历法 + 章节时序一致性校验 | `TimelineValidator.ts` | `timeline-svc` | `contracts/kg/timeline-rules.yaml` |
| `character-state-machine` | Alive/Dead/Unknown 状态机 | `CharacterStateMachine.ts` | `character-svc` | `contracts/kg/character-states.yaml` |
| `plot-binding` | 情节脉络 ↔ 事件 ↔ 角色 ↔ 伏笔 绑定图 | `PlotBinding.ts` | `plot-svc` | `contracts/kg/plot-binding.yaml` |

### 2.5 文件存储子系统

| 模块名 | 职责 | 关键类/接口 | 依赖 |
|--------|------|-------------|------|
| `s3-adapter` | 头像/封面/导出/附件 | `S3Adapter.ts` | MinIO/S3 |
| `image-cdn` | 静态资源 CDN URL 签发 | `CDNSigner.ts` | S3 |
| `backup-job` | PG 每日逻辑备份 + WORM 30 天保留 | `BackupJob.ts` | PG, S3 |
| `upload-handler` | 头像/封面分片上传 | `UploadHandler.ts` | S3 |

### 2.6 计费/订阅子系统

| 模块名 | 职责 | 关键类/接口 | 依赖 |
|--------|------|-------------|------|
| `plan-registry` | Free / Pro 月度计划定义 | `PlanRegistry.ts` | PG |
| `quota-counter` | 每日字数/章节/项目 配额 | `QuotaCounter.ts` | Redis |
| `billing-record` | 用量记录 + 报表 | `BillingRecord.ts` | PG |
| `payment-stub` | 支付集成(留接口,Sprint 0 留 mock) | `PaymentStub.ts` | — |

### 2.7 监控子系统

| 模块名 | 职责 |
|--------|------|
| `metrics-collector` | Prometheus 指标(API 延迟/AI 失败率/Token 消耗) |
| `log-aggregator` | 结构化日志(请求/AI 调用/错误) |
| `trace-exporter` | OpenTelemetry trace → Jaeger/Tempo |
| `alert-manager` | AI 失败率 > 5% / 蒸馏积压 > 100 / 延迟 P95 > 5s 告警 |

---

## 3. 数据模型契约(主控权威)

> **命名约定**: 字段名必须与云笔AI 真实 API 保持一致(中文字段名为主,英文为辅)。
> 所有表的主键默认 `id BIGSERIAL`,时间字段默认 `createdAt TIMESTAMPTZ`,`updatedAt TIMESTAMPTZ`。
> 所有外键使用 `ON DELETE CASCADE` 除非另注。

### 3.1 `users` 用户

| 字段 | 类型 | 约束 | 索引 | 说明 |
|------|------|------|------|------|
| `id` | BIGSERIAL | PK | clustered | 用户ID |
| `username` | VARCHAR(64) | NOT NULL UNIQUE | unique_btree | 用户名 |
| `email` | VARCHAR(128) | NOT NULL UNIQUE | unique_btree | 邮箱 |
| `password_hash` | VARCHAR(128) | NOT NULL | — | bcrypt/argon2 |
| `nickname` | VARCHAR(64) | NULL | — | 昵称 |
| `avatar` | VARCHAR(255) | NULL | — | 头像URL |
| `最高角色等级` | INT | NOT NULL DEFAULT 10 | btree | ≥80 = 管理员 |
| `plan_type` | VARCHAR(16) | NOT NULL DEFAULT 'free' | btree | free / pro |
| `daily_quota` | INT | NOT NULL DEFAULT 5000 | — | 每日字数配额 |
| `daily_used` | INT | NOT NULL DEFAULT 0 | — | 今日已用 |
| `quota_reset_at` | TIMESTAMPTZ | NULL | — | 下次重置时间 |
| `permissions` | JSONB | NOT NULL DEFAULT '[]' | GIN | 权限数组 |
| `createdAt` | TIMESTAMPTZ | NOT NULL DEFAULT NOW() | — | — |
| `updatedAt` | TIMESTAMPTZ | NOT NULL DEFAULT NOW() | — | — |

### 3.2 `projects` 项目

| 字段 | 类型 | 约束 | 索引 | 说明 |
|------|------|------|------|------|
| `id` | BIGSERIAL | PK | clustered | 项目ID |
| `user_id` | BIGINT | FK→users.id CASCADE | btree | 所属用户 |
| `项目名称` | VARCHAR(128) | NOT NULL | — | 小说名 |
| `项目类型` | VARCHAR(32) | NOT NULL | btree | 玄幻/仙侠/都市/言情... |
| `项目状态` | VARCHAR(16) | NOT NULL DEFAULT '连载中' | btree | 连载中/已完结 |
| `描述` | TEXT | NULL | — | 简介 |
| `封面` | VARCHAR(255) | NULL | — | 封面URL |
| `每幕事件数量配置` | JSONB | NULL | — | 节奏配置 |
| `总字数` | INT | NOT NULL DEFAULT 0 | — | 聚合缓存 |
| `章节数` | INT | NOT NULL DEFAULT 0 | — | 聚合缓存 |
| `角色数` | INT | NOT NULL DEFAULT 0 | — | 聚合缓存 |
| `createdAt` | TIMESTAMPTZ | NOT NULL | — | — |
| `updatedAt` | TIMESTAMPTZ | NOT NULL | — | — |

外键索引: `idx_projects_user_id (user_id)`

### 3.3 `chapters` 章节

| 字段 | 类型 | 约束 | 索引 | 说明 |
|------|------|------|------|------|
| `id` | BIGSERIAL | PK | clustered | 章节ID |
| `project_id` | BIGINT | FK→projects.id CASCADE | btree | |
| `关联大纲节点ID` | BIGINT | FK→outlines.id SET NULL | btree | 关联大纲节点 |
| `标题` | VARCHAR(128) | NOT NULL | — | 章节标题(含章节号) |
| `字数` | INT | NOT NULL DEFAULT 0 | — | |
| `状态` | VARCHAR(16) | NOT NULL DEFAULT 'pending' | btree | pending/complete |
| `内容` | TEXT | NULL | — | 列表用 |
| `正文` | TEXT | NULL | — | 详情用(三重冗余之一) |
| `content` | TEXT | NULL | — | 英文键名(三重冗余之一) |
| `场景脚本` | TEXT | NULL | — | SC\|序号\|地点\|... 格式 |
| `蒸馏状态` | VARCHAR(16) | NOT NULL DEFAULT '未蒸馏' | btree | 未蒸馏/进行中/已完成/失败 |
| `蒸馏失败原因` | TEXT | NULL | — | |
| `蒸馏模型` | VARCHAR(64) | NULL | — | 使用的模型标识 |
| `蒸馏完成时间` | TIMESTAMPTZ | NULL | — | |
| `正文快照哈希` | CHAR(6) | NULL | — | 6位短哈希,变更检测 |
| `排序顺序` | INT | NOT NULL DEFAULT 0 | btree | |
| `target_word_count` | INT | NOT NULL DEFAULT 3000 | — | 目标字数 |
| `createdAt` | TIMESTAMPTZ | NOT NULL | — | |
| `updatedAt` | TIMESTAMPTZ | NOT NULL | — | |

外键索引: `idx_chapters_project_id (project_id)`, `idx_chapters_outline_id (关联大纲节点ID)`
注意: `内容`/`正文`/`content` 三重冗余源于云笔真实 API,主控在首次迁移后**建议废弃** `正文` 与 `content`,但短期需保留以兼容原版客户端。

### 3.4 `outlines` 大纲(自引用树)

| 字段 | 类型 | 约束 | 索引 | 说明 |
|------|------|------|------|------|
| `id` | BIGSERIAL | PK | clustered | 节点ID |
| `project_id` | BIGINT | FK→projects.id CASCADE | btree | |
| `父节点ID` | BIGINT | FK→outlines.id CASCADE NULL | btree | 父节点(卷级) |
| `类型` | VARCHAR(16) | NOT NULL | btree | volume/chapter |
| `标题` | VARCHAR(255) | NOT NULL | — | |
| `关联章节ID` | BIGINT | FK→chapters.id SET NULL | btree | 已蒸馏章节 |
| `正文字数` | INT | NOT NULL DEFAULT 0 | — | |
| `状态` | VARCHAR(16) | NOT NULL DEFAULT 'pending' | btree | pending/complete |
| `优先级` | VARCHAR(16) | NOT NULL DEFAULT 'normal' | btree | |
| `截止日期` | TIMESTAMPTZ | NULL | — | |
| `标签` | JSONB | NOT NULL DEFAULT '[]' | GIN | |
| `摘要` | TEXT | NULL | — | Markdown 详细摘要 |
| `摘要核心` | TEXT | NULL | — | 一句话核心 |
| `颜色` | VARCHAR(32) | NULL | — | rgb(...) |
| `排序顺序` | INT | NOT NULL DEFAULT 0 | btree | |
| `目标字数` | INT | NOT NULL DEFAULT 3000 | — | |
| `实际字数` | INT | NOT NULL DEFAULT 0 | — | |
| `关键对话` | TEXT | NULL | — | |
| `人性细化` | TEXT | NULL | — | |
| `写作要点` | TEXT | NULL | — | |
| `道具物品` | JSONB | NOT NULL DEFAULT '[]' | — | |
| `势力阵营` | JSONB | NOT NULL DEFAULT '[]' | — | |
| `情绪列表` | JSONB | NOT NULL DEFAULT '[]' | — | 情绪设计 |
| `伏笔列表` | JSONB | NOT NULL DEFAULT '[]' | — | |
| `节奏控制` | JSONB | NOT NULL DEFAULT '[]' | — | |
| `视觉画面` | JSONB | NOT NULL DEFAULT '[]' | — | |
| `声音氛围` | JSONB | NOT NULL DEFAULT '[]' | — | |
| `createdAt` | TIMESTAMPTZ | NOT NULL | — | |
| `updatedAt` | TIMESTAMPTZ | NOT NULL | — | |

索引: `idx_outlines_project_parent (project_id, 父节点ID)`, `idx_outlines_sort (project_id, 排序顺序)`

### 3.5 WorldSetting 子表(17 模块)

> 所有 WorldSetting 子表都遵循统一结构: `id + project_id + 模块特定字段 + createdAt + updatedAt`,主控契约用 JSONB 存储复杂嵌套。

#### 3.5.1 `worldviews` 世界观设定

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | BIGSERIAL | PK |
| `project_id` | BIGINT FK | UNIQUE (一项目一世界观) |
| `世界名称` | VARCHAR(128) | |
| `世界类型` | VARCHAR(32) | 都市异能/玄幻/仙侠... |
| `时代背景` | TEXT | |
| `核心规则` | TEXT | |
| `地理环境` | TEXT | |
| `社会结构` | TEXT | |
| `历史背景` | TEXT | |
| `特殊元素` | TEXT | |
| `主要冲突` | TEXT | |
| `势力格局` | TEXT | |
| `备注` | TEXT | |
| `ext` | JSONB | 历法子系统/版本历史/子表 JSON |

#### 3.5.2 `story_cores` 故事核心(6 字段)

`主题`, `主线`, `冲突`, `高潮`, `结局`, `核心意义` 全部 TEXT,一项目一记录。

#### 3.5.3 `geo_maps` 地理地图(35 地点/双视图)

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | BIGSERIAL | PK |
| `project_id` | BIGINT | |
| `parent_id` | BIGINT NULL | 树形 parent |
| `名称` | VARCHAR(128) | |
| `描述` | TEXT | |
| `地图等级` | INT | 0=世界, 1=大陆, 2=区域, 3=城市, 4=地点, 5=子地点 |
| `地图类型` | VARCHAR(16) | 世界/大陆/区域/城市/地点/子地点 |
| `父地图名称` | VARCHAR(128) | 冗余 |
| `ext` | JSONB | 坐标/连边/网络布局参数 |

#### 3.5.4 `factions` 势力阵营(9 势力/4 视图)

`名称`, `类型`, `描述`, `影响力`, `核心人物`, `控制区域`, `宗旨`, `图标`, `颜色` + `ext JSONB`。子表 `faction_relations`(`faction_a`, `faction_b`, `关系类型`, `强度`)。

#### 3.5.5 `currencies` 货币体系(3 货币)

`名称`, `类型` (主币/辅币/虚拟), `兑换比例`, `图标`, `描述`, `ext JSONB`。子表 `currency_exchange_rates`。

#### 3.5.6 `items` 物品列表(86 物品/17 字段)

| 字段 | 类型 | 说明 |
|------|------|------|
| `物品名称` | VARCHAR(128) | |
| `类别` | VARCHAR(32) | 系统金手指/武器/丹药... |
| `作用`, `出处`, `获取难度`, `威力`, `价值`, `特征`, `使用人群`, `注意事项`, `保存期限`, `用量`, `使用代价`, `防御力` | TEXT | |
| `排序顺序` | INT | |
| `ext` | JSONB | 复杂属性 |

#### 3.5.7 `power_systems` 力量体系(4 层嵌套)

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | BIGSERIAL | PK |
| `project_id` | BIGINT | |
| `体系名称` | VARCHAR(128) | 星烬九考 |
| `体系类型` | VARCHAR(32) | 异能体系/修真体系/魔法体系... |
| `体系描述` | TEXT | |
| `力量来源` | TEXT | |
| `境界列表` | JSONB | 11 境界: `{id, 境界名称, 境界等级, 战力系数, 境界描述, 提升条件, 能力表现, 特殊标志, 排序顺序}` |
| `能力列表` | JSONB | `{id, 能力名称, 能力类型, 能力描述, 学习条件, 消耗代价, 排序顺序}` |
| `修行路径` | JSONB | `{修行方法, 修行资源, 修行难点, 突破要点}` |
| `限制约束` | JSONB | `{使用限制, 副作用, 反噬风险, 禁忌条款}` |

子表可选拆为 `power_realms`, `power_abilities`(性能更优)。

#### 3.5.8 `skill_systems` 功法体系(60 类型 × 9 品级)

`功法名称`, `品级`, `类型`, `体系ID` FK, `描述`, `ext JSONB`。

#### 3.5.9 `special_settings` 特殊设定/金手指(19 类型/5 大类 chip)

`名称`, `类型` (19 类之一), `描述`, `标签 JSONB`, `ext JSONB`。

#### 3.5.10 `outline_settings` 大纲设定(★P0)

外键到 `outlines` 表(3.4)。详情见 §3.4。

#### 3.5.11 `characters` 角色管理(★P1 · 24 类型/三层性格)

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | BIGSERIAL | PK |
| `project_id` | BIGINT | |
| `姓名` | VARCHAR(64) | |
| `类型` | VARCHAR(16) | 主角/女主/反派/导师/配角... (24 类) |
| `性别` | VARCHAR(8) | |
| `年龄` | VARCHAR(16) | 字符串(支持"十七岁") |
| `身份` | VARCHAR(64) | 星涡宿主 |
| `境界` | VARCHAR(64) | 当前境界名称 |
| `武器` | VARCHAR(128) | |
| `外貌` | TEXT | |
| `结局` | VARCHAR(64) | |
| `性格` | JSONB | `{表层, 中层, 内核}` 三层 |
| `人生经历` | JSONB | `[{事件, 章节}]` |
| `核心意义` | TEXT | |
| `其他信息` | JSONB | |
| `简介` | TEXT | |
| `头像颜色` | VARCHAR(64) | Tailwind 渐变类 |
| `颜色` | VARCHAR(16) | HEX |
| `力量体系ID` | BIGINT NULL | FK→power_systems |
| `初始境界ID` | BIGINT NULL | FK→power_realms |
| `当前境界ID` | BIGINT NULL | FK→power_realms |
| `初始战力系数` | DECIMAL(10,2) | |
| `当前战力系数` | DECIMAL(10,2) | |
| `存续状态` | VARCHAR(16) | 活跃/死亡/失踪 |

子表: `character_items`, `character_relations`, `character_appearances`, `character_realm_breakthroughs`。

#### 3.5.12 `character_relations` 人物关系图(8 关系/13 chip)

`character_a_id`, `character_b_id`, `关系类型` (师徒/亲属/敌对/盟友/恋人...), `强度`, `备注`, `ext JSONB`。

#### 3.5.13 `foreshadows` 伏笔管理(19 伏笔/10 埋设模式)

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | BIGSERIAL | PK |
| `project_id` | BIGINT | |
| `标题` | VARCHAR(255) | |
| `描述` | TEXT | |
| `类型` | VARCHAR(16) | 6 种之一: 悬念/伏线/暗喻/预言/巧合/对照 |
| `埋设模式` | VARCHAR(16) | 10 种之一: 对话暗示/物件刻画/景物烘托... |
| `埋设章节ID` | BIGINT NULL | FK→chapters |
| `状态` | VARCHAR(16) | 已埋设/发展中/已回收/已废弃 |
| `重要度` | INT | 1-5 |
| `回收章节ID` | BIGINT NULL | FK→chapters |
| `ext` | JSONB | 包含 `echoes` 子数组(回响) |

子表 `foreshadow_echoes`(`foreshadow_id`, `章节ID`, `描述`, `echoed_at`)。

#### 3.5.14 `plot_structures` 情节脉络(5 模板/7 幕)

`名称`, `模板` (起承转合/英雄之旅/三幕剧/七点不测/救猫咪), `结构详情 JSONB`, `关联章节IDs JSONB`。

#### 3.5.15 `event_lines` / `event_flows` 支线故事(35 事件/3 步 AI)

`event_lines`: `标题`, `描述`, `状态`, `ext JSONB`。
`event_flows`: `line_id` FK, `event_order`, `章节ID`, `角色IDs JSONB`, `事件描述`。
`element_bindx`: `event_id` FK, `要素名称`, `bindings JSONB`(绑定到章节/角色/伏笔/势力)。

#### 3.5.16 `timelines` 时间线(自定义历法/7 类型)

| 表 | 字段 |
|----|------|
| `timeline_calendars` | `project_id`, `历法名称`, `年长度`, `月数`, `月长度 JSONB`, `纪年方式` |
| `timeline_events` | `id`, `project_id`, `标题`, `历法日期`, `章节ID`, `类型` (出场/战斗/揭秘...), `描述`, `ext` |
| `timeline_chapter_time` | `(project_id, 章节ID)` UNIQUE, `历法日期`, `ext` |

#### 3.5.17 `event_lines` 已经历事件(95 事件/5 分类/蒸馏)

`标题`, `分类` (战斗/关系/觉醒/发现/其他), `历法日期`, `章节ID`, `蒸馏摘要`, `ext JSONB`。

### 3.6 AI 生成与对话

#### 3.6.1 `ai_generations` 统一生成记录(★ 核心)

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | BIGSERIAL | PK |
| `project_id` | BIGINT FK | |
| `user_id` | BIGINT FK | |
| `module_type` | VARCHAR(32) | worldview/outline/character/... |
| `target_id` | BIGINT NULL | 关联目标ID(如大纲节点) |
| `prompt` | TEXT | 输入提示词 |
| `response` | TEXT | AI 响应 |
| `adopted` | BOOLEAN | 是否已采纳 |
| `provider` | VARCHAR(32) | 厂商 |
| `model` | VARCHAR(64) | 模型ID |
| `tokens_in` | INT | 输入 token |
| `tokens_out` | INT | 输出 token |
| `cost_usd` | DECIMAL(10,6) | 估算成本 |
| `mode` | VARCHAR(32) | 续写/润色/对话/查漏/修正/展开... |
| `session_id` | VARCHAR(64) NULL | SSE 会话ID |
| `createdAt` | TIMESTAMPTZ | |

索引: `idx_gen_project_module (project_id, module_type, createdAt DESC)`

#### 3.6.2 `conversations` 对话 + `messages`

`conversations`: `id`, `user_id`, `project_id`, `标题`, `ext`。
`messages`: `id`, `conversation_id`, `role` (user/assistant/system), `content`, `action_type`, `applied BOOLEAN`。

#### 3.6.3 `ai_local_configs` 本地模型代理

`user_id`, `端点URL`, `API密钥` (AES-256 加密), `请求路径`, `自定义请求头`, `请求体模板 JSONB`。

### 3.7 蒸馏 `distill_records`

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | BIGSERIAL | PK |
| `project_id` | BIGINT | |
| `chapter_id` | BIGINT NULL | |
| `outline_node_id` | BIGINT NULL | |
| `event_id` | BIGINT NULL | 已经历事件 |
| `状态` | VARCHAR(16) | 进行中/已完成/失败 |
| `摘要` | TEXT | AI 摘要 |
| `失败原因` | TEXT | |
| `模型` | VARCHAR(64) | |
| `创建时间` | TIMESTAMPTZ | |
| `完成时间` | TIMESTAMPTZ | |

### 3.8 用户/订阅/配额

| 表 | 关键字段 |
|----|---------|
| `user_subscriptions` | `user_id`, `plan_type`, `started_at`, `expires_at`, `auto_renew` |
| `quota_counters` | `user_id`, `date`, `chars_used`, `chapters_created`, `projects_created` |
| `payments` | `user_id`, `plan_type`, `amount_cents`, `currency`, `status`, `provider`, `provider_ref` |
| `roles` | `name`, `level`, `description` |
| `permissions` | `code`, `name`, `description` |
| `role_permissions` | `(role_id, permission_id)` |

### 3.9 规则与社区

| 表 | 字段 |
|----|------|
| `rules` | `user_id`, `name`, `rule_content`, `enabled`, `scene` |
| `rules_plaza` | `rule_id`, `likes`, `favorites`, `is_official` |
| `writing_styles` | `user_id`, `name`, `style_params JSONB`, `is_shared`, `use_count` |
| `writing_styles_plaza` | 类同 rules_plaza |
| `notes` | `user_id`, `title`, `content`, `pinned` |
| `materials` | `project_id`, `name`, `details JSONB` |
| `obligations` | `project_id`, `chapter_id`, `description`, `status` (待兑现/已兑现/已爽约), `due_at` |

### 3.10 统计与日志

| 表 | 字段 |
|----|------|
| `stats_daily` | `user_id`, `date`, `chars_written`, `ai_chars`, `chapters_done` |
| `ai_token_usage` | `user_id`, `date`, `provider`, `model`, `tokens_in`, `tokens_out`, `cost_usd` |
| `operation_logs` | `user_id`, `action`, `target`, `ip`, `ua`, `created_at` |
| `online_sessions` | `user_id`, `last_heartbeat`, `ip` (30s 心跳) |

### 3.11 管理后台

`admin_users` (继承 users), `admin_audit_log` (强审计), `system_settings` (`key`, `value JSONB`)。

---

## 4. 前后端 API 契约

> **Base URL**: 主机 = `https://<your-domain>`, Axios `baseURL: "/api"` (与云笔真实 API 保持一致,**不是 `/api/v1/`**)。
> **必选头**: `Authorization: Bearer <token>`, `Content-Type: application/json`, `Origin: <your-domain>` (必须,否则 403)
> **统一响应**:
> ```json
> { "success": true, "data": { ... }, "message": "操作成功" }
> { "success": false, "message": "错误信息", "path": "/api/..." }
> ```
> **分页** (列表端点): `{ pagination: { total, page, limit, totalPages } }`

### 4.1 认证模块 (`/auth`)

| Method | Path | Request | Response | Error |
|--------|------|---------|----------|-------|
| POST | `/auth/login` | `{username, password}` | `{data: {token, user}}` | 401 用户名密码错 |
| POST | `/auth/register` | `{username, email, password, code}` | `{data: {token, user}}` | 409 邮箱已注册 |
| POST | `/auth/send-register-code` | `{email}` | `{data: {sent: true}}` | 429 频率限制 |
| GET | `/auth/puzzle-token` | — | `{data: {token, imageUrl}}` | — |
| GET | `/auth/registration-mode` | — | `{mode: "open"\|"beta"\|"closed"}` (例外格式) | — |
| PUT | `/auth/password` | `{oldPassword, newPassword}` | `{data: {ok: true}}` | 401 旧密码错 |
| GET | `/auth/profile` | — | `user` | 401 |
| PUT | `/auth/profile` | `{nickname, avatar}` | `user` | 400 校验失败 |

注: `user.permissions` 混合中英文标识(`local_ai_config`, `探讨-抽卡式`, `chapter:import`...)。

### 4.2 项目模块 (`/projects`)

| Method | Path | Request | Response | Error |
|--------|------|---------|----------|-------|
| GET | `/projects?page=&limit=&keyword=&项目类型=&项目状态=&sort=` | — | `{data: [Project], pagination}` | 401 |
| GET | `/projects/my-quota` | — | `{data: {当前项目数, 最大项目数, 可创建}}` | — |
| GET | `/projects/:id` | — | `Project` | 404 |
| POST | `/projects` | `{项目名称, 项目类型, 项目状态?, 描述?, 封面?}` | `Project` | 403 配额满 |
| PUT | `/projects/:id` | `Partial<Project>` | `Project` | 403 无权限 |
| DELETE | `/projects/:id` | — | `{data: {ok: true}}` | 403 |
| POST | `/projects/:id/export` | `{format}` | `{data: {url}}` | 500 |
| GET | `/projects/:id/export/chapters` | — | `[{章节标题, 内容}]` (Markdown 列表) | — |

### 4.3 章节模块 (`/chapters`)

| Method | Path | Request | Response | Error |
|--------|------|---------|----------|-------|
| GET | `/chapters/project/:projectId?page=&limit=&status=` | — | `Chapter[]` (列表含`内容`字段) | 401 |
| GET | `/chapters/:id` | — | `ChapterDetail` (三重冗余字段) | 404 |
| GET | `/chapters/by-outline/:outlineId` | — | `Chapter` | 404 |
| POST | `/chapters/project/:projectId` | `{标题, 关联大纲节点ID?, target_word_count?}` | `Chapter` | 400 |
| PUT | `/chapters/:id` | `{标题?, 内容?, 状态?, target_word_count?}` | `Chapter` | 403 |
| DELETE | `/chapters/:id` | — | `{ok: true}` | 403 |
| PUT | `/chapters/batch/reorder` | `{chapters: [{id, 排序顺序}]}` | `{ok: true}` | 400 |
| POST | `/chapters/project/:id/import/precheck` | `multipart: file` | `{data: {issues: []}}` | 400 解析失败 |
| POST | `/chapters/project/:id/import/batch` | `{chapters: [...]}` (timeout 120s) | `{data: {imported: n}}` | 500 |
| GET | `/chapters/project/:id/import/history` | — | `[{taskId, status, createdAt}]` | — |
| POST | `/chapters/project/:id/import/cancel/:taskId` | — | `{ok: true}` | 404 |

### 4.4 大纲模块 (`/outlines`) · 22 端点

CRUD 5 + 移动/重编号/重排序/批量 4 + 上下文/关联角色/伏笔/阵营/场景 5 + 事件线 3 + AI 生成 4 + 自动关联 1。

| Method | Path | Notes |
|--------|------|-------|
| GET | `/outlines/project/:id` | 大纲树(含全部 25+ 字段) |
| GET | `/outlines/:id` | 单节点详情 |
| POST | `/outlines/project/:id` | 创建节点 |
| PUT | `/outlines/:id` | 更新 |
| DELETE | `/outlines/:id` | 删除 |
| PUT | `/outlines/:id/move` | `{新父节点ID, 排序顺序}` |
| PUT | `/outlines/project/:id/batch` | `{outlines, replaceAll, deleteChildrenOfParents, deleteChapterIds}` |
| PUT | `/outlines/project/:id/renumber` | 重编号 |
| PUT | `/outlines/project/:id/reorder` | `{parentId, nodeIds}` |
| GET | `/outlines/project/:id/context` | AI 上下文(大) |
| GET | `/outlines/project/:id/characters` | 关联出场角色(精简版) |
| GET | `/outlines/project/:id/foreshadows` | 关联伏笔 |
| GET | `/outlines/project/:id/factions` | 关联势力 |
| GET | `/outlines/project/:id/scenes` | 场景列表 |
| GET | `/outlines/project/:id/event-line` | 事件线 |
| PUT | `/outlines/project/:id/event-line` | `{事件线}` |
| PUT | `/outlines/project/:id/event-line/chapters` | `{章节事件线列表}` |
| POST | `/outlines/project/:id/generations` | 保存 AI 生成 |
| GET | `/outlines/project/:id/generations?limit=` | 历史 |
| PUT | `/outlines/project/:id/generations/:genId/adopt` | 采纳 |
| DELETE | `/outlines/project/:id/generations/:genId` | 删除 |
| POST | `/outlines/project/:id/auto-link` | `{新实体列表}` 自动关联 |

### 4.5 角色模块 (`/characters`) · 14 端点 + 物品 6 + 关系 4 = 24 端点

CRUD 5 + AI 上下文 2 + 出场管理 2 + 关系 CRUD 4 + 批量删除 1 + 物品 6 (character_items) + 关系 4 (character_relations) + 8 (`/characters/{id}/enhance-context`, `/sync-appearances`, `/clear-appearances`, `/realm/*` 共享)。

### 4.6 世界观 17 模块 · 60+ 端点

> 统一模式(每个模块都有,部分缺失):
> - `GET /{module}/project/:id` 或 `GET /{module}/project/:id/list` 列表
> - `GET /{module}/:id` 或 `GET /{module}/project/:id/{id}` 详情
> - `POST /{module}/project/:id` 创建
> - `PUT /{module}/:id` 更新
> - `DELETE /{module}/:id` 删除
> - `GET /{module}/project/:id/context` AI 上下文
> - `POST /{module}/project/:id/generations` 保存生成
> - `GET /{module}/project/:id/generations?limit=` 历史
> - `PUT /{module}/project/:id/generations/:genId/adopt` 采纳(部分模块缺)
> - `DELETE /{module}/project/:id/generations/:genId` 删除

| 模块 | 路径前缀 | 端点数 | 关键端点 |
|------|----------|--------|----------|
| #1 世界观 | `/worldviews` | 10 | `+ /full`, `+ /versions` (POST/PUT rollback), `+ /sync` |
| #2 故事核心 | `/story-cores` | 4 | `/context` |
| #3 地理地图 | `/geo-maps` | 14 | `/list`, `/map/:mapId`, `/children-count`, `/worldview`, `/visits/batch` |
| #4 势力阵营 | `/factions` | 14 | `/list`, `/faction/:fId`, `/relations` CRUD 4, `/context` |
| #5 货币体系 | `/currencies` | 8 | `/list`, `/item` CRUD, `/sort`, `/context` |
| #6 物品列表 | `/items` | 13 | `/list`, `/all`, `/batch`, `/sort`, `/context` |
| #7 力量体系 | `/power-systems` | 11 | `/list`, `/system/:sId`, `/sort`, `/batch-delete`, `/context` |
| #8 功法体系 | `/skill-systems` | 12 | + `/stats` |
| #9 特殊设定 | `/special-settings` | 11 | + `/stats` |
| #10 大纲设定 | `/outlines` | (见 4.4) | 独立为一级入口 (C02 冲突裁决) |
| #11 角色管理 | `/characters` | (见 4.5) | 24 类型 + 三层性格 (C03) |
| #12 人物关系图 | `/characters/.../relations` | 4 | 与 #11 共用 |
| #13 伏笔管理 | `/foreshadows` | 15 | `+ /foreshadow/:fId/echo`, `+ /find-chapter`, `+ /chapter/:cId/foreshadows`, `/stats` |
| #14 情节脉络 | `/plot-structures` | 8 | `+ /list-with-stats`, `+ /plot/:pId` |
| #15 支线故事 | `/event-lines` + `/event-flow` + `/story-line` + `/element-bindx` | 33 | 4 个子模块聚合 |
| #16 时间线 | `/timeline` | 13 | `/calendar`, `/events`, `/chapter-time`, `/validate`, `/context` |
| #17 已经历事件 | `/event-lines/project/:id/...` (复用) | (复用) | 蒸馏集成 |

### 4.7 伏笔/情节/时间线 关键端点节选

| Method | Path | 说明 |
|--------|------|------|
| POST | `/foreshadows/project/:id/foreshadow/:fId/echo` | 添加回响 `{章节ID, 描述}` |
| GET | `/foreshadows/project/:id/chapter/:chapterId/foreshadows` | 章节伏笔 |
| POST | `/foreshadows/project/:id/find-chapter` | `{章节名}` → 章节ID |
| GET | `/timeline/calendar/:projectId` | 历法 |
| PUT | `/timeline/calendar/:projectId` | 保存历法 |
| GET | `/timeline/validate/:projectId` | 校验时间线 |
| GET | `/timeline/context/:projectId/:nodeId` | 节点上下文(大,可达 196 KB) |
| GET | `/element-bindx/project/:id/bindx-summary` | 绑定摘要 |
| POST | `/element-bindx/project/:id/event/:eId/batch` | `{要素名称, bindings}` |

### 4.8 AI 模块 (`/ai`) · 8 端点

| Method | Path | 说明 |
|--------|------|------|
| GET | `/ai/config` | AI 配置(等同 `/ai/status`) |
| PUT | `/ai/config` | 更新配置 |
| GET | `/ai/status` | AI 状态(全部厂商+模型列表) |
| POST | `/ai/chat` | AI 对话 `{messages, options}` |
| POST | `/ai/chat/session` | AI 会话对话 `{messages, options}` → `{sessionId}` |
| GET | `/ai/chat/stream/:sessionId?token=...` | **SSE 流式对话** (`text/event-stream`) |
| POST | `/ai/test` | AI 连接测试 `{provider, model, apiKey}` |
| GET | `/ai/models` | 扁平模型列表 (key = provider) |

请求体 `options` 结构:
```json
{
  "provider": "deepseek", "model": "deepseek-chat", "stream": true,
  "conversationId": "...", "对话ID": "...", "模式": "续写",
  "思考模式": true, "temperature": 0.85, "max_tokens": 8192
}
```

### 4.9 本地模型代理 (`/ai/local`)

| Method | Path | 说明 |
|--------|------|------|
| POST | `/ai/local/chat` | `{端点URL, API密钥, 请求路径, 自定义请求头, 请求体}` → 同步结果 |
| POST | `/ai/local/models` | 获取模型信息 |
| GET | `/api/ai/local/stream` | SSE 流式 |

### 4.10 蒸馏模块 (`/distill`) · 5 端点

| Method | Path | 说明 |
|--------|------|------|
| GET | `/distill/status/:projectId` | 获取蒸馏状态(轮询) |
| PUT | `/distill/status/:projectId` | 更新状态 `{状态}` |
| POST | `/distill/save/:projectId` | 保存蒸馏结果 `{摘要, 章节IDs}` |
| POST | `/distill/timeline/:projectId` | 蒸馏时间线 |
| POST | `/distill/reset-abnormal` | 重置异常 `{chapterId}` |

### 4.11 规则/规则广场 (`/rules` + `/rules/plaza`) · 14 端点

CRUD 5 + `/toggle` 1 + 场景规则 2 + 广场 7(列表/详情/点赞/收藏/官方/我的收藏/删除收藏)。

### 4.12 文笔风格/广场 (`/writing-styles` + `/writing-styles/plaza`) · 14 端点

CRUD 5 + `/toggle-share` 1 + `/use` 1 + 广场 7。

### 4.13 章节导入 (`/chapters/project/:id/import/*`) · 4 端点

见 4.3。

### 4.14 笔记/材料/义务 (`/notes` + `/materials` + `/obligations`)

| Module | 端点数 | 关键 |
|--------|--------|------|
| `/notes` | 5 | CRUD + `/pin` 置顶 |
| `/materials` | 5 | CRUD + `/details` |
| `/obligations` | 8 | CRUD + `/batch-update-status` + `/auto-expire` |

### 4.15 角色境界 (`/realm`) · 9 端点

`/character/:id/curve`, `/at-chapter?章节序号=`, `/breakthrough` POST, `/batch-breakthrough` POST, `/breakthroughs`, `/breakthrough/:id` PUT/DEL, `/project/:id/snapshot/:chapterId`, `/auto-breakthrough`。

### 4.16 对话管理 (`/conversations`) · 6 端点

`?project_id=` 列表, CRUD, `/:id/messages` GET/POST。

### 4.17 TTS (`/tts`) · 4 端点

`/status`, `/synthesize`, `/stream`, `/export`。19 种音色。

### 4.18 统计 (`/stats`) · 5 端点

`/today`, `/weekly`, `/monthly?` params, `/record` POST, `/project/:id`。

### 4.19 小说构建向导 (`/novel-build`) · 14 端点 ★ 11 步探讨式

| Step | Method | Path | 内容 |
|------|--------|------|------|
| 创建 | POST | `/novel-build/create` | 初始请求 |
| 1 | PUT | `/novel-build/:id/basic` | 基础信息 |
| 2 | PUT | `/novel-build/:id/worldview` | 世界观 |
| 3 | PUT | `/novel-build/:id/story-core` | 故事核心 |
| 4 | PUT | `/novel-build/:id/characters` | 角色 |
| 5 | PUT | `/novel-build/:id/plot-structure` | 情节结构 |
| 6 | PUT | `/novel-build/:id/foreshadows` | 伏笔 |
| 7 | PUT | `/novel-build/:id/geo-maps` | 地理地图 |
| 8 | PUT | `/novel-build/:id/factions` | 阵营 |
| 9 | PUT | `/novel-build/:id/power-systems` | 力量体系 |
| 10 | PUT | `/novel-build/:id/special-settings` | 特殊设定 |
| 11 | PUT | `/novel-build/:id/currencies` | 货币 |
| 全部 | GET | `/novel-build/:id/all` | 一次性获取 |
| 状态 | PUT | `/novel-build/:id/status` | `{构建状态}` |

### 4.20 心跳 · 1 端点

`POST /heartbeat?token=...` (前端 `navigator.sendBeacon`, 每 30s)。

### 4.21 管理后台 (`/admin/*`) · 50+ 端点

需 `最高角色等级 >= 80`。9 大子模块:

| 子模块 | 端点数 | 关键 |
|--------|--------|------|
| 用户管理 `/admin/users` | 14 | 列表/待审核/详情/编辑/审核/封禁/角色/配额/重置密码/导出/批量(4) |
| 角色权限 `/admin/roles` + `/admin/permissions` | 7 | CRUD + 权限分配 |
| 项目管理 `/admin/projects` | 9 | 列表/详情/章节/角色/世界观/批量删除/导出 |
| 内容管理 `/admin/content/*` | 6 | 章节/角色/世界观 CRUD |
| AI 管理 `/admin/ai/*` | 12 | 配置/对话/统计/Token 总览/每日/每月/按模型/按用户 |
| 在线用户 `/admin/online/*` | 4 | 当前/统计/趋势/历史 |
| 操作日志 `/admin/logs` | 4 | 列表/详情/统计/导出 |
| 系统统计 `/admin/stats` | 3 | 总览/趋势/仪表盘 |
| 系统配置 `/admin/settings` | 3 | 列表/单个/更新 |

### 4.22 错误码 (统一)

| HTTP | success | 场景 |
|------|---------|------|
| 200 | true | 成功 |
| 400 | false | 校验失败 |
| 401 | false | 未认证/Token 过期 |
| 403 | false | 权限不足(角色等级/项目归属) |
| 404 | false | 资源不存在 |
| 409 | false | 冲突(邮箱已注册/重复伏笔) |
| 429 | false | 频率/配额限制 |
| 500 | false | 服务器内部 |
| 502 | false | AI 上游失败 |
| 503 | false | 蒸馏队列满 |

---

## 5. 事件与异步任务契约

主控采用 **SSE + BullMQ(Redis)** 混合模式。同步走 HTTP/REST,异步走任务队列,SSE 仅用于 AI 流式输出。

### 5.1 AI 续写长文本生成管线 (SSE)

| Event | Direction | Payload | 触发 |
|-------|-----------|---------|------|
| `stream.start` | server→client | `{sessionId, requestId, model, mode}` | 收到 `POST /ai/chat/session` |
| `stream.chunk` | server→client | `{delta, index}` | 每个 token/词 |
| `stream.thinking` | server→client | `{thinkingChunk, index}` | 推理模型思考阶段 |
| `stream.tool_call` | server→client | `{toolName, args}` | 预留(未来 MCP) |
| `stream.end` | server→client | `{sessionId, totalTokens, costUsd, finishReason}` | 正常结束 |
| `stream.error` | server→client | `{code, message, retryable}` | 失败 |
| `stream.cancelled` | server→client | `{sessionId}` | 客户端断开 |

`finishReason`: `stop` | `length` | `content_filter` | `tool_calls` | `error`

### 5.2 蒸馏任务 (BullMQ `distill` 队列)

| Job Type | Trigger | Input | Output |
|----------|---------|-------|--------|
| `distill.chapter` | 章节状态变为 `complete` | `{chapterId, projectId}` | `{摘要, 模型, 状态, 完成时间}` |
| `distill.outline_node` | 手动触发 | `{outlineNodeId}` | 同上 |
| `distill.event_line` | 事件流追加 | `{eventId}` | 同上 |
| `distill.timeline` | 手动触发 | `{projectId}` | 时间线摘要 |
| `distill.recover_abnormal` | `POST /distill/reset-abnormal` | `{chapterId}` | 重试 |

Job State Machine: `waiting → active → completed | failed → (reset_abnormal) → waiting`。

事件(广播到 Redis PubSub,前端可选订阅):
- `distill.started`
- `distill.progress {percent}`
- `distill.completed {chapterId, 摘要}`
- `distill.failed {chapterId, 错误}`

### 5.3 伏笔检测与提醒

| Job Type | Trigger | Frequency |
|----------|---------|-----------|
| `foreshadow.scan_expired` | 每日 02:00 cron | 检查 `status='已埋设' AND due_at < now() AND chapter_id IS NULL` |
| `foreshadow.auto_resolve` | 章节完成时 | 自动检查章节是否触发回收(`/foreshadows/project/:id/chapter/:cId/foreshadows`) |
| `foreshadow.remind` | 时间线推进 | 在 editor 加载时拉取待回收列表 |

提醒通过 WebSocket/SSE 推送到前端(`remind.foreshadow` 事件),前端展示在右栏通知。

### 5.4 其他异步任务

| 队列 | Job | 说明 |
|------|-----|------|
| `import` | `chapter.import` | 章节批量导入(120s timeout) |
| `export` | `project.export` | 项目导出(可能数分钟) |
| `ai` | `ai.generation_record` | 生成记录落库 |
| `search` | `entity.reindex` | 知识图谱实体再索引 |
| `community` | `plaza.bump_score` | 规则/文笔热度刷新 |

---

## 6. AI 调度契约

### 6.1 模型路由 (12 厂商)

`provider-registry` 注册表(与云笔 1:1):

| provider_id | 名称 | 默认端点 | 默认模型 | 温度 | max_tokens | top_p | freq_penalty | pres_penalty | 思考支持 |
|-------------|------|---------|---------|------|------------|-------|--------------|--------------|----------|
| `deepseek` | DeepSeek | `https://api.deepseek.com/v1/chat/completions` | `deepseek-chat` | 0.85 | 8192 | 0.92 | 0.35 | 0.25 | ✓ |
| `doubao` | 豆包 | `https://ark.cn-beijing.volces.com/api/v3/chat/completions` | `doubao-seed-2.0-pro` | 0.80 | 8192 | 0.85 | 0.50 | 0.40 | ✓ |
| `qwen` | 通义千问 | `https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions` | `qwen3-235b-a22b` | 0.85 | 8192 | 0.80 | 0.50 | 0.40 | ✓ |
| `wenxin` | 文心一言 | `https://qianfan.baidubce.com/v2/chat/completions` | `ernie-4.5-8k` | 0.85 | 8192 | 0.85 | 0.50 | 0.40 | ✗ |
| `kimi` | Kimi | `https://api.moonshot.cn/v1/chat/completions` | `kimi-k2.5` | 0.80 | 8192 | 0.85 | 0.50 | 0.40 | ✓ |
| `glm` | 智谱GLM | `https://open.bigmodel.cn/api/paas/v4/chat/completions` | `glm-5` | 0.85 | 8192 | 0.85 | 0.50 | 0.40 | ✓ |
| `gemini` | Google Gemini | `https://generativelanguage.googleapis.com/v1beta/chat/completions` | `gemini-2.5-flash` | 0.85 | 8192 | 0.90 | — | — | ✗ |
| `gpt` | OpenAI | `https://api.openai.com/v1/chat/completions` | `gpt-5` | 0.85 | 8192 | 0.90 | 0.50 | 0.40 | ✓ (o 系列) |
| `nvidia` | NVIDIA NIM | `https://integrate.api.nvidia.com/v1/chat/completions` | `nvidia/nemotron-3-super-120b-a12b` | 0.85 | 8192 | 0.90 | 0.50 | 0.40 | ✓ |
| `siliconflow` | 硅基流动 | `https://api.siliconflow.cn/v1` | (转发) | — | — | — | — | — | — |
| `openrouter` | OpenRouter | `https://openrouter.ai/api/v1` | (转发) | — | — | — | — | — | — |
| `oneapi` | One API | (自定义) | (转发) | — | — | — | — | — | — |
| `custom` | 自定义兼容 | (自定义) | (转发) | — | — | — | — | — | — |

**思考模式特殊处理**:
- 推理模型列表: `deepseek-reasoner`, `deepseek-r1`, `deepseek-r2`, `o1/o3/o4 系列`, `qwen3.5`, `glm-5`, `kimi-k2.5`, `doubao-seed-2-0-pro-260215` 等
- `thinking: { type: "enabled" }`, `budget_tokens: 32768`
- gemini/wenxin 不支持思考模式
- OpenAI o 系列不传 `frequency_penalty`/`presence_penalty`

### 6.2 路由规则 (Model Router)

| 任务类型 | 推荐模型 | 备选 | 理由 |
|----------|---------|------|------|
| 长篇续写 | `deepseek-chat` | `qwen3-235b-a22b`, `doubao-seed-2.0-pro` | 性价比高,中文好 |
| 润色改写 | `claude-sonnet-4.6` (BYOK) | `gpt-5` | 文笔最佳 |
| 大纲生成 | `gpt-5.4` | `gemini-3.1-pro-preview` | 1M 窗口,结构化好 |
| 一致性检查 | `claude-opus-4.6` | `gemini-3.1-pro` | 1M 窗口,长程最稳 |
| 蒸馏摘要 | `deepseek-chat` | `qwen3-14b` | 便宜,任务简单 |
| 角色对话 | `doubao-seed-2.0-pro` | `deepseek-chat` | 角色感强 |
| 推理思考 | `deepseek-reasoner` | `o3-mini` | thinking mode |

### 6.3 上下文窗口管理 (三层架构)

| 层 | 容量 | 内容 | 存储 |
|----|------|------|------|
| L1 工作记忆 | 3000-8000 token | 当前场景 + 前 3-5 场景 + 当前角色状态 + 本章节拍 | 内存/Redis |
| L2 会话记忆 | top-k=2-5 RAG | 角色档案/世界观规则/情节线程/时间线/风格 | PG + pgvector |
| L3 归档记忆 | 全文/摘要 | 完整手稿 + 章节摘要 + 场景摘要 | PG + Object Storage |

组装顺序(L1 + L2 拼接成 prompt):
1. 系统 prompt(角色定义+格式约束) ~ 500 token
2. 项目级 L2 context(世界/角色/大纲核心) ~ 2000 token
3. 章节级 L1 context(前 3 章摘要 + 当前场景) ~ 3000 token
4. 用户指令 ~ 200 token
5. **总 token ≤ 8000**,超出则截断 L1 最旧场景

### 6.4 蒸馏机制 (Generator→Extractor→Checker)

```
[Generator]  LLM生成章节
    ↓
[Extractor]  蒸馏: 提取 实体/状态/伏笔/事件 → 写入 L2 + L3
    ↓
[Checker]    一致性检查: 与 L2 既有实体对比 → 报告
    ↓
[Apply]      人工/自动采纳 → 更新 L2 + L3
```

| 阶段 | 模型 | 输入 | 输出 | 频率 |
|------|------|------|------|------|
| Generator | deepseek-chat | L1+L2 context | 章节正文 | 用户触发 |
| Extractor | deepseek-chat | 章节全文 | `{entities, states, foreshadows, events}` | 章节完成 |
| Checker | claude-sonnet | Extractor结果 + L2 | `{conflicts: [...], suggestions: [...]}` | 每 5 章或手动 |

### 6.5 生成模式 (6 + 自定义)

| 模式 | 端点 | Prompt 模式字段 |
|------|------|-----------------|
| 续写 | `POST /ai/chat` | `模式: "续写"` |
| 润色 | `POST /ai/chat` | `模式: "润色"` |
| 对话 | `POST /ai/chat` | `模式: "对话"` |
| 查漏 | `POST /ai/chat` | `模式: "查漏"` |
| 修正 | `POST /ai/chat` | `模式: "修正"` |
| 展开 | `POST /ai/chat` | `模式: "展开"` (需选中文本) |
| 大纲AI | `POST /ai/chat/session` | `模式: "大纲AI"` |
| 角色AI | `POST /ai/chat/session` | `模式: "角色AI"` |
| 推演 | `POST /ai/chat/session` | `模式: "剧情推演"` |
| 文风调整 | `POST /ai/chat/session` | `模式: "文风调整"` |

### 6.6 配额与节流 (Quota Throttler)

| 维度 | Free | Pro | 限制 |
|------|------|-----|------|
| 每日字数 | 5,000 | 100,000 | 字符数(中英文) |
| 并发 AI 请求 | 2 | 10 | 滑动窗口 |
| 单请求 max_tokens | 8,192 | 8,192 | 不可调 |
| 蒸馏队列深度 | 5 | 50 | BullMQ concurrency |
| 项目数 | 不限 | 不限 | (原版) |
| 章节导入 | 50/次 | 500/次 | 批量 |
| Token 缓存命中率 | 80% | 90% | (估算) |

节流策略: Token Bucket (Redis),按 `user_id` 维度,失败回退到"提示升级 Pro"。

---

## 7. 前端架构契约

### 7.1 路由 (Vue Router 4)

| 路径 | 组件 | 守卫 |
|------|------|------|
| `/` | `Home.vue` | 公开 |
| `/login` | `LoginForm.vue` | 公开 |
| `/register` | `RegisterForm.vue` | 公开 |
| `/projects` | `ProjectList.vue` | 需 auth |
| `/create-novel` | `NovelBuildWizard.vue` (3 模式) | 需 auth |
| `/editor/:id` | `EditorLayout.vue` | 需 auth + 项目归属 |
| `/editor/:id/world/:module` | 17 个 `*Editor.vue` | 同上 |
| `/editor/:id/character` | `CharacterList.vue` | 同上 |
| `/editor/:id/chapter/:cid` | `ChapterEditor.vue` | 同上 |
| `/admin/**` | 管理后台组件 | `最高角色等级 >= 80` |

### 7.2 状态管理 (Pinia)

按模块分 store(共 17 + 核心):

```
stores/
├── auth.ts             # 登录态/user/permissions
├── project.ts          # 当前项目/列表/筛选
├── chapter.ts          # 当前章节/内容/自动保存
├── outline.ts          # 大纲树
├── ai.ts               # AI 会话/流式状态
├── ui.ts               # 主题/侧栏宽度/通知
├── quota.ts            # 每日配额
├── tutorial.ts         # 引导状态
└── world/
    ├── worldview.ts    # #1
    ├── storyCore.ts    # #2
    ├── geoMap.ts       # #3
    ├── faction.ts      # #4
    ├── currency.ts     # #5
    ├── item.ts         # #6
    ├── power.ts        # #7
    ├── skill.ts        # #8
    ├── special.ts      # #9
    ├── outline.ts      # #10
    ├── character.ts    # #11
    ├── relationship.ts # #12
    ├── foreshadow.ts   # #13
    ├── plot.ts         # #14
    ├── subplot.ts      # #15
    ├── timeline.ts     # #16
    └── eventline.ts    # #17
```

### 7.3 组件层级 (Component Tree)

```
<App>
  <RouterView />
  ├── <Home> / <Login> / <Register>
  ├── <ProjectList>            <-- /projects
  │   ├── <ProjectCard>
  │   ├── <StatCard> x 4
  │   └── <Toolbar>
  ├── <NovelBuildWizard>       <-- /create-novel (3 模式)
  └── <EditorLayout>           <-- /editor/:id
      ├── <TopBar>             <-- Logo + 菜单 + 工具栏 + 通知
      ├── <LeftPanel ~250px>   <-- 3 Tab: 项目/角色/世界
      │   ├── <OutlineTree>           (项目 Tab)
      │   ├── <CharacterCardGrid>     (角色 Tab)
      │   └── <WorldTab>              (世界 Tab · 17 模块)
      │       └── <ModuleDrawer>      <-- 通用容器
      │           └── <Module{1-17}Editor>
      ├── <CenterPanel>        <-- 编辑器
      │   ├── <ChapterHeader>
      │   ├── <TipTapEditor>           <-- ProseMirror
      │   └── <StatusBar>
      ├── <RightPanel ~300px>  <-- 3 Tab: AI 助手/工具箱/统计
      │   ├── <AIPanel>                <-- 6 按钮 + 流式渲染
      │   ├── <ToolboxPanel>
      │   └── <StatsPanel>
      └── <BottomStatusBar>
```

### 7.4 编辑器核心 (TipTap)

扩展: `StarterKit` + `CharacterMark` (角色名) + `LocationMark` (地名) + `ItemMark` (物品) + `ForeshadowMark` (伏笔) + 自动保存插件 (debounce 2s)。

键盘: `Ctrl+S` 立即保存, `Ctrl+Enter` 触发续写, `Tab` 缩进。

### 7.5 AI 协作面板

```
<AIPanel>
  ├── <QuickActions>          <-- 6 按钮 (续写/润色/对话/查漏/修正/展开)
  ├── <ConversationHistory>   <-- 滚动的 user/assistant 气泡
  │   ├── <UserMessage>
  │   └── <AIMessage>         <-- 富文本 + "应用修改"/"复制"按钮
  ├── <StreamingIndicator>    <-- 流式打字光标
  └── <InputBox>              <-- textarea + 2 附件按钮 + 发送
```

### 7.6 World Tab 抽屉 (`ModuleDrawer.vue`)

统一容器,17 模块共用,差异在内容组件 + 顶部按钮组(2-8 个)。

### 7.7 主题系统

| 主题 | 说明 |
|------|------|
| 默认深色 (zh-CN) | 中文 CSS 变量, 主色 `--pri: 蓝` |
| 亮色 | 浅色背景 |
| 古风 | 红/金配色 |
| 极简 | 灰/白 |
| ...共 15 种 | (源自项目管理页分析) |

实现: CSS 变量 + localStorage 持久化 + 跨窗口同步 (BroadcastChannel)。

### 7.8 响应式

断点: `<768px` 移动端(浮动 AI 按钮 + 底部抽屉), `768-1024px` 平板(双栏), `>1024px` 桌面(三栏)。

---

## 8. 后端架构契约

### 8.1 服务拆分 (Microservices vs Monolith)

**Sprint 0 选型**: **Modular Monolith (NestJS)** — 单仓库单进程,按模块切分,后续可拆。

理由:
- 230+ 端点强耦合(世界模块互相调用 context)
- 团队规模 3-5 人,微服务运维成本过高
- 共享 PG/Redis,跨服务事务简单

**未来拆分候选**:
- `ai-orchestrator` 独立(负载大)
- `distill` 独立(CPU/GPU 重)
- `admin` 独立(管理员低频)

### 8.2 进程内模块

```
backend/
├── src/
│   ├── main.ts
│   ├── app.module.ts
│   ├── common/                # 装饰器/守卫/拦截器/管道/异常
│   ├── modules/
│   │   ├── auth/
│   │   ├── user/
│   │   ├── project/
│   │   ├── chapter/
│   │   ├── outline/
│   │   ├── world/             # 17 子模块
│   │   ├── character/
│   │   ├── foreshadow/
│   │   ├── timeline/
│   │   ├── plot/
│   │   ├── ai/                # 路由层,业务在 ai-orchestrator
│   │   ├── distill/
│   │   ├── rules/
│   │   ├── community/
│   │   ├── stats/
│   │   ├── conversation/
│   │   ├── tts/
│   │   ├── novel-build/
│   │   ├── export/
│   │   └── admin/
│   ├── queue/                 # BullMQ workers
│   ├── events/                # EventEmitter (进程内) + Redis PubSub (跨进程)
│   └── config/
└── prisma/ (或 drizzle/)
```

### 8.3 API 网关 (Fastify/NestJS Middleware)

| 责任 | 实现 |
|------|------|
| JWT 校验 | `JwtMiddleware` (HS256, 与云笔一致) |
| Origin 校验 | 必须 `https://<your-domain>`,否则 403 |
| CORS | 仅允许主域 |
| 限流 | `@fastify/rate-limit` 按 user_id |
| 日志 | Pino + request id 注入 |
| Trace | OpenTelemetry auto-instrumentation |
| 错误转换 | 统一 `ApiResponse` 包装 |

### 8.4 数据库

| 库 | 用途 |
|----|------|
| PostgreSQL 16 | 主库 (JSONB 关键) |
| pgvector | RAG 嵌入 (L2 检索) |
| Redis 7 | 会话/配额/Token Bucket/SSE PubSub/BullMQ |
| ClickHouse (可选) | 大日志/统计 |
| Neo4j (可选) | 实体关系图 (P3+) |

### 8.5 关键中间件

| 中间件 | 版本 | 用途 |
|--------|------|------|
| Fastify 或 NestJS | Fastify 5 / Nest 10 | HTTP 框架 |
| Prisma 或 Drizzle | 最新 | ORM (JSONB 支持对比: Drizzle 更灵活) |
| BullMQ | 5.x | 异步任务 |
| ioredis | 5.x | Redis 客户端 |
| jsonwebtoken | 9.x | JWT |
| bcrypt | 5.x | 密码 |
| @aws-sdk/client-s3 | 3.x | 对象存储 |
| @nestjs/event-emitter | 1.x | 进程内事件 |
| prom-client | 15.x | Prometheus |
| OpenTelemetry SDK | 1.x | trace |

### 8.6 缓存策略

| Key | TTL | 失效 |
|-----|-----|------|
| `ai:status:{userId}` | 5 min | AI 配置变更 |
| `context:outlines:{projectId}` | 10 min | 大纲 PUT |
| `context:characters:{projectId}` | 10 min | 角色变更 |
| `quota:{userId}:{date}` | 当日 | 午夜滚动 |
| `sse:session:{sessionId}` | 5 min | session 关闭 |
| `token:cache:{hash}` | 1 hour | TTL |

### 8.7 部署拓扑 (Sprint 0 → 生产)

```
Sprint 0 (Docker Compose):
  [nginx] → [api:1] (单体)
  [postgres] [redis] [minio] [prometheus] [grafana]

生产 (K8s):
  [Ingress] → [api:3+] (HPA)
  [postgres-rds] [elasticache-redis] [s3] [prometheus] [grafana] [tempo] [loki]
```

---

## 9. 跨模块一致性约束

### 9.1 实体-关系全局图

```
        [Project]
           |
   ┌───────┼───────┬──────────┬──────────┐
   ↓       ↓       ↓          ↓          ↓
[Chapter] [Outline] [Character] [WorldSetting: 17 modules] [Conversation]
   |         |          |              |
   ├─关联─→ Outline   ├─Relations    ├─Faction
   |         |          ├─Items       ├─PowerSystem
   |         |          ├─Appearances ├─SkillSystem
   |         |          └─Realm       ├─Item
   |         |                         ├─Currency
   |         |                         ├─GeoMap
   |         |                         ├─Foreshadow
   |         |                         ├─PlotStructure
   |         |                         ├─EventLine / EventFlow
   |         |                         ├─Timeline (Calendar + Events)
   |         |                         └─StoryCore / Worldview / SpecialSetting
   |         ↓
   |     [ElementBindx] ← 绑定到 chapter/character/foreshadow/faction
   |
   ↓
[DistillRecord]
```

### 9.2 强一致性规则

| 约束 | 实现 |
|------|------|
| Chapter.关联大纲节点ID ↔ Outline.id | FK + 触发器,大纲节点删除时章节 `关联大纲节点ID` 置 NULL |
| Character.当前境界ID ↔ PowerSystem.境界列表 | 应用层校验(允许 ID 已删,提示"境界失效") |
| 伏笔.回收章节ID > 伏笔.埋设章节ID | 业务校验,违反返回 400 |
| Timeline.历法日期 ↔ 章节.排序顺序 | 章节时序表存 `(project_id, 章节ID, 历法日期)` |
| 角色.存续状态 ∈ {活跃,死亡,失踪,Unknown} | 状态机:`Alive → Dead/Unknown`,不可逆 |
| 势力关系.角色A ≠ 角色B | DB CHECK 约束 |
| 项目.章节数 = COUNT(chapters WHERE project_id=?) | 触发器自动维护 |

### 9.3 设定变更传播 (Setting Change Propagation)

当 `Worldview` / `Faction` / `PowerSystem` 变更时,需要广播事件:

```
worldview.updated
  → 失效 context:worldviews:{projectId} 缓存
  → 触发一致性检查 (ConsistencyChecker)
  → 如果新增境界,提醒"未绑定的角色"
  → 如果删除势力,检查引用该势力的角色/伏笔 (提示,不级联删除)
```

事件流(主控契约):

| Event | Payload | 订阅者 |
|-------|---------|--------|
| `worldview.updated` | `{projectId, field}` | consistency-checker, context-cache |
| `character.died` | `{characterId, chapterId}` | foreshadow-tracker, character-state-machine |
| `foreshadow.buried` | `{foreshadowId, chapterId}` | timeline-validator |
| `foreshadow.resolved` | `{foreshadowId, chapterId}` | foreshadow-tracker |
| `timeline.event_added` | `{projectId, eventId}` | consistency-checker |
| `chapter.distilled` | `{chapterId, projectId}` | context-cache (clear chapter) |

### 9.4 五层一致性检查 (ConStory-style)

| 层 | 触发 | 输出 |
|----|------|------|
| L1 结构化世界 | 写入时 | 字段约束 + FK |
| L2 上下文管理 | 续写前 | RAG 检索相关,token 监控 |
| L3 约束生成 | 续写时 | prompt 模板强制风格/角色 |
| L4 后审计 | 每 5 章 | Checker 模型报告 `{conflicts[]}` |
| L5 人工审阅 | 永远 | 采纳/拒绝 UI |

### 9.5 数据完整性自检 (Cron)

每日 03:00:
- 角色引用了已删除的境界 → 标记"境界失效"
- 伏笔超过 90 章未回收 → 提醒
- 时间线历法日期冲突 → 报告
- 章节字数与 `蒸馏状态` 不一致 → 重置异常

---

## 10. 子项目目录结构(主控布局)

```
master/                                   # 工作目录根
├── README.md                             # 项目入口
├── CLAUDE.md                             # 主控 Prompt (给 Claude Code 读)
├── harness.config.json                   # harness-l3-v4 配置
├── feature_list.json                     # feature 任务清单
├── progress.txt                          # 进度日志
├── init.sh                               # 一键启动脚本 (跨平台)
├── .gitignore
├── docker-compose.yml                    # Sprint 0 全栈编排
├── docker-compose.dev.yml                # 开发环境(挂载本地代码)
│
├── contracts/                            # ★ 主控权威契约
│   ├── README.md                         # 契约使用指南
│   ├── openapi/
│   │   ├── root.yaml                     # 聚合入口
│   │   ├── auth.yaml
│   │   ├── project.yaml
│   │   ├── chapter.yaml
│   │   ├── outline.yaml
│   │   ├── character.yaml
│   │   ├── world-tab/
│   │   │   ├── worldview.yaml
│   │   │   ├── story-core.yaml
│   │   │   ├── geo-map.yaml
│   │   │   ├── faction.yaml
│   │   │   ├── currency.yaml
│   │   │   ├── item.yaml
│   │   │   ├── power-system.yaml
│   │   │   ├── skill-system.yaml
│   │   │   ├── special-setting.yaml
│   │   │   ├── outline-setting.yaml
│   │   │   ├── character-mgmt.yaml
│   │   │   ├── relationship.yaml
│   │   │   ├── foreshadow.yaml
│   │   │   ├── plot.yaml
│   │   │   ├── subplot.yaml
│   │   │   ├── timeline.yaml
│   │   │   └── event-line.yaml
│   │   ├── ai.yaml
│   │   ├── distill.yaml
│   │   ├── rules.yaml
│   │   ├── stats.yaml
│   │   ├── conversation.yaml
│   │   ├── tts.yaml
│   │   ├── novel-build.yaml
│   │   ├── heartbeat.yaml
│   │   └── admin.yaml
│   ├── schemas/                          # JSON Schema (TS/Python 共享)
│   │   ├── project.json
│   │   ├── chapter.json
│   │   ├── outline.json
│   │   ├── character.json
│   │   └── world-setting/
│   │       ├── worldview.json
│   │       ├── geo-map.json
│   │       ├── power-system.json
│   │       ├── foreshadow.json
│   │       └── ... (17 个)
│   ├── events/                           # 事件契约
│   │   ├── ai-stream.ts                  # SSE 事件
│   │   ├── distill-events.ts
│   │   ├── foreshadow-events.ts
│   │   └── consistency-events.ts
│   ├── ai/
│   │   ├── providers.json                # 12 厂商注册表
│   │   ├── routing-rules.yaml            # 模型路由
│   │   ├── context-schema.json
│   │   ├── distill-pipeline.ts            # 三阶段契约
│   │   ├── thinking-modes.yaml
│   │   ├── quota-rules.yaml
│   │   └── local-proxy-schema.json
│   ├── frontend/
│   │   ├── routes.ts                     # 前端路由
│   │   ├── world-tabs.ts                 # 17 模块清单
│   │   ├── themes.ts                     # 主题列表
│   │   ├── sse-events.ts
│   │   └── editor-events.ts
│   └── CHANGELOG.md                      # 契约变更日志 (主控裁决)
│
├── backend/                              # 后端子项目
│   ├── package.json
│   ├── tsconfig.json
│   ├── nest-cli.json (或 fastify 配置)
│   ├── prisma/ (或 drizzle/)
│   │   ├── schema.prisma
│   │   ├── migrations/
│   │   └── seed.ts
│   ├── src/
│   │   ├── main.ts
│   │   ├── app.module.ts
│   │   ├── common/
│   │   ├── modules/
│   │   ├── queue/
│   │   ├── events/
│   │   └── config/
│   ├── test/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── e2e/
│   ├── Dockerfile
│   └── README.md
│
├── frontend/                             # 前端子项目
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   ├── index.html
│   ├── src/
│   │   ├── main.ts
│   │   ├── App.vue
│   │   ├── router/
│   │   ├── stores/
│   │   ├── api/                          # Axios 客户端 (从 openapi 生成)
│   │   ├── components/
│   │   │   ├── common/
│   │   │   ├── editor/
│   │   │   ├── world/                    # 17 个 *Editor.vue
│   │   │   ├── ai/
│   │   │   └── admin/
│   │   ├── pages/
│   │   ├── composables/                  # useAIStream, useAutoSave ...
│   │   ├── assets/                       # 主题 CSS / icons
│   │   └── utils/
│   ├── public/
│   ├── Dockerfile
│   └── README.md
│
├── ai-orchestrator/                      # AI 调度子项目 (Python 或 Node)
│   ├── pyproject.toml (或 package.json)
│   ├── src/
│   │   ├── provider_registry.py
│   │   ├── model_router.py
│   │   ├── context_assembler.py
│   │   ├── token_cache.py
│   │   ├── sse_gateway.py
│   │   ├── distill_pipeline.py
│   │   ├── thinking_mode.py
│   │   ├── quota_throttler.py
│   │   ├── local_proxy.py
│   │   └── generation_store.py
│   ├── tests/
│   ├── Dockerfile
│   └── README.md
│
├── knowledge-graph/                      # 知识图谱 / 一致性 (Sprint 2+)
│   ├── README.md
│   └── (待 Sprint 2 详细规划)
│
├── infra/                                # 基础设施
│   ├── docker/
│   │   ├── postgres/init.sql
│   │   ├── redis/redis.conf
│   │   └── nginx/nginx.conf
│   ├── k8s/                              # 生产 K8s manifests
│   │   ├── api.yaml
│   │   ├── postgres.yaml
│   │   ├── redis.yaml
│   │   └── ingress.yaml
│   ├── monitoring/
│   │   ├── prometheus.yml
│   │   ├── grafana-dashboards/
│   │   └── alerts.yaml
│   ├── ci/
│   │   ├── github-actions/
│   │   └── pre-commit-hooks.sh
│   └── scripts/
│       ├── backup.sh
│       ├── restore.sh
│       └── migrate.sh
│
├── docs/                                 # 文档
│   ├── architecture/
│   │   ├── system-overview.md
│   │   ├── data-flow.md
│   │   ├── sequence-diagrams/
│   │   └── deployment.md
│   ├── adr/                              # Architecture Decision Records
│   │   ├── 0001-modular-monolith.md
│   │   ├── 0002-pinia-store-per-module.md
│   │   ├── 0003-postgres-jsonb.md
│   │   ├── 0004-12-provider-ai-gateway.md
│   │   ├── 0005-distill-three-stage.md
│   │   ├── 0006-bymonth-freemium.md
│   │   ├── 0007-vue3-tiptap-stack.md
│   │   ├── 0008-tip-tap-vs-tinymce.md
│   │   ├── 0009-pgvector-for-rag.md
│   │   └── 0010-three-layer-context.md
│   ├── api/                              # 生成的 API 文档 (从 openapi)
│   ├── onboarding/
│   │   ├── dev-setup.md
│   │   └── coding-standards.md
│   └── runbooks/
│       ├── ai-failure.md
│       ├── distill-backlog.md
│       └── pg-recovery.md
│
├── features/                             # 单 feature PRD/设计/验收
│   ├── _template/
│   │   ├── prd.md
│   │   ├── design.md
│   │   ├── test.md
│   │   └── acceptance.md
│   ├── f001-auth/
│   ├── f002-project-crud/
│   ├── f003-editor/
│   ├── f004-outline-tree/
│   ├── f005-ai-continue-sse/
│   ├── f006-world-17-modules/
│   ├── f007-character/
│   ├── f008-foreshadow/
│   ├── f009-timeline/
│   ├── f010-distill/
│   ├── f011-admin/
│   ├── f012-ai-gateway/
│   └── f013-quota/
│
├── progress/                             # 进度
│   ├── sprint-0/
│   │   ├── burndown.md
│   │   ├── daily.md
│   │   └── retrospective.md
│   ├── sprint-1/
│   └── ...
│
├── scripts/                              # 工具脚本
│   ├── openapi-to-client.sh              # 生成 TS client
│   ├── openapi-to-server.sh              # 生成 server stubs
│   ├── contract-lint.py                  # 契约一致性检查
│   └── e2e-smoke.sh
│
└── .claude/                              # harness 配置
    ├── settings.json
    └── hooks/
```

---

## 11. Sprint 0 主控初始化任务清单

> **Sprint 0 目标**: 从 0 跑通"登录 → 创建项目 → 编辑器 → AI 续写(SSE)"主链。
> **工作量**: 6-8 人月(2 前端 + 1 后端 + 1 AI 工程师, 4-6 周)。

| ID | 标题 | 子项目 | 依赖 | 产出物 | 验收标准 |
|----|------|--------|------|--------|----------|
| S0-01 | 初始化 monorepo 目录 + .gitignore + README | master | — | `master/` 完整目录结构(§10) | `tree master` 与 §10 100% 一致 |
| S0-02 | 编写主控 `CLAUDE.md` (给 Claude Code 读的项目说明) | master | S0-01 | `CLAUDE.md` | 包含§1-§13 全部摘要, Claude Code 能直接读懂 |
| S0-03 | 编写 `harness.config.json` (harness-l3-v4 配置) | master | S0-02 | `harness.config.json` | 5 阶段配置完整 (research/plan/build/review/debug) |
| S0-04 | 编写 `init.sh` (Windows + Linux/Mac 跨平台) | master | S0-01 | `init.sh` | 一键 `init.sh dev` 启动 PG+Redis+MinIO+API+FE |
| S0-05 | 编写 `feature_list.json` (Phase 1 13 个 feature 任务) | master | S0-02 | `feature_list.json` | 13 条任务, 含 `id/title/depends/passes` |
| S0-06 | 初始化 `progress.txt` | master | S0-05 | `progress.txt` | Sprint 0 目标/今日计划/障碍 三段式 |
| S0-07 | 编写 OpenAPI 契约 §4.1 auth.yaml | contracts | — | `contracts/openapi/auth.yaml` | 8 端点 + JWT 心跳, 100% 与 §4.1 对应 |
| S0-08 | 编写 OpenAPI 契约 §4.2 project.yaml | contracts | — | `contracts/openapi/project.yaml` | 8 端点, 字段中文名 |
| S0-09 | 编写 OpenAPI 契约 §4.3 chapter.yaml | contracts | — | `contracts/openapi/chapter.yaml` | 11 端点 + 三重冗余字段 |
| S0-10 | 编写 OpenAPI 契约 §4.4 outline.yaml | contracts | — | `contracts/openapi/outline.yaml` | 22 端点 |
| S0-11 | 编写 OpenAPI 契约 §4.8 ai.yaml | contracts | — | `contracts/openapi/ai.yaml` | 8 端点 + SSE 规范 |
| S0-12 | 编写 JSON Schema project/chapter/outline/character | contracts | S0-07..S0-10 | `contracts/schemas/*.json` | 与 §3 表字段 100% 一致 |
| S0-13 | 编写 AI provider 注册表 (12 厂商) | contracts | — | `contracts/ai/providers.json` | 与 §6.1 表 100% 一致 |
| S0-14 | 编写模型路由规则 | contracts | S0-13 | `contracts/ai/routing-rules.yaml` | 8 任务类型路由 |
| S0-15 | 编写 `init.sh` Docker Compose (PG+Redis+MinIO+API+FE) | infra | S0-04 | `docker-compose.yml` + `docker-compose.dev.yml` | `docker compose up` 一键启动, 健康检查通过 |
| S0-16 | 初始化 NestJS/Fastify backend 骨架 | backend | S0-15 | `backend/src/main.ts` | `/health` 返回 200 |
| S0-17 | 实现 Prisma/Drizzle schema (users + projects + chapters) | backend | S0-12, S0-16 | `prisma/schema.prisma` | `prisma migrate dev` 成功 |
| S0-18 | 实现 auth 模块 (8 端点 + JWT + 心跳) | backend | S0-07, S0-17 | `backend/src/modules/auth/` | 登录返回 token, 心跳保活 |
| S0-19 | 实现 project 模块 (8 端点 + 配额) | backend | S0-08, S0-17 | `backend/src/modules/project/` | CRUD + 配额校验 |
| S0-20 | 实现 chapter 模块 (11 端点 + 三重冗余 + 自动保存) | backend | S0-09, S0-17 | `backend/src/modules/chapter/` | PUT /chapters/:id 写时同时写 3 字段 |
| S0-21 | 实现 outline 模块 (22 端点 + 树形 + 移动 + 重编号) | backend | S0-10, S0-17 | `backend/src/modules/outline/` | 卷-章树形 CRUD 完整 |
| S0-22 | 初始化 Vue 3 + Vite + TipTap + Pinia + Tailwind 骨架 | frontend | S0-15 | `frontend/src/main.ts` + `App.vue` | `pnpm dev` 启动,空白首页 |
| S0-23 | 实现登录/注册页 + auth store | frontend | S0-22, S0-07 | `pages/Login.vue` + `stores/auth.ts` | 登录跳 /projects |
| S0-24 | 实现项目列表页 (4 统计卡片 + 网格 + 搜索 + 分页) | frontend | S0-19, S0-23 | `pages/ProjectList.vue` | 显示用户 4 个项目,12/页 |
| S0-25 | 实现编辑器三栏布局 (顶/左/中/右/底) | frontend | S0-22 | `components/editor/EditorLayout.vue` | 三栏 250/auto/300, 顶底全宽 |
| S0-26 | 集成 TipTap + 自动保存 (debounce 2s) | frontend | S0-20, S0-25 | `components/editor/TipTapEditor.vue` | 输入 2s 后 PUT /chapters/:id |
| S0-27 | 实现左侧"项目 Tab" 大纲树 | frontend | S0-21, S0-25 | `components/editor/OutlineTree.vue` | 卷-章折叠/展开/选中 |
| S0-28 | 实现 AI 助手面板 (6 按钮 + 输入框) | frontend | S0-25 | `components/ai/AIPanel.vue` | 6 按钮可点击 |
| S0-29 | 实现 AI 续写 SSE 流式渲染 | frontend + ai-orchestrator | S0-11, S0-28 | `composables/useAIStream.ts` + `ai-orchestrator/sse_gateway.py` | 点击续写 → 流式打字 → 完成 |
| S0-30 | 接入 DeepSeek (一个厂商) 验证 | ai-orchestrator | S0-29, S0-13 | `ai-orchestrator/provider_registry.py` | 续写真实调用 DeepSeek 成功 |
| S0-31 | 编写 E2E 冒烟: 登录 → 创建项目 → 进编辑器 → 续写 1 章 | tests | S0-23..S0-30 | `scripts/e2e-smoke.sh` + Playwright | 跑通主链, 截图存档 |
| S0-32 | 编写 `docker-compose.yml` 集成测试 | infra | S0-31 | `docker-compose.yml` | `docker compose up` 启动后 E2E 通过 |
| S0-33 | 初始化监控 (Prometheus + Grafana) | infra | S0-32 | `infra/monitoring/` | Grafana 显示 API 延迟/AI 调用次数 |
| S0-34 | 编写 ADR §13 (10 个关键决策) | docs | — | `docs/adr/0001..0010.md` | 10 个 ADR 完整, 每条含 决策/备选/理由/影响 |
| S0-35 | 编写 `docs/architecture/system-overview.md` | docs | S0-34 | `docs/architecture/system-overview.md` | 含主控定位/模块图/数据流 |
| S0-36 | 编写 `scripts/contract-lint.py` 契约一致性检查 | scripts | S0-07..S0-14 | `scripts/contract-lint.py` | 检查 schema 字段名与 OpenAPI 一致 |
| S0-37 | CI 工作流 (GitHub Actions) lint+test+build | infra/ci | S0-36 | `.github/workflows/ci.yml` | push 触发, 全部通过 |

**Sprint 0 验收**: 跑通"注册 → 登录 → 创建项目(空) → 进入编辑器 → 输入 100 字 → 自动保存 → 触发 AI 续写 200 字 → SSE 流式显示 → 手动采纳插入 → 保存"完整链路。

---

## 12. 风险与开放问题

### 12.1 来自 `knowlage/_conflicts/2026-06-03 冲突清单` 的 11 条裁决

| # | 维度 | 裁决 (主控采纳) | 状态 |
|---|------|----------------|------|
| C01 | 模块总数 | **17 模块** (Master Reference 2026-06-03 为准) | 已裁决 |
| C02 | 大纲设定位置 | **独立为一级入口** (World Tab 一级) | 已裁决 |
| C03 | 角色类型 | **24 类 + 三层性格 + 7 段背景** | 已裁决 |
| C04 | 角色数据规模 | 取决于项目,不预设(玄穹开 20, 烬都奇谭 7) | 已裁决 |
| C05 | 伏笔管理 | **6 类型 + 10 埋设模式** | 已裁决 |
| C06 | 大纲 AI 模式 | **3 模式 (传统/抽卡/对话)** | 已裁决 |
| C07 | 项目 ID | 复刻项目用自增 ID,与原版无关 | 已裁决 |
| C08 | 章节数 | 同上 | 已裁决 |
| C09 | 势力数量 | **9 势力** (A2 §1) | 已裁决 |
| C10 | 物品数量 | 同 C04, 数据量取决于项目 | 已裁决 |
| C11 | API 端点 | **17 模块 60+ 端点** (旧 16 模块 55+ 已 superseded) | 已裁决 |

### 12.2 主控需进一步裁决的开放问题

| # | 问题 | 候选 | 建议 (主控倾向) |
|---|------|------|----------------|
| Q01 | Base URL 前缀 `/api` vs `/api/v1` | 已知云笔用 `/api`, 用户需求说 `/api/v1` | **保持 `/api`** 1:1 复刻; 新版本再 `/api/v2` |
| Q02 | 字段中文化 vs 英文化 | 云笔用中文字段名 | **保留中文 key** 作为权威 schema, 后端英文 alias (如 `id`, `createdAt`) |
| Q03 | 三重冗余 `内容/正文/content` | 是否废弃后两个 | **Sprint 0 保留三个, Sprint 1 评估迁移** |
| Q04 | ORM 选型 | Prisma vs Drizzle vs TypeORM | **Drizzle** (JSONB + 性能更佳) |
| Q05 | 实时通信 | SSE vs WebSocket | **SSE** (与原版一致, AI 流式); 通知/伏笔提醒用 SSE + Redis PubSub |
| Q06 | 部署 | Docker Compose vs K8s | Sprint 0 用 Compose, 生产 K8s |
| Q07 | 多厂商 vs 单厂商启动 | 12 厂商 vs 1 厂商 | Sprint 0 先接 DeepSeek, Sprint 1 接满 12 |
| Q08 | RAG 实现 | pgvector vs 外部 (Qdrant/Milvus) | **pgvector** (单库, 运维简单) |
| Q09 | 富文本 | TipTap vs TinyMCE vs Lexical | **TipTap** (与原版一致) |
| Q10 | 知识图谱 | Neo4j vs PG 递归 CTE | Sprint 0 用 PG + pgvector, Neo4j P3 之后 |
| Q11 | 商业化 | Freemium vs BYOK only | **两者都支持**: 默认 Freemium, BYOK 高级用户 |
| Q12 | AI 提示词模板 | 是否开源 | **Sprint 0 内部**, Sprint 1 评估开源 (差异化策略) |
| Q13 | 内容审核 | fiction-aware 审核 | Sprint 0 仅做关键词黑名单, Sprint 1 接 Moderation API |
| Q14 | 版权合规 | AI 披露 | UI 显式标注"本节由 AI 辅助生成,可继续编辑" |
| Q15 | AI 厂商密钥管理 | 系统密钥 vs 用户 BYOK | **双轨**: 系统密钥共享池 + 用户 BYOK 高级档 |

### 12.3 风险登记 (RAG)

| 风险 | 等级 | 缓解 |
|------|------|------|
| 复刻 17 模块工时超 36 人月 | 高 | Sprint 0/1 只做 P0, P3 模块后置 |
| LLM 一致性问题无完美解 | 高 | 五层架构 + 人工审阅兜底 |
| 12 厂商 API 变更 | 中 | 抽象 + 监控 + 快速切换 |
| AI 成本失控 | 中 | 配额 + 模型路由 (80% 中端) + BYOK |
| 阅文竞争 | 高 | 瞄准独立作者 + 海外, 不正面竞争 |
| 版权争议 (Bartz v. Anthropic) | 中 | 提示用户披露 + 模型训练数据合规审查 |
| 蒸馏任务积压 | 中 | BullMQ 监控 + 自动扩容 worker |
| 上下文窗口溢出 (Lost in Middle) | 中 | 三层架构 + 严格 token 预算 |
| 角色"人格漂移" | 中 | 角色卡持续注入 + DDPO 后期训练 |
| 已死角色复活 | 中 | 状态机 + 死亡时强校验 |
| 风格扁平化 | 中 | 风格指纹 + 多模型采样 |
| 用户增长 (DAU/MAU 14%) | 中 | 强 onboarding (3 步引导) |

---

## 13. 关键决策记录(ADR 雏形)

### ADR-0001: Modular Monolith (非 Microservices)

| 字段 | 内容 |
|------|------|
| **决策** | Sprint 0-2 采用 NestJS Modular Monolith,按业务模块切分;`ai-orchestrator` 可独立部署 |
| **备选** | (a) 全 Microservices (b) 纯 Monolith |
| **理由** | 230+ 端点强耦合,3-5 人团队微服务运维过重;模块化便于未来拆分 |
| **影响** | 部署简单,跨模块事务易实现;但单进程故障域大,需监控 + 自动重启 |

### ADR-0002: 前端 Pinia Store 按 17 模块 1:1 拆分

| 字段 | 内容 |
|------|------|
| **决策** | 每个世界模块独立 Pinia store,17 个 world/ + 核心 (auth/project/chapter/...) |
| **备选** | (a) 单一 Root Store (b) Redux Toolkit |
| **理由** | 与 API 1:1 对应,易于维护,Vue 3 官方推荐 |
| **影响** | 跨模块共享需要 composables;代码组织清晰 |

### ADR-0003: PostgreSQL + JSONB 存储世界模块

| 字段 | 内容 |
|------|------|
| **决策** | 主库 PG,世界模块的复杂嵌套用 JSONB;关系数据用关系表 |
| **备选** | (a) MySQL (b) MongoDB (c) 纯 JSON 文件 |
| **理由** | PG 兼具关系 + JSON 灵活度,事务/索引成熟,JSONB 性能优 |
| **影响** | 复杂查询需 `jsonb_path_ops` 索引;团队需熟悉 JSONB |

### ADR-0004: 12 厂商 AI 网关 + BYOK 双轨

| 字段 | 内容 |
|------|------|
| **决策** | 默认 Freemium(系统密钥池) + Pro/付费用户可 BYOK 接入自选模型 |
| **备选** | (a) 仅 BYOK (b) 仅单厂商 (c) 仅系统密钥 |
| **理由** | 平衡成本/灵活性;NovelCrafter BYOK 成功,云笔 Freemium 成功;两者结合最大覆盖 |
| **影响** | 网关抽象复杂度高;需 BYOK 加密存储 (AES-256) |

### ADR-0005: 蒸馏机制 Generator → Extractor → Checker

| 字段 | 内容 |
|------|------|
| **决策** | 章节完成后自动三阶段蒸馏,后审计由 Claude/Gemini 1M 模型兜底 |
| **备选** | (a) 单纯摘要 (b) MemGPT 风格 (c) 人工蒸馏 |
| **理由** | 三阶段既控制成本又保一致性;ConStory-Bench 证明纯 LLM 50-100% 漏洞需后审计 |
| **影响** | 后审计 1M 模型成本高,仅每 5 章或手动触发 |

### ADR-0006: Freemium 配额 (5,000 / 100,000 字/天)

| 字段 | 内容 |
|------|------|
| **决策** | 复刻原版配额:免费 5000 字/天,专业 100000 字/天 |
| **备选** | (a) 改用"次数" (b) 提高免费 (c) 降低免费 |
| **理由** | 1:1 复刻,后续再差异化(如提高免费层) |
| **影响** | 大量用户因价格敏感流失(Reddit 500 投诉);Pro 转化率需监控 |

### ADR-0007: Vue 3 + TipTap + Pinia + Tailwind 技术栈

| 字段 | 内容 |
|------|------|
| **决策** | 与云笔原版一致:Vue 3 SPA + TipTap (ProseMirror) + Pinia + Tailwind + 自研 UI |
| **备选** | (a) React + Slate (b) Svelte (c) 第三方 UI 库 (Element Plus) |
| **理由** | 1:1 复刻降低 UI 偏差;Vue 3 中文社区成熟;TipTap 已被验证 |
| **影响** | 与原版外观/交互高度一致;React 生态红利不可用 |

### ADR-0008: TipTap vs TinyMCE (编辑器)

| 字段 | 内容 |
|------|------|
| **决策** | **TipTap** (ProseMirror 包装) |
| **备选** | (a) TinyMCE (b) Lexical (c) Slate (d) Quill |
| **理由** | ProseMirror 生态强,自定义 Mark(角色/地名/伏笔)易扩展,Vue 3 集成好 |
| **影响** | 学习曲线中等;自动保存 + 协同编辑需自研 |

### ADR-0009: pgvector 用于 RAG (而非 Qdrant)

| 字段 | 内容 |
|------|------|
| **决策** | Sprint 0 用 PG + pgvector 单库,向量维度 1536 (OpenAI) 或 1024 (BGE) |
| **备选** | (a) Qdrant (b) Milvus (c) Weaviate |
| **理由** | 单库运维简单,事务一致;Sprint 3+ 视规模决定是否独立 |
| **影响** | 千万级向量后性能下降;需监控 + 必要时迁移 |

### ADR-0010: 三层上下文架构 (L1 工作 + L2 会话 + L3 归档)

| 字段 | 内容 |
|------|------|
| **决策** | 三层: L1 (3-8K 工作记忆 in-mem) + L2 (RAG top-k=2-5 in PG+pgvector) + L3 (全文/摘要 in S3) |
| **备选** | (a) 全部塞 prompt (b) MemGPT 风格 (c) LongStory CWC |
| **理由** | 行业共识三层架构,平衡成本/质量/实现复杂度 |
| **影响** | 上下文组装代码需精心设计;token 预算严格 8000 上限 |

### ADR-0011: BullMQ (Redis) 异步任务队列

| 字段 | 内容 |
|------|------|
| **决策** | 蒸馏/导入/导出/AI 落库用 BullMQ (Redis-backed) |
| **备选** | (a) Celery (Python) (b) Sidekiq (Ruby) (c) AWS SQS |
| **理由** | Node 生态原生,Redis 已在架构中,UI 友好,支持 cron |
| **影响** | 单点 Redis 故障需监控 + Sentinel/Cluster |

### ADR-0012: SSE 优先 (WebSocket 仅通知)

| 字段 | 内容 |
|------|------|
| **决策** | AI 流式输出 SSE;伏笔提醒/通知用 SSE + Redis PubSub;**不引入 WebSocket** |
| **备选** | (a) WebSocket (b) 短轮询 (c) gRPC streaming |
| **理由** | 与原版一致,SSE 单向足够,代理友好(Nginx 简单);WebSocket 复杂度高 |
| **影响** | 服务端需支持 SSE 心跳(防代理超时);客户端 EventSource 单向限制可接受 |

### ADR-0013: 字段中文化保留 (DB 列名 = API JSON key)

| 字段 | 内容 |
|------|------|
| **决策** | DB 列名 = API JSON key = 中文(项目名称, 关联大纲节点ID, 蒸馏状态 ...)+ 英文(id, createdAt) |
| **备选** | (a) 全英文 + i18n 转换层 (b) 中文 column + 英文 alias (c) 全中文 (前端 i18n 用 alias) |
| **理由** | 1:1 复刻,简化契约;不增加 alias 复杂度 |
| **影响** | ORM schema 需支持中文列名(Prisma 支持,Drizzle 需注意);DBA 需适应 |

### ADR-0014: Docker Compose (Sprint 0) → K8s (生产)

| 字段 | 内容 |
|------|------|
| **决策** | Sprint 0-1 用 docker-compose.yml (PG+Redis+MinIO+API+FE);生产切 K8s |
| **备选** | (a) 一开始 K8s (b) 永远 Compose (c) AWS ECS |
| **理由** | 开发体验 Compose 最佳;生产 K8s 标准;渐进式 |
| **影响** | 配置两份;CI 需支持双模式 |

### ADR-0015: 内容安全策略 (fiction-aware)

| 字段 | 内容 |
|------|------|
| **决策** | Sprint 0 仅做敏感词黑名单;Sprint 1 接 Moderation API;fictional context 白名单 |
| **备选** | (a) 无审核 (NovelAI 模式) (b) 严格审核 |
| **理由** | 反派行为不能等同真实有害;过度审核破坏创作;平台法律风险中等 |
| **影响** | 用户体验好,但部分内容风险自担(需用户协议明确) |

### ADR-0016: 移动端策略 (P3)

| 字段 | 内容 |
|------|------|
| **决策** | Sprint 0 仅做 PC 响应式(`>1024px` 三栏);移动端 P3 (浮动 AI 按钮 + 底部抽屉) |
| **备选** | (a) 移动优先重构 (b) 仅 PC |
| **理由** | 三栏不适配小屏,但 PC 是核心场景;移动端差异化竞争点 |
| **影响** | 移动端用户短期体验一般;P3 重构可能需重写布局 |

---

## 附录 A: 知识库引用索引

主控 spec 全部引自 knowlage/wiki/:

- **Overview**: `wiki/overview/产品全景.md`, `wiki/overview/技术选型.md`
- **API 端点**: `wiki/sources/API认证与架构.md`, `wiki/sources/API端点清单-核心模块.md`, `wiki/sources/API端点清单-世界设定与叙事.md`, `wiki/sources/API端点清单-辅助与管理.md`
- **API 响应(权威字段名)**: `wiki/sources/API响应-*.md` (12 个)
- **AI**: `wiki/sources/AI生成模式与蒸馏机制.md`, `wiki/sources/AI模型与长文本技术.md`, `wiki/sources/API响应-AI模块详情.md`
- **UI**: `wiki/sources/编辑器UI架构.md`, `wiki/sources/项目管理页与主题系统.md`
- **世界 17 模块**: `wiki/sources/2026-06-03 World Tab MASTER REFERENCE.md` + A1-A5 + 17 个 *Tab*.md
- **冲突裁决**: `wiki/sources/_conflicts/2026-06-03 冲突清单.md` (11 条事实点)
- **复刻/成本**: `wiki/sources/复刻指南与成本估算.md`, `wiki/sources/风险评估与实施路线.md`
- **市场**: `wiki/sources/AI小说市场格局.md`, `wiki/sources/落地页与市场定位.md`
- **产品**: `wiki/sources/产品概述.md`, `wiki/entities/云笔AI小说写作助手.md`

## 附录 B: 核心数字 (从 knowlage 提取,主控记录)

| 指标 | 数值 |
|------|------|
| 创作者 | 100 万+ |
| 累计生成 | 5000 万+ 字 |
| API 端点 | 230+ |
| 世界设定模块 | 17 (C01 裁决) |
| AI 厂商 | 12 (deepseek/doubao/qwen/wenxin/kimi/glm/gemini/gpt/nvidia/siliconflow/openrouter/oneapi) + 1 (custom) |
| 角色类型 | 24 (C03 裁决) |
| 伏笔 | 6 类型 + 10 埋设模式 (C05 裁决) |
| 势力 | 9 (C09 裁决) |
| 物品 | 86 (A2 实证) |
| 大纲节点 | 674 (C08 实证) |
| 大纲 AI 模式 | 3 (C06 裁决) |
| 章节导入 timeout | 120s |
| 心跳 | 30s |
| Token 有效期 | 604800s (7 天) |
| 免费配额 | 5000 字/天 |
| 专业配额 | 100000 字/天 |
| JWT 算法 | HS256 |
| 默认 max_tokens | 8192 |
| 默认 temperature | 0.85 (deepseek), 0.80 (doubao/kimi) |
| Top P | 0.80-0.92 |
| Freq Penalty | 0.35-0.50 |
| Pres Penalty | 0.25-0.40 |
| 思考 budget_tokens | 32768 |
| SSE 内容类型 | text/event-stream |
| 蒸馏 5 字段 | 蒸馏状态/蒸馏失败原因/蒸馏模型/蒸馏完成时间/正文快照哈希 |
| 三重冗余 | 内容/正文/content |
| 真实项目 ID | 6310 (烬都奇谭), 9657 (玄穹开) |
| 管理员阈值 | 最高角色等级 >= 80 |
| 字符 token 比例 | 10 万字 ≈ 13-15 万 token |
| 有效上下文 | 标称 10-20% (Chroma 研究) |
| 章节字数范围 | 2,285-5,408 字 (实测) |
| LLM 故事漏洞 | 比人类多 50-100% (ConStory-Bench) |
| LongStory 完整度提升 | 3.9 → 31.76 (CWC) |
| Multi-turn PPO 一致性降低 | 55%+ |

---

> **本规格说明书 v1.0 完结**。后续将基于 Sprint 0 反馈迭代 v1.1,并在 Phase 2 (世界观) / Phase 3 (叙事) / Phase 4 (高级) 启动时扩充对应子模块的详细契约。
