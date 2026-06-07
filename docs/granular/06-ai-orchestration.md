# 06 · AI 调度契约 (主控权威)

> 来源: `docs/MASTER-PROJECT-SPEC.md` §6 + `knowlage/wiki/sources/API认证与架构.md` + `knowlage/wiki/sources/AI功能设计与交互.md`
> 12 厂商 + 8 任务路由 + 3 层上下文 + 3 阶段蒸馏

## 1. 12 厂商注册表 (主控权威)

> 完整 JSON 见 `contracts/ai/providers.json`

| Key | 厂商 | 默认 Base URL | 鉴权 | 默认模型 | 思考模式 |
|-----|------|--------------|------|----------|----------|
| `deepseek` | DeepSeek | `https://api.deepseek.com/v1` | Bearer | `deepseek-chat` | ✅ |
| `anthropic` | Anthropic Claude | `https://api.anthropic.com/v1` | `x-api-key` | `claude-opus-4-8` | ✅ |
| `openai` | OpenAI | `https://api.openai.com/v1` | Bearer | `gpt-4o` / `o1` | 部分 |
| `google` | Google Gemini | `https://generativelanguage.googleapis.com/v1beta` | Query Key | `gemini-2.0-flash-exp` | ❌ |
| `zhipu` | 智谱 AI | `https://open.bigmodel.cn/api/paas/v4` | Bearer | `glm-4-plus` | ❌ |
| `qwen` | 通义千问 | `https://dashscope.aliyuncs.com/compatible-mode/v1` | Bearer | `qwen-max` | ❌ |
| `wenxin` | 文心一言 | `https://qianfan.baidubce.com/v2` | Bearer | `ernie-4.0` | ❌ |
| `moonshot` | 月之暗面 Kimi | `https://api.moonshot.cn/v1` | Bearer | `moonshot-v1-128k` | ❌ |
| `doubao` | 豆包 | `https://ark.cn-beijing.volces.com/api/v3` | Bearer | `doubao-pro-256k` | ❌ |
| `spark` | 讯飞星火 | `https://spark-api-open.xf-yun.com/v1` | Bearer | `spark-v3.5` | ❌ |
| `hunyuan` | 腾讯混元 | `https://hunyuan.tencent.com/v1` | Bearer | `hunyuan-pro` | ❌ |
| `local` | 本地 (Ollama / LM Studio) | `http://localhost:11434/v1` | None | `qwen2.5:72b` | ❌ |

**默认厂商**: `deepseek` (中文网文适配 + 价格低)
**BYOK 模式**: 用户在 `/ai/config` 设置自己的 API Key, 主控不存储, 仅转发

## 2. 8 任务类型路由 (主控权威)

| 任务类型 | 推荐厂商 | 模型 | 温度 | max_tokens | 备注 |
|----------|---------|------|------|-----------|------|
| **续写** | DeepSeek | `deepseek-chat` | 0.85 | 8192 | 默认任务 |
| **蒸馏** | DeepSeek | `deepseek-chat` | 0.3 | 4096 | 低温度保证摘要稳定 |
| **扩写** | Anthropic | `claude-sonnet-4-6` | 0.85 | 8192 | 长文本生成能力 |
| **润色** | Anthropic | `claude-sonnet-4-6` | 0.7 | 4096 | 文学性 |
| **改写** | Anthropic | `claude-sonnet-4-6` | 0.7 | 4096 | 文学性 |
| **对话** | DeepSeek | `deepseek-chat` | 0.85 | 4096 | 与 AI 助手对话 |
| **大纲生成** | Anthropic | `claude-opus-4-8` | 0.85 | 8192 | ★ 需要最强模型 |
| **角色生成** | Anthropic | `claude-opus-4-8` | 0.85 | 8192 | ★ 需要最强模型 |

**路由决策点**: `ai-orchestrator/orchestrator/router.py` 根据任务类型 + 用户配置 + 配额 + 模型可用性 决策

## 3. 3 层上下文组装 (主控权威)

主控自动组装 LLM 输入的 messages:

| 层级 | 内容 | 预算 (tokens) | 优先级 |
|------|------|--------------|--------|
| **Layer 1 · 系统 Prompt** | 任务指令 + 输出格式 + 风格约束 | ~1000 | 最高 |
| **Layer 2 · 项目知识图谱** | 世界观/角色/大纲/伏笔/时间线 摘要 (按相关性排序) | ~5000 | 高 |
| **Layer 3 · 当前上下文** | 当前章节 + 前 N 章摘要 (蒸馏后) + 用户选中片段 | ~2000 | 中 |

**总预算**: 8K (DeepSeek) / 32K (Claude) / 200K (Gemini 1.5 Pro) / 1M (Gemini 2.0)

**超预算处理**:
1. 优先保留 Layer 1 (不可压缩)
2. Layer 2 按"与当前任务相关度"排序, 截断低相关条目
3. Layer 3 用前 N 章**摘要**代替原文

## 4. 3 阶段蒸馏管线 (主控权威)

> 来源: `knowlage/wiki/concepts/蒸馏机制.md` + `蒸馏机制` concept 页 (authoritative)

章节保存后, 异步触发蒸馏:

| 阶段 | 任务 | 输入 | 输出 | 模型 |
|------|------|------|------|------|
| **Generator** | 生成原始摘要 | 章节正文 | 5 字段摘要 {人物, 事件, 地点, 转折, 伏笔} | DeepSeek |
| **Extractor** | 抽取结构化信息 | Generator 输出 + 上下文 | `event_flows`, `timeline_events`, `foreshadows` 自动建议 | DeepSeek |
| **Checker** | 一致性校验 | Extractor 输出 + 知识图谱 | 冲突列表 (如伏笔冲突角色死亡) | DeepSeek (低温度) |

**触发时机**:
- 章节保存 (PUT /chapters/:id) → 入队
- 每 30 秒 BullMQ 消费一批
- 蒸馏完成 → 写回 chapter.蒸馏状态 = "已完成"

**失败处理**:
- 重试 3 次
- 仍失败 → chapter.蒸馏状态 = "失败" + chapter.蒸馏失败原因
- 用户可在 UI 手动 `/distill/reset-abnormal` 重置

## 5. 配额 (主控权威)

| 计划 | 每日字数 | 项目数 | 单章字数 | 模型 |
|------|----------|--------|----------|------|
| **free** | 5000 | 1 | 3000 | 仅 DeepSeek |
| **pro** | 100000 | 10 | 5000 | 全部 12 厂商 |

**配额重置**: 每天 0 点 (用户时区) 自动重置 `users.daily_used = 0`
**超额**: 返回 429 + `{ quota_reset_at: "..." }`

## 6. 6+ 生成模式

| 模式 | 触发 | 行为 |
|------|------|------|
| **续写** | 选中片段末尾 | 续写 200-500 字 |
| **扩写** | 选中片段 | 扩展为 2-3 倍 |
| **润色** | 选中片段 | 提升文学性, 不改情节 |
| **改写** | 选中片段 | 重写, 保留情节 |
| **对话** | 输入框 | 与 AI 自由对话 |
| **蒸馏** | (自动) | 后台异步 |

## 7. SSE 流式规范 (主控权威)

7 个事件类型 (TypeScript 类型见 `contracts/events/ai-stream.ts`):

```typescript
type AIStreamEvent =
  | { type: 'stream.start', sessionId, requestId, model, mode, provider, timestamp }
  | { type: 'stream.chunk', delta, index, timestamp }
  | { type: 'stream.thinking', thinkingChunk, index, timestamp }  // 推理模型
  | { type: 'stream.tool_call', toolName, args, timestamp }        // 预留 MCP
  | { type: 'stream.done', totalTokens, promptTokens, completionTokens, finishReason, content, thinking, timestamp }
  | { type: 'stream.error', code, message, retryable, timestamp }
  | { type: 'stream.aborted', reason, timestamp }
```

**SSE wire format**:
```
event: stream.start
data: {"sessionId":"...","requestId":"...","model":"deepseek-chat","mode":"续写","provider":"deepseek","timestamp":1234567890}

event: stream.chunk
data: {"delta":"这是","index":1}

event: stream.done
data: {"totalTokens":42,"finishReason":"stop","content":"这是一段..."}
```

## 8. AI 调度主控架构

```
┌──────────────────────────────────────────────────────────┐
│  Frontend (Vue 3)                                         │
│  ├─ composables/useAIStream.ts                            │
│  └─ POST /ai/chat/session → GET /ai/chat/stream/:id (SSE) │
└────────┬─────────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────┐
│  Backend (Node.js)                                        │
│  ├─ POST /ai/chat (同步)                                  │
│  └─ POST /ai/chat/session (返回 sessionId)                 │
└────────┬─────────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────┐
│  AI Orchestrator (Python FastAPI)                         │
│  ├─ /ai/chat/* (12 厂商适配)                              │
│  ├─ /ai/local/* (本地模型代理)                            │
│  ├─ /ai/stream (SSE 网关)                                 │
│  ├─ Provider Registry (12 厂商)                           │
│  ├─ Router (8 任务类型)                                   │
│  ├─ Context Builder (3 层组装)                            │
│  ├─ Distill Pipeline (3 阶段, BullMQ 消费者)              │
│  └─ Quota Manager (5000/天 free, 100000/天 pro)            │
└────────┬─────────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────┐
│  BullMQ (Redis)                                           │
│  └─ 蒸馏任务队列 (async, 3 阶段)                          │
└──────────────────────────────────────────────────────────┘
```

---

*最后更新: 2026-06-07 · 主控 v1.0*
