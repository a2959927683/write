# frontend-agent 边界规则

## 可改范围

- `frontend/`
- 与 frontend 任务明确相关的测试文件, 仅在 brief 指定时修改

## 禁止范围

- 不修改 `contracts/`, 除非主控 brief 明确授权。
- 不修改 `backend/`, `ai-orchestrator/`, `infra/`, `knowledge-graph/`。
- 不修改主控公共文件: `README.md`, 根目录 `CLAUDE.md`, `feature_list.json`, `progress.txt`。

## 设计权威

- 前端实现必须先读 ADR 0022 指定的 HTML 原型、handoff 文档和真实截图。
- contracts 决定数据结构和 API 调用, 原型决定视觉和交互参考。

## Git 规则

- 每个任务使用独立 worktree 和分支: `feature/S0-XX-short-name`。
- 提交格式: `[S0-XX] feat(scope): 中文说明`。
- 开工前运行: `python scripts/install-git-guard.py`。

## 回流

- 小问题写 `progress.txt` 的 `[INFO]`。
- 阻塞或契约错误写 `[CRITICAL]`, 并停手等主控仲裁。
