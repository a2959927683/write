# 05 · 17 World Tab 模块 (主控权威清单)

> 来源: `docs/MASTER-PROJECT-SPEC.md` §3.5 + §4.6 + `knowlage/wiki/sources/_conflicts/2026-06-03 冲突清单.md`
> C01 冲突裁决: 17 模块 (Master Reference 2026-06-03 为准)
> C02 冲突裁决: 大纲设定独立为一级入口 (World Tab #10)

## 17 模块总览

| # | 模块 | 中文名 | 数据规模 | API 端点 | 优先级 |
|---|------|--------|----------|----------|--------|
| #1 | 世界观设定 | Worldview | 1 记录/项目 | 10 | P0 |
| #2 | 故事核心 | StoryCore | 1 记录/项目 (6 字段) | 4 | P0 |
| #3 | 地理地图 | GeoMap | 35 地点/项目 (6 级) | 14 | P1 |
| #4 | 势力阵营 | Faction | 9 势力/项目 (9 类型) | 14 | P1 |
| #5 | 货币体系 | Currency | 3 货币/项目 | 8 | P2 |
| #6 | 物品列表 | Item | 86 物品/项目 (17 字段) | 13 | P1 |
| #7 | 力量体系 | PowerSystem | 1 体系/项目 (11 境界 + 6 能力) | 11 | P0 |
| #8 | 功法体系 | SkillSystem | 60 类型 × 9 品级 | 12 | P2 |
| #9 | 特殊设定 | SpecialSetting | 19 类型/项目 (金手指) | 11 | P2 |
| **#10** | **大纲设定** | **OutlineSetting** | **★P0 (独立一级入口)** | **(22)** | **★P0** |
| #11 | 角色管理 | Character | 24 类型 (玄穹开 20, 烬都奇谭 7) | 24 | P1 |
| #12 | 人物关系图 | CharacterRelation | 8 关系/13 chip | 4 | P2 |
| #13 | 伏笔管理 | Foreshadow | 19 伏笔 (6 类型 + 10 模式) | 15 | P0 |
| #14 | 情节脉络 | PlotStructure | 5 模板/7 幕 | 8 | P1 |
| #15 | 支线故事 | EventLine + EventFlow + ElementBindx | 35 事件/项目 | 33 | P1 |
| #16 | 时间线 | Timeline | 7 类型 + 自定义历法 | 13 | P1 |
| #17 | 已经历事件 | EventLine (复用) | 95 事件 + 蒸馏集成 | (复用) | P1 |

## 关键模块详解

### #1 世界观设定 (Worldview) — P0

11 字段:
- `世界名称`, `世界类型`, `时代背景`, `核心规则`, `地理环境`
- `社会结构`, `历史背景`, `特殊元素`, `主要冲突`, `势力格局`, `备注`
- `ext JSONB` (历法子系统/版本历史/子表 JSON)

**关键 API**: `+ /full`, `+ /versions` (POST/PUT/rollback), `+ /sync`

**Schema**: `contracts/schemas/world-setting/worldview.json` ✅

### #2 故事核心 (StoryCore) — P0

6 字段: `主题`, `主线`, `冲突`, `高潮`, `结局`, `核心意义`

**Schema**: `contracts/schemas/world-setting/story-core.json` ✅

### #7 力量体系 (PowerSystem) — P0 (C08 裁决)

4 层嵌套结构:
- `境界列表` (11 境界, `{id, 境界名称, 境界等级, 战力系数, 境界描述, 提升条件, 能力表现, 特殊标志, 排序顺序}`)
- `能力列表` (6 能力, `{id, 能力名称, 能力类型, 能力描述, 学习条件, 消耗代价, 排序顺序}`)
- `修行路径` (4 路径, `{修行方法, 修行资源, 修行难点, 突破要点}`)
- `限制约束` (5 限制, `{使用限制, 副作用, 反噬风险, 禁忌条款}`)

**Schema**: `contracts/schemas/world-setting/power-system.json` ✅

**示例**: 星烬九考 (11 境界: 感烬 / 引烬 / 凝烬 / 锻烬 / 合烬 / 破烬 / 化烬 / 掌烬 / 御烬 / 归烬 / 神烬)

### #10 大纲设定 (OutlineSetting) — ★P0 (独立一级入口)

> C02 冲突裁决: 大纲设定**独立为 World Tab 一级入口**, 不再归入"叙事管理"二级菜单

树形自引用结构, 卷-章 二级:

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | BIGSERIAL | PK |
| `project_id` | FK | |
| `父节点ID` | FK NULL | 卷级父节点 |
| `类型` | volume/chapter | |
| `标题` | VARCHAR(255) | |
| `关联章节ID` | FK NULL | 已蒸馏章节 |
| `摘要` | TEXT | Markdown 详细摘要 |
| `摘要核心` | TEXT | 一句话核心 |
| `关键对话`, `人性细化`, `写作要点` | TEXT | |
| `道具物品`, `势力阵营`, `情绪列表`, `伏笔列表`, `节奏控制`, `视觉画面`, `声音氛围` | JSONB | |
| `目标字数` | INT (3000) | |
| `实际字数` | INT | |

**22 个 API 端点**: CRUD 5 + 移动/重编号/重排序/批量 4 + 上下文/关联 5 + 事件线 3 + AI 生成 4 + 自动关联 1

**Schema**: `contracts/schemas/outline.json` ✅

### #11 角色管理 (Character) — ★P1 (C03 裁决)

24 类型 + 三层性格 + 7 段背景:

| 维度 | 内容 |
|------|------|
| **24 类型** | 主角/女主/男主/反派/导师/配角/盟友/对手/家族成员/恋人/朋友/敌人/路人/神秘人物/历史人物/穿越者/重生者/系统持有者/金手指持有者/阵营领袖/组织成员/种族代表/其他 |
| **三层性格** | `{表层, 中层, 内核}` |
| **境界** | FK → power_systems + FK → power_realms |
| **战力系数** | 初始/当前 (DECIMAL(10,2)) |
| **人生经历** | `[{事件, 章节}]` |
| **存续状态** | 活跃/死亡/失踪/退场/未登场 |

**24 个 API 端点**: CRUD 5 + AI 上下文 2 + 出场管理 2 + 关系 CRUD 4 + 批量删除 1 + 物品 6 + 关系 4 + 8 (境界共享)

**Schema**: `contracts/schemas/world-setting/character.json` ✅

**C04 冲突裁决**: 角色数据规模不预设, 取决于项目 (玄穹开 20, 烬都奇谭 7)

### #13 伏笔管理 (Foreshadow) — P0 (C05 裁决)

6 类型 + 10 埋设模式:

| 6 类型 | 10 埋设模式 |
|--------|------------|
| 悬念 | 对话暗示 |
| 伏线 | 物件刻画 |
| 暗喻 | 景物烘托 |
| 预言 | 梦境预言 |
| 巧合 | 他人转述 |
| 对照 | 旁白议论 |
| | 行为异常 |
| | 环境异常 |
| | 数字暗示 |
| | 姓名暗示 |

**15 个 API 端点**: CRUD 5 + `/echo` (回响) + `/find-chapter` + `/chapter/:cId/foreshadows` + `/stats` + 自动检测 1

**Schema**: `contracts/schemas/world-setting/foreshadow.json` ✅

### #15 支线故事 (4 子模块聚合) — P1

**4 个子模块**:
1. `event_lines` 支线 (标题/描述/状态)
2. `event_flows` 事件流 (line_id/event_order/章节ID/角色IDs)
3. `story_line` 故事线
4. `element_bindx` 要素绑定 (event_id/要素名称/bindings)

**33 个 API 端点** (4 个子模块聚合)

**Schema**: `contracts/schemas/world-setting/event-line.json` ✅

### #16 时间线 (Timeline) — P1 (C06 裁决)

3 子表:
1. `timeline_calendars` 自定义历法 (历法名称/年长度/月数/月长度 JSONB/纪年方式)
2. `timeline_events` 7 类型事件 (出场/战斗/揭秘/关系/地点/势力/其他)
3. `timeline_chapter_time` 章节与历法日期映射 (UNIQUE (project_id, 章节ID))

**13 个 API 端点**:
- `/calendar` GET/PUT
- `/events` GET/POST
- `/chapter-time` GET/PUT
- `/validate` GET (校验时间线一致性)
- `/context/:nodeId` GET (大, 可达 196 KB)
- `+ 5 通用 CRUD`

**Schema**: `contracts/schemas/world-setting/timeline.json` ✅

## UI 通用范式 (来自 `2026-06-03 World Tab UI 通用范式.md`)

每个 World Tab 模块都有统一交互:
- **列表视图**: 卡片网格 / 列表 / 树形
- **详情视图**: 抽屉 / 弹窗 / 全屏
- **编辑视图**: 表单 / 双向绑定 JSON
- **AI 生成**: 弹窗 + 采纳按钮
- **统计**: 卡片 + 图表

## 跨模块联动 (主控一致性规则)

1. **#1 世界观 ↔ #2 故事核心**: 同步更新
2. **#7 力量体系 ↔ #11 角色**: FK 关联,境界变更广播
3. **#11 角色 ↔ #12 人物关系图**: 关系图自动更新
4. **#13 伏笔 ↔ #11 角色**: 谁埋的 / 谁回收
5. **#13 伏笔 ↔ #10 大纲 ↔ 章节**: 三方联动
6. **#16 时间线 ↔ #17 已经历事件**: 蒸馏后回流
7. **#4 势力 ↔ #11 角色**: 核心人物关联
8. **#6 物品 ↔ #11 角色**: 持有物品

主控通过 `knowledge-graph/` 子项目维护这些一致性。
