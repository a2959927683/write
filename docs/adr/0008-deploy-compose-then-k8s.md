# 0008 · 部署: Docker Compose (Sprint 0) → K8s (生产)

## 状态
已采纳 · 2026-06-07

## 背景
主控需要决定 Sprint 0 部署方案。两种主流路径:
- **Docker Compose**: 简单, 单机
- **K8s**: 复杂, 生产级

## 决策
- **Sprint 0** (开发/演示): **Docker Compose**
- **生产** (Sprint 4+): **K8s**

## 备选

### 备选 A: 直接 K8s
- ✅ 生产级
- ❌ Sprint 0 复杂度爆炸
- ❌ 单机演示不必要

### 备选 B (已采纳): Compose → K8s 渐进
- ✅ Sprint 0 简单 (一个 `docker compose up` 跑全栈)
- ✅ 后续可平滑迁移到 K8s (容器化已就绪)
- ❌ 需要写两套编排 (Compose + K8s manifests)

## Sprint 0 服务清单 (docker-compose.yml)

| 服务 | 镜像 | 端口 | 依赖 |
|------|------|------|------|
| postgres | postgres:16-alpine | 5432 | — |
| redis | redis:7-alpine | 6379 | — |
| minio | minio/minio:latest | 9000, 9001 | — |
| backend | node:20-alpine | 3000 | postgres, redis |
| frontend | node:20-alpine (dev) | 5173 | backend |
| ai-orchestrator | python:3.11-slim | 8000 | redis |
| prometheus | prom/prometheus | 9090 | backend, ai-orchestrator |
| grafana | grafana/grafana | 3001 | prometheus |

## 关键设计

1. **挂载本地代码**: `docker-compose.dev.yml` 用 volumes 挂载 `./backend`, `./frontend`, `./ai-orchestrator`
2. **健康检查**: 每个服务有 `healthcheck` 字段
3. **依赖顺序**: `depends_on: { postgres: { condition: service_healthy } }`
4. **网络**: 默认 bridge 网络, 服务名即 DNS
5. **数据卷**: 命名卷 `pg_data`, `redis_data`, `minio_data`, 不挂载宿主机

## .env.example

```bash
# JWT
JWT_SECRET=change-me-in-prod-please-use-256-bit-random

# 数据库
POSTGRES_USER=cloudpen
POSTGRES_PASSWORD=cloudpen-dev
POSTGRES_DB=cloudpen

# Redis (无密码, dev only)
REDIS_URL=redis://redis:6379

# MinIO
MINIO_ROOT_USER=cloudpen
MINIO_ROOT_PASSWORD=cloudpen-dev

# AI 默认
AI_PROXY_DEFAULT_PROVIDER=deepseek
DEEPSEEK_API_KEY=sk-your-key-here

# 蒸馏
DISTILL_QUEUE_NAME=distill-queue
DISTILL_BATCH_SIZE=5
```

## 影响
- `init.sh` 是入口, 内部调用 `docker compose up -d`
- 健康检查通过后, E2E 冒烟测试 (S0-31) 启动
- 监控 (Prometheus + Grafana) 默认开启

## 后续 (Sprint 4+)
- K8s manifests: `infra/k8s/`
- Helm chart
- ArgoCD 或 GitOps
- 多区域部署
