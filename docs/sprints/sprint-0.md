# Sprint 0 · 跑通主链

> **目标:** 跑通"注册 → 登录 → 创建项目 → 编辑器 → AI 续写(SSE) → 采纳保存"完整链路
> **关联:** [`docs/ROADMAP.md`](../ROADMAP.md) · [`feature_list.json`](../../feature_list.json) · [`progress.txt`](../../progress.txt)
> **可视化:** [`explain/13-整个项目执行规划-路线图.html`](../../explain/13-整个项目执行规划-路线图.html)

---

## 📊 Sprint 元数据

| 字段 | 值 |
|------|---|
| **代号** | Sprint 0 · "跑通主链" |
| **时间窗** | 2026-06-07 ~ 2026-07-19 (约 6 周) |
| **任务总数** | 37 |
| **当前进度** | 9/37 (24%) |
| **工作量** | 6-8 人月 |
| **团队规模** | 5 人 (1 主控 + 1 后端 + 2 前端 + 1 AI) |
| **状态** | 🟡 进行中 (主控阶段) |
| **下一里程碑** | M1 · 主链跑通 (2026-07-19) |

---

## 🎯 Sprint 0 目标 (验收主链 7 步)

```
1. 注册 → 2. 登录 → 3. 创建项目 → 4. 进编辑器 → 5. 写 100 字 → 6. AI 续写 → 7. SSE 流式显示 → 采纳保存
```

**验收命令:**
```bash
./init.sh dev          # 一键启动全栈
./init.sh e2e          # 跑 E2E 冒烟测试
# 主链 7 步全过 = Sprint 0 验收通过
```

---

## 🏗️ 5 阶段执行流程

### 🎨 阶段 1 · 主控画图纸 (进度 9/11 = 82%)

**目标:** 把所有"图纸"写好,后面所有人照着干。

| 任务 ID | 标题 | 子项目 | 产出物 | 状态 |
|---------|------|--------|--------|------|
| S0-01 | 初始化 monorepo 目录 | master | 目录骨架 | ✅ |
| S0-02 | 编写主控 CLAUDE.md | master | `CLAUDE.md` | ✅ |
| S0-03 | 编写 harness.config.json | master | `harness.config.json` | ✅ |
| S0-04 | 编写 init.sh (跨平台) | master | `init.sh` | ⏳ |
| S0-05 | 编写 feature_list.json (37 任务) | master | `feature_list.json` | ✅ |
| S0-06 | 初始化 progress.txt 详化 | master | `progress.txt` | ⏳ |
| S0-07 | OpenAPI auth.yaml (8 端点) | contracts | `auth.yaml` | ✅ |
| S0-08 | OpenAPI project.yaml (8 端点) | contracts | `project.yaml` | ✅ |
| S0-09 | OpenAPI chapter.yaml (11 端点) | contracts | `chapter.yaml` | ⏳ |
| S0-10 | OpenAPI outline.yaml (22 端点) | contracts | `outline.yaml` | ⏳ |
| S0-11 | OpenAPI ai.yaml + SSE | contracts | `ai.yaml + ai-stream.ts` | ✅ |
| S0-12 | 11 个 JSON Schema | contracts | `schemas/*.json` | ✅ |
| S0-13 | AI providers.json (12 厂商) | contracts | `providers.json` | ✅ |
| S0-14 | AI 路由规则 routing-rules.yaml | contracts | `routing-rules.yaml` | ⏳ |

---

### 🔧 阶段 2 · 搭建工地 (进度 0/2 = 0%)

**目标:** 装好开发环境, 所有人能一键启动。

| 任务 ID | 标题 | 子项目 | 产出物 | 状态 |
|---------|------|--------|--------|------|
| S0-15 | docker-compose.yml (PG+Redis+MinIO+API+FE+AI) | infra | `docker-compose.yml` | ⏳ |

**关键:** 一行 `./init.sh dev` 启动全部服务。

**包含服务:**
- PostgreSQL 16 (5432)
- Redis 7 (6379)
- MinIO (9000, 9001)
- Backend (Node.js, 3000)
- Frontend (Vite, 5173)
- AI Orchestrator (Python, 8000)
- Prometheus (9090) - 可选
- Grafana (3001) - 可选

---

### 🏛️ 阶段 3 · 后端打地基 (进度 0/6 = 0%)

**目标:** API 服务先跑起来。

| 任务 ID | 标题 | 子项目 | 产出物 | 状态 |
|---------|------|--------|--------|------|
| S0-16 | NestJS/Fastify 骨架 | backend | `backend/src/main.ts` | ⏳ |
| S0-17 | Prisma/Drizzle schema (users+projects+chapters) | backend | `prisma/schema.prisma` | ⏳ |
| S0-18 | auth 模块 (8 端点 + JWT + 心跳) | backend | `backend/src/modules/auth/` | ⏳ |
| S0-19 | project 模块 (8 端点 + 配额) | backend | `backend/src/modules/project/` | ⏳ |
| S0-20 | chapter 模块 (11 端点 + 三重冗余 + 自动保存) | backend | `backend/src/modules/chapter/` | ⏳ |
| S0-21 | outline 模块 (22 端点 + 树形 + 移动 + 重编号) | backend | `backend/src/modules/outline/` | ⏳ |

**验收:** `curl /api/auth/login` 能拿到 token。

---

### 🎨 阶段 4 · 前端 + AI 并行 (进度 0/9 = 0%)

**目标:** 前端 7 个页面 + AI 调度跑通 SSE 流式输出。

**前端线 (7 任务):**

| 任务 ID | 标题 | 产出物 | 状态 |
|---------|------|--------|------|
| S0-22 | Vue 3 + Vite + TipTap + Pinia + Tailwind 骨架 | `frontend/src/main.ts` | ⏳ |
| S0-23 | 登录/注册页 + auth store | `pages/Login.vue + stores/auth.ts` | ⏳ |
| S0-24 | 项目列表页 (4 卡片 + 网格 + 搜索 + 分页) | `pages/ProjectList.vue` | ⏳ |
| S0-25 | 编辑器三栏布局 (250/auto/300) | `components/editor/EditorLayout.vue` | ⏳ |
| S0-26 | TipTap + 自动保存 (debounce 2s) | `components/editor/TipTapEditor.vue` | ⏳ |
| S0-27 | 左侧项目 Tab 大纲树 | `components/editor/OutlineTree.vue` | ⏳ |
| S0-28 | AI 助手面板 (6 按钮) | `components/ai/AIPanel.vue` | ⏳ |

**AI 线 (2 任务):**

| 任务 ID | 标题 | 产出物 | 状态 |
|---------|------|--------|------|
| S0-29 | AI 续写 SSE 流式渲染 | `composables/useAIStream.ts + sse_gateway.py` | ⏳ |
| S0-30 | 接入 DeepSeek 验证 | `ai-orchestrator/provider_registry.py` | ⏳ |

---

### ✅ 阶段 5 · 验收 (进度 0/9 = 0%)

**目标:** 端到端跑通 + 监控就绪 + CI 上线。

| 任务 ID | 标题 | 产出物 | 状态 |
|---------|------|--------|------|
| S0-31 | E2E 冒烟: 登录→创建→编辑→续写 | `tests/e2e/smoke.spec.ts` | ⏳ |
| S0-32 | docker-compose.yml 集成测试 | `docker-compose.yml` | ⏳ |
| S0-33 | Prometheus + Grafana 监控 | `infra/monitoring/` | ⏳ |
| S0-34 | 16 个 ADR | `docs/adr/*.md` | ✅ (已超额 18/16) |
| S0-35 | docs/architecture/system-overview.md | `system-overview.md` | ✅ |
| S0-36 | scripts/contract-lint.py | `contract-lint.py` | ⏳ |
| S0-37 | CI 工作流 (GitHub Actions) | `.github/workflows/ci.yml` | ⏳ |

---

## 🔗 关键依赖路径

```
S0-15 (docker)
  ├─► S0-16 (后端骨架)
  │     └─► S0-17 (DB) ─► S0-18/19/20/21 (4 模块)
  │                              │
  └─► S0-22 (前端骨架)            │
        └─► S0-25 (三栏) ◄────────┘
              └─► S0-26/27/28
                    └─► S0-29 (SSE) ─► S0-30 (DeepSeek) ─► S0-31 (E2E)
```

**最关键节点:** S0-15 (Docker) → S0-17 (数据库 schema) → S0-29 (SSE)

---

## 👥 团队配置

| 角色 | 人数 | 时间 | 主要任务 |
|------|------|------|----------|
| 🎩 主控 | 1 | 全程 | 写契约 + 调度 + 仲裁 |
| ⚙️ 后端 | 1 | 4 周 | S0-16~21 (6 任务) |
| 🎨 前端 | 2 | 3 周 | S0-22~28 (7 任务) |
| 🧙 AI 工程师 | 1 | 2 周 | S0-29~30 (2 任务) |
| 🔧 运维 | 1 | 1 周 | S0-15, S0-32~33 (3 任务) |

---

## 📅 6 周排期 (建议)

### Week 1 (2026-06-07 ~ 06-13) · 主控冲刺
- 主控: 补齐 S0-04/09/10/14 (剩余图纸)
- 主控: 定稿 ADR 0017/0018
- 全员: 招聘 + 入职
- 运维: 准备开发环境

### Week 2 (06-14 ~ 06-20) · 工地搭建
- 运维: S0-15 Docker Compose
- 主控: 写第 1 批 7 个 brief (关键路径)
- 后端: 准备 S0-16

### Week 3 (06-21 ~ 06-27) · 地基浇筑
- 后端: S0-16 + S0-17 (骨架 + DB)
- 前端: S0-22 (Vue 骨架)
- 主控: 写第 2 批 brief

### Week 4 (06-28 ~ 07-04) · 业务模块
- 后端: S0-18 + S0-19 (auth + project)
- 前端: S0-23 + S0-24 (登录 + 列表)
- AI: 接 DeepSeek 试调

### Week 5 (07-05 ~ 07-11) · 主链接通
- 后端: S0-20 + S0-21 (chapter + outline)
- 前端: S0-25~28 (编辑器 + AI 面板)
- AI: S0-29 SSE

### Week 6 (07-12 ~ 07-19) · 验收冲刺
- 全员: S0-30 接通 DeepSeek
- 全员: S0-31 E2E 测试
- 主控: 复盘 + M1 里程碑庆祝

---

## ✅ Sprint 0 完工验收清单

跑通这条完整主链, Sprint 0 才算完成:

```
□ 注册 → 收到 token + user
□ 登录 → JWT 7 天有效
□ 30s 心跳 → 在线状态保活
□ 创建项目 → /projects → 跳转编辑器
□ 编辑器三栏布局 → 18%/50%/32%
□ 输入 100 字 → 2s 后自动保存 (PUT /chapters/:id)
□ 三重冗余字段同时写入 (内容/正文/content)
□ 点击 AI 续写 → POST /ai/chat/session → sessionId
□ GET /ai/chat/stream/:id (SSE) → 7 事件流
□ 流式打字效果显示 → 完整内容
□ 点击采纳插入 → 内容存入章节
□ 30s 后蒸馏任务自动触发
□ E2E 截图存档
```

---

## 🚨 Sprint 0 风险与缓解

| 风险 | 级别 | 缓解 |
|------|------|------|
| 团队招聘不到位 | 🔴 高 | 提前 2 周启动招聘, 优先填后端 + AI |
| DeepSeek API 变更 | 🟡 中 | 抽象层 + 监控 + 备用 OpenAI |
| TipTap 学习曲线 | 🟡 中 | 1 周技术调研 + 简化 MVP 功能 |
| Docker 在 Windows 兼容性 | 🟡 中 | init.sh 跨平台 + Git Bash 文档 |
| SSE 反向代理超时 | 🟢 低 | Nginx 配置 proxy_buffering off |

---

## 🎯 Sprint 0 后的下一步

完成 Sprint 0 后 (M1 里程碑达成), 立即:
1. 全员复盘 (1 天)
2. 启动 Sprint 1 (17 模块)
3. 招聘第 6 人 (知识图谱工程师)
4. 更新 `docs/sprints/sprint-1.md` 细化

---

*最后更新: 2026-06-07 · 主控 v1.0*
*下一次更新: 每周 + 任务完成时*
