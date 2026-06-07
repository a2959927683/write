# 0009 · 鉴权: JWT (HS256) + 30s 心跳

## 状态
已采纳 · 2026-06-07

## 背景
云笔鉴权用 JWT (HS256) + 前端 30s 心跳 (来自 `wiki/sources/API认证与架构.md`)。
主控需要决定: 沿用云笔, 还是升级到 RS256 / 改心跳频率?

## 决策
- **JWT 算法**: HS256 (与云笔一致, 单密钥, 性能更高)
- **心跳**: 30s 一次, `navigator.sendBeacon` 上行
- **Token 有效期**: 7 天 (含 refresh)
- **心跳用途**: 在线状态 + token 续期 (滑动窗口)

## 备选

### 备选 A: RS256 (非对称)
- ✅ 更安全, 可以做密钥轮换
- ✅ 多服务可以独立验证
- ❌ 性能略低
- ❌ 与云笔不一致

### 备选 B (已采纳): HS256 (对称)
- ✅ 1:1 还原
- ✅ 性能高
- ✅ 简单
- ❌ 密钥泄露 = 全部 token 可伪造 (但单服务足够)

### 心跳频率

| 频率 | 优点 | 缺点 |
|------|------|------|
| 10s | 实时 | 流量大 |
| **30s** (已采纳) | 平衡 | — |
| 60s | 省流量 | 不够实时 |
| 不心跳 | 0 流量 | 无法做在线统计 |

## 实现

```typescript
// frontend/src/composables/useHeartbeat.ts
export function useHeartbeat() {
  useEffect(() => {
    const send = () => {
      const token = localStorage.getItem('token')
      if (!token) return
      const url = `/api/heartbeat?token=${encodeURIComponent(token)}`
      navigator.sendBeacon(url, '')
    }
    send()  // 立即发一次
    const timer = setInterval(send, 30_000)
    return () => clearInterval(timer)
  }, [])
}
```

```typescript
// backend/src/modules/auth/heartbeat.ts
router.post('/heartbeat', async (req, res) => {
  const { token } = req.query
  if (!token) return res.status(401).json({ success: false, message: 'No token' })
  try {
    const payload = jwt.verify(token, JWT_SECRET)
    // 更新 last_active_at
    await db.users.update({
      where: { id: payload.userId },
      data: { lastActiveAt: new Date() }
    })
    res.json({ success: true })
  } catch (e) {
    res.status(401).json({ success: false, message: 'Token invalid' })
  }
})
```

## Token 结构

```json
{
  "userId": 1,
  "username": "alice",
  "planType": "pro",
  "最高角色等级": 50,
  "iat": 1718342400,
  "exp": 1718947200
}
```

## 影响
- `backend` 用 `jsonwebtoken` (Node.js) 或 `PyJWT` (Python)
- 前端用 `localStorage` 存 token (注意 XSS 防护)
- 30s 心跳在 `App.vue` 全局启动
- 心跳失败 → token 过期 → 跳登录页

## 后续
- 考虑用 HttpOnly Cookie 替代 localStorage (防 XSS)
- RS256 升级 (如果多服务需要)
- Refresh token 机制 (现在 7 天有效期内不需要)
