# 04 · Sprint 0 主控初始化任务清单 (摘要)

> 来源: `docs/MASTER-PROJECT-SPEC.md` §11
> 完整 37 任务见 `feature_list.json`
> Sprint 0 目标: 跑通"登录 → 创建项目 → 编辑器 → AI 续写 (SSE)"主链

## 任务分组 (按子项目)

### master (主控本身)
- **S0-01** ✅ 初始化 monorepo 目录
- **S0-02** ✅ 编写主控 CLAUDE.md
- **S0-03** ✅ 编写 harness.config.json
- **S0-04** 编写 init.sh (跨平台)
- **S0-05** ✅ 编写 feature_list.json (37 任务)
- **S0-06** 初始化 progress.txt 详细化

### contracts (主控权威)
- **S0-07** ✅ OpenAPI auth.yaml (8 端点)
- **S0-08** ✅ OpenAPI project.yaml (8 端点)
- **S0-09** OpenAPI chapter.yaml (11 端点)
- **S0-10** OpenAPI outline.yaml (22 端点)
- **S0-11** ✅ OpenAPI ai.yaml + ai-stream.ts (8 端点 + 7 事件)
- **S0-12** ✅ 11 个 JSON Schema (project, chapter, outline, worldview, story-core, geo-map, faction, currency, item, power-system, skill-system, special-setting, character, foreshadow, plot-structure, event-line, timeline)
- **S0-13** ✅ AI providers.json (12 厂商)
- **S0-14** 模型路由规则 routing-rules.yaml

### infra
- **S0-15** docker-compose.yml (PG+Redis+MinIO+API+FE+AI)
- **S0-32** 集成测试 docker-compose
- **S0-33** Prometheus + Grafana
- **S0-37** CI 工作流 (GitHub Actions)

### backend
- **S0-16** NestJS/Fastify 骨架
- **S0-17** Prisma/Drizzle schema
- **S0-18** auth 模块
- **S0-19** project 模块
- **S0-20** chapter 模块 (三重冗余)
- **S0-21** outline 模块 (树形 22 端点)

### frontend
- **S0-22** Vue 3 + Vite + TipTap + Pinia + Tailwind 骨架
- **S0-23** 登录/注册页 + auth store
- **S0-24** 项目列表页 (4 卡片 + 网格 + 搜索 + 分页)
- **S0-25** 编辑器三栏布局 (250/auto/300)
- **S0-26** TipTap + 自动保存 (debounce 2s)
- **S0-27** 左侧项目 Tab 大纲树
- **S0-28** AI 助手面板 (6 按钮)

### ai-orchestrator
- **S0-29** AI 续写 SSE 流式渲染
- **S0-30** 接入 DeepSeek 验证

### tests
- **S0-31** E2E 冒烟: 登录 → 创建 → 编辑 → 续写

### docs
- **S0-34** 16 个 ADR
- **S0-35** system-overview.md

### scripts
- **S0-36** contract-lint.py (契约一致性检查)

## 依赖图 (关键路径)

```
S0-01 (主控目录)
  ├─ S0-02 (CLAUDE.md)
  │   └─ S0-03 (harness.config.json)
  │       └─ S0-05 (feature_list.json)
  │           └─ S0-06 (progress.txt)
  ├─ S0-04 (init.sh)
  │   └─ S0-15 (docker-compose)
  │       ├─ S0-16 (backend 骨架)
  │       │   └─ S0-17 (prisma schema)
  │       │       ├─ S0-18 (auth)
  │       │       ├─ S0-19 (project)
  │       │       └─ S0-20 (chapter) ─┐
  │       │           └─ S0-21 (outline)│
  │       └─ S0-22 (frontend 骨架)      │
  │           ├─ S0-23 (登录页)        │
  │           │   └─ S0-24 (项目列表)  │
  │           └─ S0-25 (三栏)         │
  │               ├─ S0-26 (TipTap) ───┘
  │               ├─ S0-27 (大纲树)
  │               └─ S0-28 (AI 面板)
  │                   └─ S0-29 (SSE)
  │                       └─ S0-30 (DeepSeek)
  │                           └─ S0-31 (E2E)
  │                               └─ S0-32 (集成)
  │                                   └─ S0-33 (监控)
  └─ S0-34 (16 ADR) ─┐
       S0-35 (overview)─┘
                    └─ S0-36 (contract-lint)
                        └─ S0-37 (CI)

S0-07..S0-14 (contracts) 是横向依赖, 不阻塞后端/前端实现, 但阻塞 S0-36 (lint)
```

## Sprint 0 验收

跑通以下完整链路:
1. 注册 → 登录 (S0-18 + S0-23)
2. 创建项目 (S0-19 + S0-24)
3. 进入编辑器 (S0-25)
4. 输入 100 字 → 自动保存 (S0-26)
5. 触发 AI 续写 200 字 (S0-29 + S0-30)
6. SSE 流式显示
7. 手动采纳插入 → 保存

## 工作量估算

- **6-8 人月** (2 前端 + 1 后端 + 1 AI 工程师, 4-6 周)
- 主控本身 (任务 S0-01..S0-14, S0-34..S0-37): **1 周**
- 基础设施 (S0-15, S0-32, S0-33): **1 周**
- 后端 (S0-16..S0-21): **1-2 周**
- 前端 (S0-22..S0-28): **2-3 周**
- AI 调度 (S0-29, S0-30): **1 周**
- E2E + CI (S0-31, S0-36, S0-37): **1 周**
