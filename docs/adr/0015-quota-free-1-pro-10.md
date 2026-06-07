# 0015 · 鉴权细节: 1 项目 (free) / 10 项目 (pro) 配额

## 状态
已采纳 · 2026-06-07

## 背景
云笔的免费版只能创建 1 个项目, 专业版 10 个 (来自 `wiki/sources/API认证与架构.md`)。
主控需要决定: 沿用云笔配额, 还是调整?

## 决策
**主控沿用云笔配额**:
- **free**: 1 个项目, 5000 字/天, 仅 DeepSeek
- **pro**: 10 个项目, 100000 字/天, 全部 12 厂商
- **team** (Sprint 2+): 不限, 多用户协作

## 备选

### 备选 A: 沿用云笔 1/10 (已采纳)
- ✅ 1:1 还原
- ✅ 简单, 业务清晰
- ❌ free 太受限, 可能劝退新用户

### 备选 B: 放宽到 3/20
- ✅ 新用户友好
- ❌ 与云笔不一致
- ❌ 收入可能下降

### 备选 C: 完全免费
- ❌ 不可持续
- ❌ AI 成本无法覆盖

## 实现

```sql
-- users 表
ALTER TABLE users ADD COLUMN 最高角色等级 INT NOT NULL DEFAULT 10;
ALTER TABLE users ADD COLUMN plan_type VARCHAR(16) NOT NULL DEFAULT 'free';
ALTER TABLE users ADD COLUMN daily_quota INT NOT NULL DEFAULT 5000;
ALTER TABLE users ADD COLUMN daily_used INT NOT NULL DEFAULT 0;
ALTER TABLE users ADD COLUMN quota_reset_at TIMESTAMPTZ;
```

```python
# backend/src/common/guards/quota.py
class QuotaGuard:
    def __init__(self, plan: str = 'free'):
        self.plan = plan
        self.limits = {
            'free': {'maxProjects': 1, 'dailyQuota': 5000, 'maxChapterWords': 3000},
            'pro': {'maxProjects': 10, 'dailyQuota': 100000, 'maxChapterWords': 5000},
        }

    async def check_project_create(self, user):
        limit = self.limits[user.plan_type]
        current = await db.projects.count(where={'userId': user.id})
        if current >= limit['maxProjects']:
            raise HTTPException(403, f"项目数已达上限 ({limit['maxProjects']})")

    async def check_daily_quota(self, user, words_to_consume):
        await self._reset_if_needed(user)
        if user.daily_used + words_to_consume > user.daily_quota:
            raise HTTPException(429, {
                'message': '今日配额已用完',
                'quotaResetAt': user.quota_reset_at,
            })
        await db.users.update(
            where={'id': user.id},
            data={'dailyUsed': user.daily_used + words_to_consume}
        )

    async def _reset_if_needed(self, user):
        if user.quota_reset_at and user.quota_reset_at < datetime.now():
            await db.users.update(
                where={'id': user.id},
                data={'dailyUsed': 0, 'quotaResetAt': datetime.now() + timedelta(days=1)}
            )
```

## 升级流程 (Sprint 2+)

```
free 用户点击 "升级 Pro"
  → 跳转支付 (微信/支付宝/Stripe)
  → 支付成功 webhook
  → backend 更新 plan_type = 'pro'
  → 用户立即生效
```

## 影响
- `users` 表加 5 个字段
- `POST /projects` 加配额校验
- `POST /ai/chat/*` 加每日配额校验
- 前端 `/projects/my-quota` 显示剩余配额

## 后续
- 团队版 (Sprint 2+)
- 年付优惠 (Sprint 2+)
- 邀请奖励 (Sprint 3+)
