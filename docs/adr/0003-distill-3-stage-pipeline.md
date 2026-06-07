# 0003 · AI 蒸馏管线: 3 阶段 Generator → Extractor → Checker

## 状态
已采纳 · 2026-06-07

## 背景
云笔的"蒸馏机制"是基础 AI 摘要 (单阶段)。主控在 knowlage 知识库 `蒸馏机制.md` (authoritative) 中确认:
- **Generator**: 原始摘要
- **Extractor**: 结构化抽取
- **Checker**: 一致性校验

主控需要决定: 蒸馏是 1 阶段 (云笔) 还是 3 阶段 (knowlage 推荐)?

## 决策
**主控采用 3 阶段蒸馏管线**, 异步 BullMQ 任务, 章节保存后自动触发。

## 备选

### 备选 A: 1 阶段 (云笔原版)
- ✅ 简单, 1 个 LLM 调用
- ❌ 摘要质量不稳定
- ❌ 不会触发伏笔/角色一致性校验
- ❌ 无法支持跨章节事件抽取

### 备选 B (已采纳): 3 阶段 (Generator → Extractor → Checker)
- ✅ 摘要质量稳定 (低温度 Checker)
- ✅ 自动建议伏笔/角色/事件
- ✅ 跨模块一致性自动校验
- ❌ 3 个 LLM 调用, 成本约 3x
- ❌ 延迟较长 (但异步, 用户无感)

## 理由
1. knowlage 知识库 `蒸馏机制.md` 明确推荐 3 阶段
2. 3 阶段是 knowlage 作者认为云笔的关键改进点之一
3. 蒸馏是异步任务, 用户不会感知延迟
4. 成本增加可控 (DeepSeek 价格 $0.14/百万 tokens, 3 阶段约 $0.001/章)

## 实现

```python
# ai-orchestrator/orchestrator/distill_pipeline.py

class DistillPipeline:
    async def run(self, chapter_id: int):
        chapter = await self.get_chapter(chapter_id)

        # 阶段 1: Generator
        summary = await self.generator.generate(chapter.content)

        # 阶段 2: Extractor
        events = await self.extractor.extract(summary, context=chapter.context)

        # 阶段 3: Checker
        conflicts = await self.checker.check(events, knowledge_graph)

        # 写回
        await self.write_back(chapter_id, summary, events, conflicts)
```

## 失败处理
- 任一阶段失败 → 重试 3 次
- 仍失败 → chapter.蒸馏状态 = "失败" + chapter.蒸馏失败原因
- 用户可在 UI 手动 `/distill/reset-abnormal` 重置

## 影响
- `contracts/ai/distill-pipeline.ts` 定义 3 阶段契约
- `contracts/openapi/distill.yaml` (待写) 定义 5 个端点
- `backend` 需要 BullMQ 消费者
- `ai-orchestrator` 需要 3 个 provider 调用模板

## 后续
- 监控蒸馏成功率 (目标 > 95%)
- 如果 Checker 阶段产生大量误报, 调高温度
- 考虑加入"蒸馏历史" 视图 (用户回溯)
