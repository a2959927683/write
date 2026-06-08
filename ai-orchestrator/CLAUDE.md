# ai-agent 边界规则

## 可改范围

- `ai-orchestrator/`
- 与 AI orchestrator 任务明确相关的测试文件, 仅在 brief 指定时修改

## 禁止范围

- 不修改 `contracts/`, 除非主控 brief 明确授权。
- 不修改 `backend/`, `frontend/`, `infra/`, `knowledge-graph/`。
- 不修改主控公共文件: `README.md`, 根目录 `CLAUDE.md`, `feature_list.json`, `progress.txt`。

## AI 约束

- provider、模型、SSE 事件必须遵守 `contracts/ai/` 与 `contracts/events/`。
- 系统池 + BYOK、MiniMax token plan 等预算规则以 ADR 0021 为准。

## Git 规则

- 每个任务使用独立 worktree 和分支: `feature/S0-XX-short-name`。
- 提交格式: `[S0-XX] feat(scope): 中文说明`。
- 开工前运行: `python scripts/install-git-guard.py`。

## 回流

- 小问题写 `progress.txt` 的 `[INFO]`。
- 阻塞或契约错误写 `[CRITICAL]`, 并停手等主控仲裁。
