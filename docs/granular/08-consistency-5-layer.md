# 08 · 跨模块一致性五层架构 (主控权威)

> 来源: `docs/MASTER-PROJECT-SPEC.md` §9
> 五层架构 + 跨模块一致性 + 设定变更传播

## 1. 五层一致性架构

主控将"长篇小说一致性"问题拆为五层, 逐层处理:

| 层 | 名称 | 问题 | 主控方案 |
|----|------|------|----------|
| **L1** | **设定层** | 世界观/力量体系/势力/角色 是否自洽? | `contracts/schemas/world-setting/*.json` JSON Schema 强约束 |
| **L2** | **结构层** | 大纲/卷/章/场景 是否完整? | outline 自引用树 + `关联章节ID` 强约束 |
| **L3** | **时间层** | 事件时间线是否合理? | timeline 三表 (calendar/event/chapter_time) + `validate` API |
| **L4** | **关系层** | 角色-角色 / 角色-势力 / 角色-伏笔 是否自洽? | character_relations / faction_relations / foreshadow_echoes |
| **L5** | **蒸馏层** | 章节正文与结构/时间/关系是否一致? | 3 阶段蒸馏 (Generator → Extractor → Checker) |

## 2. 跨模块联动矩阵

| 从 → 到 | 触发 | 主控动作 |
|---------|------|----------|
| #1 世界观 → 所有引用 | 修改/删除 | 广播 `worldview.changed` 事件, 所有引用它的伏笔/角色/章节 UI 标红 |
| #7 力量体系 → #11 角色 | 境界变更 | 角色 `当前境界ID` 强制同步, 战力系数重新计算 |
| #7 力量体系 → 章节 | 上下文组装 | AI prompt 的 Layer 2 加入最新境界定义 |
| #11 角色 → #12 关系图 | 增删角色 | 关系图自动更新, 孤立节点标灰 |
| #13 伏笔 → #11 角色 | 增删 | 伏笔 `埋设章节ID` / `回收章节ID` 必须指向已存在章节 |
| #13 伏笔 → #10 大纲 | 增删 | 大纲编辑时显示"此大纲关联 X 个伏笔" |
| #10 大纲 → 章节 | 蒸馏完成 | 章节 `关联大纲节点ID` 自动设置 |
| #16 时间线 → #17 已经历事件 | 蒸馏完成 | 蒸馏摘要自动写入 `timeline_events` |
| #4 势力 → #11 角色 | 成员变更 | 势力的 `核心人物` 字段同步 |
| #6 物品 → #11 角色 | 持有物品 | `character_items` 子表 |

## 3. 设定变更传播规则

主控采用 **EventBus (Redis Pub/Sub)** 广播设定变更:

```typescript
// contracts/events/consistency-events.ts
type ConsistencyEvent =
  | { type: 'worldview.changed', projectId, worldviewId, fields: string[] }
  | { type: 'powersystem.realm.changed', projectId, systemId, realmId, oldValue, newValue }
  | { type: 'character.added', projectId, characterId }
  | { type: 'character.removed', projectId, characterId, replacementId? }
  | { type: 'foreshadow.added', projectId, foreshadowId, chapterId, type, mode }
  | { type: 'foreshadow.recycled', projectId, foreshadowId, chapterId }
  | { type: 'outline.distilled', projectId, outlineId, chapterId }
  | { type: 'timeline.event.added', projectId, eventId, calendarDate, type }
  | { type: 'faction.member.changed', projectId, factionId, characterIds }
  | { type: 'character.item.added', projectId, characterId, itemId }
```

**消费方**:
- `ai-orchestrator` → 失效相关 AI prompt 缓存, 重新组装上下文
- `backend` → 同步聚合字段 (项目总字数/章节数/角色数)
- `frontend` → 实时推送 UI 更新 (SSE)

## 4. 定期自检任务 (Cron)

主控在 `backend` 启动后注册 cron 任务:

| Cron | 任务 | 频率 |
|------|------|------|
| `0 3 * * *` | 跨项目时间线校验 (L3) | 每日 3:00 |
| `0 4 * * *` | 伏笔状态扫描 (过期未回收) | 每日 4:00 |
| `0 5 * * *` | 角色 ↔ 章节 出场一致性 (L4) | 每日 5:00 |
| `0 6 * * *` | 力量体系 ↔ 角色境界校验 (L1) | 每日 6:00 |
| `*/30 * * * *` | 蒸馏队列消费 (L5) | 每 30 分钟 |

## 5. 一致性违规处理

检测到的违规, 按严重度分三级:

| 级别 | 示例 | 处理 |
|------|------|------|
| **错误 (Error)** | 伏笔回收章节不存在 | 自动修复 + 通知用户 |
| **警告 (Warning)** | 角色在已死章节再次出场 | 标红 + 询问用户 |
| **提示 (Info)** | 时间线跨度超过自定义历法一年 | 仅显示 |

## 6. knowledge-graph/ 子项目 (主控维护)

```
knowledge-graph/
├── README.md                      # 子项目说明
├── consistency_rules.md           # 5 层规则文档
├── src/
│   ├── nodes/                     # 节点类型 (10 种: worldview, character, ...)
│   ├── edges/                     # 边类型 (8 种: 设定-引用, 角色-出场, ...)
│   ├── propagator/                # 设定变更传播器
│   └── validator/                 # 校验器
└── tests/
```

技术栈: PostgreSQL + JSONB + pgvector (语义相似度检索)

## 7. 主控 vs knowledge-graph 子项目边界

| 职责 | 主控 | knowledge-graph/ |
|------|------|-----------------|
| 定义一致性规则 | ✅ | — |
| 实现校验器 | — | ✅ |
| 维护事件总线 | ✅ | — |
| 持久化知识图谱 | — | ✅ |
| 跨子项目协调 | ✅ | — |

---

*最后更新: 2026-06-07 · 主控 v1.0*
