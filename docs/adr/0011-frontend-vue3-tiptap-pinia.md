# 0011 · 前端: Vue 3 + Vite + TipTap + Pinia + Tailwind

## 状态
已采纳 · 2026-06-07

## 背景
云笔前端是 Vue 3 + TipTap + Pinia + Tailwind (来自 `wiki/sources/技术架构与部署方案.md`)。
主控需要决定: 沿用云笔技术栈, 还是改 React / Svelte?

## 决策
**主控采用 Vue 3 + Vite + TipTap + Pinia + Tailwind**, 与云笔完全一致。

## 选型

| 层面 | 选型 | 理由 |
|------|------|------|
| 框架 | **Vue 3** (Composition API) | 与云笔一致, 团队熟悉 |
| 构建 | **Vite 5** | 启动快, HMR 流畅 |
| 富文本 | **TipTap** (基于 ProseMirror) | 云笔使用, 适合长文本 |
| 状态 | **Pinia** (按 17 模块分 store) | Vue 3 官方推荐 |
| 样式 | **Tailwind CSS** + CSS 变量 | 主题系统友好 |
| 图标 | **Remix Icon** (`ri-robot-line` 等) | 云笔使用 |
| HTTP | **Axios** + **EventSource** (SSE) | RESTful + 流式 |
| 测试 | **Vitest** (单测) + **Playwright** (E2E) | 与 Vite 集成 |
| 路由 | **Vue Router 4** | — |
| 拖拽 | **vuedraggable** (基于 SortableJS) | 大纲树/列表 |

## 项目结构

```
frontend/src/
├── main.ts
├── App.vue
├── router/
│   └── index.ts
├── stores/                       # Pinia
│   ├── auth.ts
│   ├── project.ts
│   ├── chapter.ts
│   ├── outline.ts
│   ├── character.ts
│   ├── worldviews/               # 17 模块对应 17 个 store
│   │   ├── worldview.ts
│   │   ├── story-core.ts
│   │   ├── geo-map.ts
│   │   └── ... 14 more
│   ├── ai.ts
│   └── ui.ts                     # 主题/抽屉状态
├── pages/
│   ├── Landing.vue
│   ├── Login.vue
│   ├── Register.vue
│   ├── ProjectList.vue
│   ├── ProjectCreate.vue
│   ├── Editor.vue
│   └── admin/                    # 管理后台
├── components/
│   ├── layout/
│   │   ├── TopBar.vue
│   │   ├── LeftPanel.vue
│   │   ├── RightPanel.vue
│   │   └── StatusBar.vue
│   ├── editor/
│   │   ├── EditorLayout.vue
│   │   ├── TipTapEditor.vue
│   │   ├── OutlineTree.vue
│   │   └── AutoSaveIndicator.vue
│   ├── world-tab/                # 17 模块对应 17 个组件
│   │   ├── ModuleDrawer.vue      # 通用抽屉容器
│   │   ├── WorldviewEditor.vue
│   │   ├── StoryCoreEditor.vue
│   │   └── ... 15 more
│   ├── ai/
│   │   ├── AIPanel.vue           # 6 按钮
│   │   ├── AIStreamRenderer.vue  # SSE
│   │   └── AISettings.vue
│   └── ui/                       # 通用组件
│       ├── Button.vue
│       ├── Drawer.vue
│       ├── Modal.vue
│       └── ...
├── composables/
│   ├── useAIStream.ts
│   ├── useHeartbeat.ts
│   ├── useAutoSave.ts
│   ├── useAuth.ts
│   └── ...
├── api/                          # Axios 实例 + 端点
│   ├── client.ts
│   ├── auth.ts
│   ├── project.ts
│   └── ...
├── types/                        # TypeScript 类型
│   └── (re-export from contracts/schemas)
└── utils/
```

## 主题系统 (15 主题)

```typescript
// stores/ui.ts
export const useUIStore = defineStore('ui', () => {
  const theme = ref<'light' | 'dark' | 'sepia' | ...>('dark')

  const themes = [
    { key: 'dark', name: '深邃', primary: '#3B82F6', bg: '#0F172A' },
    { key: 'light', name: '明亮', primary: '#2563EB', bg: '#FFFFFF' },
    { key: 'sepia', name: '羊皮', primary: '#92400E', bg: '#FEF3C7' },
    // ... 12 more
  ]

  return { theme, themes }
})
```

## 影响
- 所有 17 World Tab 模块的 Vue 组件共享 `ModuleDrawer` 容器
- TipTap 自定义节点 (伏笔标注, 人物标注, 时间标注)
- Pinia store 与 17 World Tab 模块**一一对应** (1:1)
- Tailwind CSS 变量 + dark mode

## 后续
- 移动端布局 (Sprint 3+)
- 国际化 (i18n, Sprint 2+)
- 离线编辑 (Service Worker, Sprint 4+)
