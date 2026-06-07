# Sprint 3+ · 生产上线 (占位文档)

> 🟡 **PLACEHOLDER · 占位中** — Sprint 2 完工后再细化
> 关联: [`docs/ROADMAP.md`](../ROADMAP.md)
> 触发条件: Sprint 2 验收通过 (M3 Beta 测试完成)

---

## 📊 元数据 (粗略)

| 字段 | 值 |
|------|---|
| **代号** | Sprint 3+ · "生产上线" |
| **时间窗** | 2026-10 中 ~ 2026-12 末 (持续) |
| **任务数 (估)** | 持续迭代 |
| **工作量 (估)** | 持续 |
| **团队** | 5 人核心 (稳定运营) |
| **目标里程碑** | M4 · v1.0 上线 (2026-11-30) + M5 · 商业化 (2026-12-31) |
| **状态** | ⚪ 未启动 |

---

## 🎯 目标 (一句话)

**真正卖给用户 — Beta 转正式, K8s 上线, 支付集成, 移动端 + 海外版本启动。**

---

## 🚀 5 大上线动作 (待细化)

### ① Docker Compose → K8s 迁移
- `infra/k8s/` manifests (api / postgres / redis / minio / ingress)
- Helm chart
- ArgoCD 或 GitOps
- 多区域部署 (国内 + 海外)

### ② 监控告警全开
- Prometheus + Grafana + Alertmanager
- 关键指标:
  - AI 失败率 > 5% 告警
  - 蒸馏队列积压 > 100 告警
  - API 延迟 P95 > 5s 告警
  - 数据库连接数 > 80% 告警
- OpenTelemetry trace → Jaeger/Tempo
- 日志聚合 → Loki

### ③ 支付集成
- Stripe (海外) / 微信支付 (国内) / 支付宝 (国内)
- 订阅模型: Free / Pro / Team
- 用量计费 + 月结/年付
- Webhook 处理 + 退款流程

### ④ 移动端 (P3)
- 浮动 AI 按钮 + 底部抽屉
- 响应式重构 (< 768px 完整支持)
- 离线编辑 (Service Worker)
- PWA 支持

### ⑤ 海外版本 (i18n)
- 英文 / 日文 / 韩文 / 西班牙文
- 适配海外 AI 厂商 (OpenAI / Claude / Gemini 优先)
- 多区域 CDN (Cloudflare / AWS CloudFront)
- 海外法务合规 (GDPR / CCPA)

---

## 🚧 待办 (Sprint 2 末细化)

- [ ] K8s manifests 全套设计
- [ ] Helm chart 编写
- [ ] 监控指标全清单
- [ ] Stripe/微信/支付宝集成方案
- [ ] 移动端 UI 重新设计 (找设计师)
- [ ] i18n 翻译预算
- [ ] 海外服务器选型 (AWS/Azure/GCP)
- [ ] 法务合规 review
- [ ] 营销/推广预算
- [ ] 客服支持系统
- [ ] 内容审核策略 (fiction-aware)
- [ ] 灰度发布机制
- [ ] 数据备份与灾难恢复
- [ ] SLA 承诺 (99.9% uptime?)

---

## 📅 大致时间线 (粗估)

| 周 | 重点 |
|----|------|
| Week 1-2 | K8s 迁移 + 监控告警 |
| Week 3 | Stripe/微信支付集成 |
| Week 4 | Beta → v1.0 公开发布 (M4) |
| Week 5-6 | 商业化推广 + 第一批付费用户 (M5) |
| Week 7+ | 移动端开发 + i18n 启动 |
| 持续 | 性能优化 / 新功能迭代 / 用户反馈 |

---

## ⚠️ 已知风险 (粗略)

- K8s 学习曲线陡 → 提前 2 周 PoC
- 支付集成合规风险 → 法务先 review
- 移动端开发成本高 → P3 后置, 先 PWA
- 海外用户难触达 → 早期 BYOK 模式自然过滤
- 服务器成本飙升 → 严格配额 + 自动伸缩
- 大厂跟进竞争 → 持续差异化 (蒸馏 + 一致性 + 17 模块)

---

## 💰 商业化里程碑

| 节点 | 目标 |
|------|------|
| M4 · v1.0 上线 | 1000 个注册用户 |
| M5 · 商业化启动 | 100 个付费用户 (Pro $9.9/月) |
| 2027 Q1 | 1000 个付费用户 (MRR $10K) |
| 2027 Q2 | Team 版上线, 引入企业客户 |
| 2027 Q3 | 海外版本上线 |
| 2027 Q4 | 10000 个付费用户 (MRR $100K) |

---

## 📚 关联

- 部署: `docs/adr/0008-deploy-compose-then-k8s.md`
- 监控: `docs/MASTER-PROJECT-SPEC.md` §2.7
- 配额: `docs/adr/0015-quota-free-1-pro-10.md`
- 移动端: `docs/adr/0016-mobile-strategy.md` (待写)
- 海外: 待 ADR

---

## 🚫 当前不要做

**在 Sprint 2 未完工前**, **不要**细化本文档。

**Sprint 3 启动时**, 主控负责拆分为多个文档:
- `sprint-3.md` · K8s + 监控 + 支付
- `sprint-4.md` · 移动端
- `sprint-5.md` · i18n + 海外
- 后续按需新建

---

*占位 · 2026-06-07 · 等 M3 Beta 测试通过后细化*
