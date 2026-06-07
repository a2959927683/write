// contracts/events/ai-stream.ts
// 主控权威契约 - AI 流式对话事件 (SSE)
// 7 个事件类型, 与 OpenAPI /ai/chat/stream 一致

export type StreamMode =
  | '续写' | '润色' | '改写' | '扩写' | '总结'
  | '对话' | '查漏' | '修正' | '展开' | '蒸馏' | '自定义';

export interface BaseStreamEvent {
  sessionId: string;
  requestId: string;
  timestamp: number;
}

export interface StreamStartEvent extends BaseStreamEvent {
  type: 'stream.start';
  model: string;
  mode: StreamMode;
  provider: string;
}

export interface StreamChunkEvent extends BaseStreamEvent {
  type: 'stream.chunk';
  delta: string;        // 单个 token / 词
  index: number;        // 序列号
}

export interface StreamThinkingEvent extends BaseStreamEvent {
  type: 'stream.thinking';
  thinkingChunk: string;
  index: number;
}

export interface StreamToolCallEvent extends BaseStreamEvent {
  type: 'stream.tool_call';
  toolName: string;
  args: Record<string, any>;
}

export interface StreamDoneEvent extends BaseStreamEvent {
  type: 'stream.done';
  totalTokens: number;
  promptTokens: number;
  completionTokens: number;
  finishReason: 'stop' | 'length' | 'tool_calls' | 'content_filter';
  content: string;      // 完整内容
  thinking?: string;    // 完整思考 (如启用)
}

export interface StreamErrorEvent extends BaseStreamEvent {
  type: 'stream.error';
  code: 'provider_error' | 'rate_limit' | 'quota_exceeded' | 'context_overflow' | 'unknown';
  message: string;
  retryable: boolean;
}

export interface StreamAbortedEvent extends BaseStreamEvent {
  type: 'stream.aborted';
  reason: 'user_abort' | 'timeout' | 'connection_lost';
}

export type AIStreamEvent =
  | StreamStartEvent
  | StreamChunkEvent
  | StreamThinkingEvent
  | StreamToolCallEvent
  | StreamDoneEvent
  | StreamErrorEvent
  | StreamAbortedEvent;

// SSE wire format
export const SSE_FORMAT = `event: stream.start
data: {"sessionId":"...","requestId":"...","model":"deepseek-chat","mode":"续写","provider":"deepseek","timestamp":1234567890}

event: stream.chunk
data: {"delta":"这是","index":1}

event: stream.chunk
data: {"delta":"一段","index":2}

event: stream.done
data: {"totalTokens":42,"finishReason":"stop","content":"这是一段..."}
`;
