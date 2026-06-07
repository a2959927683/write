# 云笔AI 复刻项目主控

> 跨平台启动脚本 (Windows Git Bash + Linux + macOS)

## 用法

```bash
# 开发模式 (启动 PG + Redis + MinIO + API + FE + AI Orchestrator, 挂载本地代码, 改代码即生效)
./init.sh dev

# 仅启动数据库 (PG + Redis + MinIO), 后端/前端/AI 跑本地
./init.sh db

# 全栈生产模式 (build 镜像 + detached 启动)
./init.sh prod

# 停止所有
./init.sh stop

# 清理所有 (包括数据卷)
./init.sh clean

# 跑契约一致性检查
./init.sh lint

# 跑 E2E 冒烟测试
./init.sh e2e

# 查看帮助
./init.sh help
```

## 前置依赖

- Docker 20+ (含 docker compose v2)
- Windows 用户: Git Bash + Docker Desktop
- 4GB+ 内存 (PG + Redis + MinIO + 3 个服务)

## 服务端口

| 服务 | 端口 | 用途 |
|------|------|------|
| Frontend (Vue 3) | 5173 | Vite dev server |
| Backend (Node.js) | 3000 | Fastify/NestJS API |
| AI Orchestrator (Python) | 8000 | FastAPI + SSE |
| PostgreSQL | 5432 | 项目/章节/世界设定 |
| Redis | 6379 | 会话/配额/AI 响应缓存/BullMQ |
| MinIO | 9000 / 9001 | 头像/导出/封面 (S3 兼容) |
| Prometheus | 9090 | 监控 |
| Grafana | 3001 | 监控可视化 |

## 故障排查

- **端口冲突**: 修改 `docker-compose.yml` 中的端口映射
- **PG 连接失败**: 确认 `pg_data` 卷未损坏, 或 `docker volume rm master_pg_data` 后重新 `init.sh dev`
- **AI 调用失败**: 检查 `contracts/ai/providers.json` 中 `apiKey` 已配置, 或在 `/ai/config` 中设置 BYOK
- **SSE 断开**: 检查反向代理 (Nginx) 是否禁用了 `text/event-stream`

## 目录对应

| 服务 | 路径 | 镜像 (Sprint 0+) |
|------|------|------------------|
| frontend | `./frontend` | node:20-alpine + pnpm |
| backend | `./backend` | node:20-alpine |
| ai-orchestrator | `./ai-orchestrator` | python:3.11-slim |
| postgres | (容器内) | postgres:16-alpine |
| redis | (容器内) | redis:7-alpine |
| minio | (容器内) | minio/minio:latest |

## 环境变量

复制 `.env.example` 为 `.env` 并填入:

```bash
cp .env.example .env
# 然后编辑 .env
```

关键变量:
- `JWT_SECRET` (生产环境必须改)
- `AI_PROXY_DEFAULT_PROVIDER` (默认 deepseek)
- `DISTILL_QUEUE_NAME` (默认 distill-queue)

---

*主控 v1.0 · 2026-06-07*
