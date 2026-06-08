# ADR 0018 · 多 Agent Git 协作规则

## 状态

✅ **ACCEPTED · 已采纳** (2026-06-07)
> 提议日期: 2026-06-07
> 拍板日期: 2026-06-07
> 关联讨论: `docs/discussions/2026-06-07-git协作规则.md` (RESOLVED)
> 关联 HTML: `explain/10-git多agent协作规则-讨论稿.html` · `explain/11-git协作规则-教练推荐答案.html`

---

## 背景

主控将派多个子 agent 并行干活 (frontend / backend / ai-orchestrator / knowledge-graph / infra)。
5 个 agent 同时改代码, **如果没规则 = 必爆炸**。

---

## 决策

### ✅ 已达成共识 (1 条 · 早期)

**A1:** 用 `git worktree` 隔离工作目录, 每个子 agent 在独立 worktree 干活。

### ✅ 5 个核心问题决策 (本次拍板)

#### Q1 · 分支策略 → **一任务一分支 + worktree (B+C 混合)** ✅

```
main (主控守护, 永远稳定)
  ├─ feature/S0-18-auth      ← backend agent 在 worktree-1 干
  ├─ feature/S0-22-vue-shell ← frontend agent 在 worktree-2 干
  └─ feature/S0-15-docker    ← infra agent 在 worktree-3 干
```

**理由:**
- 一任务一分支 → 完工合一个, 失败回滚一个, **互不连坐**
- worktree 隔离 → 物理目录分开, **不会改到对方文件**
- AI agent 适合"短命分支" (几小时完工就合)

**命令模板:**
```bash
# 创建任务分支 + worktree
git worktree add ../wt-S0-18 -b feature/S0-18-auth

# 子 agent 在 ../wt-S0-18 干活, 不会影响 master/
```

#### Q2 · commit 规范 → **任务 ID 前缀 + Conventional 中文 (C 混合版)** ✅

**模板:**
```
[S0-18] feat(auth): 实现登录端点 + JWT 签发

- 添加 /api/auth/login 端点
- 实现 bcrypt 密码校验
- 返回 7 天有效期的 JWT token
- 单测覆盖率 90%

契约: contracts/openapi/auth.yaml
brief: master/briefs/S0-18-auth.md

Co-Authored-By: backend-agent <agent@orchestrator.local>
```

**4 个关键点:**
1. **任务 ID 前缀** `[S0-18]` → 立即定位到主控任务
2. **Conventional type** `feat/fix/docs/refactor/test/chore` → CI 可解析
3. **scope 模块** `(auth)` → 一眼看出改哪个模块
4. **Co-Authored-By** → 标记哪个 agent 做的, 出问题好定位

#### Q3 · 合并节奏 → **两档制 (A+D 混合)** ✅

**判断标准:** 看 `feature_list.json` 任务的 `subproject` 字段。

**🟢 普通任务 → CI 自动合**
```
子 agent 完工 → push feature/S0-XX → 触发 GitHub Actions
  ├─ 跑 contract-lint (契约一致性)
  ├─ 跑 unit test
  ├─ 跑 build
  └─ 全过 → 自动 squash merge 到 main
```

**适用:** `backend` / `frontend` / `ai-orchestrator` 子项目

**🔴 敏感任务 → 主控人审才合**

**适用:**
- 改了 `contracts/` 的任务
- 跨模块的任务
- 数据库迁移任务
- 影响主链的任务
- subproject = `contracts` 或 `master`

#### Q4 · 冲突解决 → **3 层防御 (C+A+D)** ✅

**第 1 层 · 边界约束 (99% 的情况)**

在每个子项目 CLAUDE.md 写死:
- backend-agent **只能改** `backend/`
- frontend-agent **只能改** `frontend/`
- 谁都**不能改** `contracts/` (除非主控明确派任务)
- 公共文件 (README/CLAUDE.md) **只能主控改**

**第 2 层 · 自动合并 (真冲突时)**

`git rebase + 自动 merge`:
- 不同文件 → git 自动合 ✅
- 同文件不同行 → git 自动合 ✅
- 同文件同行 → 进第 3 层 ⚠️

**第 3 层 · 主控仲裁 (万分之一)**

- 主控读两边代码, 判谁对
- 在 progress.txt 记录裁决
- 必要时开 ADR
- 败方 agent 重新基于胜方代码做

#### Q5 · 契约保护 → **pre-commit hook + CI 双保险 (A+B)** ✅

> 2026-06-08 实施备注:
> 当前远程 `origin` 是 Gitee, 因此远程兜底从原讨论中的 GitHub Actions 调整为 Gitee Go (`.workflow/GitGuardPipeline.yml`)。
> 本地 hook 也从不可提交的 `.git/hooks/` 调整为可提交的 `.githooks/`, 再用 `core.hooksPath=.githooks` 启用。
> 决策意图不变: 本地先拦截, 远程再兜底。

**🛡️ 第 1 道防线 · pre-commit hook (本地拦截)**

```bash
# .git/hooks/pre-commit
#!/bin/bash

# 检查是否改了 contracts/
CHANGED=$(git diff --cached --name-only | grep "^contracts/")

if [ -n "$CHANGED" ]; then
  # 检查是不是主控 agent 在 commit
  if [ "$AGENT_TYPE" != "orchestrator" ]; then
    echo "❌ 拒绝 commit: 子 agent 不能改 contracts/"
    echo "改动的文件:"
    echo "$CHANGED"
    echo ""
    echo "如需修改契约, 请联系主控发起 ADR。"
    exit 1
  fi
fi

# 跑契约 lint
python scripts/contract-lint.py || exit 1
```

**🛡️ 第 2 道防线 · GitHub Actions CI (远程兜底)**

```yaml
# .github/workflows/protect-contracts.yml
name: Protect Contracts
on: [pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: 检查 contracts/ 改动
        run: |
          if git diff --name-only origin/main | grep "^contracts/"; then
            if [[ "${{ github.actor }}" != "orchestrator-bot" ]]; then
              echo "❌ 只有主控可以改 contracts/"
              exit 1
            fi
          fi
      - name: 跑 contract-lint
        run: python scripts/contract-lint.py
```

### ✅ 3 个延伸决策

#### E1 · push 远程 → **✅ 必须 push** ✅
否则 CI 跑不了 + 主控看不到进度。

子 agent 每完成一个 commit, 立即 push 到对应的 feature 分支。

#### E2 · tag 规则 → **Sprint 对应版本号** ✅

| Sprint | tag | 标志 |
|--------|-----|------|
| Sprint 0 完工 | `v0.1.0` | M1 主链跑通 |
| Sprint 1 完工 | `v0.2.0` | M2 17 模块齐备 |
| Sprint 2 完工 | `v0.3.0` | M3 Beta 测试 |
| Sprint 3 公开上线 | `v1.0.0` | M4 v1.0 |
| Sprint 3 商业化 | `v1.1.0` | M5 商业化 |

#### E3 · reflog 兜底 → **✅ 必须保留 90 天** ✅

```bash
# .gitconfig 配置
git config --global gc.reflogExpire 90.days
git config --global gc.reflogExpireUnreachable 90.days
```

子 agent 误删/误改文件 → 主控可用 `git reflog` 恢复。

---

## 备选

### 备选 A · GitHub Flow 严格版
- 一 agent 一分支 + PR + CI lint + 主控批准合
- ✅ 流程严格, 不易出错
- ❌ 流程重, 多 agent 速度受限

### 备选 B · Trunk-Based + Worktree 轻量
- 都基于 main, worktree 隔离, 本地频繁 commit, 定期 rebase
- ✅ 速度快
- ❌ 冲突频繁需自动化

### 备选 C (已采纳) · 一任务一分支 + worktree + 两档制合并
- ✅ 任务隔离清晰
- ✅ 普通任务自动合 (速度), 敏感任务人审 (安全)
- ✅ 适配 AI agent 短命分支特性
- ❌ 需 GitHub Actions CI 配套

---

## 决策依赖图 (验证一致性)

```
Q1 (一任务一分支) ──► Q3 (两档制合并: 按 subproject 判)
                          ↓
Q2 ([S0-XX] 前缀) ────► Q4 (3 层防御: 边界 → 自动 → 仲裁)
                          ↓
                       Q5 (双保险: hook + CI)
```

所有决策**互相一致, 无冲突** ✅

---

## 影响范围

落地需要更新:

| 文件 | 改动 |
|------|------|
| `master/CLAUDE.md` | 新增 "git 规则" 段 |
| `.githooks/pre-commit` + `.githooks/commit-msg` | 新建 (Q5 第 1 道防线, 可提交) |
| `.workflow/GitGuardPipeline.yml` | 新建 (Q5 第 2 道防线, Gitee Go) |
| `scripts/contract-lint.py` | 新建 (S0-36 任务) |
| `scripts/install-git-guard.py` | 新建 (启用 `.githooks/` + reflog 90 天) |
| 每个子项目 `CLAUDE.md` | 新增 "边界约束" + "commit 规范" 段 |
| `.gitconfig` | reflog 90 天 (E3) |
| `docs/git-workflow.md` | 新增工作流文档 |

---

## 落地清单 (按顺序执行)

| 步骤 | 任务 | 时长 |
|------|------|------|
| 1 | 写 `.git/hooks/pre-commit` | 10 分钟 |
| 2 | 写 `.github/workflows/protect-contracts.yml` | 15 分钟 |
| 3 | 写 `scripts/contract-lint.py` | 20 分钟 |
| 4 | 更新主控 `CLAUDE.md` 加 git 规则段 | 10 分钟 |
| 5 | 更新每个子项目 `CLAUDE.md` 边界段 (×5) | 25 分钟 |
| 6 | 配置 `.gitconfig` reflog 90 天 | 5 分钟 |
| 7 | 写 `docs/git-workflow.md` 工作流文档 | 30 分钟 |

**合计: 约 2 小时 → 整套 git 规则上线**

---

## 后续

- ✅ 已转 ACCEPTED
- ⏭️ 下一步: 按"落地清单"执行 (步骤 1-7)
- 📊 监控指标: 0 例子 agent 改 contracts / 0 例严重冲突
- 🔄 复盘节点: Sprint 0 完工 (M1 里程碑) 时回顾本 ADR 是否需要调整

---

*提议人: 用户 + 教练 · 2026-06-07*
*拍板人: 用户 · 2026-06-07*
*状态: 🟡 PROPOSED → ✅ ACCEPTED*
