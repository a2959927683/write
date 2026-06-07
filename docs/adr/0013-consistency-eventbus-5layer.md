# 0013 · 跨模块一致性: EventBus + 5 层校验

## 状态
已采纳 · 2026-06-07

## 背景
长篇小说一致性是云笔的核心痛点之一 (主控也认为这是关键差异化)。
主控需要决定: 如何实现跨模块一致性?

## 决策
**主控采用 EventBus (Redis Pub/Sub) + 5 层校验 + Cron 任务**。

## 5 层架构

| 层 | 名称 | 实现 |
|----|------|------|
| **L1 设定层** | JSON Schema 强约束 | `contracts/schemas/world-setting/*.json` |
| **L2 结构层** | outline 自引用树 + `关联章节ID` 强约束 | PostgreSQL FK + 应用层校验 |
| **L3 时间层** | timeline 三表 + `validate` API | `GET /timeline/validate/:projectId` |
| **L4 关系层** | character_relations / faction_relations / foreshadow_echoes | PostgreSQL FK + EventBus |
| **L5 蒸馏层** | 3 阶段蒸馏 (Generator → Extractor → Checker) | BullMQ 异步任务 |

## EventBus 设计

```typescript
// contracts/events/consistency-events.ts
type ConsistencyEvent =
  | { type: 'worldview.changed', projectId, worldviewId, fields }
  | { type: 'powersystem.realm.changed', projectId, systemId, realmId, oldValue, newValue }
  | { type: 'character.added', projectId, characterId }
  | { type: 'character.removed', projectId, characterId }
  | { type: 'foreshadow.added', projectId, foreshadowId, chapterId, type, mode }
  | { type: 'foreshadow.recycled', projectId, foreshadowId, chapterId }
  | { type: 'outline.distilled', projectId, outlineId, chapterId }
  | { type: 'timeline.event.added', projectId, eventId, calendarDate, type }
  | { type: 'faction.member.changed', projectId, factionId, characterIds }
  | { type: 'character.item.added', projectId, characterId, itemId }
```

```python
# backend/src/events/pubsub.py
import redis.asyncio as redis
import json

class EventBus:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)

    async def publish(self, channel: str, event: dict):
        await self.redis.publish(channel, json.dumps(event, default=str))

    async def subscribe(self, channel: str, handler):
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(channel)
        async for message in pubsub.listen():
            if message["type"] == "message":
                event = json.loads(message["data"])
                await handler(event)
```

## Cron 任务

```python
# backend/src/jobs/consistency_checks.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

@scheduler.scheduled_job('cron', hour=3)
async def check_timeline_consistency():
    """每日 3:00 跨项目时间线校验 (L3)"""
    projects = await db.projects.find_many()
    for p in projects:
        result = await validate_timeline(p.id)
        if result.errors:
            await notify_user(p.user_id, result)

@scheduler.scheduled_job('cron', hour=4)
async def check_foreshadow_expiry():
    """每日 4:00 伏笔过期扫描"""
    expired = await db.foreshadows.find_many(
        where={"状态": "已埋设", "createdAt": {"lt": datetime.now() - timedelta(days=180)}}
    )
    for f in expired:
        await notify_user(f.project.user_id, f"伏笔 {f.标题} 已埋设 180 天未回收")

@scheduler.scheduled_job('cron', hour=5)
async def check_character_appearances():
    """每日 5:00 角色 ↔ 章节 出场一致性 (L4)"""
    # 角色在已死章节再次出场 → 标红
    ...

@scheduler.scheduled_job('cron', hour=6)
async def check_power_system_realm():
    """每日 6:00 力量体系 ↔ 角色境界校验 (L1)"""
    ...
```

## 一致性违规分级

| 级别 | 处理 |
|------|------|
| **错误 (Error)** | 自动修复 + 通知用户 |
| **警告 (Warning)** | UI 标红 + 询问用户 |
| **提示 (Info)** | 仅显示 |

## knowledge-graph/ 子项目

主控的 `knowledge-graph/` 子项目负责:
- 持久化知识图谱 (PostgreSQL + JSONB + pgvector)
- 跨模块校验器实现
- 与主控 EventBus 集成

边界:
- 主控: 定义规则 + 维护事件总线
- knowledge-graph: 实现校验 + 持久化图谱

## 影响
- `backend` 需要引入 `ioredis` (Pub/Sub)
- `backend` 需要引入 `apscheduler` (Cron)
- `knowledge-graph/` 子项目需 Sprint 1 启动
- `ai-orchestrator` 订阅 worldview.changed 等事件, 失效相关 AI 缓存

## 后续
- 加入"一致性仪表盘" (用户主动查看)
- 加入"批量修复" (一键修复所有错误)
- pgvector 用于语义相似度检索 (找相似伏笔/角色)
