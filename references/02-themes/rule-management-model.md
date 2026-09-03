# AES 规则管理 Theme Model

> **归属：AES Product Design。** 本 Reference 处理 AES 平台上可管理的匹配规则。命中后不再读取 Common Theme。本模型明确指定的页面、Pattern、Feature、Component 和术语均为锁定方案；下游只执行、展开和验证，不得重新决策。未指定事项才进入对应层级判断。

## 目录

- Theme 定位与执行顺序
- 规则业务决策
- 页面拆解框架
- 规则列表页设计
- 新增与编辑表单设计
- 详情抽屉设计
- 下游锁定与参考证据
- 禁止推断、准出与输出契约

## 1. Theme 定位与执行顺序

本模型由 `../02-themes/index.md` 路由进入，负责规则业务对象、模式分支、页面拆解、字段语义、业务不变量和稳定的下游方案。

按以下顺序执行：

1. 完成第 2 节 `rule_decision`；未知事实进入 `confirmation_items`。
2. 按第 3 节拆出列表页、新增表单、编辑表单和按需详情抽屉。
3. 按第 4、5、6 节逐页输出页面契约；每个页面先声明下游 Reference，再执行 Theme 锁定结果。
4. 将锁定结果写入第 7 节 `prescribed_downstream_contracts`。
5. 下游只补全布局、状态、校验、异常和实现映射；无法执行时返回 Theme，不得自行换方案。

命中后：

- 页面容器读取 `../03-templates/`；复杂交互读取 `../04-patterns/`；单项能力读取 `../05-features/`；组件映射读取 `../06-components/`；
- 本 Theme 已指定的事项只读取对应 Reference 的执行规则，不重新选型；
- `../05-features/import.md` 是导入的唯一设计来源；`../05-features/asset-scope.md` 是可配置资产范围的唯一设计来源；
- 用户最终确认优先于本 Theme。用户修改方案后，更新锁定契约并记录影响。

## 2. 规则业务决策

本节是所有页面的业务决策闸门。第 3 至第 6 节只能展开本节结论，不得重新判断。

### 2.1 决策维度

| 维度 | 取值 | 业务影响 |
| --- | --- | --- |
| 规则用途 | `allowlist` / `blocklist` / `other` | 决定响应动作、告警和生效语义 |
| 匹配结构 | `subject` / `condition-combination` | 决定匹配内容结构、规则数量语义、名称与描述提案 |
| 条件编辑模式 | `simple-flat` / `logical-groups` / `entity-cards` | 决定使用简单动态条件、复杂条件组或对象卡片 |
| 响应动作 | `allow` / `block` / `detect` / `custom` | 页面统一称“响应动作”；多个动作写入 `allowed_values` |
| 告警信息 | 适用性、是否需要、字段集合 | 决定告警区域和相关列表字段 |
| 生效范围 | `fixed-global` / `configurable` | 可配置时强制调用 `asset-scope` |
| 过期时间 | `fixed-permanent` / `customizable` | 固定永久时不生成配置项 |
| 详情页 | `not-required` / `user-requested` | 只有用户明确指定时生成详情抽屉 |

### 2.2 `rule_decision`

```yaml
rule_decision:
  rule_intent: { value: allowlist | blocklist | other, confirmed: true | false }
  match_mode: { value: subject | condition-combination, confirmed: true | false }
  condition_editor:
    mode: simple-flat | logical-groups | entity-cards | ""
    confirmed: true | false
  response_action:
    mode: fixed | configurable
    value: allow | block | detect | custom | ""
    allowed_values: []
    confirmed: true | false
  alert_config:
    applicable: true | false | unknown
    required: true | false | unknown
    fields: []
    confirmed: true | false
  asset_scope: { value: fixed-global | configurable, confirmed: true | false }
  expiration: { mode: fixed-permanent | customizable, confirmed: true | false }
  detail:
    mode: not-required | user-requested
    user_requested: true | false
    container: drawer
    confirmed: true | false
  data_transfer:
    import:
      proposed: true | false
      user_decision: pending | enabled | disabled
    export:
      proposed: true | false
      user_decision: pending | enabled | disabled
  notice:
    required: true
    visible: true
    content_fields: [rule_purpose, current_count, count_limit]
    confirmed: true | false
  confirmation_items: []
```

约束：

- `response_action.mode=configurable` 时，`allowed_values` 必须非空；固定动作使用 `value`，不得让下游重新补动作选项。
- `alert_config.applicable=true` 时必须继续确认 `required` 和 `fields`；三项不完整前不得生成告警字段或交互。
- `match_mode.value=condition-combination` 时必须确认 `condition_editor.mode`，并强制读取 `../04-patterns/condition-expression-editor.md`。Theme 锁定模式和业务参数后，Pattern 只执行。
- 没有多对象语义且不需要条件组或可调 AND/OR 时，提案 `simple-flat`；需要多条件组或组级 AND/OR 时提案 `logical-groups`；需要强调多对象边界或对象关系时提案 `entity-cards`。用户指定结果优先。
- `match_mode=condition-combination` 时，规则名称和规则描述作为一组命名规则元数据；规则描述承担规则说明作用，不再生成备注。
- `match_mode=subject` 时，不生成规则名称、规则 ID 或规则描述；生成主体字段和备注，备注供管理员记录注意事项。
- 字段目录、操作符集合、组关系权限、对象语义、空表达式语义和业务校验必须来自 PRD 或用户确认；未知项进入 `confirmation_items`，不得由 Pattern 或 Component 自行补齐。
- `detail.user_requested=true` 是生成详情的唯一条件。其他原因只能形成是否需要详情的确认项，不得自行生成。
- `data_transfer.import` 和 `data_transfer.export` 只记录 Theme 基于需求信号给出的提案，不代表已启用；是否提供必须由用户确认。
- 用户确认启用导入或导出后，才读取对应的 `../05-features/import.md` 或 `../05-features/export.md`（当前能力文档为 Feature；不得另造一套导入/导出流程）。未确认时不得生成对应入口或下游能力契约。
- 影响字段、区域或操作的未知事实全部进入 `confirmation_items`；确认前不生成受影响内容。

## 3. 页面拆解框架

本节先确定页面集合、容器和页面之间的关系，再进入第 4、5、6 节逐页设计。不得跳过本节直接拼字段或交互。

```text
规则管理
├── 规则列表页（必需，独立页面）
│   ├── 页面提示区
│   ├── 批量操作区
│   ├── 检索与筛选区
│   ├── 规则表格区
│   └── 分页区
├── 新增规则表单（必需，Modal）
├── 编辑规则表单（必需，Modal）
└── 规则详情（仅用户指定，Drawer）
```

删除、启用、禁用、导入、导出、资产适用规则检测和结果反馈是页面内操作或单项能力，不拆成独立页面。

```yaml
page_inventory:
  list:
    required: true
    template: ../03-templates/list.md
    template_id: page-table-basic
    list_role: primary
    container: full-page
    interaction_mode: manage
  create_form:
    required: true
    template: ../03-templates/form.md
    form_container: modal
    form_mode: create
    entry_mode: contextual
    flow_structure: single-surface
  edit_form:
    required: true
    template: ../03-templates/form.md
    form_container: modal
    form_mode: edit
    entry_mode: contextual
    flow_structure: single-surface
  detail:
    required: false
    enabled_when: rule_decision.detail.user_requested=true
    template: ../03-templates/detail.md
    container: drawer
  operations:
    delete_confirm: required
    status_confirm: required
    import: { enabled_when: rule_decision.data_transfer.import.user_decision=enabled, feature: ../05-features/import.md }
    export: { enabled_when: rule_decision.data_transfer.export.user_decision=enabled, feature: ../05-features/export.md }
```

页面拆解约束：

- 默认使用一张规则列表；不得生成虚构的示例或内置规则，真实数据以接口为准。
- 单主体多类型只有在字段、权限或生命周期明显不同且用户确认时，才拆为顶部 Tab。
- 行为组合不按条件字段拆页，一条完整表达式对应一条规则。
- 列表、新增、编辑和详情共享字段语义，但分别输出各自的字段与页面契约；不得把列表列和表单字段混成一张页面表。

## 4. 规则列表页设计

### 4.1 页面框架与设计顺序

先读取 `../03-templates/list.md`，确定并执行锁定的 `page-table-basic + primary + full-page + manage`。页面最终展示区域固定为以下顺序；该顺序是页面视觉顺序，不代表 Reference 的读取顺序：

```text
规则列表页
├── 页面提示区
├── 批量操作区
├── 检索与筛选区
├── 规则表格区
└── 分页区
```

通用页面壳层、刷新位置、分页承载、列设置和列表状态按 List Template 执行；不得改变上述区域和顺序。

列表页按以下设计决策顺序执行：

1. 读取 `../03-templates/list.md`，确定页面主容器、标题栏、表格和分页骨架。
2. 读取 `../04-patterns/filtering.md`，确定检索与筛选能力的候选方案。
3. 根据 Theme 已锁定事项、PRD 明确要求和用户确认结果，形成最终 `filter_contract`。
4. 读取 `../04-patterns/page-notice.md`，执行页面提示区。
5. 读取 `../04-patterns/table-management.md` 和 `../05-features/table-selection.md`，执行批量操作区。
6. 根据已确认的 `filter_contract`、列表字段契约和操作契约，执行规则表格区。
7. 按 List Template 和 Table Management Pattern 执行分页、排序、刷新和查询状态保留。

Filtering 必须在工具栏、表格字段和分页交互设计之前完成方案确认。

### 4.2 检索与筛选区

检索与筛选区必须先读取 `../04-patterns/filtering.md`。

Filtering 只补全筛选模式的交互、状态和组件能力，不负责覆盖 Theme 已确认的业务字段，也不负责替用户决定是否需要导入、导出或资产检测。

筛选方案分为三个阶段：

```text
Filtering Reference
→ Theme / PRD 形成筛选提案
→ 用户确认
→ 锁定最终 filter_contract
```

#### 4.2.1 筛选提案

Theme 根据 PRD 和已确认的业务字段生成 `filter_contract.proposal`。提案可以包含检索模式、快速筛选字段、关键词搜索字段、批量搜索能力和默认筛选条件，但不代表最终页面方案，不得直接生成页面入口。

字段来源必须区分：`prd-required`、`user-specified`、`theme-recommended` 和 `ai-proposed`。

#### 4.2.2 用户确认

以下内容需要由用户最终确认：检索模式、快速筛选字段、关键词搜索字段、是否启用批量精准搜索、批量搜索字段和分隔方式、默认筛选条件、字段名称和字段顺序。用户确认后将结果写入 `filter_contract.final`。

#### 4.2.3 最终执行

只有 `filter_contract.final` 可以进入页面设计和下游实现。`final.decision_locked=true` 后，Pattern 只负责执行，不得切换检索模式、增删筛选字段、将表格字段自动加入筛选区或重复生成另一套筛选入口。真实组件或接口无法执行时，必须返回 Theme 或用户确认层。

三种筛选模式互斥：`condition-search`、`quick-filter-search`、`flat-filter`，不得同时生成多种模式。

```yaml
filter_contract:
  proposal:
    search_mode: quick-filter-search | condition-search | flat-filter
    quick_filter_fields: []
    search_fields: []
    batch_search:
      enabled: true | false
      fields: []
      separator: ""
    default_filters: []
  user_decision:
    status: pending | confirmed
    selected_mode: ""
    selected_quick_filter_fields: []
    selected_search_fields: []
    selected_batch_search:
      enabled: true | false
      fields: []
      separator: ""
    selected_default_filters: []
  final:
    search_mode: ""
    decision_source: user | theme
    decision_locked: true | false
    quick_filter_fields: []
    search_fields: []
    batch_search:
      enabled: true | false
      fields: []
      separator: ""
    default_filters: []
```

### 4.3 页面提示区

先读取 `../04-patterns/page-notice.md`，再执行 Theme 锁定结果：

- `rule_decision.notice.visible=true` 时，Pattern 不得重新判断是否展示；
- 内容声明规则用途、当前规则数量和数量上限；
- 具体文案由需求提供，缺失时写入 `confirmation_items`；
- 提示等级、布局和交互由 `page-notice.md` 补全，不得改变内容字段。

### 4.4 批量操作区

先读取 `../04-patterns/table-management.md` 和 `../05-features/table-selection.md`，再执行以下锁定结果：

- 操作顺序为新增、删除、启用、禁用；新增始终可用，依赖选中项的操作在无选中项时禁用；
- 可配置生效资产时，追加始终可用的“资产适用规则检测”，并完整执行 `../05-features/asset-applicability-check.md`；固定全局时不显示；
- 导入和导出只根据 PRD 信号形成是否需要的 Theme 提案，不绑定单主体或行为组合；只有用户确认启用后，才分别读取并执行 `../05-features/import.md` 或 `../05-features/export.md`；
- 删除、启用、禁用确认目标和数量；全部成功、部分失败和全部失败反馈按 Table Management Pattern 执行；
- 不在本 Theme 重写勾选、导入、导出或资产检测的完整流程。

### 4.5 规则表格区

先读取 `../04-patterns/table-management.md`，再按本节输出列表列、排序和操作列。所有列均是 Theme 提案；用户已指定时采用用户结果，未指定时进入 `confirmation_items`，确认后才进入 `list_field_contract.final_columns`。

```yaml
list_field_proposal:
  field_key: ""
  necessity: theme-required | theme-recommended | conditional | user-specified
  proposed_label: ""
  proposed_order: 0
  visible: true | false
  sortable: true | false
  user_decision: pending | accepted | rejected
  final_label: ""
  final_order: 0
```

| 建议顺序 | 抽象列/能力 | 级别 | 建议名称 | 排序 | 业务规则 |
| ---: | --- | --- | --- | --- | --- |
| 1 | 规则 ID | `conditional` | 规则 ID | 否 | 仅命名规则（通常为行为组合）展示；单主体不作为用户配置或展示字段 |
| 2 | 规则核心内容 | `theme-required` | 由用户定义 | 否 | 单主体显示主体值；行为组合显示可读摘要并支持复制完整表达式 |
| 3 | 启用状态 | `theme-required` | 启用状态 | 否 | 状态操作需确认；保持同模块现有位置 |
| 4 | 创建时间 | `theme-required` | 创建时间 | 是 | 默认 `created_at DESC` |
| 5 | 最近修改时间 | `theme-required` | 最近修改时间 | 是 | 显示完整时间 |
| 6 | 操作列 | `theme-required` | 操作 | 否 | 建议包含编辑、删除并冻结在列尾 |
| 7 | 规则名称 | `conditional` | 规则名称 | 否 | 仅行为组合命名规则使用；单主体不展示 |
| 8 | 规则描述 | `conditional` | 规则描述 | 否 | 仅行为组合命名规则使用；承担规则说明作用 |
| 9 | 备注 | `conditional` | 备注 | 否 | 仅单主体使用，供管理员记录注意事项 |
| 10 | 主体类型 | `conditional` | 按需求命名 | 否 | 仅单主体且同一入口管理多种主体时适用 |
| 11 | 分配资产 | `conditional` | 按需求命名 | 否 | `asset_scope=configurable` 时必须存在 |
| 12 | 排除资产 | `conditional` | 按需求命名 | 否 | `asset_scope=configurable` 时必须存在 |
| 13 | 生效资产 | `conditional` | 按需求命名 | 否 | `asset_scope=configurable` 时必须存在 |
| 14 | 过期时间 | `conditional` | 过期时间 | 是 | 仅 `expiration.mode=customizable` 时适用 |
| 15 | 响应动作 | `conditional` | 响应动作 | 否 | 按 `response_action` 执行 |
| 16 | 告警信息 | `conditional` | 告警信息 | 否 | 仅告警适用且需要时使用 |
| 17 | 创建者 | `theme-recommended` | 创建者 | 否 | 仅服务端提供真实字段时提案 |
| 18 | 最近修改人 | `theme-recommended` | 最近修改人 | 否 | 仅服务端提供真实字段时提案 |

表格执行规则：

- 用户拒绝 `theme-required` 列时不强制生成，但要记录影响；页面无法完成核心任务时返回 `conflicts`。
- 用户最终决定列名称、显示、顺序和操作项；下游不得新增列或调整顺序。
- 表格区只消费 `filter_contract.final`，不得重新选择筛选模式或补充筛选字段；表格字段不因出现在表格中而自动进入筛选区。
- `asset_scope=configurable` 时，固定采纳“分配资产、排除资产、生效资产”三种语义，不可省略、合并或改成单一“分配范围”；名称可以由用户微调，但列表、表单、详情和资产抽屉必须保持同一语义映射。
- 列表出现的时间字段均支持排序；默认按创建时间从最新到最早。排序切换保留检索和筛选条件并回到第一页。
- 编辑打开编辑 Modal；删除读取 `../04-patterns/tiered-confirmation.md`，确认文案为 `确定要删除该规则吗？`。
- 一行始终对应一条完整规则，不把组合条件拆成多行规则。

### 4.6 匹配内容展示

- 单主体显示完整主体值，支持悬浮复制主体值。
- 行为组合显示可读摘要，支持查看或复制完整条件表达式。
- 不得把主体值改称“规则 ID”“规则值”或其他标识。

### 4.7 分页区与列表上下文

分页、刷新、页码变化、查询条件保留和返回恢复执行 `../03-templates/list.md` 与 `../04-patterns/table-management.md`。编辑成功、批量操作完成或详情关闭后，保留当前检索、筛选、排序、页码和可恢复的滚动位置。

## 5. 新增与编辑表单设计

### 5.1 页面框架与调用顺序

新增和编辑分别输出页面契约，但共享字段语义和业务不变量：

```text
新增规则 Modal
├── 标题区
├── 单面表单内容区
└── 确定 / 取消

编辑规则 Modal
├── 标题区
├── 单面表单内容区
└── 确定 / 取消
```

按以下顺序执行：

1. 读取 `../03-templates/form.md`，执行锁定的 `modal + contextual + single-surface`。
2. 读取 `../04-patterns/form-management.md`，按用户确认的表单字段、依赖、校验、状态和提交保护执行，不重新选择容器或流程结构。
3. `asset_scope=configurable` 时读取 `../05-features/asset-scope.md`；单主体快速新增时读取 `../05-features/contextual-remark-default.md`。
4. 行为组合模式先按第 5.4 节形成并锁定条件表达式输入，再读取 `../04-patterns/condition-expression-editor.md` 执行选定模式；Pattern 与 Component 层不得重新选型或改写业务参数。

### 5.2 表单字段提案与顺序

列表列契约不直接充当表单字段契约。表单按以下顺序单独提案；用户最终决定字段、名称和顺序，确认后分别写入 `create_form_contract.final_fields` 和 `edit_form_contract.final_fields`。

| 建议顺序 | 表单字段 | 级别 | 新增 | 编辑 | 规则 |
| ---: | --- | --- | --- | --- | --- |
| 1 | 启用状态 | `theme-required` | 默认启用 | 显示当前值 | 建议为首项 |
| 2 | 规则名称 | `conditional` | 仅行为组合 | 仅行为组合 | 与规则描述组成命名规则方案；单主体不生成 |
| 3 | 规则描述 | `conditional` | 仅行为组合 | 仅行为组合 | 与规则名称组成命名规则方案；单主体不生成 |
| 4 | 过期时间 | `conditional` | 按过期模式 | 按过期模式 | 规则信息分组；固定永久时不生成 |
| 5 | 规则核心内容 | `theme-required` | 单主体为主体字段；行为组合为完整表达式 | 按模式处理 | 单主体不生成规则名称、规则 ID、规则描述 |
| 6 | 响应动作 | `conditional` | 按 `rule_decision` | 按 `rule_decision` | 固定或在 `allowed_values` 中选择 |
| 7 | 生效资产配置 | `conditional` | 按资产范围 | 按资产范围 | 可配置时执行 `asset-scope` |
| 8 | 告警信息 | `conditional` | 按告警决策 | 按告警决策 | 只使用 `alert_config.fields` |
| 9 | 备注 | `conditional` | 仅单主体 | 仅单主体 | 供管理员记录注意事项；行为组合不生成 |

规则 ID 由后台生成，新增和编辑表单均不显示、不填写。用户拒绝规则核心内容后，创建或编辑任务无法成立，必须返回冲突。

表单分组归属固定为：`规则信息` 包含启用状态、规则名称、规则描述和可配置的过期时间；`规则内容` 包含规则核心内容；生效资产、响应动作和告警信息按各自条件使用独立分组。行为组合模式使用规则名称和规则描述，不生成备注；单主体模式不生成规则名称、规则 ID 和规则描述，仅生成主体字段与备注。规则描述和备注的字段名称、是否显示和顺序仍由用户最终确认。

### 5.3 单主体表单

- 主体类型固定时不显示选择器；同一入口管理多种主体时才提案主体类型字段，名称按用户需求呈现。
- 主体值一行一个，支持多行批量新增；忽略空行并按业务约定归一化。一个值对应一条规则。
- 同批重复、存量重复、保留对象和规则冲突必须明确反馈，不得静默丢弃。
- 新增反馈全部成功、部分成功和全部失败明细；导入结果不使用本条语义，完整执行 `import.md`。
- 编辑时主体值和主体类型默认只读；更换主体应删除后新增。业务明确允许修改时重新执行重复、保留对象和冲突处理。

### 5.4 行为组合表单

行为组合表单用于配置一条完整条件表达式。基础字段、字段提案与顺序、响应动作、告警、资产和过期时间继续执行前述章节；规则配置内容必须作为独立的“规则内容”表单分组呈现。行为组合使用规则名称和规则描述，不生成备注。

Theme 必须先根据第 2 节结论形成以下锁定输入，再调用 `../04-patterns/condition-expression-editor.md`。不适用于当前模式的字段使用空值，不得由 Pattern 或 Component 猜测业务事实：

```yaml
condition_expression_contract:
  purpose: rule-match
  editor_mode:
    value: simple-flat | logical-groups | entity-cards
    decision_source: user | theme | business-reference
    decision_locked: true
  field_catalog: []
  group_contract:
    max_group_levels: 2
    level_source: pattern-default | user | theme
    root_group:
      relation: AND | OR | ""
      relation_editability: locked | user-adjustable | ""
      allowed_relations: []
    child_group:
      relation: AND | OR | ""
      relation_editability: locked | user-adjustable | ""
      allowed_relations: []
  entity_contract:
    count_mode: fixed | user-expandable | none
    min_objects: 0
    max_objects: null
    entity_cards: []
    entity_relations: []
  empty_expression:
    mode: forbidden | match-all
    decision_source: user | theme | business-reference
    confirmed: true | false
    runtime_confirmation: required | not-required
    display_message: ""
  limits:
    max_conditions_per_group: null
    max_groups: null
    max_total_conditions: null
  business_validation:
    - duplicate-rule
    - rule-conflict
    - unsupported-expression
    - unsupported-entity-relation
  submission:
    output: structured-expression
    business_semantics: one-expression-one-rule
```

锁定要求：

- `editor_mode.value` 必须与 `rule_decision.condition_editor.mode` 一致；模式选择和三种模式的具体呈现、AND/OR 位置、动态组件、联动、嵌套、对象关系与空表达式交互均由 `condition-expression-editor.md` 唯一解释。
- `field_catalog` 必须给出字段、允许的条件运算符、值控件、校验和提示；组关系是否可调、允许值、对象卡片及对象关系只按需求或用户确认填写。
- 默认最多两层条件组；只有用户明确指定更高的有限层级时才修改 `max_group_levels`，不得允许无限嵌套。
- 默认不允许空表达式。只有用户确认“空表达式代表任意条件均匹配”时才锁定为 `match-all`，并保留删除最后一个有效条件前的运行时确认。
- 无论包含多少条件、条件组或对象卡片，完整表达式只生成并提交一条规则，不得拆成多条列表记录，也不使用单主体的部分成功语义。
- Pattern 负责表达式结构与输入校验；规则重复、规则冲突、不支持的表达式和对象关系由规则业务服务校验。提交失败时保留完整表达式并定位错误。

### 5.5 响应动作、告警、资产与过期

- 固定响应动作按 `response_action.value` 呈现；可配置时只提供 `allowed_values`，不得追加动作。
- 告警仅在 `alert_config.applicable=true` 且 `required=true` 时显示，并只使用 `alert_config.fields`；切换到不适用动作后不显示、不提交。
- `asset_scope=fixed-global` 时不显示资产配置，仅说明“对全部资产生效”。用户确认不是固定全部资产生效时，强制执行 `asset-scope.md`。
- 资产配置必须表达分配、排除、生效三种语义；全部资产、指定资产、包含项、排除项、失效资产和无权限资产的处理完整执行 `asset-scope.md`。
- `expiration.mode=fixed-permanent` 时不显示配置；可自定义时支持永不过期或自定义时间，并明确时区、最小值、当天边界和到期状态。
- 字段名称统一为“过期时间”，按产品要求配合小信息图标；具体交互参照文件 Hash 黑名单规则的过期时间方式。

### 5.6 新增、编辑、快速新增与提交结果

新增和编辑必须分别输出，不得用一个通用 `form_contract` 代替：

```yaml
form_contracts:
  create:
    form_container: modal
    form_mode: create
    entry_mode: contextual
    flow_structure: single-surface
    field_proposals: []
    final_fields: []
    interaction_contracts: []
  edit:
    form_container: modal
    form_mode: edit
    entry_mode: contextual
    flow_structure: single-surface
    field_proposals: []
    final_fields: []
    readonly_fields: []
    interaction_contracts: []
```

- 新增按一条完整规则或多条单主体规则提交；编辑只处理一条完整规则。
- 编辑成功后关闭 Modal 并保留列表上下文；失败时保留输入并展示字段或冲突错误。
- 从安全事件、告警或病毒相关模块快速新增时，回填可确定字段；单主体备注完整执行 `contextual-remark-default.md`，行为组合规则描述按用户确认的字段契约处理。
- 表单分组、控件布局、确定、取消、未保存修改保护和提交状态按 Form Template 与 Form Management Pattern 执行。

## 6. 详情抽屉设计

### 6.1 生成条件与页面框架

只有 `rule_decision.detail.user_requested=true` 时生成详情；否则不读取 Detail Template，也不生成详情入口。

生成时先读取 `../03-templates/detail.md`，执行锁定的 Drawer：

```text
规则详情 Drawer
├── 标题区：规则详情 / 关闭
├── 基本信息区
├── 规则核心内容区
├── 条件能力区（按 rule_decision）
└── 状态与审计信息区
```

### 6.2 详情内容契约

- 详情只读展示用户已确认且适用于详情的字段，不新增字段。
- 字段名称和值语义与列表和表单一致；规则核心内容继续使用用户确认名称。
- 单主体展示完整主体类型和主体值；行为组合展示完整条件表达式及组间关系。
- `asset_scope=configurable` 时展示分配资产、排除资产和生效资产，名称与其他页面一致；查看完整资产执行 `asset-scope.md` 的抽屉能力。
- 告警和过期信息只在对应 `rule_decision` 条件成立时展示。
- 详情没有编辑需求时不生成空白 Footer；关闭后恢复列表上下文。

## 7. 下游锁定与参考证据

```yaml
prescribed_downstream_contracts:
  template:
    - { contract_id: rule-list, locked: true, values: page_inventory.list }
    - { contract_id: rule-create-form, locked: true, values: page_inventory.create_form }
    - { contract_id: rule-edit-form, locked: true, values: page_inventory.edit_form }
    - { contract_id: rule-detail, locked: true, enabled_when: rule_decision.detail.user_requested=true, values: page_inventory.detail }
  patterns:
    - { contract_id: filtering, locked: true, enabled_when: filter_contract.final.decision_locked=true, values: filter_contract.final }
    - { contract_id: table-management, locked: true, values: { table_task: manage, column_contract: list_field_contract.final_columns } }
    - { contract_id: form-management, locked: true, values: { fields_source: create_form_contract.final_fields | edit_form_contract.final_fields } }
    - { contract_id: page-notice, locked: true, values: { visible: true, content_source: rule_decision.notice } }
    - { contract_id: condition-expression-editor, locked: true, enabled_when: rule_decision.match_mode.value=condition-combination, values: condition_expression_contract }
  features:
    - { contract_id: table-selection, locked: true, enabled_when: bulk_operations_confirmed }
    - { contract_id: import, locked: true, enabled_when: rule_decision.data_transfer.import.user_decision=enabled, source: ../05-features/import.md }
    - { contract_id: export, locked: true, enabled_when: rule_decision.data_transfer.export.user_decision=enabled, source: ../05-features/export.md }
    - { contract_id: asset-scope, locked: true, enabled_when: rule_decision.asset_scope.value=configurable, values: { required_semantics: [assigned, excluded, effective] } }
    - { contract_id: asset-applicability-check, locked: true, enabled_when: rule_decision.asset_scope.value=configurable }
    - { contract_id: contextual-remark-default, locked: true, enabled_when: entry_type=quick-create and rule_decision.match_mode.value=subject }
  components: []
  copy:
    - { contract_id: rule-terminology, locked: true, values: AES terminology }
  unresolved_items: []
```

参考页面只按能力参照，不整页照搬：

| 能力 | 参考基准 | 允许继承 |
| --- | --- | --- |
| 规则列表 | 自定义 IOC、白名单管理列表 | 列表骨架、工具栏、表格、批量操作和行操作 |
| 单主体表单 | 自定义 IOC、白名单新增/编辑弹窗 | 主体输入、多行新增、启用状态、备注和 Modal |
| 行为组合表单 | 真实条件组合页面或用户参考图 | 字段、操作符、值、逻辑关系和条件组构建 |
| 生效资产 | 任务中心新增快速扫描任务的任务对象 | 分配、排除和生效资产契约 |
| 资产适用检测 | 安全策略列表的资产适用策略检测 | 资产检索、适用结果和实际生效项标识 |

不得从 IOC 页面自动继承黑名单、告警、过期时间或具体条件字段；不得从白名单继承特定主体类型或放通范围。用户明确要求 > 用户确认结论 > 本 Theme 锁定契约 > 真实参考页面 > Common Design。

## 8. 禁止推断、准出与输出契约

禁止引入策略优先级、复制、继承或策略层级合成；禁止把客户端规则库版本当作平台规则；禁止使用“命中结果”“处置动作”“处置方式”替代“响应动作”；禁止把主体值写成“规则值”或把域名写成“域名地址”；禁止把单主体多行误当成一条组合规则；禁止生成未定义实体。

准出前确认：

- `rule_decision` 完整，未知事实已进入 `confirmation_items`；
- 条件组合已确认 `condition_editor.mode`，并已形成完整、锁定的 `condition_expression_contract`；
- 条件编辑模式、字段目录、关系权限、对象语义、空表达式语义和业务校验均有明确来源，Pattern 未重新决策；
- 完整条件表达式只提交为一条规则，不使用单主体的部分成功语义；
- 已先输出 `page_inventory`，再分别完成列表、新增、编辑和条件详情的页面契约；
- 列表列、表单字段和详情字段分别有明确契约，共享语义但没有混成一张页面表；
- 列表先读取 List Template，再读取 Filtering 并完成提案、用户确认和最终锁定，之后按顺序读取 Page Notice、Table Management 和 Table Selection 执行页面区域；
- 新增和编辑分别输出字段、模式差异和提交结果；详情只在用户指定时输出；
- `asset_scope=configurable` 时三种资产语义均存在；导入/导出只有用户确认启用后才读取并完整执行对应能力文档；
- 下游没有重新决策锁定事项，无法执行时已返回 Theme。

```yaml
aes_stage_result:
  current_stage: theme
  status: resolved | needs_confirmation
  matched_references: [rule-management-model.md]
  resolved_design_abilities:
    - design_ability: match-rule-management
      relation: override
      aes_references: [rule-management-model.md]
      matched_aes_rules: []
      common_design_required: false
      common_design_fallbacks: []
      reference_gaps: []
      conflicts: []
  stage_contract:
    theme_contract:
      business_pattern: match-rule-management
      theme_resolution: { matched_theme: rule-management, common_theme_required: false }
      rule_decision: {}
      page_inventory: {}
      condition_expression_contract: {}
      list_contract:
        filter_contract:
          proposal: {}
          user_decision: {}
          final: {}
        toolbar_contract: {}
        list_field_contract: { proposals: [], final_columns: [] }
        sort_contract: {}
      create_form_contract: { field_proposals: [], final_fields: [], interaction_contracts: [] }
      edit_form_contract: { field_proposals: [], final_fields: [], interaction_contracts: [] }
      detail_contract:
        enabled: true | false
        enabled_when: rule_decision.detail.user_requested=true
        fields: []
      confirmation_items: []
  downstream_requirements:
    next_stage: template
    required_references:
      - { reference: ../03-templates/list.md, enabled_when: always }
      - { reference: ../03-templates/form.md, enabled_when: always }
      - { reference: ../03-templates/detail.md, enabled_when: rule_decision.detail.user_requested=true }
      - { reference: ../04-patterns/filtering.md, enabled_when: always }
      - { reference: ../04-patterns/table-management.md, enabled_when: always }
      - { reference: ../04-patterns/form-management.md, enabled_when: always }
      - { reference: ../04-patterns/page-notice.md, enabled_when: always }
      - { reference: ../04-patterns/condition-expression-editor.md, enabled_when: rule_decision.match_mode.value=condition-combination }
      - { reference: ../04-patterns/tiered-confirmation.md, enabled_when: delete-or-status-operation }
      - { reference: ../05-features/table-selection.md, enabled_when: bulk_operations_confirmed }
      - { reference: ../05-features/import.md, enabled_when: rule_decision.data_transfer.import.user_decision=enabled }
      - { reference: ../05-features/export.md, enabled_when: rule_decision.data_transfer.export.user_decision=enabled }
      - { reference: ../05-features/asset-scope.md, enabled_when: rule_decision.asset_scope.value=configurable }
      - { reference: ../05-features/asset-applicability-check.md, enabled_when: rule_decision.asset_scope.value=configurable }
      - { reference: ../05-features/contextual-remark-default.md, enabled_when: entry_type=quick-create and rule_decision.match_mode.value=subject }
    prescribed_downstream_contracts:
      template: 第 7 节 template 数组
      patterns: 第 7 节 patterns 数组
      features: 第 7 节 features 数组
      components: 第 7 节 components 数组
      copy: 第 7 节 copy 数组
      unresolved_items: 第 7 节 unresolved_items
    design_questions: confirmation_items
  return_to_stage: none | theme
  return_reason: ""
  common_design_fallbacks: []
  reference_gaps: []
  conflicts: []
  blocking_questions: []
```

输出约束：

- 存在 `user_decision=pending`、未确认的 `rule_decision` 或其他阻断页面生成的事实时，`status=needs_confirmation`，并同步写入 `confirmation_items`、`design_questions` 和 `blocking_questions`。
- 所有必要事实已确认且不存在冲突时，`status=resolved`；不得因为已给出 Theme 提案就提前标记为已解决。
- `list_contract`、`create_form_contract`、`edit_form_contract` 分别输出，不得互相代替；详情未由用户指定时，`detail_contract.enabled=false` 且不输出虚构字段。
- `required_references` 和 `prescribed_downstream_contracts` 必须按实际条件展开，不得返回空占位。
