# 15 · 知识库引用索引 (主控记录)

> 来源: `C:\Users\Administrator\Desktop\claude\write_clone\knowlage\`
> 主控 v1.0 启动时, Claude Code 必须先读 `knowlage/CLAUDE.md`
> **注意**: 这是主控的**只读知识库**, 不可修改

## 知识库三层结构 (Karpathy LLM Wiki 方法论)

```
knowlage/
├── raw/          (Layer 1: 原始资料, 只读, LLM 不可修改)
├── wiki/         (Layer 2: 知识库, LLM 全权维护)
└── CLAUDE.md     (Layer 3: Schema, 共同演进)
```

## 87 个 wiki 页面 (主控全部已深度阅读)

### Overview (2 页)
- `wiki/overview/产品全景.md` — 综合产品概览
- `wiki/overview/技术选型.md` — 综合技术栈选型

### Concepts (5 页)
- `wiki/concepts/AI辅助写作.md` (authoritative) — 六大操作/16 context/SSE/12 厂商
- `wiki/concepts/世界观管理系统.md` (authoritative) — **17 模块** (2026-06-03 升级)
- `wiki/concepts/长篇小说一致性维护.md` (superseded → 冲突清单 C01)
- `wiki/concepts/伏笔管理.md` (superseded → World Tab 伏笔管理 #13)
- `wiki/concepts/蒸馏机制.md` (authoritative) — AI 摘要→上下文压缩

### Comparisons (3 页)
- `wiki/comparisons/AI小说写作工具竞品对比.md`
- `wiki/comparisons/世界观管理系统横向对比.md`
- `wiki/comparisons/定价模式对比.md`

### Entities (6 页)
- `wiki/entities/云笔AI小说写作助手.md` (主对标)
- `wiki/entities/DeepSeek.md`
- `wiki/entities/NovelAI.md`
- `wiki/entities/NovelCrafter.md`
- `wiki/entities/Sudowrite.md`
- `wiki/entities/阅文集团.md`

### Sources (71 页)

#### 产品 (8 页)
- `wiki/sources/产品概述.md`
- `wiki/sources/落地页与市场定位.md`
- `wiki/sources/项目管理页与主题系统.md`
- `wiki/sources/小说创建流程详解.md`
- `wiki/sources/复刻指南与成本估算.md`
- `wiki/sources/风险评估与实施路线.md`
- `wiki/sources/技术架构与部署方案.md`
- `wiki/sources/功能设计与创新.md`

#### API (16 页)
- `wiki/sources/API认证与架构.md`
- `wiki/sources/API端点清单-核心模块.md`
- `wiki/sources/API端点清单-世界设定与叙事.md`
- `wiki/sources/API端点清单-辅助与管理.md`
- `wiki/sources/API响应-AI模块详情.md`
- `wiki/sources/API响应-TTS与对话.md`
- `wiki/sources/API响应-世界观与故事核心.md`
- `wiki/sources/API响应-力量体系详解.md`
- `wiki/sources/API响应-地图与势力.md`
- `wiki/sources/API响应-大纲数据结构.md`
- `wiki/sources/API响应-新发现与设计问题.md`
- `wiki/sources/API响应-物品货币金手指.md`
- `wiki/sources/API响应-统计规则文笔.md`
- `wiki/sources/API响应-角色数据.md`
- `wiki/sources/API响应-通用约定与认证.md`
- `wiki/sources/API响应-项目与章节.md`

#### 编辑器 (3 页)
- `wiki/sources/编辑器UI架构.md`
- `wiki/sources/2026-05-31 编辑器界面与无障碍树分析.md` (superseded)
- `wiki/sources/2026-05-31 Playwright实地调研.md` (superseded)

#### 市场 (1 页)
- `wiki/sources/AI小说市场格局.md`

#### AI 功能 (4 页)
- `wiki/sources/AI功能设计与交互.md`
- `wiki/sources/AI模型与长文本技术.md`
- `wiki/sources/AI生成模式与蒸馏机制.md`
- `wiki/sources/2026-06-01 AI功能测试报告.md`

#### World Tab 2026-06-03 升级 (30 页)
**A1-A5 批次原始研究** (5 页):
- `wiki/sources/2026-06-03 World Tab A1 世界基础.md`
- `wiki/sources/2026-06-03 World Tab A2 世界进阶.md`
- `wiki/sources/2026-06-03 World Tab A3 世界补充.md`
- `wiki/sources/2026-06-03 World Tab A4 叙事核心.md`
- `wiki/sources/2026-06-03 World Tab A5 叙事尾部.md`

**17 模块级 source** (17 页):
- `wiki/sources/2026-06-03 World Tab 世界观设定 #1.md`
- `wiki/sources/2026-06-03 World Tab 故事核心 #2.md`
- `wiki/sources/2026-06-03 World Tab 地理地图 #3.md`
- `wiki/sources/2026-06-03 World Tab 势力阵营 #4.md`
- `wiki/sources/2026-06-03 World Tab 货币体系 #5.md`
- `wiki/sources/2026-06-03 World Tab 物品列表 #6.md`
- `wiki/sources/2026-06-03 World Tab 力量体系 #7.md`
- `wiki/sources/2026-06-03 World Tab 功法体系 #8.md`
- `wiki/sources/2026-06-03 World Tab 特殊设定 #9.md`
- `wiki/sources/2026-06-03 World Tab 大纲设定 #10.md`
- `wiki/sources/2026-06-03 World Tab 角色管理 #11.md`
- `wiki/sources/2026-06-03 World Tab 人物关系图 #12.md`
- `wiki/sources/2026-06-03 World Tab 伏笔管理 #13.md`
- `wiki/sources/2026-06-03 World Tab 情节脉络 #14.md`
- `wiki/sources/2026-06-03 World Tab 支线故事 #15.md`
- `wiki/sources/2026-06-03 World Tab 时间线 #16.md`
- `wiki/sources/2026-06-03 World Tab 已经历事件 #17.md`

**总览与规范** (5 页):
- `wiki/sources/2026-06-03 World Tab MASTER REFERENCE.md` (主权威)
- `wiki/sources/2026-06-03 World Tab UI 通用范式.md`
- `wiki/sources/2026-06-03 World Tab API 端点总览.md`
- `wiki/sources/2026-06-03 World Tab 抽屉 UI 验证.md`

#### 早期 5/31 文档 (5 页, 大部分 superseded)
- `wiki/sources/2026-05-31 云笔AI产品全景分析.md` (superseded)
- `wiki/sources/2026-05-31 深度功能分析.md` (superseded)
- `wiki/sources/2026-05-31 编辑器界面与无障碍树分析.md` (superseded)

#### 早期 6/01 文档 (8 页, 多数 superseded)
- `wiki/sources/2026-06-01 AI小说系统全面研究报告.md`
- `wiki/sources/2026-06-01 API逆向工程报告.md`
- `wiki/sources/2026-06-01 产品逆向工程综合报告.md`
- `wiki/sources/2026-06-01 小说创建流程分析.md`
- `wiki/sources/2026-06-01 落地页分析.md`
- `wiki/sources/2026-06-01 项目管理页分析.md`

#### 冲突追踪 (1 页)
- `wiki/sources/_conflicts/2026-06-03 冲突清单.md` (★ 主控权威)

#### 世界设定/叙事 (7 页, DEPRECATED, 不要读)
- `wiki/sources/世界设定-世界观与故事核心.md` (DEPRECATED)
- `wiki/sources/世界设定-力量体系与物品系统.md` (DEPRECATED)
- `wiki/sources/世界设定-势力阵营与货币体系.md` (DEPRECATED)
- `wiki/sources/世界设定-地理地图.md` (DEPRECATED)
- + 早期叙事管理 3 页 (DEPRECATED)

### raw/ (人类领地, 只读)

主控的 50 个并行 agent 已完整扫描以下 19 个关键文件:

**产品 (4)**:
- `raw/product/10-landing-page-analysis.md`
- `raw/product/21-projects-page-analysis.md`
- `raw/product/30-novel-creation-flow.md`
- `raw/product/99-comprehensive-product-report.md`

**编辑器 (3)**:
- `raw/editor/40-world-material-modules.md`
- `raw/editor/41-world-narrative-modules.md`
- `raw/editor/50-ai-features-analysis.md`

**API (7)**:
- `raw/api/51-api-reverse-engineering.md`
- `raw/api/98-api-real-responses.md`
- `raw/api/api-01-project-chapter-outline.md`
- `raw/api/api-02-worldview-modules.md`
- `raw/api/api-03-narrative-modules.md`
- `raw/api/api-04-ai-stats-user.md`
- `raw/RESEARCH-PROTOCOL.md`

**World Tab (6)**:
- `raw/world-tab-A1-世界基础.md` (18 KB)
- `raw/world-tab-A2-世界进阶.md` (20 KB)
- `raw/world-tab-A3-世界补充.md` (20 KB)
- `raw/world-tab-A4-叙事核心.md` (40 KB)
- `raw/world-tab-A5-叙事尾部.md` (18 KB)
- `raw/world-tab-MASTER-REFERENCE.md` (96 KB, ★ 合并 v3)

**市场 (1)**:
- `raw/market/AI小说系统-全面研究报告.md`

## 状态判断规则 (主控启动必读)

启动时**第一步**判断页面 `frontmatter.status`:
- `status: authoritative` → 信任
- `status: superseded` → **必须读 superseded_by 字段**找到权威源
- `status: deprecated` → **不要读正文**, 直接跳 superseded_by
- 无 status 字段 → 默认信任 (早期页面, 待评估)

**绝不**仅凭"入度最高"或"内容最多"判断权威性。DEPRECATED 页往往入度更高, 是陷阱。

## 主控消费策略

| 任务 | 推荐 source (按权威性) |
|------|----------------------|
| **做后端** | ① API端点清单-核心模块 ② API端点清单-世界设定与叙事 ③ API端点清单-辅助与管理 ④ 2026-06-03 World Tab API 端点总览 |
| **做前端 / World Tab** | ① 2026-06-03 World Tab UI 通用范式 ② 17 个模块级 source (#1-#17) ③ 2026-06-03 World Tab MASTER REFERENCE |
| **做产品 / 复刻决策** | ① 产品概述 ② 2026-06-01 小说创建流程分析 ③ 复刻指南与成本估算 |
| **数据模型字段** | ① raw/api/98-api-real-responses ② raw/world-tab-MASTER-REFERENCE ③ contracts/schemas/*.json (主控权威) |
| **AI 调度** | ① AI功能设计与交互 ② AI生成模式与蒸馏机制 ③ AI模型与长文本技术 |

## 主控与 knowlage 的边界

| 主控 | knowlage |
|------|----------|
| **可写**: contracts/, docs/, feature_list.json, progress.txt, 颗粒化文档 | **只读**: 主控从不修改 knowlage |
| **可写**: 子项目代码 (Sprint 1+) | 人类管理 (放入资料) |
| **基于**: knowlage/wiki/ 的页面内容 | 主控成果物应该反向 link 到 knowlage/wiki/ 页面 (但不能写) |

---

*最后更新: 2026-06-07 · 主控 v1.0 · 50 个 Opus agent 深度扫描完成*
