# 07 · 11 条冲突裁决 (主控权威)

> 来源: `C:\Users\Administrator\Desktop\claude\write_clone\knowlage\wiki\sources\_conflicts\2026-06-03 冲突清单.md`
> 11 条事实点, 以 2026-06-03 新研究为准
> 主控全盘采纳 2026-06-03 裁决

| # | 维度 | 早期版本 (2026-05-31) | 2026-06-03 新研究 | 主控最终裁决 |
|---|------|----------------------|-------------------|--------------|
| **C01** | World Tab 模块总数 | 16 | **17** (含大纲设定独立) | ✅ **17** (Master Reference 2026-06-03) |
| **C02** | 大纲设定位置 | 归入"叙事管理"二级 | **独立为 World Tab 一级入口** | ✅ **独立 (#10)** |
| **C03** | 角色类型 | 8 | **24** + 三层性格 + 7 段背景 | ✅ **24 类型** |
| **C04** | 角色数据规模 | 预设 7-20 | 取决于项目 | ✅ **不预设** (玄穹开 20, 烬都奇谭 7) |
| **C05** | 伏笔管理 | 3 类型 | **6 类型 + 10 埋设模式** | ✅ **6+10** |
| **C06** | 时间线类型 | 5 | **7** (出场/战斗/揭秘/关系/地点/势力/其他) | ✅ **7** |
| **C07** | 大纲结构 | 多级 | **卷-章 二级树** (5 字段核心) | ✅ **二级树** |
| **C08** | 力量体系 | 8 境界 | **11 境界 + 6 能力 + 5 限制 + 4 路径** | ✅ **11+6+5+4** |
| **C09** | 势力类型 | 6 | **9** (组织/国家/门派/家族/商会/学院/宗教/部落/其他) | ✅ **9** |
| **C10** | 项目 ID 范围 | 1-10000 | **6310 / 9657 / 9529 / 9320** | ✅ **真实 ID 范围** |
| **C11** | AI 厂商数 | 10 | **12** | ✅ **12** |

## 各冲突影响范围

### C01 + C02 — 模块数与大纲独立
- **影响**: 17 个 World Tab 模块, 大纲设定独立为一级入口 (`/outlines` 端点路径与原 `/worldviews` 同级)
- **Schema 调整**: `outline.json` 独立, 不再嵌在 `worldview.json` 的 `ext` 中
- **前端调整**: World Tab 抽屉新增"大纲设定"卡片 (#10), 不再归入"叙事"二级

### C03 + C04 — 角色 24 类型 + 不预设规模
- **影响**: `character.json` 中 `类型` enum 扩为 24 个
- **业务规则**: 不写死"每个项目最多 20 个角色", 由用户自由创建
- **示例项目差异**: 玄穹开 20 角色, 烬都奇谭 7 角色

### C05 — 伏笔 6+10
- **影响**: `foreshadow.json` 中 `类型` enum 为 6 个, `埋设模式` enum 为 10 个
- **API 调整**: `/foreshadows/stats` 增加按 `埋设模式` 统计

### C06 — 时间线 7 类型
- **影响**: `timeline.json` 的 Event 类型 enum 为 7 个 (出场/战斗/揭秘/关系/地点/势力/其他)
- **前端调整**: 章节时间线 UI 增加"关系"和"势力"两个 chip 颜色

### C07 — 大纲卷-章二级
- **影响**: `outline.json` 的 `类型` enum 简化为 `volume/chapter`
- **数据库调整**: 删除"卷中卷"三级嵌套逻辑
- **API 调整**: `/outlines/:id/move` 只允许跨父节点移动, 不允许跨级

### C08 — 力量体系 11+6+5+4
- **影响**: `power-system.json` 的 4 个 JSONB 数组边界清晰
- **数据库调整**: 子表 `power_realms` (11 境界) + `power_abilities` (6 能力) 可选拆分
- **境界算法**: 战力系数 = f(境界等级) 用于跨境界对决 AI 推演

### C09 — 势力 9 类型
- **影响**: `faction.json` 的 `类型` enum 扩为 9 个
- **业务规则**: 9 类型对应 9 种颜色 (关系图用)

### C10 — 项目 ID 范围
- **影响**: 实际观察的样本项目 ID 是 6310 / 9657 / 9529 / 9320, 主控 BIGSERIAL 自增无影响
- **数据迁移**: 复刻时不需要强制保持 ID 一致, 行为上保持一致即可

### C11 — AI 厂商 12 家
- **影响**: `providers.json` 注册 12 家 (DeepSeek / Anthropic / OpenAI / Google / 智谱 / 通义 / 文心 / 月之暗面 / 豆包 / 讯飞 / 腾讯 / 本地)
- **优先级**: DeepSeek 为默认 (中文网文适配 + 价格低)

## 11 条冲突与主控 contracts/ 的对应

| 冲突 | 主控 Schema / Config 文件 |
|------|------------------------|
| C01 | (顶层目录结构) |
| C02 | `contracts/schemas/outline.json` (独立) |
| C03 | `contracts/schemas/world-setting/character.json` (24 enum) |
| C04 | (无 schema 约束, 业务层处理) |
| C05 | `contracts/schemas/world-setting/foreshadow.json` (6+10 enum) |
| C06 | `contracts/schemas/world-setting/timeline.json` (7 enum) |
| C07 | `contracts/schemas/outline.json` (volume/chapter) |
| C08 | `contracts/schemas/world-setting/power-system.json` (11+6+5+4) |
| C09 | `contracts/schemas/world-setting/faction.json` (9 enum) |
| C10 | (无影响) |
| C11 | `contracts/ai/providers.json` (12 厂商) |

## 冲突处理原则

1. **权威性优先**: 所有 11 条冲突以 2026-06-03 为准
2. **早于 2026-06-01 的 source**: 默认 superseded, 不直接读 (见 `knowlage/CLAUDE.md` 启动指令)
3. **新发现**: 在主控 `progress.txt` 追加, 必要时创建新的 source 页

---

*最后更新: 2026-06-07 · 主控 v1.0*
