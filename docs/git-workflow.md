# Git Workflow · 本地护栏优先

> 权威来源: `docs/adr/0018-多agent-git协作规则.md`
> 当前策略: 不绑卡、不使用付费 Gitee Go、不依赖 GitHub Actions。本地 hook + 主控手动检查是硬规则。

---

## 1. 分支与 worktree

每个 Sprint 任务一个分支, 每个 agent 一个独立 worktree。

```bash
git worktree add ../wt-S0-15 -b feature/S0-15-docker
```

命名规则:

| 类型 | 分支格式 | 示例 |
|------|----------|------|
| Sprint 任务 | `feature/S0-XX-short-name` | `feature/S0-15-docker` |
| 主控治理 | `codex/topic-name` | `codex/git-guard` |
| 紧急修复 | `fix/S0-XX-short-name` | `fix/S0-18-auth-token` |

---

## 2. Commit 规范

提交标题必须符合:

```text
[S0-18] feat(auth): 实现登录端点
[ADR-0018] chore(git): 落地 Git 护栏
```

允许的 type:

```text
feat fix docs refactor test chore ci build perf style revert
```

规则:

- Sprint 任务使用 `[S0-XX]`。
- 主控 ADR / 治理任务使用 `[ADR-XXXX]`。
- scope 使用小写英文或短横线, 如 `auth`, `git`, `infra`, `frontend-shell`。
- 说明可以用中文, 但必须具体。

---

## 3. 本地护栏是硬规则

每个 checkout / worktree 首次开工前运行:

```bash
python scripts/install-git-guard.py
```

验证:

```bash
git config --get core.hooksPath
git config --get gc.reflogExpire
git config --get gc.reflogExpireUnreachable
```

期望:

```text
.githooks
90.days
90.days
```

---

## 4. Contracts 保护

默认所有子 agent 禁止修改 `contracts/`。

只有主控明确发起契约任务时, 才允许:

```powershell
$env:AGENT_TYPE='orchestrator'
git commit -m "[S0-09] docs(contracts): 补充 chapter API 契约"
```

契约提交必须同时:

1. 修改对应 `contracts/` 文件。
2. 追加 `contracts/CHANGELOG.md`。
3. 通过 `python scripts/contract-lint.py`。

---

## 5. 主控合并前手动检查

每次合并 PR / 任务分支前, 主控必须在本地运行:

```bash
python scripts/contract-lint.py
python -m py_compile .githooks/pre-commit .githooks/commit-msg scripts/install-git-guard.py scripts/contract-lint.py
git status --short
```

预期:

- `contract-lint passed`
- 只出现已知 Sprint 0 缺口 warning
- Python 脚本编译无输出、退出码 0
- `git status --short` 中没有意外 staged 文件

后续业务代码出现后, 再按子项目补:

- backend: 单测 / build
- frontend: typecheck / build
- ai-orchestrator: 单测
- infra: docker compose smoke test

---

## 6. 远程仓库策略

- GitHub 用作主要代码托管和 PR 记录。
- Gitee 保留为备份远程。
- 当前不使用 GitHub Actions, 因账号 billing locked 且用户不打算绑卡。
- 当前不使用 Gitee Go, 因需要付费/开通。

远程检查不是硬依赖。本地检查通过 + 主控 review 才是合并依据。

---

## 7. 冲突处理

优先级:

1. 不同目录自动合并。
2. 同目录不同文件由对应 owner 处理。
3. 同文件冲突交给主控仲裁。
4. 契约冲突必须停手, 在 `progress.txt` 记录 `[CRITICAL]`。

---

## 8. 回滚

每个任务分支必须可以单独回滚。

```bash
git reflog
git reset --hard <safe-commit>
```

本仓库通过 `scripts/install-git-guard.py` 把 reflog 保留期设置为 90 天。
