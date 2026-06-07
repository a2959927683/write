# 0012 · AI 调度: 自建 AI Proxy (12 厂商抽象)

## 状态
已采纳 · 2026-06-07

## 背景
主控需要给 12 个 AI 厂商提供统一接口, 决定: 自建 vs 用 LiteLLM?

## 决策
**主控采用自建 AI Proxy**, 放在 `ai-orchestrator/` 子项目 (Python + FastAPI)。

## 备选

### 备选 A: 自建 (已采纳)
- ✅ 完全控制
- ✅ 业务逻辑可深度定制 (3 阶段蒸馏, 3 层上下文)
- ✅ 不引入外部依赖
- ❌ 工作量大 (12 个 adapter)

### 备选 B: LiteLLM
- ✅ 快速接入 100+ 厂商
- ❌ 与主控业务耦合度低
- ❌ 蒸馏/上下文等业务逻辑仍要自己写
- ❌ 引入 Python 依赖 (主控是 Python, OK)

## 架构

```
ai-orchestrator/
├── app/
│   ├── main.py                   # FastAPI 启动
│   ├── routers/
│   │   ├── ai_chat.py            # /ai/chat/* (12 厂商统一入口)
│   │   ├── ai_stream.py          # /ai/stream (SSE 网关)
│   │   └── ai_admin.py           # 管理 (测试/统计)
│   ├── providers/                # 12 厂商 adapter
│   │   ├── base.py               # 抽象基类
│   │   ├── deepseek.py           # OpenAI 兼容
│   │   ├── anthropic.py          # Anthropic SDK
│   │   ├── openai.py             # OpenAI SDK
│   │   ├── google.py             # Google Generative AI
│   │   ├── zhipu.py
│   │   ├── qwen.py
│   │   ├── wenxin.py
│   │   ├── moonshot.py
│   │   ├── doubao.py
│   │   ├── spark.py
│   │   ├── hunyuan.py
│   │   └── local.py              # Ollama / LM Studio
│   ├── orchestrator/
│   │   ├── router.py             # 8 任务类型路由
│   │   ├── context_builder.py    # 3 层上下文组装
│   │   ├── distill_pipeline.py   # 3 阶段蒸馏
│   │   ├── quota.py              # 配额管理
│   │   └── stream_gateway.py     # SSE 网关
│   ├── schemas/                  # Pydantic (复用 contracts/schemas/)
│   └── config.py
└── tests/
```

## 抽象基类

```python
# providers/base.py
from abc import ABC, abstractmethod
from typing import AsyncIterator

class BaseProvider(ABC):
    name: str
    default_base_url: str
    auth_scheme: str

    @abstractmethod
    async def chat(
        self,
        messages: list[dict],
        model: str,
        options: dict,
    ) -> dict:
        """同步调用, 返回完整响应"""
        pass

    @abstractmethod
    async def stream(
        self,
        messages: list[dict],
        model: str,
        options: dict,
    ) -> AsyncIterator[dict]:
        """流式调用, yield chunk dict"""
        pass

    def transform_request(self, messages, model, options) -> dict:
        """将主控统一格式转为厂商原生格式"""
        raise NotImplementedError

    def transform_response(self, raw: dict) -> dict:
        """将厂商原生格式转为主控统一格式"""
        raise NotImplementedError

    def transform_chunk(self, raw: dict) -> dict:
        """流式 chunk 转换"""
        raise NotImplementedError
```

## DeepSeek Adapter (示例, OpenAI 兼容)

```python
# providers/deepseek.py
from openai import AsyncOpenAI
from .base import BaseProvider

class DeepSeekProvider(BaseProvider):
    name = "deepseek"
    default_base_url = "https://api.deepseek.com/v1"
    auth_scheme = "bearer"

    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.client = None

    def _ensure_client(self, base_url: str = None, api_key: str = None):
        key = api_key or self.api_key
        url = base_url or self.default_base_url
        self.client = AsyncOpenAI(api_key=key, base_url=url)

    async def chat(self, messages, model, options):
        self._ensure_client(options.get("baseUrl"), options.get("apiKey"))
        response = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=options.get("temperature", 0.85),
            max_tokens=options.get("max_tokens", 8192),
        )
        return self.transform_response(response)

    async def stream(self, messages, model, options):
        self._ensure_client(options.get("baseUrl"), options.get("apiKey"))
        stream = await self.client.chat.completions.create(
            model=model, messages=messages, stream=True,
            temperature=options.get("temperature", 0.85),
            max_tokens=options.get("max_tokens", 8192),
        )
        async for chunk in stream:
            yield self.transform_chunk(chunk)

    def transform_response(self, raw):
        return {
            "content": raw.choices[0].message.content,
            "totalTokens": raw.usage.total_tokens,
            "promptTokens": raw.usage.prompt_tokens,
            "completionTokens": raw.usage.completion_tokens,
            "finishReason": raw.choices[0].finish_reason,
        }

    def transform_chunk(self, raw):
        return {
            "delta": raw.choices[0].delta.content or "",
            "finishReason": raw.choices[0].finish_reason,
        }
```

## Anthropic Adapter (不同 API 风格)

```python
# providers/anthropic.py
from anthropic import AsyncAnthropic
from .base import BaseProvider

class AnthropicProvider(BaseProvider):
    name = "anthropic"
    default_base_url = "https://api.anthropic.com"
    auth_scheme = "x-api-key"

    async def chat(self, messages, model, options):
        client = AsyncAnthropic(
            api_key=options.get("apiKey"),
            base_url=options.get("baseUrl", self.default_base_url),
        )
        # Anthropic API 分离 system message
        system = next((m["content"] for m in messages if m["role"] == "system"), "")
        msgs = [m for m in messages if m["role"] != "system"]

        response = await client.messages.create(
            model=model,
            system=system,
            messages=msgs,
            max_tokens=options.get("max_tokens", 8192),
            temperature=options.get("temperature", 0.85),
        )
        return {
            "content": response.content[0].text,
            "totalTokens": response.usage.input_tokens + response.usage.output_tokens,
            "promptTokens": response.usage.input_tokens,
            "completionTokens": response.usage.output_tokens,
            "finishReason": response.stop_reason,
        }
    # ... stream 同理
```

## 路由决策

```python
# orchestrator/router.py
class Router:
    def __init__(self, registry: ProviderRegistry):
        self.registry = registry

    async def route(self, task_type: str, user_config: dict) -> tuple[Provider, str]:
        # 1. 用户在 options 中显式指定 (最高优先级)
        if user_config.get("provider") and user_config.get("model"):
            return (
                self.registry.get(user_config["provider"]),
                user_config["model"],
            )

        # 2. 用户默认配置
        if user_config.get("defaultProvider"):
            return (
                self.registry.get(user_config["defaultProvider"]),
                user_config.get("defaultModel", "deepseek-chat"),
            )

        # 3. 任务类型默认 (从 routing-rules.yaml 读)
        rules = load_yaml("contracts/ai/routing-rules.yaml")
        rule = rules["tasks"].get(task_type, rules["default"])
        return (
            self.registry.get(rule["provider"]),
            rule["model"],
        )
```

## 影响
- 12 个 adapter 是 `ai-orchestrator/` 的核心代码
- 主控 `contracts/ai/providers.json` 是配置权威
- 路由规则 `contracts/ai/routing-rules.yaml` 是策略权威
- 任何新增厂商: 加 adapter + 更新 providers.json + 跑测试

## 后续
- 监控每个 provider 的成功率/延迟
- 失败自动 fallback (如 DeepSeek 挂了 → 切到 DeepSeek-R1 或其他)
- 加入"推荐路由" (根据 prompt 类型智能选模型)
