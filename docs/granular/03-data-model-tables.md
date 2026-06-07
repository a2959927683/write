# 03 · 数据模型字段表 (主控权威,与原文 1:1)

> 来源: `docs/MASTER-PROJECT-SPEC.md` §3
> Schema 文件: `contracts/schemas/*.json` + `world-setting/*.json`
> 字段名采用**中文**(与云笔 API 1:1 对应),主控契约权威

## 1. 核心实体 (11 大类)

### `users` 用户
- 字段 14: id, username, email, password_hash, nickname, avatar, 最高角色等级, plan_type, daily_quota, daily_used, quota_reset_at, permissions, createdAt, updatedAt
- Schema 文件: (待写 `contracts/schemas/user.json`)

### `projects` 项目
- 字段 13: id, user_id, **项目名称**, **项目类型**, **项目状态**, **描述**, **封面**, **每幕事件数量配置**, 总字数, 章节数, 角色数, createdAt, updatedAt
- Schema 文件: `contracts/schemas/project.json` ✅

### `chapters` 章节 (★ 三重冗余)
- 字段 21: id, project_id, **关联大纲节点ID**, **标题**, **字数**, **状态**, **内容**, **正文**, **content**, **场景脚本**, **蒸馏状态**, **蒸馏失败原因**, **蒸馏模型**, **蒸馏完成时间**, **正文快照哈希**, **排序顺序**, target_word_count, createdAt, updatedAt
- **三重冗余**: `内容` / `正文` / `content` 三个字段保存相同内容,源于云笔 API 不同接口
- Schema 文件: `contracts/schemas/chapter.json` ✅

### `outlines` 大纲 (★P0, 自引用树)
- 字段 25+: id, project_id, **父节点ID**, **类型** (volume/chapter), **标题**, **关联章节ID**, 正文字数, 状态, 优先级, 截止日期, 标签, 摘要, 摘要核心, 颜色, 排序顺序, 目标字数, 实际字数, 关键对话, 人性细化, 写作要点, 道具物品, 势力阵营, 情绪列表, 伏笔列表, 节奏控制, 视觉画面, 声音氛围, createdAt, updatedAt
- Schema 文件: `contracts/schemas/outline.json` ✅

## 2. WorldSetting 17 模块子表

### 2.1 `worldviews` 世界观设定 (#1, P0)
- 字段 12 + ext JSONB
- 一项目一记录 (UNIQUE project_id)
- Schema: `contracts/schemas/world-setting/worldview.json` ✅

### 2.2 `story_cores` 故事核心 (#2, P0)
- 6 字段: 主题, 主线, 冲突, 高潮, 结局, 核心意义
- 一项目一记录
- Schema: `contracts/schemas/world-setting/story-core.json` ✅

### 2.3 `geo_maps` 地理地图 (#3, P1)
- 字段 8 + ext JSONB (35 地点, 6 级树形)
- 树形: parent_id
- 6 级: 0=世界, 1=大陆, 2=区域, 3=城市, 4=地点, 5=子地点
- Schema: `contracts/schemas/world-setting/geo-map.json` ✅

### 2.4 `factions` 势力阵营 (#4, P1)
- 字段 10 + ext JSONB
- 9 类型 (C09 裁决): 组织/国家/门派/家族/商会/学院/宗教/部落/其他
- 4 视图: 列表/关系图/详情/编辑
- 子表: `faction_relations` (faction_a, faction_b, 关系类型, 强度)
- Schema: `contracts/schemas/world-setting/faction.json` ✅

### 2.5 `currencies` 货币体系 (#5, P2)
- 字段 6 + ext JSONB
- 3 货币: 主币/辅币/虚拟
- 子表: `currency_exchange_rates`
- Schema: `contracts/schemas/world-setting/currency.json` ✅

### 2.6 `items` 物品列表 (#6, P1)
- 字段 17 (物品名称, 类别, 作用, 出处, 获取难度, 威力, 价值, 特征, 使用人群, 注意事项, 保存期限, 用量, 使用代价, 防御力, 排序顺序, ext, ...)
- 86 物品/项目
- Schema: `contracts/schemas/world-setting/item.json` ✅

### 2.7 `power_systems` 力量体系 (#7, ★P0, C08 裁决)
- 4 层嵌套 JSONB:
  - **境界列表** (11 境界)
  - **能力列表** (6 能力)
  - **修行路径** (4 路径)
  - **限制约束** (5 限制)
- 可选子表拆分: `power_realms`, `power_abilities`
- Schema: `contracts/schemas/world-setting/power-system.json` ✅

### 2.8 `skill_systems` 功法体系 (#8, P2)
- 字段 6: 功法名称, 品级 (9 种), 类型 (12 种), 体系ID FK, 描述, ext
- 60 类型 × 9 品级
- Schema: `contracts/schemas/world-setting/skill-system.json` ✅

### 2.9 `special_settings` 特殊设定/金手指 (#9, P2)
- 字段 5: 名称, 类型 (19 类), 描述, 标签 JSONB, ext
- 19 类型: 系统/重生/穿越/签到/兑换/抽奖/副本/升级/修炼/血脉/异能/天眼/预知/吞噬/复制/召唤/鉴定/强化/其他
- Schema: `contracts/schemas/world-setting/special-setting.json` ✅

### 2.10 大纲设定 (#10, ★P0)
- 见 `outlines` 表 (§1)

### 2.11 `characters` 角色管理 (#11, ★P1, C03 裁决)
- 字段 22: id, project_id, 姓名, 类型 (24 类), 性别, 年龄, 身份, 境界, 武器, 外貌, 结局, **性格** (表/中/内 三层), **人生经历** (事件+章节), 核心意义, 其他信息, 简介, 头像颜色, 颜色, 力量体系ID, 初始境界ID, 当前境界ID, 初始战力系数, 当前战力系数, 存续状态
- 24 类型 enum
- 子表 4: character_items / character_relations / character_appearances / character_realm_breakthroughs
- Schema: `contracts/schemas/world-setting/character.json` ✅

### 2.12 `character_relations` 人物关系图 (#12, P2)
- 字段 6: character_a_id, character_b_id, 关系类型 (8 种), 强度, 备注, ext
- 8 关系: 师徒/亲属/敌对/盟友/恋人/朋友/敌对/其他
- 13 chip 类型
- 与 #11 共用 API 端点

### 2.13 `foreshadows` 伏笔管理 (#13, ★P0, C05 裁决)
- 字段 11: id, project_id, 标题, 描述, **类型** (6 种), **埋设模式** (10 种), 埋设章节ID, 状态, 重要度, 回收章节ID, ext (含 echoes 子数组)
- 子表: `foreshadow_echoes` (foreshadow_id, 章节ID, 描述, echoed_at)
- 6 类型: 悬念/伏线/暗喻/预言/巧合/对照
- 10 埋设模式: 对话暗示/物件刻画/景物烘托/梦境预言/他人转述/旁白议论/行为异常/环境异常/数字暗示/姓名暗示
- Schema: `contracts/schemas/world-setting/foreshadow.json` ✅

### 2.14 `plot_structures` 情节脉络 (#14, P1)
- 字段 5: id, project_id, 名称, 模板, 结构详情 JSONB, 关联章节IDs
- 5 模板: 起承转合/英雄之旅/三幕剧/七点不测/救猫咪
- 7 幕结构
- Schema: `contracts/schemas/world-setting/plot-structure.json` ✅

### 2.15 支线故事 (#15, P1)
- 4 个子模块聚合:
  - `event_lines` (标题/描述/状态)
  - `event_flows` (line_id/event_order/章节ID/角色IDs/事件描述)
  - `story_line`
  - `element_bindx` (event_id/要素名称/bindings)
- 35 事件/项目, 3 步 AI 生成
- Schema: `contracts/schemas/world-setting/event-line.json` ✅

### 2.16 时间线 (#16, P1, C06 裁决)
- 3 子表:
  - `timeline_calendars` (历法名称/年长度/月数/月长度 JSONB/纪年方式)
  - `timeline_events` (标题/历法日期/章节ID/类型/描述/ext/importance)
  - `timeline_chapter_time` (UNIQUE (project_id, 章节ID), 历法日期)
- 7 事件类型: 出场/战斗/揭秘/关系/地点/势力/其他
- Schema: `contracts/schemas/world-setting/timeline.json` ✅

### 2.17 已经历事件 (#17, P1)
- 与 #15 复用 event_lines 表
- 95 事件/项目, 5 分类 (战斗/关系/觉醒/发现/其他)
- 蒸馏集成: 蒸馏完成后自动写入

## 3. AI 与对话

### `ai_generations` 统一生成记录 (★ 核心)
- 字段 12+: id, project_id, user_id, 模式, provider, model, prompt, response, status, tokens, latency_ms, createdAt
- 所有 World Tab 模块的 AI 生成记录

### `conversations` 会话
- 字段 8: id, project_id, user_id, 标题, 模式, createdAt, updatedAt
- 子表 `messages` (conversation_id, role, content, tokens, createdAt)

## 4. 规则与文笔

### `rules` 规则
- 字段 8: id, project_id, 名称, 描述, 分类, 是否启用, 是否共享, createdAt
- 11 类业务规则

### `writing_styles` 文笔风格
- 字段 6: id, project_id, 名称, 描述, 提示词, 是否共享
- 15 主题

## 5. 笔记/材料/义务

### `notes` 笔记
- 字段 6: id, project_id, 标题, 内容, 是否置顶, createdAt

### `materials` 材料
- 字段 6: id, project_id, 标题, 类型, 内容, details

### `obligations` 义务
- 字段 8: id, project_id, 标题, 描述, 状态, 截止日期, 创建时间
- 含 `/batch-update-status`, `/auto-expire` API

## 6. 统计

### `stats_daily` 每日统计
- 字段: user_id, date, 字数, 章节数, AI调用次数, tokens

### `stats_weekly` 每周统计
- 字段: user_id, week_start, 字数, 章节数, 完成率

## 7. 蒸馏

### `distill_jobs` 蒸馏任务
- 字段 10: id, project_id, chapter_id, 阶段 (Generator/Extractor/Checker), 状态, 输入, 输出, 错误, started_at, completed_at

## 8. 管理后台

### `audit_logs` 操作日志
- 字段 8: id, user_id, 操作, 资源类型, 资源ID, IP, UserAgent, createdAt

## 9. TTS (语音合成)

### `tts_voices` 音色
- 字段 6: id, 名称, 性别, 语言, 描述, sample_url
- 19 种音色

## 10. 已知 11 条冲突 → 数据模型影响

见 `docs/granular/07-conflict-adjudication.md`

---

*字段数总计: ~250 个 (核心) + ~150 个 (子表) = 400+ 字段*
*Schema 文件总计: 17 个*
