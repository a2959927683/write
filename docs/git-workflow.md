# Git Workflow · 多 Agent 协作护栏

> 权威来源: `docs/adr/0018-多agent-git协作规则.md`
> 当前远程: Gitee (`origin`)
> 推荐迁移方向: GitHub 为主远程, 使用 GitHub Actions 免费 CI

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

主控分支 `master-codex` 必须保持可回滚、可审查。

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

## 3. Contracts 保护

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

## 4. 安装本地护栏

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

## 5. GitHub 远程护栏 (推荐)

仓库内提供 GitHub Actions 流水线:

```text
.github/workflows/git-guard.yml
```

它会运行:

- `python scripts/contract-lint.py`
- Python hook 脚本语法检查

GitHub 仓库页面需要手动设置保护分支:

1. 打开 GitHub 仓库 `Settings`。
2. 进入 `Branches`。
3. 添加规则保护 `master-codex` 或 `master`。
4. 勾选 `Require a pull request before merging`。
5. 勾选 `Require status checks to pass before merging`。
6. 选择 `Contract and hook guard` 作为必过检查。

迁移命令示例:

```bash
git remote rename origin gitee
git remote add origin https://github.com/<your-name>/<repo>.git
git push -u origin master-codex
git push origin codex/git-guard
```

---

## 6. Gitee 远程护栏 (备用)

仓库内提供 Gitee Go 流水线:

```text
.workflow/GitGuardPipeline.yml
```

它会运行:

- `python scripts/contract-lint.py`
- Python hook 脚本语法检查

Gitee Go 需要付费/开通时, 本项目不强依赖它。若仍使用 Gitee, 页面还需要手动设置保护分支:

1. 打开 Gitee 仓库设置。
2. 找到分支保护规则。
3. 保护 `master-codex`。
4. 禁止直接 push。
5. 要求 Pull Request / Merge Request。
6. 要求流水线通过后再合并。

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
