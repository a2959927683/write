# 0005 · 数据模型字段名 1:1 还原中文

## 状态
已采纳 · 2026-06-07

## 背景
云笔 API 真实字段名是**中文** (如 `项目名称`, `关联大纲节点ID`, `蒸馏状态`)。主控需要决定:
- **保持中文字段名** (与云笔 API 一致)
- **改用英文字段名** (国际化友好)

## 决策
**主控采用中文字段名作为权威**, 英文仅作为 JSON Schema 的 `$id` 或别名。

## 备选

### 备选 A: 英文字段名
- ✅ 国际化友好
- ✅ 主流 ORM 友好 (Prisma, TypeORM)
- ❌ 与云笔 API 不一致, 需要双向转换
- ❌ 失去"中文字段 = 业务字段" 的可读性

### 备选 B (已采纳): 中文字段名 + 英文 alias
- ✅ 1:1 复刻, 无转换层
- ✅ 可读性强 (中文业务字段名即文档)
- ✅ JSON Schema 用英文 $id, Python/TypeScript 可 import
- ❌ 一些 ORM 不支持中文 (需要 workaround)
- ❌ 国际开发者可能不适应

## 已知 trade-off

| 问题 | 解决方案 |
|------|----------|
| Prisma schema 不支持中文 | 实际用 `snake_case` 物理列 + `map` 映射到中文 |
| TypeScript interface 字段是中文 | 用 `as const` 或定义映射类型 |
| PostgreSQL 列名是中文 | 用双引号包裹 `"项目名称"`, 或者物理列是英文, 应用层映射 |
| OpenAPI 工具链 (Swagger UI) | 完全支持, 直接显示中文 |

## 实现

PostgreSQL 表设计:
```sql
CREATE TABLE projects (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
  "项目名称" VARCHAR(128) NOT NULL,           -- 中文物理列 (用双引号)
  "项目类型" VARCHAR(32) NOT NULL,
  "项目状态" VARCHAR(16) NOT NULL DEFAULT '连载中',
  ...
);
```

Prisma schema (推荐物理列用 snake_case, 模型字段用中文):
```prisma
model Project {
  id        BigInt   @id @default(autoincrement())
  userId    BigInt   @map("user_id")
  项目名称  String   @map("project_name") @db.VarChar(128)
  项目类型  String   @map("project_type") @db.VarChar(32)
  ...
  @@map("projects")
}
```

## 影响
- 所有 `contracts/schemas/*.json` 用中文字段
- 所有 `contracts/openapi/*.yaml` 用中文字段
- `backend` Prisma schema 用 `@@map` 物理列 = 英文 snake_case
- `ai-orchestrator` Pydantic 模型用 Field(alias="中文名")

## 后续
- 考虑加入 `field_translations.yaml` 提供 i18n 支持
- 数据库迁移工具需要能处理中文物理列 (Prisma migrate 可以)
