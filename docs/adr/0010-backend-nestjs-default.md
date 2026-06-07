# 0010 · 后端框架: Node.js + NestJS (vs Fastify)

## 状态
已采纳 · 2026-06-07

## 背景
主控需要选择后端框架。两个候选:
- **NestJS**: 企业级, 强约定, 装饰器风格 (类似 Spring)
- **Fastify**: 高性能, 插件风格 (类似 Express)

## 决策
**主控采用 NestJS** (默认), 允许子项目权衡改用 Fastify。

## 备选

### 备选 A: NestJS (已采纳)
- ✅ 强约定, 团队接手快
- ✅ 内建 DI / 模块化 / 守卫 / 拦截器
- ✅ OpenAPI 集成 (@nestjs/swagger) 自动生成
- ✅ Prisma / Drizzle / TypeORM 都有官方模块
- ❌ 略重, 启动慢

### 备选 B: Fastify
- ✅ 性能最高 (2-3x NestJS)
- ✅ 插件风格灵活
- ❌ 团队需要自己写模块化结构
- ❌ 强类型支持弱

### 备选 C: Express
- ❌ 太过时, 不考虑

## 理由
1. 主控需要清晰的模块结构 (5 大子系统 / 17 World Tab 子模块)
2. NestJS 的 `@nestjs/swagger` 可以从 controller 自动生成 OpenAPI, 与主控契约同步
3. 团队 (2 前端 + 1 后端) 接手成本低
4. 性能不是 Sprint 0 瓶颈 (单实例足以)

## 模块结构

```
backend/src/
├── main.ts                       # 启动
├── app.module.ts                 # 根模块
├── common/
│   ├── guards/                   # AuthGuard / RoleGuard
│   ├── interceptors/             # Logging / Transform
│   ├── filters/                  # ExceptionFilter
│   └── decorators/               # @CurrentUser / @Roles
├── modules/
│   ├── auth/                     # S0-18
│   ├── project/                  # S0-19
│   ├── chapter/                  # S0-20
│   ├── outline/                  # S0-21
│   ├── character/                # Sprint 1
│   ├── worldviews/               # 17 World Tab 路由
│   ├── ai/                       # AI 转发 (proxy 到 ai-orchestrator)
│   ├── distill/                  # 蒸馏任务入队
│   ├── admin/                    # 50+ 端点
│   └── ...
├── queue/
│   ├── bullmq.config.ts
│   └── consumers/
├── events/
│   └── pubsub.ts
└── config/
    ├── database.ts
    ├── redis.ts
    └── jwt.ts
```

## 与主控 contracts/ 的集成

```typescript
// backend/src/modules/auth/auth.controller.ts
import { ApiOperation, ApiResponse, ApiTags } from '@nestjs/swagger'

@ApiTags('auth')
@Controller('auth')
export class AuthController {
  constructor(private authService: AuthService) {}

  @Post('login')
  @ApiOperation({ summary: '用户名密码登录' })
  @ApiResponse({ status: 200, description: '成功' })
  @ApiResponse({ status: 401, description: '用户名或密码错误' })
  async login(@Body() dto: LoginDto) {
    return this.authService.login(dto)
  }
  // ... 7 more endpoints 与 contracts/openapi/auth.yaml 对应
}
```

## 性能基准

| 框架 | RPS (Hello World) | 启动时间 | 内存 |
|------|-------------------|----------|------|
| **NestJS** | ~25k | 800ms | 80MB |
| Fastify | ~70k | 200ms | 40MB |
| Express | ~15k | 100ms | 30MB |

Sprint 0 单实例 ~25k RPS 足够 (10k 并发用户)

## 影响
- `backend/package.json` 用 `@nestjs/*` 系列
- 所有 controller 加 `@ApiTags` / `@ApiOperation` / `@ApiResponse` 装饰器
- `prisma` 作为 ORM (Sprint 1 评估 Drizzle 备选)
- 测试用 `@nestjs/testing` + Jest

## 后续
- 如果性能瓶颈, 改用 Fastify adapter (NestJS 支持)
- 考虑 GraphQL (如果前端觉得 REST 太啰嗦)
- 微服务拆分 (如果单实例撑不住)
