# ADR 0022 · 前端实现以 5 个 HTML 原型 + 真实截图为权威参考

## 状态

✅ **ACCEPTED · 已采纳** (2026-06-08)

> 关联: `docs/adr/0011-frontend-vue3-tiptap-pinia.md` · `docs/adr/0007-editor-3-column-18-50-32.md`
> 关联可视化: `explain/21-discussion-summary.html`

---

## 背景

主控前期文档已确定前端技术栈为 Vue 3 + Vite + TipTap + Pinia + Tailwind, 并记录云笔真实截图与编辑器三栏比例。

2026-06-08 讨论中, 用户指出前端资料中应有 **5 个 HTML 原型图**。经搜索确认, 原型不在 `knowlage/` 目录内, 而在 `write_clone/docs/frontend-handoff/` 与 `write_clone/docs/design/handoff/`。

因此需要明确: 前端 agent 实现 UI 时, 哪些文件是权威设计参考。

---

## 决策

前端实现以以下两类资料为权威参考:

### 1. 5 个 HTML 原型图

工程师优先使用 `frontend-handoff` 干净版:

```text
C:/Users/Administrator/Desktop/claude/write_clone/docs/frontend-handoff/
├── README.md
├── PROTOTYPE-READING-NOTES.md
├── handoff-F001-lib.md
├── handoff-F002-editor.md
├── handoff-F003-create.md
├── handoff-F004-login.md
├── handoff-F005-settings.md
└── pages/
    ├── lib.html
    ├── editor.html
    ├── create.html
    ├── login.html
    └── settings.html
```

设计整合版作为补充参考:

```text
C:/Users/Administrator/Desktop/claude/write_clone/docs/design/handoff/
├── f001-项目库-v1.html
├── f002-编辑器-v1.5.html
├── f003-创建小说-v1.html
├── f004-登录-v1.html
└── f005-设置-v1.html
```

### 2. 135 张真实产品截图

真实截图位置:

```text
C:/Users/Administrator/Desktop/claude/write_clone/knowlage/raw/screenshots/
```

截图用于补充真实比例、交互状态、字段文案、按钮状态和细节样式。

---

## Sprint 0 对应关系

| 原型 / 截图 | Sprint 任务 | 用途 |
|-------------|-------------|------|
| `pages/login.html` | S0-23 | 登录 / 注册页 |
| `pages/lib.html` | S0-24 | 项目库 / 项目列表 |
| `pages/editor.html` | S0-25 / S0-26 / S0-27 / S0-28 | 编辑器三栏 / TipTap / 大纲树 / AI 面板 |
| `pages/settings.html` | S0-23 / S0-30 | 用户设置 / AI 配置参考 |
| `pages/create.html` | Sprint 1+ / Sprint 0 简版 | 创建小说 / 11 步向导参考 |
| `raw/screenshots/*.png` | 全部前端任务 | 真实云笔 UI 细节补充 |

---

## 使用规则

1. **HTML 原型优先**: frontend-agent 实现页面时先读对应 `pages/*.html` 与 `handoff-F*.md`。
2. **截图补细节**: 原型没覆盖的状态, 用 `knowlage/raw/screenshots/` 补。
3. **contracts 定数据**: UI 字段和 API 调用仍以 `contracts/` 为最终权威。
4. **不复制原型**: 当前不把外部 HTML 复制进 master, 只记录路径引用。
5. **不改 knowlage**: `knowlage/` 仍保持只读。

---

## 影响

- frontend-agent 的 brief 必须引用对应 HTML 原型和 handoff 文档。
- Sprint 0 前端不再只靠文字描述复刻, 而是按 HTML 原型 + 截图实现。
- `README.md` 导航应提示前端实现参考 ADR 0022。
- 后续如外部路径迁移, 主控需要更新本 ADR 或复制快照到 master。

---

## 暂不做

- 不复制 5 个 HTML 到 master。
- 不创建单独 `docs/frontend-prototypes.md`。
- 不改 frontend 代码。
- 不写 frontend brief。

---

## 后续

等开始写 frontend 相关 brief 时, 每个 brief 增加“设计参考”字段:

```markdown
## 🎨 设计参考
- HTML 原型: C:/Users/Administrator/Desktop/claude/write_clone/docs/frontend-handoff/pages/editor.html
- 交接文档: C:/Users/Administrator/Desktop/claude/write_clone/docs/frontend-handoff/handoff-F002-editor.md
- 真实截图: C:/Users/Administrator/Desktop/claude/write_clone/knowlage/raw/screenshots/screenshot-editor-main.png
```

---

*提议人: 用户 + 教练 · 2026-06-08*
*拍板人: 用户 · 2026-06-08*
