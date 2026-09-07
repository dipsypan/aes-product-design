# AES 表格管理 Pattern

> **归属：AES Product Design。** 本 Reference 是 AES（深信服下一代端点安全）产线专属表格方案规范，不作为跨产线通用规范。本文明确规定的 AES 规则优先于 Common Design；未覆盖事项由 `prd-design-code` 调用 Common Design 补充。

本 Pattern 适用于所有承载结构化集合数据的表格，可由 List、Detail、Form Template，或 Modal、Drawer、局部 Feature 直接调用。调用方负责确定页面容器、所在区域、区域顺序和可用空间；本 Pattern 只决定表格内部能力、表格局部状态及其与父级查询上下文的联动。

## 目录

1. [定位与职责边界](#1-定位与职责边界)
2. [输入与能力裁剪](#2-输入与能力裁剪)
3. [筛选接入与查询联动](#3-筛选接入与查询联动)
4. [工具栏与批量操作](#4-工具栏与批量操作)
5. [字段、列与表头](#5-字段列与表头)
6. [排序与行交互](#6-排序与行交互)
7. [分页、选择与刷新](#7-分页选择与刷新)
8. [表格局部状态](#8-表格局部状态)
9. [依赖路由与证据](#9-依赖路由与证据)
10. [输出契约](#10-输出契约)
11. [准出自检](#11-准出自检)

## 1. 定位与职责边界

### 1.1 适用场景

命中以下任一场景时可读取本 Pattern：

- 独立列表页或对象管理页中的主表格；
- 详情页、Tab 或分区中的关联对象表格、执行记录表格；
- Modal、Drawer 中的查询、浏览或选择表格；
- 表单中的只读集合表格；
- 纯展示、报表或局部数据表格。

表格不要求先经过 `../03-templates/list.md`。调用方已经确定宿主容器和页面区域时直接执行；尚未确定页面类型、主容器或区域归属时返回对应 Template，不在本 Pattern 补造页面框架。

### 1.2 本 Pattern 负责

- 根据表格任务裁剪查询、工具栏、选择、操作、分页、列设置和刷新能力；
- 组织表格内部区域及其稳定顺序；
- 确定字段来源、默认列、表头、列宽、排序和行交互；
- 维护表格查询、分页、选择和局部状态之间的一致性；
- 根据命中能力调用其他 Pattern、Feature 和 Component。

### 1.3 本 Pattern 不负责

- 决定页面类型、Modal/Drawer/独立页容器、页面头部、Footer 和页面区域顺序；
- 决定是否存在概览、左树、页面提示条或详情 Tab；
- 重新选择上游已锁定的筛选方式、业务字段、权限规则和业务操作；
- 重复定义筛选组件、字段展示、状态切换、勾选、导入导出、小 i、文字链或业务组件实现；
- 将宿主页面的整体加载、整体失败或整体无权限状态包装成表格局部状态。

概览、左树、父对象、Tab 等只作为 `parent_query_scope` 输入。表格同步执行该范围，不拥有或重新编排这些区域。

## 2. 输入与能力裁剪

### 2.1 宿主上下文

调用方至少返回：

```yaml
table_context:
  host_template: list | detail | form | modal | drawer | other
  table_role: primary | embedded | selector | read-only | report
  container_id: ""
  available_width: narrow | standard | wide | unknown
  parent_query_scope: {}
  parent_refresh_placement: page-header | local | none | unknown
```

- `host_template` 只说明宿主来源，不改变本 Pattern 的规则优先级。
- `table_role=embedded` 时不得擅自生成页面头部、Footer、概览或左树。
- `table_role=read-only` 或 `report` 时默认关闭对象选择、批量操作和行内修改。
- `table_role=selector` 时由宿主 Template 或 Feature 决定选择提交方式和 Footer；本 Pattern 只返回表格选择结果。
- `parent_refresh_placement` 已存在刷新入口时，表格不得重复生成局部刷新。

### 2.2 表格任务

```yaml
table_task: browse | manage | select | display | report
```

| 表格任务 | 默认主交互 | 默认能力倾向 |
| --- | --- | --- |
| `browse` | 识别对象并进入详情 | 查询、排序、分页、字段链接 |
| `manage` | 新增、编辑、状态切换和对象操作 | 工具栏、选择、行操作、分页 |
| `select` | 查找并选择对象 | 查询、选择、分页 |
| `display` | 查看宿主上下文中的集合信息 | 精简列、局部状态，按需分页 |
| `report` | 比较、统计或导出数据 | 排序、列设置、导出，按需查询 |

字段自身存在点击行为时，字段交互优先于整行交互。配置管理表格默认禁止整行进入编辑；浏览型表格只有真实页面或上游契约明确支持时才允许整行进入详情。

### 2.3 能力开关

根据需求、Theme、Template、Feature 和真实证据确定能力，不按表格出现就默认全部开启：

```yaml
capabilities:
  filtering: true | false
  toolbar: true | false
  selection: true | false
  batch_actions: true | false
  row_actions: true | false
  pagination: true | false
  column_settings: true | false
  local_refresh: true | false
```

- 上游已锁定的能力直接执行；能力之间冲突时返回锁定来源层。
- 不存在对应能力时不展示控件，也不保留空白占位。
- 关闭分页必须有数据量、虚拟滚动、完整展示或其他明确依据；不得因表格位于详情中就默认关闭。
- 纯展示表格仍必须满足字段可读、空值、局部加载、局部失败和溢出规则。

## 3. 筛选接入与查询联动

### 3.1 Filtering Pattern 依赖

`capabilities.filtering=true` 时必须读取 [`filtering.md`](filtering.md)，完整接收其输出，不在本文件复制另一套筛选选型和字段契约：

```yaml
search_mode: condition-search | quick-filter-search | flat-filter
decision_source: user | theme | pattern
decision_locked: true | false
search_fields: []
quick_filter_fields: []
flat_filter_fields: []
batch_search: {}
default_filters: []
```

本 Pattern 只负责把已确定的筛选方案接入当前表格：

- `condition-search`：在当前表格区域上方接入高级筛选；不得重复生成轻量查询控件。
- `quick-filter-search`：在表格头部右侧接入快速筛选和搜索框。
- `flat-filter`：在表格上方或头部查询区平铺少量筛选项与搜索框，适合详情内嵌表格等空间受限场景。
- Theme 或用户锁定模式时直接执行；真实组件或接口无法满足时返回锁定来源层。
- 批量搜索是搜索框的按需扩展能力，不是列设置或独立必选按钮。

### 3.2 查询状态

使用一个 `query_context` 维护当前表格范围：

```yaml
query_context:
  parent_scope: {}
  filters: []
  keyword: ""
  sort: {}
  page: 1
  page_size: 20
```

- 父级范围、筛选、搜索、排序和分页共同决定当前查询结果。
- 父级范围、搜索、筛选或排序变化后回到第一页。
- 删除或清空条件后，筛选组件和表格结果同步更新。
- 字段点击产生筛选时必须回显到当前筛选组件。
- 局部刷新保留当前查询状态；不得同时维护两份不一致的筛选状态。
- 宿主要求恢复上下文时，返回后恢复查询、页码和表格滚动位置；宿主页面其他区域的恢复由调用方负责。

## 4. 工具栏与批量操作

### 4.1 工具栏结构

`capabilities.toolbar=true` 时，根据已开启能力组合：

```text
表格头部
├── 左侧：操作区（主操作、次要操作）
└── 右侧：查询、列设置、局部刷新（按需）
```

- 新增使用主按钮样式并位于左侧首位，不收入下拉菜单。
- 批量操作优先外放高频项，极限不超过 7 个；超出部分收入「批量操作」或「更多」菜单。
- 外放按钮只写「删除」「启用」「禁用」等动作名称，不写「批量删除」「批量启用」。
- 危险或不可逆操作是否外放、是否确认，由业务规则和 [`tiered-confirmation.md`](tiered-confirmation.md) 决定。
- 查询、列设置、批量搜索和刷新入口必须可辨识，不得互相替代。

### 4.2 按钮与对象可执行性

| 操作类型 | 未选择对象时 |
| --- | --- |
| 新增、导入及不依赖选择的入口 | 可点击 |
| 删除、启用、禁用等对象操作 | 禁用 |
| 导出 | 按 Export Feature 返回的范围规则执行 |

- 本 Pattern 只确定操作是否依赖选择结果，以及入口位于工具栏还是行内。
- 业务状态、对象类型等导致的可执行、部分执行或整体阻断，读取 [`action-eligibility.md`](action-eligibility.md)。
- 操作权限与入口显隐必须来自上游 `permission_contract`；`action-eligibility` 不处理权限。缺少权限规则且会改变交互时写入 `pattern_gaps`，不得自行推断。
- 禁用控件必须具有当前对象、当前操作对应的 `disabled_reason`，并能通过真实悬浮或既有承载查看。

### 4.3 选择与批量结果

- `capabilities.selection=true` 时完整读取 [`../05-features/table-selection.md`](../05-features/table-selection.md)。
- 勾选上限由业务或技术提供；未提供时不得自行设置。
- 根据批量操作数量和对象资格，使用 `action-eligibility` 决定禁选、部分执行或整体阻断。
- 执行前明确最终可执行对象数量；需要确认时调用 `tiered-confirmation`。
- 全部成功、部分失败和全部失败必须返回数量与失败原因，不得静默跳过对象。
- 操作完成后刷新当前表格并保留查询状态；选择集合清理由 Table Selection Feature 处理。

### 4.4 条件 Feature

- 存在导入入口时加入 [`../05-features/import.md`](../05-features/import.md)。
- 存在导出入口时加入 [`../05-features/export.md`](../05-features/export.md)。
- `asset_applicability_check.enabled=true` 时加入 [`../05-features/asset-applicability-check.md`](../05-features/asset-applicability-check.md)；关闭时不生成入口。

## 5. 字段、列与表头

### 5.1 字段来源与默认列

按以下优先级确定字段：

1. 用户明确指定字段时，以用户定义的名称、含义、顺序和默认显示状态为基线。
2. 用户未限制“只能使用这些字段”时，可补充业务 Reference 的必要字段和结构列，但不得静默补充。
3. 用户明确要求“不增加字段”时不得补充业务字段；功能因此无法成立时返回冲突。
4. 用户未指定字段时，使用业务 Reference 的字段基线，并选择完成当前表格任务所需的最小字段集合。

浏览或管理表格的最小字段集合通常支持判断：

1. 当前对象是谁；
2. 是否需要关注或处理；
3. 当前状态或结果是什么；
4. 关键变化发生在什么时间。

详情存在不代表表格应展示详情全部字段。表格支持快速比较和判断，详情负责完整解释；两者共享字段语义和数据真值，不强制共享默认展示范围。

同时遵守：

- 操作列存在时固定右侧且不可隐藏；选择列存在时固定左侧且不可隐藏。
- 至少固定一个主要识别列，保证横向滚动后仍能识别当前行。
- 不得因接口字段较多而默认全部展示。
- 非默认字段可通过列设置恢复，业务禁止或无权限展示的字段除外。
- 完整业务列组必须遵循业务 Reference 定义的字段、顺序和连续性，不得拆散或运行时追加到末尾。
- 复用真实页面列时，完整复用字段含义、表头、说明、展示方式、空值、点击行为、固定方式、列宽和响应式表现。
- 不需要有`序号`列

输出补充字段说明：

```yaml
column_source: user-defined | business-default | mixed
user_defined_columns: []
supplemented_columns: []
supplement_notice: ""
```

### 5.2 字段展示依赖

字段展示方式读取 [`field-display.md`](field-display.md)。本 Pattern 不重新决定文本、标签、状态点、图标或链接的业务语义，只约束表格布局：

- 对象名称或主要标识放在业务字段前部。
- 无值统一显示 `-`；时间使用平台统一格式。
- 普通数据行默认保持稳定行高，普通文本单行省略并悬浮展示完整内容。
- 双行展示只用于业务明确的强关联主次信息，不用于解决文本过长。
- 字段内交互不得同时触发行详情。
- 可点击字段需要当前页打开或跨页面跳转时，加入 [`../05-features/link-navigation.md`](../05-features/link-navigation.md)。
- 可直接修改离散业务状态时，加入 [`status-change.md`](status-change.md)，不得在本 Pattern 自建状态切换链路。

资产字段差异：

- “影响资产”命中资产卡片规则时加入 [`../06-components/asset-card.md`](../06-components/asset-card.md)；点击不得触发行详情。
- “生效资产”复用安全策略资产标签样式：终端图标 + `X个资产`，全部范围显示“全部资产”；点击只打开对应资产明细。

### 5.3 列宽与表头

- 表头文字禁止换行、截断或省略。
- 固定内容列使用固定宽度；短文本列使用最小宽度和内容自适应；长文本列设置最大宽度并省略；主要对象列承担剩余弹性空间。
- 每列最小宽度必须容纳完整表头文字、排序图标、小 i、筛选图标和标准间距。
- 可调整列宽时不得缩小到表头完整宽度以下，并考虑最长语言文案。
- 表头状态变化不得改变表头高度或引发布局跳动。
- 表头需要解释时加入 [`../05-features/info-icon.md`](../05-features/info-icon.md)；本 Pattern 只把其占用空间写入 `header_contract`。

```yaml
header_contract:
  - key: ""
    label: ""
    sortable: false
    info_icon: false
    filterable: false
    min_width: ""
```

### 5.4 列设置与滚动

- `capabilities.column_settings=true` 时支持显示/隐藏、顺序和宽度调整，并按账号保存。
- 多来源列配置和历史用户配置必须使用稳定字段标识；业务固定列组与旧配置冲突时迁移旧配置。
- 横向滚动条出现时保持可见；纵向滚动时表头保持可见。
- 1366 和 1920 宽度下，核心判断字段默认可见。
- 不得为消除滚动而过度压缩列宽或造成大面积省略。

## 6. 排序与行交互

### 6.1 排序

存在以下字段时默认提供可见排序入口：

- 优先级、等级；
- 所有时间字段；
- 威胁类型及业务定义了明确顺序的分类字段。

首次排序方向：优先级和等级从高到低，时间最新在前，分类字段按业务字典顺序。枚举不得直接按显示文案或字符串值排序。

默认排序按以下顺序确定：

1. 需求或业务 Reference 已明确时直接采用；
2. 存量页面保持现有默认排序；
3. 新页面按核心浏览顺序确定；无法判断时列为确认项。

- 默认只激活一个主排序字段，并显示激活状态。
- 切换排序后回到第一页并保留筛选条件。
- 排序不得破坏置顶对象或特殊对象位置等业务不变量。

### 6.2 行主交互与操作列

- 行操作按频率和重要性排列，外放 2 至 3 个，其余收入「更多」。
- 危险或不可逆操作优先收入更多菜单。
- 启停、处置等离散状态修改执行 `status-change`；复杂表单或关联影响不得行内直接修改。
- 字段点击、选择框和操作列点击不得触发行主交互。
- 操作后刷新受影响数据并反馈成功或失败，保持宿主上下文不变。
- 无权限操作按上游 `permission_contract` 处理；不得把权限问题伪装为业务不可执行。

## 7. 分页、选择与刷新

### 7.1 分页

`capabilities.pagination=true` 时：

- 分页放在表格底部，展示总数、当前页和每页数量。
- 页码、每页数量和总数必须与当前查询一致。
- 当前页因数据变化为空时回到最后有效页。
- 父级范围、搜索、筛选或排序变化后回到第一页。

### 7.2 选择信息

- 已选数量和清空入口由 Table Selection Feature 决定，默认位于分页器左侧或宿主指定的批量操作栏。
- 当前页全选、跨页选择和全部结果全选的范围必须明确。
- 全部结果全选受当前查询和权限范围约束。
- `table_role=selector` 时只向宿主返回选择结果，不决定确认按钮和 Footer。

### 7.3 刷新

- 父级已经提供刷新入口时 `capabilities.local_refresh=false`，同一张表格不得生成第二个刷新入口。
- 局部刷新入口只刷新当前表格数据，不刷新或迁移宿主页面其他区域。
- 刷新保留父级范围、筛选、搜索、排序和页码。
- 刷新期间保留已有数据并显示加载状态，避免闪空和重复触发。

## 8. 表格局部状态

通用状态语义由 Common Design 的 `references/04-patterns/05-state-patterns.md` 补充；本节只处理表格局部细则。

必须按实际能力覆盖：

- 首次加载：保留表格结构，使用表格加载态或骨架。
- 查询、排序、分页和刷新加载：保留已有数据并标识更新中。
- 初始无数据：按宿主允许的操作提供创建、导入、配置或接入引导。
- 查询无结果：说明当前条件无结果，并提供清空或调整条件入口。
- 局部请求失败：保留查询条件和已有数据，提供重试。
- 局部字段失败：优先保留当前行，在字段位置反馈失败。
- 数据权限为空：按上游权限规则反馈，不展示错误的创建引导。

宿主页面整体加载、整体错误、整体无权限，以及概览、左树等其他区域状态由调用方处理。表格局部失败不得擅自覆盖整个宿主页面。

## 9. 依赖路由与证据

### 9.1 依赖矩阵

| 命中条件 | 必须读取 |
| --- | --- |
| 存在搜索或筛选 | [`filtering.md`](filtering.md) |
| 字段需要确定展示语义 | [`field-display.md`](field-display.md) |
| 存在可修改离散状态 | [`status-change.md`](status-change.md) |
| 操作依赖对象业务资格 | [`action-eligibility.md`](action-eligibility.md) |
| 操作需要确认 | [`tiered-confirmation.md`](tiered-confirmation.md) |
| 存在复选框选择 | [`../05-features/table-selection.md`](../05-features/table-selection.md) |
| 存在导入或导出 | 对应 Import / Export Feature |
| 字段是当前页或跨页面链接 | [`../05-features/link-navigation.md`](../05-features/link-navigation.md) |
| 表头需要小 i | [`../05-features/info-icon.md`](../05-features/info-icon.md) |
| 字段使用影响资产卡片 | [`../06-components/asset-card.md`](../06-components/asset-card.md) |

权限规则当前没有 AES 独立 Pattern。上游未返回 `permission_contract` 且 Common Design 也无法确定产品差异时，记录 `reference_gaps: [table-permission-policy]`。

### 9.2 证据顺序

1. 用户明确且已确认的要求；
2. AES 业务不变量和业务 Reference；
3. 同产品、同类型真实页面和项目代码；
4. AES Pattern、Feature 和 Component；
5. Common Design 与组件库默认能力。

找不到真实组件、权限或业务规则证据时返回缺口，不得虚构入口、字段或交互。

## 10. 输出契约

```yaml
pattern_contract:
  pattern_id: table-management
  table_context:
    host_template: list | detail | form | modal | drawer | other
    table_role: primary | embedded | selector | read-only | report
    container_id: ""
    available_width: narrow | standard | wide | unknown
    parent_query_scope: {}
    parent_refresh_placement: page-header | local | none | unknown
  table_task: browse | manage | select | display | report
  capabilities:
    filtering: false
    toolbar: false
    selection: false
    batch_actions: false
    row_actions: false
    pagination: false
    column_settings: false
    local_refresh: false
  filtering_contract: {}
  query_context: {}
  toolbar_contract: {}
  permission_contract: {}
  column_source: user-defined | business-default | mixed
  user_defined_columns: []
  supplemented_columns: []
  supplement_notice: ""
  column_contract: []
  header_contract: []
  sort_contract: {}
  row_interaction_contract: {}
  pagination_contract: {}
  local_state_contract: {}
  required_patterns: []
  required_features: []
  required_components: []
  return_to_stage: none | theme | template | feature
  pattern_gaps: []
  conflicts: []
  reference_evidence: []
```

## 11. 准出自检

- 已明确宿主、表格角色、表格任务和可用空间，没有要求必须先经过 List Template。
- 页面容器、区域顺序、概览、左树、提示条和 Footer 没有在本 Pattern 重新决策。
- 查询、工具栏、选择、批量操作、行操作、分页、列设置和刷新均按需开启。
- 筛选完整采用 Filtering Pattern 的三种模式和字段契约，没有维护第二套枚举。
- 父级范围只作为查询输入，没有被误写成表格拥有的页面区域。
- 用户指定字段优先；自动补充字段已逐项说明，用户限制字段时没有擅自增加。
- 表格与详情共享字段语义和数据真值，但没有强制展示详情全部字段。
- 字段展示、状态切换、小 i、文字链、选择、导入导出和资产卡片均按条件调用对应依赖。
- 权限来自上游契约，没有交给 `action-eligibility` 推断。
- 表头、列宽、固定列、滚动、排序、分页和行交互满足当前宿主空间。
- 父级已提供刷新时没有生成重复刷新入口。
- 只覆盖表格局部状态，没有接管宿主页面整体状态。
- 所有组件、业务字段、权限和交互均有真实证据；缺口已写入 `pattern_gaps`。
- 未破坏任何 `business_invariants`。
