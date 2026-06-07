# 02 · master/ 目录结构 (主控布局)

> 来源: `docs/MASTER-PROJECT-SPEC.md` §10
> 最后更新: 2026-06-07

```
master/                                   # 工作目录根
├── README.md                             # 项目入口 (导航)
├── CLAUDE.md                             # 主控 Prompt (Claude Code 读)
├── harness.config.json                   # harness-l3-v4 配置
├── feature_list.json                     # feature 任务清单 (Sprint 0: 37 任务)
├── progress.txt                          # Sprint 进度日志
├── init.sh                               # 一键启动 (Windows + Linux/Mac)
├── .gitignore
├── docker-compose.yml                    # Sprint 0 全栈编排 (PG+Redis+MinIO+API+FE+AI)
├── docker-compose.dev.yml                # 开发环境 (挂载本地代码)
├── .env.example                          # 环境变量示例
│
├── contracts/                            # ★ 主控权威契约 (子项目必须遵守)
│   ├── README.md                         # 契约使用指南
│   ├── CHANGELOG.md                      # 契约变更日志 (主控裁决)
│   ├── openapi/
│   │   ├── root.yaml                     # 聚合入口 (待写)
│   │   ├── auth.yaml                     # ✅ 已写 (8 端点 + JWT + 心跳)
│   │   ├── project.yaml                  # ✅ 已写 (8 端点 + 配额)
│   │   ├── chapter.yaml                  # (待写, 11 端点)
│   │   ├── outline.yaml                  # (待写, 22 端点)
│   │   ├── character.yaml                # (待写, 24 端点)
│   │   ├── ai.yaml                       # ✅ 已写 (8 端点 + SSE 规范)
│   │   ├── distill.yaml                  # (待写, 5 端点)
│   │   ├── rules.yaml                    # (待写, 14 端点)
│   │   ├── stats.yaml                    # (待写, 5 端点)
│   │   ├── conversation.yaml             # (待写, 6 端点)
│   │   ├── tts.yaml                      # (待写, 4 端点)
│   │   ├── novel-build.yaml              # (待写, 14 端点 11 步)
│   │   ├── heartbeat.yaml                # (待写, 1 端点)
│   │   ├── admin.yaml                    # (待写, 50+ 端点)
│   │   └── world-tab/                    # 17 World Tab 模块契约
│   │       ├── worldview.yaml
│   │       ├── story-core.yaml
│   │       ├── geo-map.yaml
│   │       ├── faction.yaml
│   │       ├── currency.yaml
│   │       ├── item.yaml
│   │       ├── power-system.yaml
│   │       ├── skill-system.yaml
│   │       ├── special-setting.yaml
│   │       ├── outline-setting.yaml
│   │       ├── character-mgmt.yaml
│   │       ├── relationship.yaml
│   │       ├── foreshadow.yaml
│   │       ├── plot.yaml
│   │       ├── subplot.yaml
│   │       ├── timeline.yaml
│   │       └── event-line.yaml
│   ├── schemas/                          # JSON Schema (TS/Python 共享)
│   │   ├── project.json                  # ✅
│   │   ├── chapter.json                  # ✅
│   │   ├── outline.json                  # ✅
│   │   ├── character.json                # ✅ (在 world-setting/)
│   │   ├── user.json                     # (待写)
│   │   ├── ai-generation.json            # (待写)
│   │   ├── conversation.json             # (待写)
│   │   └── world-setting/
│   │       ├── worldview.json            # ✅
│   │       ├── story-core.json           # ✅
│   │       ├── geo-map.json              # ✅
│   │       ├── faction.json              # ✅
│   │       ├── currency.json             # ✅
│   │       ├── item.json                 # ✅
│   │       ├── power-system.json         # ✅
│   │       ├── skill-system.json         # ✅
│   │       ├── special-setting.json      # ✅
│   │       ├── character.json            # ✅
│   │       ├── foreshadow.json           # ✅
│   │       ├── plot-structure.json       # ✅
│   │       ├── event-line.json           # ✅
│   │       └── timeline.json             # ✅
│   ├── events/                           # 事件契约 (TS 类型)
│   │   ├── ai-stream.ts                  # ✅ SSE 7 事件类型
│   │   ├── distill-events.ts             # (待写)
│   │   ├── foreshadow-events.ts          # (待写)
│   │   └── consistency-events.ts         # (待写, 跨模块一致性)
│   ├── ai/                               # AI 调度契约
│   │   ├── providers.json                # ✅ 12 厂商注册表
│   │   ├── routing-rules.yaml            # (待写, 8 任务类型路由)
│   │   ├── context-schema.json           # (待写, 3 层上下文)
│   │   ├── distill-pipeline.ts           # (待写, 3 阶段契约)
│   │   ├── thinking-modes.yaml           # (待写)
│   │   ├── quota-rules.yaml              # (待写, 5000字/天 free, 100000字/天 pro)
│   │   └── local-proxy-schema.json       # (待写)
│   └── frontend/                         # 前端契约
│       ├── routes.ts                     # (待写, 路由表)
│       ├── world-tabs.ts                 # (待写, 17 模块清单)
│       ├── themes.ts                     # (待写, 15 主题)
│       ├── sse-events.ts                 # (待写, re-export ai-stream.ts)
│       └── editor-events.ts              # (待写, TipTap 事件)
│
├── backend/                              # 后端子项目 (Node.js + Fastify/NestJS) (待初始化)
│   ├── package.json
│   ├── tsconfig.json
│   ├── nest-cli.json
│   ├── prisma/
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
│   └── test/
│
├── frontend/                             # 前端子项目 (Vue 3 + Vite) (待初始化)
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── src/
│   │   ├── main.ts
│   │   ├── App.vue
│   │   ├── router/
│   │   ├── stores/                       # Pinia (按 17 模块 + auth + project + ...)
│   │   ├── pages/
│   │   ├── components/
│   │   │   ├── editor/                   # TipTap
│   │   │   ├── world-tab/                # 17 模块组件
│   │   │   ├── ai/
│   │   │   └── layout/
│   │   └── composables/
│   └── public/
│
├── ai-orchestrator/                      # AI 调度子项目 (Python + FastAPI) (待初始化)
│   ├── pyproject.toml
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/
│   │   │   ├── ai_chat.py                # /ai/chat/*
│   │   │   ├── ai_stream.py              # SSE
│   │   │   └── ai_admin.py
│   │   ├── providers/                    # 12 厂商适配器
│   │   │   ├── base.py
│   │   │   ├── deepseek.py
│   │   │   ├── anthropic.py
│   │   │   ├── openai.py
│   │   │   └── ... (9 more)
│   │   ├── orchestrator/
│   │   │   ├── router.py                 # 模型路由
│   │   │   ├── context_builder.py        # 3 层上下文组装
│   │   │   ├── distill_pipeline.py       # 3 阶段蒸馏
│   │   │   ├── quota.py                  # 配额
│   │   │   └── stream_gateway.py         # SSE 网关
│   │   └── schemas/                      # Pydantic (复用 contracts/schemas/)
│   └── tests/
│
├── knowledge-graph/                      # 知识图谱 (伏笔-角色-情节-时间线 一致性) (待初始化)
│   ├── README.md
│   ├── consistency_rules.md              # 强一致性规则
│   ├── src/
│   │   ├── nodes/                        # 节点类型
│   │   ├── edges/                        # 边类型
│   │   ├── propagator/                   # 设定变更传播
│   │   └── validator/                    # 校验器
│   └── tests/
│
├── infra/                                # 基础设施 (Docker / K8s / CI / 监控) (待初始化)
│   ├── docker/
│   │   ├── Dockerfile.backend
│   │   ├── Dockerfile.frontend
│   │   └── Dockerfile.ai-orchestrator
│   ├── k8s/                              # (生产期)
│   ├── monitoring/
│   │   ├── prometheus.yml
│   │   └── grafana/
│   └── ci/
│       └── github-actions.yml
│
├── tests/                                # 集成/E2E 测试 (待初始化)
│   ├── e2e/
│   │   ├── smoke.spec.ts
│   │   └── playwright.config.ts
│   └── integration/
│
├── docs/                                 # 主控权威文档
│   ├── MASTER-PROJECT-SPEC.md            # ✅ 完整规格 (1825 行)
│   ├── adr/                              # 架构决策记录 (待写 16 个)
│   ├── architecture/                     # 系统架构图 / 数据流
│   └── granular/                         # ✅ 颗粒化文档 (按主题拆分)
│
├── features/                             # 单 feature PRD 与设计稿 (Sprint 1+ 启动)
│   └── .gitkeep
│
├── progress/                             # Sprint / 复盘 / 决策日志 (Sprint 1+ 启动)
│   └── .gitkeep
│
├── scripts/                              # 工具脚本
│   └── contract-lint.py                  # (S0-36 待写)
│
└── .claude/                              # Claude Code 技能与命令
    ├── settings.json
    └── commands/
```

## 关键统计

- 已初始化文件: 25+ (主控核心 + 11 schemas + 3 OpenAPI + providers + ai-stream + 5 个文档)
- 待初始化文件: ~50 (子项目源码 + Docker + 监控 + 16 ADR)
- Sprint 0 进度: 9/37 (24%)
