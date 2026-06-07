# 0007 · 三栏布局 18% / 50% / 32% (来自云笔实测)

## 状态
已采纳 · 2026-06-07

## 背景
云笔编辑器是经典三栏 IDE 布局 (来自 `wiki/sources/2026-06-01 落地页分析.md`):
- 左侧边栏 (项目/角色/世界) — 约 18%
- 中间编辑区 (TipTap 富文本) — 约 50%
- 右侧 AI 助手面板 — 约 32%

主控需要决定: 沿用云笔比例, 还是优化比例?

## 决策
**主控采用 18% / 50% / 32%**, 与云笔完全一致。

## 备选

### 备选 A: 沿用云笔 18/50/32
- ✅ 1:1 还原
- ✅ 习惯云笔的用户无感迁移
- ❌ 18% 偏窄, 角色/世界 Tab 列表可能拥挤

### 备选 B: 优化为 20/45/35
- ✅ 左侧稍宽, 容纳角色卡片
- ❌ 中间编辑区缩窄, 写作体验下降

### 备选 C: 响应式
- ✅ 不同屏幕自适应
- ❌ 失去云笔的固定感

## 实际像素

在 1920×1080 屏幕下 (云笔实测基准):
- 总宽度: 1920px
- 左侧: 约 350px (18%)
- 中间: 约 960px (50%)
- 右侧: 约 610px (32%)

## 实现

```vue
<!-- frontend/src/components/editor/EditorLayout.vue -->
<template>
  <div class="editor-layout">
    <div class="left-panel" :style="{ width: '18%' }">
      <LeftPanel />
    </div>
    <div class="center-panel" :style="{ width: '50%' }">
      <TipTapEditor />
    </div>
    <div class="right-panel" :style="{ width: '32%' }">
      <RightPanel />
    </div>
  </div>
</template>

<style>
.editor-layout {
  display: flex;
  width: 100vw;
  height: calc(100vh - 60px); /* 减去顶部菜单 */
  overflow: hidden;
}
</style>
```

## 最小宽度支持

- 最小屏幕: 1280×720
- 小于 1280: 折叠左右面板为图标按钮

## 影响
- 17 World Tab 模块卡片宽度按 18% 容器优化
- TipTap 工具栏在 50% 容器内显示
- AI 助手面板按钮在 32% 容器内显示

## 后续
- 收集用户反馈, 如果大量反馈"中间太挤", 考虑加响应式
- 移动端 (< 768px) 完全不同的布局 (单栏 + 抽屉), 暂不在 Sprint 0 范围
