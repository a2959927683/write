# Sprint 1 · 17 模块完整 (占位文档)

> 🟡 **PLACEHOLDER · 占位中** — Sprint 0 完工后再细化
> 关联: [`docs/ROADMAP.md`](../ROADMAP.md)
> 触发条件: Sprint 0 验收通过 (M1 里程碑达成)

---

## 📊 元数据 (粗略)

| 字段 | 值 |
|------|---|
| **代号** | Sprint 1 · "17 模块完整" |
| **时间窗** | 2026-07 中 ~ 2026-08 末 (约 8 周) |
| **任务数 (估)** | ~80 |
| **工作量 (估)** | 12-15 人月 |
| **团队** | 6 人 (Sprint 0 + 1 知识图谱工程师) |
| **目标里程碑** | M2 · 17 模块齐备 (2026-08-31) |
| **状态** | ⚪ 未启动 |

---

## 🎯 目标 (一句话)

**17 块乐高积木全部能用 — 用户可以创建一个项目, 把 17 模块都填上 (角色/世界观/伏笔/...), AI 能基于这些写出一致的章节。**

---

## 🧱 4 大核心交付物 (待细化)

### ① 17 World Tab 后端 (60+ 端点)
- 17 个模块的 CRUD + /context + /generations 统一范式
- 详细工时拆解: 待 Sprint 0 末细化

### ② 17 World Tab 前端组件
- 共用 `ModuleDrawer.vue` 容器
- 17 个 `*Editor.vue` 组件
- 详细组件清单: 待 Sprint 0 末细化

### ③ 3 阶段蒸馏管线 (BullMQ)
- Generator → Extractor → Checker
- 章节完成自动触发
- 详细实现: 待 Sprint 0 末细化

### ④ 知识图谱启动 + 第 2-5 个 AI 厂商
- 伏笔追踪 + 一致性校验
- Claude / GPT / 智谱 / 通义 接入
- 详细拆解: 待 Sprint 0 末细化

---

## 🚧 待办 (Sprint 0 末细化)

- [ ] 拆解 17 模块的端点工时 (每模块 4-6 端点)
- [ ] 拆解 17 模块的前端组件复杂度 (简单/中等/复杂)
- [ ] 蒸馏管线的 BullMQ 任务设计
- [ ] 知识图谱的 schema 设计 (节点 + 边)
- [ ] 第 2-5 个 AI 厂商接入顺序
- [ ] 招聘知识图谱工程师 (Sprint 0 末必须到位)
- [ ] 细化 6 周排期
- [ ] 定义 Sprint 1 验收主链

---

## 📅 大致时间线 (粗估)

| 周 | 重点 |
|----|------|
| Week 1-2 | 17 World Tab 后端 (前 8 个模块: P0+P1) |
| Week 3-4 | 17 World Tab 后端 (后 9 个模块: P2) + 前端组件 |
| Week 5-6 | 蒸馏管线 + 知识图谱 |
| Week 7 | 第 2-5 个 AI 厂商接入 |
| Week 8 | E2E + 验收 + M2 里程碑 |

---

## ⚠️ 已知风险 (粗略)

- 17 模块工时可能超估 → 砍 P2 模块到 Sprint 2
- 蒸馏管线复杂度 → 先实现 Generator, Extractor/Checker 后置
- 知识图谱无现成实现 → pgvector + Neo4j 二选一(待定)

---

## 📚 关联

- 主控规格: `docs/MASTER-PROJECT-SPEC.md` §3.5 (17 模块数据模型)
- 颗粒化: `docs/granular/05-world-tab-17-modules.md`
- 冲突裁决: `docs/granular/07-conflict-adjudication.md` (C01-C11)
- 一致性: `docs/granular/08-consistency-5-layer.md`

---

## 🚫 当前不要做

**在 Sprint 0 未完工前**, **不要**细化本文档。否则:
- ❌ 浪费时间 (Sprint 0 末很多想法会变)
- ❌ 占用主控 context
- ❌ 子 agent 容易看错文档

**Sprint 0 完工后**, 主控负责把本文件改写为完整版 (像 sprint-0.md 那样)。

---

*占位 · 2026-06-07 · 等 M1 里程碑后细化*
