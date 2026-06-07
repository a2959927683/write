# 0004 · 12 AI 厂商注册表 + DeepSeek 默认

## 状态
已采纳 · 2026-06-07

## 背景
云笔已经接入 12 家 AI 厂商 (C11 冲突裁决)。主控需要决定:
- **是否完整支持 12 家**? (vs 仅 3-5 家)
- **默认厂商选谁**? (影响用户首次体验)

## 决策
**主控完整支持 12 家厂商**, **默认 DeepSeek-V3 Chat**。

12 家注册表: `contracts/ai/providers.json`

## 12 家厂商

| Key | 厂商 | 默认模型 |
|-----|------|----------|
| `deepseek` | DeepSeek | `deepseek-chat` (默认) |
| `anthropic` | Anthropic Claude | `claude-opus-4-8` |
| `openai` | OpenAI | `gpt-4o` |
| `google` | Google Gemini | `gemini-2.0-flash-exp` |
| `zhipu` | 智谱 AI | `glm-4-plus` |
| `qwen` | 通义千问 | `qwen-max` |
| `wenxin` | 文心一言 | `ernie-4.0` |
| `moonshot` | 月之暗面 Kimi | `moonshot-v1-128k` |
| `doubao` | 豆包 | `doubao-pro-256k` |
| `spark` | 讯飞星火 | `spark-v3.5` |
| `hunyuan` | 腾讯混元 | `hunyuan-pro` |
| `local` | 本地 (Ollama / LM Studio) | `qwen2.5:72b` |

## 备选

### 备选 A: 仅 3 家 (DeepSeek + OpenAI + Claude)
- ✅ 简单, 适配快
- ❌ 失去对国内云厂商 (智谱/通义/豆包等) 的覆盖
- ❌ 用户期望"12 厂商", 砍掉不符合 1:1 复刻策略

### 备选 B (已采纳): 12 家 + BYOK
- ✅ 1:1 还原
- ✅ 用户可以选择更便宜的 (DeepSeek) 或更强的 (Claude Opus)
- ✅ 本地模型 (Ollama) 给隐私敏感用户
- ❌ 适配工作量大 (12 个 provider)
- ❌ 一些国内厂商 API 经常变化, 维护成本高

## DeepSeek 默认的理由
1. **价格低**: $0.14/$0.28 per 1M tokens (vs Claude $3/$15)
2. **中文强**: 中文网文场景下表现优于 GPT-4o
3. **思考能力**: deepseek-chat 支持思考模式
4. **稳定性**: API 稳定, 错误率低
5. **响应速度**: 接近 100 tokens/s

## 影响
- 任何新增厂商: 修改 `contracts/ai/providers.json` + 新增 adapter
- 用户切换厂商: `PUT /ai/config { provider, model, apiKey }`
- AI 配额按字数计算, 不分厂商 (避免用户切换厂商逃配额)
- 路由规则见 `contracts/ai/routing-rules.yaml` (待写, S0-14)

## 后续
- 监控每个厂商的可用性 + 延迟 + 错误率
- 如果某厂商长期不可用, 标记为 `enabled: false` 但不删除
- 考虑加入 "推荐路由" (根据任务类型自动选最优)
