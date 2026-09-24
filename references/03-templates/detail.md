# AES 详情页 Template

> **归属：AES Product Design。** 本 Reference 是 AES（深信服下一代端点安全）产线专属 Template，不作为 Common Design 的通用模板。
> `Coverage: override`

## 目录

1. 定位与执行顺序
2. 先选择详情容器
3. 通用概要区与正文规则
4. Drawer 分支
5. 独立 Page 分支
6. Modal 分支
7. Template 登记
8. 输出契约
9. 实现与参考证据
10. 状态、异常与边界
11. 退出检查

## 1. 定位与执行顺序

本 Template 用于 AES PC 端对象详情的容器选型、信息组织和交互设计。病毒、日志、任务、事件、客户端等业务名称不是新的页面类型。

Theme 或用户已经锁定容器、正文组织、宽度或连续浏览能力时，直接执行已锁定契约；只有未锁定事项才按本文判断。若锁定要求与本文硬边界冲突，必须指出冲突和影响，不得静默改写需求。

详情设计必须按以下顺序执行：

```text
选择详情容器
├── Drawer + Contextual
│   └── 判断 Tab → 判断宽度 → 映射 templateId → 组织分区 → 判断底部连续浏览
├── Page + Stable / Drilldown
│   └── 判断分区或 Tab → 定义路由、返回和页面级操作
└── Modal + Contextual
    └── 承载当前流程中的少量、临时、只读详情
```

- 只有选择 `drawer + contextual` 后，才执行抽屉的 Tab、宽度、固定模板和底部操作区判断。
- `templateId` 是选型结果，不得用已有编号反推或限制页面结构。
- 下钻抽屉仍是 Drawer，只是在顶部增加返回上一层抽屉的入口；它不同于拥有独立路由的 `page + drilldown`。
- 前端封装状态在结构选型完成后核验，不得为了命中封装而改变已确认的容器、宽度或正文组织。

## 2. 先选择详情容器

### 2.1 容器定义

| `detail_container` | `entry_mode` | 使用场景 | 不适用场景 |
| --- | --- | --- | --- |
| `drawer` | `contextual` | 保留父页上下文，快速查看、轻量处置或连续浏览记录 | 需要独立 URL、复杂配置或沉浸式分析 |
| `page` | `stable` | 具有稳定菜单、页头 Tab 或其他固定入口的独立详情任务 | 仅临时查看一条记录 |
| `page` | `drilldown` | 从来源页进入独立空间，进行深度理解或处理 | 必须持续对照父列表 |
| `modal` | `contextual` | 当前流程内短时查看少量只读信息，关闭后立即回到原流程 | 长内容、多模块、连续浏览或复杂操作 |
| `other` | 按业务确定 | 以上容器无法保留已确认的主要任务和区域关系 | 仅因现有封装不匹配而自定义 |

### 2.2 决策顺序

1. 菜单、页头 Tab 或其他稳定入口直接承载详情任务时，使用 `page + stable`。
2. 需要独立 URL、浏览器前进后退、新标签页打开、分享定位、刷新恢复或深度处理时，使用 `page + drilldown`。
3. 需要频繁对照父列表、连续查看多条记录、快速标记或轻量处置时，使用 `drawer + contextual`。
4. 只需在当前流程中短时查看少量只读信息，且关闭后立即返回原流程时，使用 `modal + contextual`。
5. 以上结构均无法承载时，使用 `other`，并完整说明容器、入口和退出方式。

Tab 数量不参与容器选择。Drawer 与独立 Page 都可以使用分区或多个 Tab，容器取决于上下文、路由、任务深度和操作复杂度。

### 2.3 通用边界

- 禁止连续嵌套超过 2 层抽屉。
- 二级内容复杂或已形成独立任务时，从一级抽屉跳转独立下钻页。
- 查看与编辑复杂度差异明显时，查看可使用抽屉，编辑跳转独立页面。
- 同一列表、同类对象、同一层级必须使用一致的详情容器。

## 3. 通用概要区与正文规则

### 3.1 页面骨架

Drawer 与独立 Page 共享“导航—概要—提示—正文”的信息层级：

```text
详情
├── 容器导航区
│   ├── Drawer：业务对象类型 + 详情                         关闭 ×
│   ├── 下钻 Drawer：返回 + 业务对象类型 + 详情                关闭 ×
│   └── 独立 Page：稳定页面入口，或返回入口 / 面包屑
├── 浅色概要区
│   ├── 左侧对象区：对象主标题 + 标签；下方关键字段不超过两行
│   └── 右侧操作区：固定一行，按容器宽度控制可见槽位
├── 页面提示区（按需）
└── 正文内容区：分区平铺或 Tab
```

页面存在授权、风险、影响范围或其他业务提示时，预留 `noticeRegion`，展示条件、内容和 `IxAlert` banner 复用读取 `../06-components/page-notice.md`。

### 3.2 浅色概要区

所有详情页的对象概要区统一使用浅色背景，不再区分有底色或无底色。具体颜色、间距和圆角沿用前端封装及产品 Token，不照搬历史页面的渐变背景。

- 对象主标题行不计入关键字段行数。
- 主标题下方的关键字段布局不得超过 **2 行**。
- 只有用户明确且强烈要求某些字段必须置顶时，才允许超过 2 行；必须在 `summary_fields_override` 中记录字段和原因。
- 超出概要区容量的字段进入正文，不得靠缩小字号、压缩间距或挤占右侧操作区解决。
- 对象主标题使用当前实例最稳定、最可识别的名称或业务主键；不得显示空标题。
- 状态、等级、类型标签可以与主标题横向排列，但不能替代主标题。
- 长标题单行省略并通过 Tooltip 展示完整内容，不得挤压右侧操作区。
- 关键字段按“身份/范围 → 状态/结果 → 关键时间”组织，不按接口顺序罗列。
- 长描述、原始日志、完整路径、备注历史和低频字段进入正文。
- 空值统一显示 `-`；零值显示 `0`。

共享概要区线框：

```text
┌──────────────────────────────────────────────────────────────┐
│ 浅色概要区                                                   │
│ [等级/状态] 对象主标题                         [操作] [更多] │  ← 标题行
│ 关键字段 1 │ 关键字段 2 │ 关键字段 3                         │  ← 第 1 行
│ 关键字段 4 │ 关键字段 5                                     │  ← 第 2 行（上限）
└──────────────────────────────────────────────────────────────┘
```

### 3.3 右侧操作槽位

“更多”本身占用 1 个可见槽位。操作按当前任务的频率和重要性排序；危险操作不得仅因重要而默认外显。

| 容器宽度 | 可见槽位上限 | 未溢出 | 溢出后 |
| --- | ---: | --- | --- |
| 640px Drawer | 2 | 操作数 ≤ 2 时全部外显 | 外显最高优先级的 1 个操作 + 更多；第 2 个及以后收入更多 |
| 960px Drawer | 3 | 操作数 ≤ 3 时全部外显 | 外显最高优先级的 2 个操作 + 更多；第 3 个及以后收入更多 |
| 其他宽度或独立 Page | 按实际宽度 | 保持一行且不挤压标题 | 明确可见槽位，并以相同原则收纳至更多 |

- 操作区固定在概要区右侧且仅占一行，不得换到概要字段下方。
- 禁用操作必须展示具体原因。
- 操作执行后更新当前详情；从父列表打开时同步父列表，不改变当前查询上下文。

### 3.4 正文组织：先判断分区或 Tab

“正文内容模块”是拥有独立业务标题和完整内容的一组信息，例如执行信息、关联对象、处理结果；字段行不是独立模块。

1. 只有 1 个正文模块时，直接平铺，禁止生成单个 Tab。
2. 有 2 个及以上模块时，仍默认分区平铺。
3. 只有以下任一条件成立时才使用 Tab：
   - 平铺后内容明显过多，长距离滚动使用户难以定位。
   - 模块属于用户不会连续阅读的独立任务、数据集或分析视角。
   - 模块本身较重，分别包含表格、时间线、图表、原始数据或独立操作。
   - 同一数据需要在结构化详情、JSON / 原始日志等互斥视图间切换。

模块较多但内容短、需要连续阅读时仍使用分区。不得以模块数量或 Tab 数量机械决定组织形式或容器。

### 3.5 正文内容通则

- 标题使用明确业务名称，不使用“其他信息”“更多信息”。
- 描述字段使用 label-value；集合数据使用表格；过程和关联关系使用对应组件。
- JSON、原始日志、代码和嵌入表格横向占满所在分区或 Tab 的可用宽度，不进入 label-value 网格。
- `content_type=table` 时，将 `table-management` 写入该模块的 `pattern_requirements`，并传递 `host_template=detail`、`table_role=embedded` 和正文可用宽度；不得调用 List Template，也不得由 Table Pattern 重选详情容器或 Tab。
- 分区内容不得套装饰性卡片；背景、边框和阴影不能代替标题与间距。
- Tab 使用顶部线型导航和稳定唯一标识；溢出时保留 `showAllTabsPanel` 能力，不压缩文字、换行或缩小字号。
- 切换 Tab 保留已加载数据和局部状态；连续浏览切换到另一条记录时回到默认 Tab。独立 Page 需要直接定位时，将当前 Tab 写入路由。

## 4. Drawer 分支

只有 `detail_container=drawer` 时执行本节，顺序不可颠倒。

### 4.1 第一步：判断是否使用 Tab

按第 3.4 节选择 `sections` 或 `tabs`，再进入宽度判断。不得先看到某个固定模板，再反向选择 Tab。

### 4.2 第二步：判断宽度

1. 用户明确指定宽度时优先采用，并校验可用空间；最大不得超过 `1200px`。
2. 使用 Tab 且用户未指定宽度时，**建议 960px**。若同模块已有一致的 640px 带 Tab 抽屉，且当前内容能够完整承载，可以沿用 640px。
3. 不使用 Tab 且用户未指定宽度时：
   - 所有嵌入表格中的最大列数 **> 4**，选择 960px；或
   - 全部区域的举证字段总数 **> 15**，选择 960px；
   - 其他情况默认 640px。
4. “举证字段总数”是全部区域合计，不要求任一单独区域超过 15 个；按配置字段统计，不按某条记录的实际取值长度改变宽度。
5. 用户指定其他宽度且 640px / 960px 固定模板均无法承载时，返回 `templateId: custom`，不得声称复用固定宽度模板。
6. 合理内容在 1200px 内仍无法承载时，重新判断为独立下钻页，不继续加宽。
7. 同模块、同类型抽屉宽度保持一致，不因单条数据长短动态改变。

### 4.3 第三步：映射固定模板

| 宽度 | 正文组织 | `templateId` | `encapsulation` |
| --- | --- | --- | --- |
| 640px | 无 Tab | `drawer-detail-640` | `false` |
| 640px | 有 Tab | `drawer-detail-640-tabs` | `false` |
| 960px | 无 Tab | `drawer-detail-960` | `false` |
| 960px | 有 Tab | `drawer-detail-960-tabs` | `false` |

四个编号采用“容器—任务—变体”的命名顺序，`drawer-` 明确表示 Drawer 容器。它们是待前端封装对齐的稳定目标；前端真实入口发布并核验前保持 `encapsulation: false`，发布后同步修改本文件与 `index.md`。Common Design 中既有的 `page-detail-drawer` 只作为存量调用的迁移对象，不是第五种模板，也不得作为新编号的命名样板。

### 4.4 第四步：执行正文布局

#### 4.4.1 无 Tab

- 分区标题使用 `14px`、`font-weight: 600`、默认行高 `36px`；左侧使用 `2px × 12px` 蓝色竖线并垂直居中。
- 竖线使用平台主色，AES 基准为 `#1c6eff`；同模块已有统一 Token 时使用对应 Token。
- 分区之间不使用分割线，以前一分区内容和下一标题之间默认 `16px` 间距建立层次。
- 只有一个正文模块且无需标题时，直接展示内容。

640px 无 Tab 线框：

```text
┌──────────────────────────────────────────────┐
│ 对象类型详情                          关闭 × │
├──────────────────────────────────────────────┤
│ 浅色概要区                         [操作][…] │
│ 对象主标题                                 │
│ 关键字段……（最多两行）                     │
├──────────────────────────────────────────────┤
│ ▏分区一                                    │
│ Label 1                                    │
│ Value 1                                    │
│ Label 2                                    │
│ Value 2                                    │
│ ▏分区二                                    │
│ 内容                                       │
└──────────────────────────────────────────────┘
```

960px 无 Tab 线框：

```text
┌──────────────────────────────────────────────────────────────────┐
│ 对象类型详情                                              关闭 × │
├──────────────────────────────────────────────────────────────────┤
│ 浅色概要区                               [操作1][操作2][更多]    │
│ 对象主标题；关键字段最多两行                                │
├──────────────────────────────────────────────────────────────────┤
│ ▏分区一                                                        │
│ Label 1：Value 1                   Label 2：Value 2              │
│ Label 3：Value 3                   Label 4：Value 4              │
│ ▏分区二                                                        │
│ 表格 / JSON 横向占满内容区                                    │
└──────────────────────────────────────────────────────────────────┘
```

#### 4.4.2 有 Tab

- 每个 Tab 独立判断是否需要二次分区。
- 不需要分区时，直接在 Tab 下平铺内容。
- 需要分区时，使用横向占满内容区的浅色分区标题带，不使用无 Tab 的蓝色竖线标题。
- 浅色标题带只表达真实内容分组，不将每组内容包装成装饰性卡片；仅业务需要时提供展开/收起。

640px 有 Tab 线框：

```text
┌──────────────────────────────────────────────┐
│ 对象类型详情                          关闭 × │
├──────────────────────────────────────────────┤
│ 浅色概要区                         [操作][…] │
│ 对象主标题；关键字段最多两行               │
├──────────────────────────────────────────────┤
│ [Tab 一] [Tab 二]                           │
├──────────────────────────────────────────────┤
│ 浅色分区标题带                              │
│ Label 1                                    │
│ Value 1                                    │
│ Label 2                                    │
│ Value 2                                    │
│                                             │
│ 无需分区的 Tab：直接平铺内容                │
└──────────────────────────────────────────────┘
```

960px 有 Tab 线框：

```text
┌──────────────────────────────────────────────────────────────────┐
│ 对象类型详情                                              关闭 × │
├──────────────────────────────────────────────────────────────────┤
│ 浅色概要区                               [操作1][操作2][更多]    │
│ 对象主标题；关键字段最多两行                                │
├──────────────────────────────────────────────────────────────────┤
│ [结构化详情] [关联数据] [JSON 原文]                            │
├──────────────────────────────────────────────────────────────────┤
│ 浅色分区标题带                                                │
│ Label 1：Value 1                   Label 2：Value 2              │
│ Label 3：Value 3                   Label 4：Value 4              │
│ JSON / 表格在对应 Tab 中横向占满内容区                          │
└──────────────────────────────────────────────────────────────────┘
```

#### 4.4.3 字段列数

- 640px Drawer：一行一组 label-value。
- 960px Drawer：一行两组独立 label-value。
- 字段列数与是否使用 Tab 无关。
- 用户指定其他宽度时，按实际可用空间组织字段，并在契约中使用 `width-adapted`。

### 4.5 第五步：判断底部操作区

只有需要在当前结果序列中连续浏览、快捷切换记录时，才设置 `sequence_navigation: enabled`，并固定显示“上一个 / 下一个 / 关闭”。没有快捷切换诉求时，不显示整个底部操作区。

连续浏览底部线框：

```text
┌──────────────────────────────────────────────┐
│                  正文内容                    │
├──────────────────────────────────────────────┤
│ [上一个] [下一个] [关闭]                    │  ← 固定底部操作区
└──────────────────────────────────────────────┘
```

- 底部操作区与宽度、Tab 和分区样式无关，不增加新的模板编号。
- 上一个、下一个按打开 Drawer 时父列表的搜索、筛选、左树范围和排序结果确定。
- 第一条禁用“上一个”，最后一条禁用“下一个”，仅一条时两者均禁用；按钮位置保持稳定。
- 切换期间禁用上一个和下一个；仅最后一次请求可以更新详情。
- 切换成功后重置正文滚动位置、默认 Tab、展开项、局部选择和错误状态。
- 切换失败时保留原记录和原序号，不得显示半条新数据。
- 当前记录被删除后优先展示下一条；没有下一条时展示上一条；序列为空时关闭 Drawer。
- 父列表搜索、筛选、左树、排序或分页改变时关闭 Drawer。
- `sequence_navigation: disabled` 时通过右上角关闭；不得为单独关闭或普通业务操作生成底部栏。

### 4.6 下钻 Drawer

下钻 Drawer 仍从四个固定 Drawer 模板中选型，只在顶部增加返回上一层 Drawer 的入口。“返回”与“关闭”是两个不同动作。

```text
父页面          一级 Drawer                 二级下钻 Drawer
┌────────┐     ┌──────────────────┐        ┌──────────────────────┐
│ 列表   │     │ 对象详情     ×   │        │ ‹ 返回  子项详情  × │
│        │ ──> │ 概要与正文       │ ─────> │ 概要与正文           │
└────────┘     └──────────────────┘        └──────────────────────┘
```

- `drawer_navigation: drilldown` 仅表示顶部具有返回上一层 Drawer 的入口。
- 返回：关闭当前层并恢复上一层 Drawer 的滚动、Tab 和局部状态。
- 关闭：退出整个 Drawer 链并回到父页面。
- 若二级内容需要独立 URL、复杂处理或超过两层，改用 `page + drilldown`。

## 5. 独立 Page 分支

独立 Page 使用 `page + stable` 或 `page + drilldown`。它不执行 Drawer 的 640/960 宽度、字段列数、固定底部操作区或四个 Drawer 模板判断。

### 5.1 分区 Page

适用于信息较多但属于同一连续任务、需要按顺序理解的详情。

```text
┌──────────────────────────────────────────────────────────────┐
│ ‹ 返回 / 面包屑                                             │
├──────────────────────────────────────────────────────────────┤
│ 浅色概要区                          [操作 1] [操作 2] [更多] │
│ 对象主标题；关键字段最多两行                               │
├──────────────────────────────────────────────────────────────┤
│ 模块一                                                       │
│ 内容                                                         │
├──────────────────────────────────────────────────────────────┤
│ 模块二                                                       │
│ 内容                                                         │
└──────────────────────────────────────────────────────────────┘
```

### 5.2 Tab Page

适用于多个独立任务、数据集或分析视角。

```text
┌──────────────────────────────────────────────────────────────┐
│ ‹ 返回 / 面包屑                                             │
├──────────────────────────────────────────────────────────────┤
│ 浅色概要区                          [操作 1] [操作 2] [更多] │
│ 对象主标题；关键字段最多两行                               │
├──────────────────────────────────────────────────────────────┤
│ [总览] [关联告警] [攻击分析] [处置记录]                    │
├──────────────────────────────────────────────────────────────┤
│ 当前 Tab 的独立内容、操作和状态                             │
└──────────────────────────────────────────────────────────────┘
```

### 5.3 Page 导航与操作

- `page + drilldown` 使用返回入口和浏览器导航；返回后恢复父列表的搜索、筛选、排序、分页和滚动位置。
- `page + stable` 使用产品稳定导航退出，不强制显示返回来源。
- 独立 Page 的 `sequence_navigation` 与 `footer_mode` 均为 `not-applicable`。
- 默认 Tab 对应最高频首要任务，不机械命名为“基本信息”。
- 需要直接定位时将当前 Tab 写入路由；刷新和前进后退应恢复当前 Tab。
- 页面级操作放在概要区右侧；只作用于当前 Tab 的操作放在 Tab 工具区。
- 顶部概要和关键操作是否吸顶，沿用同模块既有页面；无存量基准时不额外吸顶。

独立 `page + drilldown` 使用 `page-detail-drilldown`。当前没有单独登记 `page + stable` 的固定详情模板；若没有其他已登记模板承载，使用 `custom` 并说明稳定入口和页面结构。

## 6. Modal 分支

`modal + contextual` 指在当前工作流中临时打开的小型详情弹窗：内容少、以只读为主、关闭后立即回到原流程。

- 不执行 Drawer 的 Tab、宽度、固定模板或连续浏览判断。
- 不用于长内容、多模块、嵌入大表格、复杂操作或需要独立 URL 的详情。
- 内容增长后，按任务关系改用 Drawer 或独立 Page。
- 当前未登记固定详情 Modal 模板时，返回 `templateId: custom`、`encapsulation: false`，并在 `customReason` 中说明。

## 7. Template 登记

| 页面类型 | 已确认结构 | `templateId` | `encapsulation` |
| --- | --- | --- | --- |
| 640px 无 Tab Drawer | Drawer + Contextual + 640px + Sections | `drawer-detail-640` | `false` |
| 640px 有 Tab Drawer | Drawer + Contextual + 640px + Tabs | `drawer-detail-640-tabs` | `false` |
| 960px 无 Tab Drawer | Drawer + Contextual + 960px + Sections | `drawer-detail-960` | `false` |
| 960px 有 Tab Drawer | Drawer + Contextual + 960px + Tabs | `drawer-detail-960-tabs` | `false` |
| 独立下钻详情页 | Page + Drilldown | `page-detail-drilldown` | `false` |
| 自定义详情 | 没有已登记模板可承载 | `custom` | `false` |

- `encapsulation: true` 表示已核验真实前端页面封装入口；`false` 表示按完整 Template 契约自行实现。
- `encapsulation: false` 不阻断设计或开发，也不得为了获得封装而改变详情结构。
- 四个 Drawer 模板可共用内部骨架，但必须具有与 `templateId` 对应的稳定入口或注册映射，核验后才可改为 `true`。
- 下钻 Drawer 继续使用相应 Drawer 编号，不新增模板。
- 没有既有模板可承载时使用 `custom`，不得删减结构来强行命中编号。

## 8. 输出契约

设计详情页时必须返回以下契约；不适用字段填写 `not-applicable` 或 `null`，不得省略关键决策依据。

```yaml
template_contract:
  templateId: "drawer-detail-640 | drawer-detail-640-tabs | drawer-detail-960 | drawer-detail-960-tabs | page-detail-drilldown | custom"
  encapsulation: "true | false"
  customReason: ""

  detail_container: "page | drawer | modal | other"
  entry_mode: "stable | drilldown | contextual"
  content_organization: "sections | tabs"

  drawer_width: "640 | 960 | user-specified | not-applicable"
  width_reason: "user-specified | existing-module-reference | tab-recommended | existing-640-tabs | table-over-four-columns | evidence-fields-over-fifteen | default-640 | not-applicable"
  width_inputs:
    max_embedded_table_columns: null
    evidence_field_count_total: null # 全部区域举证字段的合计值

  drawer_navigation: "standard | drilldown | not-applicable"
  sequence_navigation: "enabled | disabled | not-applicable"
  footer_mode: "sequence-controls | none | not-applicable"

  header_contract:
    drawer_title: "业务对象类型 + 详情 | not-applicable"
    object_title: 当前对象实例的主标识
    summary_background: tinted
    summary_field_max_rows: 2
    summary_fields: []
    summary_fields_override:
      enabled: false
      fields: []
      reason: ""
    action_contract:
      visible_slot_limit: "2 | 3 | width-adapted"
      direct_action_limit_when_overflow: "1 | 2 | width-adapted"
      exposed_actions: []
      more_actions: []
      more_occupies_slot: true
    noticeRegion: "page-notice | none"

  body_contract:
    section_style: "blue-rail-title | tinted-title-band | none | page-existing"
    label_value_columns: "1 | 2 | width-adapted | page-existing"
    full_width_content_types: [table, raw-data]
  body_modules:
    - module_id: ""
      tab_key: "" # 无 Tab 时留空
      section_style: "blue-rail-title | tinted-title-band | none | page-existing"
      content_type: "descriptions | table | timeline | chart | raw-data | other"
      pattern_requirements: []

  selection_reason: 说明容器、正文组织、宽度、概要区与操作槽位的判断依据
  reference_page: 真实参考页面
```

契约填写规则：

- Drawer 必须返回 `drawer_width`、两个 `width_inputs` 和 `width_reason`；其他容器使用 `not-applicable` / `null`。
- `evidence_field_count_total` 必须填写全部区域的举证字段合计，不能填写单一区域最大值。
- 640px Drawer 的 `visible_slot_limit=2`、溢出时 `direct_action_limit_when_overflow=1`。
- 960px Drawer 的 `visible_slot_limit=3`、溢出时 `direct_action_limit_when_overflow=2`。
- “更多”始终占一个可见槽位；`exposed_actions` 仅填写直接外显操作，`more_actions` 填写被收纳操作。
- 只有用户强烈指定概要区超过两行时，才设置 `summary_fields_override.enabled: true`，并填写超额字段与原因。
- `body_contract.section_style` 表示正文默认样式；带 Tab 且各 Tab 不同时，通过 `body_modules[].section_style` 逐项记录。
- `drawer_navigation=drilldown` 不改变 Drawer 的 `templateId`。
- `sequence_navigation=enabled` 对应 `footer_mode=sequence-controls`；`disabled` 对应 `none`。

## 9. 实现与参考证据

### 9.1 实现绑定

- `encapsulation: true` 时，在编码阶段核验目标分支中的真实模板入口和参数；封装未覆盖的能力按本契约补充。
- `encapsulation: false` 时，不得声称复用了页面模板，按本 Template 契约与项目组件实现。
- 参考页面只用于核对容器、概要区、正文组织、导航和视觉关系，不自动继承其业务字段、操作、权限和历史样式。

### 9.2 前端参考

以下路径均相对于前端工程 `/Users/sangfor/Documents/aes-mgr-front0830`。

| 详情结构 | 参考页面 | 关键源码 |
| --- | --- | --- |
| 连续浏览 Drawer | 病毒详情 | `app/aes-virus/src/view/virus_list/components/virus_table.vue` |
| 病毒详情正文 | 病毒信息、资产信息、检测与处置记录 | `app/aes-virus/src/view/virus_detail/index.vue` |
| 单记录 Drawer | 任务详情 | `app/aes-task/src/view/components/drawer_task_detail.vue` |
| 640px 带 Tab Drawer | 安全事件行为详情 | `app/aes-incident/src/view/mod_sec_event/components/behavior_detail_drawer/index.vue` |
| 独立下钻 Page | 安全事件详情 | `app/aes-incident/src/view/mod_sec_event/event_detail/index.vue` |
| 独立下钻 Page | 任务中心详情 | `app/aes-task/src/view/task_detail/index.vue` |
| 独立下钻 Page | 客户端详情 | `app/aes-agent/src/view/agent_detail/index.vue` |

病毒详情需要同时核对列表中的 Drawer 容器与详情正文：前者提供宽度、连续浏览和关闭方式，后者提供概要与正文模块。

## 10. 状态、异常与边界

### 10.1 加载与失败

- 首次加载使用与页面结构匹配的骨架或加载态，避免空白容器。
- 概要与正文可以分开加载；概要失败时不得显示错误对象标题，正文局部失败只替换对应分区或 Tab。
- 整体失败显示重试入口，并保留退出或返回能力。
- 操作成功后刷新受影响区域并同步父列表；失败时保留当前内容和用户位置。

### 10.2 空值与长内容

- 普通空字段显示 `-`；整个模块无数据时显示模块级空状态，不罗列整屏 `-`。
- 长标题、路径、哈希、ID 和描述必须提供省略、换行、复制或 Tooltip 中合适的一种完整查看方式。
- 原始 JSON、日志和代码使用等宽字体并支持复制；数据量大时使用虚拟滚动或按需加载。
- 字段和值不得与操作区重叠，不得因国际化长文案改变操作区固定位置。

### 10.3 权限与离开

- 无查看权限时不进入详情；局部无权限时在对应模块展示明确状态。
- 无操作权限的动作按平台规则隐藏或禁用；禁用时说明原因。
- 高风险操作必须二次确认，成功与失败均提供明确反馈。
- 存在未保存输入时，关闭 Drawer、返回、切换 Tab 或跳转前按影响范围提供离开确认。

## 11. 退出检查

交付详情页设计前逐项确认：

- [ ] 已先选择 `detail_container` 与 `entry_mode`，没有从固定模板反推容器。
- [ ] Drawer 已按“Tab → 宽度 → templateId → 分区 → 底部操作区”完成判断。
- [ ] 有 Tab 时默认建议 960px；沿用 640px 时有同模块参考且内容可承载。
- [ ] 无 Tab 宽度判断使用“最大表格列数”和“全部区域举证字段总数”。
- [ ] 概要区统一为浅色；主标题下关键字段不超过两行，例外已记录。
- [ ] 640px / 960px 的 label-value 分别为一行一组 / 一行两组。
- [ ] 640px / 960px 的操作可见槽位分别为 2 / 3，且“更多”占槽位。
- [ ] 无 Tab 使用蓝色竖线分区标题；有 Tab 时各 Tab 独立决定是否使用浅色标题带。
- [ ] JSON 与表格横向占满内容区。
- [ ] 只有连续浏览时才显示“上一个 / 下一个 / 关闭”固定底部区。
- [ ] 下钻 Drawer 使用返回按钮但仍映射四个 Drawer 模板；独立下钻 Page 没有误套 Drawer 逻辑。
- [ ] 已输出完整 `template_contract`，并基于真实前端入口填写 `encapsulation`。
