# 0014 · 数据库: PostgreSQL 16 + JSONB

## 状态
已采纳 · 2026-06-07

## 背景
主控需要选择 OLTP 数据库。两个候选:
- **PostgreSQL**: 强关系, JSONB 灵活
- **MongoDB**: 文档数据库

## 决策
**主控采用 PostgreSQL 16 + JSONB**。

## 理由
1. **17 World Tab 模块结构差异大**: JSONB 灵活, 同时保留关系查询能力
2. **强关系需求**: 用户/项目/章节/角色 是强关系, PostgreSQL FK 强约束
3. **全文搜索**: `tsvector` + `pg_trgm` 用于章节/伏笔搜索
4. **生态**: Prisma / Drizzle / TypeORM 支持好
5. **pgvector 扩展**: Sprint 1+ 语义相似度检索

## 表设计原则

| 字段类型 | 适用 | 例子 |
|----------|------|------|
| **强类型列** | 必填, 高频查询 | `id`, `user_id`, `项目名称`, `蒸馏状态` |
| **JSONB** | 结构差异大, 低频查询 | `境界列表`, `人生经历`, `ext` |
| **TEXT** | 长文本, 全文搜索 | `正文`, `内容`, `描述` |
| **TIMESTAMPTZ** | 时间 | `createdAt`, `updatedAt`, `蒸馏完成时间` |
| **JSONB[] 数组** | 多值 | `标签`, `情绪列表`, `伏笔列表` |

## 关键 JSONB 字段 (来自 `MASTER_PROJECT_SPEC.md` §3)

```sql
-- outlines.摘要核心
"摘要核心" TEXT  -- 简短, 不放 JSONB
"摘要" TEXT       -- Markdown 详细摘要

-- outlines.关键对话 / 人性细化 / 写作要点
"关键对话" TEXT
"人性细化" TEXT
"写作要点" TEXT

-- outlines.道具物品 / 势力阵营 / 情绪列表
"道具物品" JSONB DEFAULT '[]'  -- [{物品ID, 描述, 章节}]
"势力阵营" JSONB DEFAULT '[]'  -- [{势力ID, 关系, 章节}]
"情绪列表" JSONB DEFAULT '[]'  -- [{情绪, 强度, 章节}]
"伏笔列表" JSONB DEFAULT '[]'  -- [{伏笔ID, 描述}]
"节奏控制" JSONB DEFAULT '[]'
"视觉画面" JSONB DEFAULT '[]'
"声音氛围" JSONB DEFAULT '[]'

-- power_systems 4 层嵌套
"境界列表" JSONB  -- 11 项
"能力列表" JSONB  -- 6 项
"修行路径" JSONB  -- 4 项
"限制约束" JSONB  -- 5 项
```

## 索引策略

| 表 | 索引 | 理由 |
|----|------|------|
| `projects` | `(user_id)`, `(项目状态)` | 用户项目列表 + 状态筛选 |
| `chapters` | `(project_id)`, `(关联大纲节点ID)`, `(蒸馏状态)` | 项目章节 + 大纲关联 + 蒸馏队列 |
| `outlines` | `(project_id, 父节点ID)`, `(project_id, 排序顺序)` | 树形查询 + 排序 |
| `characters` | `(project_id)`, `(力量体系ID)`, `(当前境界ID)` | 角色列表 + 境界查询 |
| `foreshadows` | `(project_id)`, `(状态)`, `(重要度)` | 状态筛选 + 重要度排序 |
| `timeline_events` | `(project_id, 历法日期)`, `(章节ID)`, `(类型)` | 时间线查询 + 章节关联 |

## GIN 索引 (JSONB)

```sql
-- 角色标签搜索
CREATE INDEX idx_characters_性格 ON characters USING GIN (性格);

-- 大纲 JSONB 字段搜索
CREATE INDEX idx_outlines_伏笔 ON outlines USING GIN (伏笔列表);
```

## 全文搜索 (tsvector)

```sql
-- 章节全文搜索
ALTER TABLE chapters ADD COLUMN 搜索向量 tsvector
  GENERATED ALWAYS AS (
    setweight(to_tsvector('simple', coalesce(标题, '')), 'A') ||
    setweight(to_tsvector('simple', coalesce(正文, '')), 'B')
  ) STORED;

CREATE INDEX idx_chapters_搜索 ON chapters USING GIN (搜索向量);
```

## 分区 (Sprint 2+)

| 表 | 分区键 | 分区策略 |
|----|--------|----------|
| `chapters` | `(project_id)` HASH | 单项目 1000 章, 按项目分 16 区 |
| `timeline_events` | `时间戳` RANGE | 按月分区, 自动滚动 |

## 备份策略

- 每日全量备份 (`pg_dump`)
- 30 天保留
- 主从复制 (Sprint 3+)

## 影响
- `backend` 用 `Prisma` (Sprint 0 评估) 或 `Drizzle` (Sprint 1 候选)
- 所有 `contracts/schemas/*.json` 是 JSONB 的形态定义
- AI 上下文组装时, 复杂 JSONB 字段需要序列化为 Markdown (LLM 友好)

## 后续
- pgvector 启用 (Sprint 1)
- 物化视图 (Sprint 2, 加速统计)
- 数据归档 (Sprint 3, 旧章节冷存储)
