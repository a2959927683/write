# 0006 · Base URL: /api 而非 /api/v1/

## 状态
已采纳 · 2026-06-07

## 背景
云笔真实 API 的 Base URL 是 `/api` (而非 `/api/v1/`, `/api/v2/`)。
用户消息中曾提到 `/api/v1/`, 主控需要裁决。

## 决策
**主控采用 `/api` 作为 Base URL**, 与云笔真实 API 1:1 对应。

## 备选

### 备选 A: /api/v1/ (用户消息暗示)
- ✅ 符合 REST 命名规范 (v1 暗示版本)
- ❌ 与云笔真实 API 不一致
- ❌ 后续 v2 迁移成本高

### 备选 B (已采纳): /api
- ✅ 1:1 还原云笔
- ✅ 现有客户端直接对接
- ❌ 不符合 v1 命名规范 (但云笔也没用)

## 实现

```typescript
// frontend/src/api/index.ts
import axios from 'axios'

const api = axios.create({
  baseURL: '/api',  // NOT /api/v1/
  headers: {
    'Content-Type': 'application/json',
    'Origin': window.location.origin,  // 必须, 否则 403
  },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```

## 反向代理配置 (Nginx)

```nginx
location /api/ {
  proxy_pass http://backend:3000/api/;
  proxy_set_header Host $host;
  proxy_set_header X-Real-IP $remote_addr;
  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  proxy_set_header X-Forwarded-Proto $scheme;

  # SSE 必须禁用缓冲
  proxy_buffering off;
  proxy_cache off;
  proxy_set_header Connection '';
  proxy_http_version 1.1;
  chunked_transfer_encoding off;
}
```

## 影响
- 所有 `contracts/openapi/*.yaml` 的 `servers.url` 必须是 `/api`
- 反向代理配置 `proxy_pass /api/`
- CORS 配置 `Access-Control-Allow-Origin: <your-domain>` (不能用 `*`)

## 后续
- 如果未来需要 v2, 通过 query 参数 `?v=2` 或 header `X-API-Version: 2` 切换
- 不引入 URL 路径版本号
