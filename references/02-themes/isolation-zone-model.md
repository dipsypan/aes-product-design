# AES 隔离区 Theme Model

> `Coverage: override`

> **归属：AES Product Design。** 本 Reference 定义 AES 产线中隔离区的业务模型、页面任务和下游约束。

## 目录

1. Theme 定位与执行顺序
2. 业务决策
3. 页面拆解框架
4. 页面业务设计
5. 下游锁定
6. 输出契约与准出检查

## 1. Theme 定位与执行顺序

本 Theme 负责：

- 隔离记录、处置对象、执行资产和隔离来源之间的关系。
- 哪些处置结果可以进入隔离区。
- 隔离记录的唯一性和最新处置规则。
- 列表、详情抽屉以及恢复、删除任务的业务内容。
- 恢复、删除失败后的记录保留和重试规则。
- 必须锁定的下游页面和操作契约。

本 Theme 不负责：

- 通用列表、表格、抽屉和表单模板。
- 通用筛选、批量选择和任务表单交互。
- 文件、注册表、服务、账户等实体的完整字段目录。
- 任务中心的完整任务生命周期和执行结果展示。
- 组件 API、代码实现和通用文案规则。

执行顺序：

```text
业务决策
→ 业务对象与关系
→ 业务不变量与生命周期
→ 页面任务拆解
→ 页面业务契约
→ 锁定必要的下游方案
→ 输出 Theme 契约
```

## 2. 业务决策

### 2.1 决策输入

| 变量 | 含义 | 取值 | 信息来源 |
| --- | --- | --- | --- |
| `disposal_recoverable` | 处置结果是否可恢复 | `true / false` | 用户/产品事实 |
| `record_uniqueness` | 隔离记录唯一性 | `one-record-per-entity` | 产品业务规则 |
| `latest_disposal_wins` | 多次处置是否只保留最新处置 | `true / false` | 产品业务规则 |
| `entity_can_be_disposed_again` | 实体未恢复前是否允许再次处置 | `true / false` | 产品业务规则 |
| `operation_task_based` | 恢复和删除是否通过任务下发 | `true / false` | 产品事实 |
| `failure_record_visibility` | 操作失败后是否保留记录 | `keep / remove` | 产品事实 |
| `failure_result_location` | 失败原因查看位置 | `task_center_only / isolation_zone` | 产品事实 |
| `retry_after_delete_failure` | 删除失败后是否允许重试 | `true / false` | 产品事实 |
| `operation_disabled_while_executing` | 任务执行中是否禁用操作 | `true / false` | 产品事实 |
| `auto_cleanup` | 是否自动过期或清理 | `true / false` | 产品事实 |
| `default_sort` | 列表默认排序 | `disposal_time_desc` | 产品事实 |
| `source_link_open_mode` | 隔离来源打开方式 | `same_tab / new_tab` | 产品事实 |
| `delete_confirmation` | 删除是否需要二次确认 | `true / false` | 产品事实 |
| `entity_field_source` | 实体字段目录来源 | `requirement / product_fact / pending` | 用户/项目实现 |

### 2.2 业务判断

| 条件 | 业务结论 | 页面和能力影响 |
| --- | --- | --- |
| `disposal_recoverable=true` | 可恢复处置结果进入隔离区 | 生成隔离记录 |
| `disposal_recoverable=false` | 不可逆处置结果不进入隔离区 | 不生成隔离记录 |
| `record_uniqueness=one-record-per-entity` | 每个实体在隔离区最多一条记录 | 不按处置历史拆分记录 |
| `latest_disposal_wins=true` | 多次处置只保留最新处置类型和时间 | 更新原隔离记录 |
| `entity_can_be_disposed_again=false` | 未恢复前不能再次处置 | 不按备份版本拆分 |
| `operation_task_based=true` | 恢复和删除均通过任务执行 | 结果由任务中心承载 |
| `failure_record_visibility=keep` | 失败后记录继续展示 | 可继续操作 |
| `retry_after_delete_failure=true` | 删除失败允许再次删除 | 删除操作不永久关闭 |
| `operation_disabled_while_executing=false` | 执行中不禁用操作 | 当前行仍展示恢复和删除 |
| `auto_cleanup=false` | 不存在自动清理 | 只在成功后移除记录 |
| `source_link_open_mode=new_tab` | 隔离来源新页签打开 | 保留隔离区上下文 |
| `delete_confirmation=false` | 删除无需二次确认 | 仅展示黄色风险提示条 |

```yaml
theme_decision:
  theme_id: isolation-zone
  selected_business_model: recoverable-isolation-record-management
  decision_inputs:
    disposal_recoverable: true
    record_uniqueness: one-record-per-entity
    latest_disposal_wins: true
    entity_can_be_disposed_again: false
    operation_task_based: true
    failure_record_visibility: keep
    failure_result_location: task_center_only
    retry_after_delete_failure: true
    operation_disabled_while_executing: false
    auto_cleanup: false
    default_sort: disposal_time_desc
    source_link_open_mode: new_tab
    delete_confirmation: false
    entity_field_source: pending
  business_model_confirmed: true
  needs_confirmation:
    - entity_specific_field_catalog
    - isolation_zone_permission_matrix
```

### 2.3 业务对象与关系

| 业务对象 | 定义 | 关系 |
| --- | --- | --- |
| 隔离记录 | 当前仍处于隔离状态的实体记录 | 由实体、资产和最新处置操作组成 |
| 处置对象 | 被处置并进入隔离区的实体 | 隶属于一条隔离记录 |
| 执行资产 | 执行处置并保存隔离备份的资产 | 一条隔离记录对应一个执行资产 |
| 处置操作 | 导致实体进入隔离区的最新处置动作 | 决定处置类型和处置时间 |
| 隔离来源 | 触发处置的事件、告警、日志或其他来源 | 被隔离记录引用 |
| 恢复任务 | 撤销原处置的任务 | 作用于隔离记录 |
| 删除任务 | 删除隔离备份的任务 | 成功后移除隔离记录 |

```text
处置对象 + 执行资产
        ↓
隔离记录
   ├── 最新处置操作
   ├── 隔离来源
   ├── 恢复任务
   └── 删除任务
```

### 2.4 业务不变量

- 只有可恢复的处置结果进入隔离区。
- 每个实体在隔离区最多对应一条记录。
- 隔离区记录的是实体当前的隔离状态，不是处置操作历史。
- 同一实体多次处置时，只保留最新一次处置类型和处置时间。
- 例如：服务先被禁用、后被删除，隔离区不增加第二条记录，而是将原记录更新为最新的删除服务记录。
- 实体未恢复前不能再次处置，因此不需要按备份版本或处置批次拆分。
- 列表和详情中的同一业务字段保持相同语义。
- 详情字段不能少于列表已有的业务信息。
- 恢复和删除必须通过任务下发到执行资产。
- 恢复失败后隔离记录继续展示。
- 删除失败后隔离记录继续展示，并允许再次删除。
- 恢复或删除执行中，当前行的恢复和删除操作暂不禁用。
- 恢复或删除失败原因只在任务中心查看，隔离区不展示失败原因。
- 恢复或删除成功后，隔离记录从隔离区移除。
- 不存在隔离记录自动过期或自动清理机制。

### 2.5 生命周期与权限

```yaml
lifecycle_contract:
  entity: isolation_record
  initial_state: quarantined
  states:
    - quarantined
    - restore_executing
    - restore_failed
    - delete_executing
    - delete_failed
    - restored
    - deleted
  transitions:
    - { from: quarantined, action: restore, to: restore_executing, permission: isolation.restore }
    - { from: quarantined, action: delete, to: delete_executing, permission: isolation.delete }
    - { from: restore_executing, action: success, to: restored, permission: task-system }
    - { from: restore_executing, action: failure, to: restore_failed, permission: task-system }
    - { from: delete_executing, action: success, to: deleted, permission: task-system }
    - { from: delete_executing, action: failure, to: delete_failed, permission: task-system }
    - { from: restore_failed, action: retry_restore, to: restore_executing, permission: isolation.restore }
    - { from: delete_failed, action: retry_delete, to: delete_executing, permission: isolation.delete }
  terminal_states:
    - restored
    - deleted
  deletion_rule: 恢复或删除任务成功后，记录从隔离区移除
  failure_recovery: 失败记录保留；删除失败允许再次删除；失败原因在任务中心查看
  permission_unknown:
    - isolation_zone_permission_matrix
```

## 3. 页面拆解框架

| 页面任务 | 页面目标 | 建议 Template | 是否锁定 |
| --- | --- | --- | --- |
| 隔离记录列表 | 查看、筛选和处理隔离记录 | `list` | true |
| 隔离记录详情 | 查看实体、资产和处置信息 | `detail` | true |
| 恢复任务 | 恢复一个或多个实体 | `form` | true |
| 删除任务 | 删除一个或多个隔离备份 | `form` | true |
| 任务执行结果 | 查看执行成功、失败和失败原因 | 任务中心已有页面 | false |

隔离区页面固定由列表页和详情抽屉组成。恢复和删除通过任务弹窗完成，不在隔离区直接执行资产操作。

## 4. 页面业务设计

### 4.1 隔离记录列表

#### 页面目标

用户可以查看、筛选、查看详情、恢复或删除隔离记录，并支持批量恢复和批量删除。

#### 页面框架调用

- `template_requirement: list`
- `locked: true`
- 锁定原因：隔离区固定采用列表承载多条隔离记录管理。

#### 固定列表字段

| 字段 | 业务说明 |
| --- | --- |
| 处置时间 | 最新一次处置的时间 |
| 处置类型 | 最新处置，例如删除注册表、隔离文件、禁用服务 |
| 处置对象 | 按 `[实体类型名称]实体名称` 呈现 |
| 处置对象信息 | 可疑实体列表的信息陈列 + 隔离区占用大小 |
| 执行资产 | 执行处置的资产 |
| 隔离方式 | 处置触发方式 |
| 隔离来源 | 触发处置的来源 |
| 操作人 | 执行平台操作的用户或服务 |
| 资产名 | 执行资产名称 |
| 资产责任人 | 执行资产责任人 |
| 资产组 | 执行资产所属资产组 |
| 资产 IP 地址 | 执行资产 IP |
| AgentID | 执行资产 AgentID |
| 操作 | 详情、处置 |

```yaml
list_field_contract:
  final_columns:
    - { field_key: disposal_time, label: 处置时间 }
    - { field_key: disposal_type, label: 处置类型 }
    - { field_key: disposal_object, label: 处置对象 }
    - { field_key: disposal_object_info, label: 处置对象信息 }
    - { field_key: execution_asset, label: 执行资产 }
    - { field_key: isolation_method, label: 隔离方式 }
    - { field_key: isolation_source, label: 隔离来源 }
    - { field_key: operator, label: 操作人 }
    - { field_key: asset_name, label: 资产名 }
    - { field_key: asset_owner, label: 资产责任人 }
    - { field_key: asset_group, label: 资产组 }
    - { field_key: asset_ip, label: 资产 IP 地址 }
    - { field_key: agent_id, label: AgentID }
    - { field_key: actions, label: 操作 }
```

#### 字段和操作规则

- 默认按处置时间倒序排列。
- 处置对象显示为 `[实体类型名称]实体名称`，例如 `[文件名] etyewte.txt`、`[用户名] Admin`。
- 点击处置对象字段，打开详情抽屉。
- 处置类型显示最新一次导致实体进入隔离区的处置。
- 隔离方式取以下值：
  - 通过安全事件处置
  - 通过告警链处置
  - 通过日志调查处置
  - 通过病毒列表处置
  - 客户端自动处置
  - 客户端手动处置
  - 通过黑名单规则处置
  - 联动接口处置
- 其他平台通过处置接口下发时，隔离方式取“联动接口处置”。
- 隔离来源显示为“来源名称（ID：来源ID）”。
- 点击隔离来源，在新页签打开对应隔离来源详情页。
- 操作列支持查看详情。
- 操作列支持“处置”下拉菜单，菜单项为恢复和删除。
- 列表支持批量恢复和批量删除。
- 任务执行中不禁用恢复和删除。
- 恢复或删除失败后记录继续展示。
- 恢复或删除成功后记录从列表移除。

```yaml
page_contract:
  page_id: isolation-list
  page_goal: 管理当前仍处于隔离状态的实体记录
  business_object: isolation_record
  template_requirement: list
  required_actions:
    - view_detail
    - open_action_menu
    - restore
    - delete
    - batch_restore
    - batch_delete
  required_states:
    - quarantined
    - restore_executing
    - restore_failed
    - delete_executing
    - delete_failed
  pattern_requirements:
    - filtering
    - table-management
  feature_requirements:
    - table-selection
    - link-navigation
  needs_confirmation:
    - entity_specific_field_catalog
    - isolation_zone_permission_matrix
```

### 4.2 隔离记录详情抽屉

#### 页面目标

查看一条隔离记录的实体信息、执行资产信息和处置操作信息，并发起恢复或删除。

#### 触发逻辑

- 点击处置对象列的值，打开详情抽屉。
- 点击操作列中的详情，打开详情抽屉。

#### 页面框架调用

- `template_requirement: detail`
- `locked: true`
- 锁定原因：两个入口必须打开同一个详情抽屉。

#### 页面结构

```text
详情抽屉
├── 顶部实体区域
│   ├── 实体名称 + 实体类型标签
│   ├── 处置类型 + 执行资产
│   └── 恢复、删除按钮
├── 处置对象信息
├── 执行资产信息
└── 处置操作信息
```

#### 页面业务内容

| 页面区域 | 必须包含的内容 |
| --- | --- |
| 顶部实体区域第一行 | 实体名称 + 实体类型名称，实体类型名称使用标签 |
| 顶部实体区域第二行 | 处置类型 + 执行资产 |
| 顶部操作区 | 恢复、删除 |
| 处置对象信息 | 全部实体信息，覆盖列表中的处置对象和处置对象信息字段 |
| 执行资产信息 | 资产名、资产责任人、资产组、资产 IP 地址、AgentID |
| 处置操作信息 | 处置时间、隔离方式、隔离来源、操作人 |

业务规则：

- 处置对象字段在详情中使用具体实体类型名称，例如“文件名”“用户名”，不能直接命名为“处置对象”。
- 详情信息必须与列表字段一一对应。
- 详情字段只能比列表字段多，不能比列表字段少。
- 详情抽屉不展示恢复或删除失败原因。
- 失败原因只在任务中心任务记录查看。
- 执行中不禁用恢复和删除按钮。

```yaml
page_contract:
  page_id: isolation-detail-drawer
  page_goal: 查看单条隔离记录的实体、资产和处置操作信息
  business_object: isolation_record
  template_requirement: detail
  required_actions:
    - restore
    - delete
    - close
  pattern_requirements:
    - detail-drawer
  feature_requirements:
    - link-navigation
  needs_confirmation:
    - entity_specific_field_catalog
```

### 4.3 恢复任务

恢复是撤销原处置操作。系统通过创建恢复任务，将任务下发给执行资产执行，用户在任务中心任务记录中查看执行结果。

| 场景 | 弹窗标题 | 默认任务名称 | 执行对象信息组织方式 |
| --- | --- | --- | --- |
| 单个对象 | `新增任务_恢复「实体类型」` | `恢复「实体类型」_YYYYMMDDHHmmss` | Label-Value 逐项展示执行资产和实体信息，不使用表格 |
| 多个对象且类型相同 | `新增任务_批量恢复「实体类型」` | `批量恢复「实体类型」_YYYYMMDDHHmmss` | 表格逐行展示多个执行对象 |
| 多个对象且类型不同 | `新增任务_批量恢复` | `批量恢复_YYYYMMDDHHmmss` | 表格逐行展示多个执行对象 |

单个恢复和同类型批量恢复的弹窗顶部均展示对应恢复操作的说明解释提示条。

批量执行对象表格固定包含三列：

- 执行资产
- 处置对象
- 处置对象信息

多处置类型批量恢复时，顶部展示：

> 涉及多个处置类型时，下发后会自动根据处置类型拆分多个任务，具体可在任务记录查看。

其中“任务记录”后带跳转按钮，整体作为蓝色跳转按钮呈现，点击后打开任务中心任务记录页面。

```yaml
restore_task_contract:
  task_based: true
  result_location: task-center.task-record
  single_object:
    title: 新增任务_恢复「实体类型」
    notice_required: true
    execution_object:
      organization: label-value
      use_table: false
    task_name: 恢复「实体类型」_YYYYMMDDHHmmss
  same_type_batch:
    title: 新增任务_批量恢复「实体类型」
    notice_required: true
    execution_object:
      organization: table
      columns: [execution_asset, disposal_object, disposal_object_info]
    task_name: 批量恢复「实体类型」_YYYYMMDDHHmmss
  mixed_type_batch:
    title: 新增任务_批量恢复
    execution_object:
      organization: table
      columns: [execution_asset, disposal_object, disposal_object_info]
    task_name: 批量恢复_YYYYMMDDHHmmss
    split_by_disposal_type: true
    task_record_link:
      label: 任务记录
      visual_style: blue-link-button
      action: open_task_record_page
      target: task-center.task-record
```

### 4.4 删除任务

删除是从隔离区中删除隔离备份。删除后备份无法被找回。删除通过创建删除任务下发给执行资产执行，用户在任务中心任务记录中查看执行结果。

删除无需二次确认。

| 场景 | 弹窗标题 | 默认任务名称 | 执行对象信息组织方式 |
| --- | --- | --- | --- |
| 单个对象 | `新增任务_删除「实体类型」` | `删除「实体类型」_YYYYMMDDHHmmss` | Label-Value 逐项展示执行资产和实体信息，不使用表格 |
| 多个对象且类型相同 | `新增任务_批量删除「实体类型」` | `批量删除「实体类型」_YYYYMMDDHHmmss` | 表格逐行展示多个执行对象 |
| 多个对象且类型不同 | `新增任务_批量删除` | `批量删除_YYYYMMDDHHmmss` | 表格逐行展示多个执行对象 |

所有删除任务弹窗顶部必须展示黄色风险提示条：

> 删除后，所选对象将被永久删除，后续无法被找回，请谨慎操作。

批量执行对象表格固定包含三列：

- 执行资产
- 处置对象
- 处置对象信息

多处置类型批量删除时，黄色提示条展示两行内容：

第一行：

> 删除后，所选对象将被永久删除，后续无法被找回，请谨慎操作。

第二行：

> 涉及多个处置类型时，下发后会自动根据处置类型拆分多个任务，具体可在任务记录查看。

其中“任务记录”后带跳转按钮，整体作为蓝色跳转按钮呈现，点击后打开任务中心任务记录页面。

```yaml
delete_task_contract:
  task_based: true
  irreversible: true
  confirmation_required: false
  result_location: task-center.task-record
  warning_notice:
    visible: true
    visual_style: yellow-warning-banner
    content: 删除后，所选对象将被永久删除，后续无法被找回，请谨慎操作。
  single_object:
    title: 新增任务_删除「实体类型」
    execution_object:
      organization: label-value
      use_table: false
    task_name: 删除「实体类型」_YYYYMMDDHHmmss
  same_type_batch:
    title: 新增任务_批量删除「实体类型」
    execution_object:
      organization: table
      columns: [execution_asset, disposal_object, disposal_object_info]
    task_name: 批量删除「实体类型」_YYYYMMDDHHmmss
  mixed_type_batch:
    title: 新增任务_批量删除
    execution_object:
      organization: table
      columns: [execution_asset, disposal_object, disposal_object_info]
    task_name: 批量删除_YYYYMMDDHHmmss
    split_by_disposal_type: true
    warning_notice:
      content:
        - 删除后，所选对象将被永久删除，后续无法被找回，请谨慎操作。
        - 涉及多个处置类型时，下发后会自动根据处置类型拆分多个任务，具体可在任务记录查看。
    task_record_link:
      label: 任务记录
      visual_style: blue-link-button
      action: open_task_record_page
      target: task-center.task-record
```

## 5. 下游锁定

```yaml
prescribed_downstream_contracts:
  templates:
    - { contract_id: isolation-list, locked: true, template: list }
    - { contract_id: isolation-detail-drawer, locked: true, template: detail }
    - { contract_id: isolation-restore-task, locked: true, template: form }
    - { contract_id: isolation-delete-task, locked: true, template: form }

  patterns:
    - { contract_id: filtering, locked: false, default_sort: disposal_time_desc }
    - { contract_id: table-management, locked: true, values: list_field_contract }
    - { contract_id: form-management, locked: true, values: [restore_task_contract, delete_task_contract] }
    - { contract_id: tiered-confirmation, locked: false, enabled_when: false }

  features:
    - { contract_id: table-selection, locked: true, values: [restore, delete] }
    - contract_id: link-navigation
      locked: true
      values:
        isolation_source: { open_mode: new_tab, target: source_detail }
        task_record: { open_mode: task_center_page, target: task-center.task-record, visual_style: blue-link-button }

  components:
    - contract_id: page-notice
      locked: true
      enabled_when: delete_task
      values:
        visual_style: yellow-warning-banner
        content: 删除后，所选对象将被永久删除，后续无法被找回，请谨慎操作。

  copy:
    - contract_id: isolation-terminology
      locked: true
      values:
        terms: [隔离区, 隔离记录, 处置对象, 处置对象信息, 隔离方式, 隔离来源, 恢复, 删除, 任务记录]
```

下游执行原则：

- Theme 锁定业务结构、字段语义和任务分支。
- Template 补全列表、详情抽屉和任务表单容器。
- Pattern 补全筛选、表格、表单和信息组织交互。
- Feature 执行批量选择、来源跳转和任务记录跳转。
- Component 执行黄色风险提示条和其他真实组件映射。
- 不同实体类型的字段目录由需求定义，不在 Theme 中自行补全。
- 权限矩阵未确认前，不得自行判断具体角色权限。

## 6. 输出契约与准出检查

```yaml
theme_contract:
  theme_id: isolation-zone
  business_model_confirmed: true
  theme_decision: theme_decision
  business_objects:
    - isolation_record
    - disposal_object
    - execution_asset
    - disposal_operation
    - isolation_source
    - restore_task
    - delete_task
  object_relationships:
    - isolation_record_contains_disposal_object
    - isolation_record_belongs_to_execution_asset
    - isolation_record_references_isolation_source
    - restore_task_operates_on_isolation_record
    - delete_task_operates_on_isolation_record
  business_invariants:
    - recoverable_only
    - one_record_per_entity
    - latest_disposal_only
    - no_repeat_disposal_before_resolution
    - list_detail_consistency
    - task_based_operation
    - failure_record_retention
    - no_auto_cleanup
  lifecycle_contract: lifecycle_contract
  page_contracts:
    - isolation-list
    - isolation-detail-drawer
    - isolation-restore-task
    - isolation-delete-task
  prescribed_downstream_contracts: prescribed_downstream_contracts
  needs_confirmation:
    - entity_specific_field_catalog
    - isolation_zone_permission_matrix
  reference_gaps: []
```

准出要求：

- 所有业务判断条件都有对应输入变量。
- 已明确隔离区只接收可恢复的处置结果。
- 已明确每个实体在隔离区只有一条记录，多次处置只保留最新处置类型和时间。
- 已明确实体未恢复前不能再次处置。
- 列表固定字段和隔离方式枚举完整保留。
- 隔离来源格式、点击行为和新页签打开方式已定义。
- 操作列详情和处置下拉菜单已定义。
- 详情抽屉触发逻辑、顶部两行结构和三大分类已定义。
- 详情字段不少于列表字段对应信息。
- 恢复和删除均通过任务下发。
- 单个对象使用 Label-Value 组织执行对象信息。
- 多个对象使用表格组织执行对象信息，固定包含执行资产、处置对象、处置对象信息。
- 恢复说明提示条、删除黄色风险提示条和删除无需二次确认已定义。
- 多处置类型任务按处置类型拆分。
- “任务记录”作为蓝色跳转按钮打开任务中心任务记录页面。
- 失败原因只在任务中心展示。
- 恢复失败保留隔离记录；删除失败保留记录并允许再次删除。
- 执行中不禁用恢复和删除操作。
- 不存在自动过期和自动清理。
- 未确认的实体字段目录和权限矩阵没有被自行补全。
