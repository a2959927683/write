# 0016 · 章节三重冗余: 内容 / 正文 / content (与云笔 API 兼容)

## 状态
已采纳 · 2026-06-07

## 背景
云笔真实 API 在不同接口返回不同字段名存储**相同内容**:
- 列表接口: `内容`
- 详情接口: `正文` (有时也叫 `content`)

这是云笔的早期遗留, 没有规范化。主控需要决定: 沿用三重冗余, 还是规范化?

## 决策
**主控采用三重冗余作为短期兼容方案, 长期废弃**。

## 三重冗余的字段

```sql
CREATE TABLE chapters (
  id BIGSERIAL PRIMARY KEY,
  "内容" TEXT,    -- 列表接口用
  "正文" TEXT,    -- 详情接口用
  "content" TEXT, -- 英文键名 (前端代码可能用)
  ...
);
```

## 写入策略

```python
# backend/src/modules/chapter/chapter.service.ts
async update_chapter(id, dto):
  # 三重写入
  await db.chapters.update({
    where: { id },
    data: {
      "内容": dto.内容,
      "正文": dto.内容,  # 同步
      "content": dto.内容, # 同步
      "正文快照哈希": hash_short(dto.内容),  # 变更检测
    }
  })
```

## 读取策略

```python
async get_chapter_detail(id):
  chapter = await db.chapters.find_unique({where: {id}})
  # 统一返回 正文 字段
  return {
    ...chapter,
    "正文": chapter.正文 or chapter.内容 or chapter.content,
  }
```

## 废弃路径 (Sprint 2+)

| 阶段 | 时间 | 动作 |
|------|------|------|
| **现在 (Sprint 0)** | 2026-06 | 三重写入, 读取统一用 `正文` |
| **Sprint 1** | 2026-07 | 前端代码 100% 使用 `正文` |
| **Sprint 2** | 2026-08 | 数据库触发器禁止 `内容` 写入 (只读) |
| **Sprint 3** | 2026-09 | 数据库迁移: 删除 `内容` 和 `content` 列 |
| **Sprint 4** | 2026-10 | 移除前端 `内容` / `content` 引用 |

## 变更检测

```python
# 利用 6 位短哈希, 避免每次 PUT 都触发蒸馏
正文快照哈希 = chapter.正文[:1000].encode('utf-8')
hash6 = hashlib.md5(正文快照哈希).hexdigest()[:6]

# 当 PUT 提交时
if dto.正文快照哈希 != hash6:
    # 内容实际变更, 触发蒸馏
    await distill_queue.enqueue(chapter_id)
```

## 影响
- `contracts/schemas/chapter.json` 标注 `x-three-fold-redundancy` 字段
- `backend` chapter service 三重写入
- 蒸馏触发基于 6 位哈希, 避免重复蒸馏
- 主控 `progress.txt` 跟踪废弃进度

## 后续
- 监控三重冗余字段的同步率 (应 100% 一致)
- Sprint 2 决定: 是否强制前端只用 `正文`
- 如果云笔 2026 年内规范化, 主控同步
