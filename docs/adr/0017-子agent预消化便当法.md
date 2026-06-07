# ADR 0017 · 子 Agent 预消化便当法

## 状态

✅ **ACCEPTED · 已采纳** (2026-06-07)
> 提议日期: 2026-06-07
> 拍板日期: 2026-06-07
> 关联讨论: `docs/discussions/2026-06-07-子agent调度方案.md` (RESOLVED)
> 关联 HTML: `explain/09-子agent调度方案-讨论稿.html` · `explain/12-adr0017-子agent便当法-教练推荐答案.html`

---

## 背景

主控 (orchestrator) 计划派多个子 agent 并行实施 Sprint 0 的 37 个任务。
每个子 agent 在自己的子项目目录下用 `/harness-l3-v4` 管理,走 5 阶段 (研究/规划/构建/复盘/调试)。

**用户识别的卡点:**
> 前面的研究设计阶段需要大量资料,这是卡点

具体表现:
- 子 agent 启动就要读 `knowlage/` 87 个 wiki 页 → context 200K+ tokens
- 读完 80% 不相关 → 浪费 token + 误导决策
- 研究阶段花 30-60 分钟 → 还没动手
- 多 agent 并发 → token 账单爆炸

---

## 决策

**主控采用"预消化便当法"**: 主控提前消化知识,产出 brief 喂给子 agent,而不是让子 agent 自己去菜市场。

### 核心铁律

> **主控的核心价值 = 把知识库压缩成 brief。**
> **子 agent 的核心价值 = 把 brief 变成代码。**

### 实施 (4 解药组合拳)

| # | 解药 | 状态 | 备注 |
|---|------|------|------|
| 🥇 1 | **预消化便当** (`master/briefs/`) | 必做 | 主控写 brief, 子 agent 直接读 |
| 🥈 2 | **L3-v4-Lite** (子项目砍掉"研究"阶段) | 必做 | 4 阶段: 规划/构建/复盘/调试 |
| 🥉 3 | **knowlage/INDEX.md** (按需精准检索) | 必做 | 主控写一次, 所有子 agent 受益 |
| 🏅 4 | **二级 research-agent** (短命消化) | 按需 | 边缘任务才用 |

---

## ✅ 6 个落地细节决策 (已定稿)

### Q1 · brief 模板字段 → **升级到 9 字段** ✅

**新增 3 字段:**
- 📌 **依赖任务** (防止 agent 抢跑)
- ⏱️ **估算工时** (主控判超时, 默认 4h, 超 6h 必须报警)
- 🚨 **失败回滚** (防止失败 agent 留垃圾)

**完整 9 字段模板:**
```markdown
# S0-XX · 任务名 brief

## 🎯 任务 [必填]
任务概述 (5 行内说清)

## 📌 依赖任务 [必填]
- 必须先完成: S0-XX, S0-YY
- 完工后阻塞: S0-ZZ

## 📜 必读契约 [必填]
- contracts/openapi/xxx.yaml
- contracts/schemas/xxx.json

## 🔧 技术约束 [必填]
- 关键技术决策 (中文字段名 / JWT HS256 等)

## ⏱️ 估算工时 [必填]
N 小时 (超 N+2h 必须报警)

## ✅ 验收 [必填]
可执行的命令 (curl / test 等)

## 🚫 不要做 [必填]
反向约束 (不实现 X / 不碰 Y)

## 🚨 失败回滚 [必填]
git reset --hard origin/main; xxx

## 📚 想深挖再看 [可选]
- knowlage/wiki/sources/xxx.md
```

### Q2 · brief 写作节奏 → **分 3 批写 (C 方案)** ✅

| 批次 | 数量 | 何时写 | 内容 |
|------|------|--------|------|
| 🥇 第 1 批 · 关键路径 | 7 个 | **Day 1 立刻** | S0-04/15/16/17/18/22/29 |
| 🥈 第 2 批 · 主链剩余 | ~15 个 | Day 2-3 滚动 | S0-19~31 中间任务 |
| 🥉 第 3 批 · 辅助 | ~15 个 | 按需写 | ADR/监控/CI/文档等 |

**理由:**
- 第 1 批 → 快速试点验证
- 第 2 批 → 试点改进后批量产
- 第 3 批 → 防止过早写无效 brief

### Q3 · brief 写错处理 → **子 agent 只能反馈, 不能改** ✅

**4 步流程:**
1. 子 agent 发现 brief 错 → **立刻停手**
2. 在 `xxx/progress.txt` 写 `[BRIEF_ERROR]` 标记
3. 主控仲裁 (30 分钟内响应)
4. 主控改 brief + commit + 通知 agent 重启

**3 条铁律:**
- ❌ 子 agent 绝对不能自己改 brief (失去权威)
- ✅ 必须留痕 (progress.txt 可追溯)
- ⏱️ 主控 30 分钟内响应 (否则子 agent 转去做别的)

### Q4 · L3-v4-Lite 调试回流 → **双轨 + 3 级标签** ✅

| 级别 | 渠道 | 响应时间 |
|------|------|---------|
| 🟢 **INFO** (小问题) | `progress.txt` `[INFO]` | 主控定期看 |
| 🟡 **WARN** (中问题) | `issues/` `[WARN]` | 主控 1 天内回 |
| 🔴 **CRITICAL** (大问题/契约错) | progress + issues + `[CRITICAL]` | 主控 30 分钟内回 |
| 📡 **EMERGENCY** (阻塞) | 触发 `SendMessage` 推送 | 主控立即响应 |

### Q5 · `knowlage/INDEX.md` 维护 → **主控独占** ✅

**主控可以做 ✅:**
- 新增条目到 INDEX.md
- 修订条目的"权威"标记
- 下线过期的 source
- 合并冲突的 source
- 判定 authoritative

**子 agent 不能做 ❌:**
- 修改 INDEX.md
- 判定权威性
- 修改任何 source 文件
- **但可以** → 在 progress.txt 用 `[INDEX_SUGGEST]` 给主控提建议

### Q6 · 二级 research-agent → **默认 spawn, 并行才 isolation** ✅

| 场景 | 方式 |
|------|------|
| research-agent 短命 (&lt;5min) | ✅ 直接 spawn |
| 只读 + 总结 + 退场 | ✅ 直接 spawn |
| 需写文件 | ⚠️ 必须 isolation |
| 多个独立主题并行 | ⚠️ isolation 并行 |

**实战 90% 用 spawn**, 只有"3+ 主题并行"才上 isolation。

---

## 备选方案

### 备选 A · 子 agent 自己读 knowlage (用户最初想法)
- ✅ 自治, 主控工作量低
- ❌ context 爆炸, token 烧光, 易出错
- ❌ 多 agent 重复消化同一份知识 = 浪费

### 备选 B · 主控全程喂饭 (传统集中式)
- ✅ 控制强
- ❌ 主控成瓶颈, 失去并行优势
- ❌ 退化为"主控写代码"

### 备选 C (已采纳) · 预消化便当
- ✅ 主控前期投入, 后期所有子 agent 受益
- ✅ Context 占用降 80-90%
- ✅ 保持子 agent 自治
- ❌ 主控需写 brief (但 3 批分摊, 工作量可控)

---

## 效果对比

| 指标 | 备选 A | 备选 C (本 ADR) |
|------|---------|-----------------|
| 子 agent 启动时间 | 30-60 分钟 | 2-5 分钟 |
| Context 占用 | 200K+ tokens | 15-30K |
| token 成本 | 高 | 降 80-90% |
| 出错率 | 中 | 低 |
| 主控工作量 | 低 | 中 (前期投入) |

---

## 影响

### 主控新增产出物

```
master/
├── briefs/                                ← 新增目录
│   ├── README.md                          ← 说明 + 9 字段模板
│   ├── _template.md                       ← brief 模板
│   ├── S0-04-init-sh.md                   ← 第 1 批
│   ├── S0-15-docker-compose.md            ← 第 1 批
│   ├── S0-16-nestjs-skeleton.md           ← 第 1 批
│   ├── S0-17-prisma-schema.md             ← 第 1 批
│   ├── S0-18-auth.md                      ← 第 1 批
│   ├── S0-22-vue-shell.md                 ← 第 1 批
│   ├── S0-29-sse-stream.md                ← 第 1 批
│   └── ... (第 2/3 批按需写)
└── knowlage/INDEX.md                      ← 主控维护 (knowlage/ 下唯一可写)
```

### 子项目 harness.config.json 改动

```json
{
  "harness": {
    "version": "l3-v4-lite",
    "phases": [
      { "id": "plan",    "inputs": ["../master/briefs/S0-18-auth.md"] },
      { "id": "build",   "outputs": ["src/modules/auth/"] },
      { "id": "review",  "scripts": ["pnpm test:auth"] },
      { "id": "debug" }
    ]
  }
}
```

### 子项目 CLAUDE.md 新增段

每个子项目 CLAUDE.md 必须新增"调试回流"段:
```markdown
## 调试回流协议
- 小问题 → progress.txt `[INFO]`
- 中问题 → issues/ `[WARN]`
- 大问题 → 双轨 `[CRITICAL]`
- 阻塞紧急 → SendMessage 推送
```

---

## 落地清单 (按顺序执行)

| 步骤 | 任务 | 时长 |
|------|------|------|
| 1 | 写 `master/briefs/README.md` + `_template.md` (9 字段) | 30 分钟 |
| 2 | 写第 1 批 7 个 brief (S0-04/15/16/17/18/22/29) | 3 小时 |
| 3 | 更新 `harness.config.json` 增加 `l3-v4-lite` 模式 | 20 分钟 |
| 4 | 写 `knowlage/INDEX.md` 索引文件 | 1 小时 |
| 5 | 更新每个子项目 `CLAUDE.md` 反馈协议段 | 30 分钟 |
| 6 | 派 1 个 infra-agent 试点 (做 S0-15) | 2 小时 |
| 7 | 试点复盘 → 调整 brief 模板 → 批量写第 2 批 | 2 小时 |

**合计: 约 9 小时 → 整套机制跑起来**

---

## 后续

- ✅ 已转 ACCEPTED
- ⏭️ 下一步: 按"落地清单"执行 (步骤 1-7)
- 📊 监控指标: 子 agent 平均启动时间 < 5 分钟, 平均 context 占用 < 30K
- 🔄 复盘节点: Sprint 0 完工 (M1 里程碑) 时回顾本 ADR 是否需要调整

---

*提议人: 用户 + 教练 · 2026-06-07*
*拍板人: 用户 · 2026-06-07*
*状态: 🟡 PROPOSED → ✅ ACCEPTED*
