# AES 分级二次确认 Pattern

> **归属：AES Product Design。** 本 Reference 是 AES（深信服下一代端点安全）产线专属 Pattern，不作为 Common Design 的通用交互规范。
> `Coverage: extend`
> 本文明确规定的 AES 方案优先；未覆盖事项由 `prd-design-code` 按 Coverage 调用 Common Design 补充。

## 目的与边界

本 Reference 依次决定：

1. 是否需要二次确认；
2. 已有业务确认承载后是否仍需追加二次确认；
3. 使用 `input-confirmation` 还是 `click-confirmation`；
4. 使用 Popconfirm 还是 Modal；
5. 批量不可逆操作是否通过列表或表格回显操作对象。

使用约束：

- 先由 Theme、Feature 和页面框架确定业务对象、操作语义与页面入口，再调用本 Reference。
- 本 Reference 只处理确认方式、确认容器、操作范围和确认内容，不新增业务操作，不改变业务对象或生命周期。
- 用户本次明确表达并确认的要求具有最高优先级；其次保留真实产品已有且经过确认的规则；其余情况使用本文规则。
- 除用户明确指定外，`input-confirmation` 的系统判断是闭集规则，只能来自本文已登记的超高危操作及其数量阈值，不得凭主观风险感受新增。
- 业务影响、不可逆后果、回显字段和对象数据必须来自 Theme、Feature、需求、真实页面、项目代码或接口证据；证据不足且会改变结论时返回待确认。

本 Reference 不重新判断权限、操作是否应该存在、按钮位置与样式以及接口字段。

## 输入契约

```yaml
operation:
  action: 操作按钮名称
  object_context: 操作对象上下文
  object_unit: 对象计量单位
  operation_scope: single | batch
  changes_business_data_or_state: true | false
  reversibility: reversible | irreversible | not-applicable
  effective_object_count: 最终实际操作对象数量
  registered_critical_risk_rule: none | 已命中的超高危规则
  quantity_threshold_met: true | false | not-applicable
  prescribed_popconfirm: true | false
  primary_identifier_field: ""
  identification_fields: []
  object_rows: []
  impact_items: []
  consequence_copy: ""
  primary_confirmation_carrier_type: none | task-form | preview-page | config-review | other
  primary_confirmation_carrier_sufficient: true | false
reference_evidence: []
```

关键取值规则：

- `action`：取用户点击的操作按钮名称，例如“删除”“禁用”“隔离文件”“隔离资产”。
- `object_context`：从页面标题、列表对象、详情对象或表单标题识别，例如“策略”“任务计划”“文件”“资产”“客户端”。
- `object_unit`：按对象语义填写量词，例如策略用“条”、资产或客户端用“台”、文件用“个”；必须来自业务语义或现有页面表达。
- `operation_scope`：单行、详情或针对一个主对象的操作为 `single`；勾选工具栏、批量入口或明确针对多个主对象的操作为 `batch`。只按主操作对象和入口判断，不按受影响对象数量判断。
- `changes_business_data_or_state`：只读查看、展开、复制等不产生变化的操作为 `false`。
- `reversibility`：只有产品内存在明确的撤销、恢复或反向操作时才为 `reversible`；永久删除等无法还原的操作为 `irreversible`；导出等不改变业务数据或状态的操作为 `not-applicable`。不得仅因风险高就判定为不可逆。
- `effective_object_count`：资格过滤后最终实际发送请求的主操作对象数量；问句、回显和请求范围必须一致。批量入口过滤后只剩 1 个对象时仍为 `batch`，但 `{N}` 和回显只包含该对象。
- `registered_critical_risk_rule`、`quantity_threshold_met`：只按本文登记表判断；未命中规则时分别为 `none` 和 `not-applicable`。
- `prescribed_popconfirm`：仅命中本文 Popconfirm 白名单时为 `true`。
- `primary_identifier_field`：一个稳定字段即可唯一或高辨识度识别对象时填写。
- `identification_fields`：单字段不足时，填写最小必要联合标识字段。
- `object_rows`：只包含最终实际操作对象，不含已排除对象或仅受影响对象。
- `impact_items`：本次操作的业务影响，可用于单个操作的编号列表或补充说明；没有证据时不得编造。
- `consequence_copy`：Input Confirmation 展示的风险、不可逆性或后果说明；缺失且影响用户判断时返回待确认。
- `primary_confirmation_carrier_sufficient`：已有任务表单、预览页或配置复核页同时覆盖本次操作的对象、动作和主要后果时为 `true`；仅出现操作入口、对象名称或普通提示不算充分。

例如，删除 1 条策略即使影响 5 台资产，仍是 `single`；从批量工具栏删除多条策略才是 `batch`。

## 唯一判断流程

先判断是否需要二次确认，再判断二次确认的形式。确认不成立时立即结束，不再判断回显、容器、组件变体或确认文案。用户未指定的事项执行以下流程。

```text
前置规则：是否命中无条件 Popconfirm 白名单？
├─ 是 → confirmation_required: true
│       confirmation_role: standalone
│       confirmation_method: click-confirmation
│       confirmation_container: popconfirm
│       object_echo_format: none；结束
└─ 否 → 进入是否需要二次确认的判断

一、判断是否需要二次确认

1. 操作是否改变业务数据、业务状态或安全状态？
   ├─ 否 → confirmation_required: false；结束
   └─ 是 → 继续

2. 是否已有一次足够明确的业务确认承载？
   ├─ 是
   │  ├─ 属于已登记的超高危操作，且命中该规则的数量阈值
   │  │  └─ confirmation_required: true；confirmation_role: additional；confirmation_method: input-confirmation
   │  └─ 否 → confirmation_required: false；不再追加二次确认；结束
   └─ 否
      ├─ 属于已登记的超高危操作，且命中该规则的数量阈值
      │  └─ confirmation_required: true；confirmation_role: standalone；confirmation_method: input-confirmation
      └─ 否 → confirmation_required: true；confirmation_role: standalone；confirmation_method: click-confirmation

二、二次确认成立后，判断确认形式

3. 是否为批量不可逆操作？
   ├─ 否 → object_echo_format: none
   └─ 是
      ├─ 存在一个稳定、唯一或在当前范围内足够辨识的字段 → list
      ├─ 单字段不足，但已确定最小必要联合标识字段 → table
      └─ 无法确定联合标识字段 → 返回待确认

4. 根据确认方式和对象回显选择容器
   ├─ object_echo_format 为 list 或 table → modal
   ├─ confirmation_method 为 input-confirmation → modal
   └─ 其余 click-confirmation → modal
```

步骤 3 只决定是否回显实际操作对象。只要需要回显就必须使用 Modal。不可逆性不会将 Click Confirmation 升级为 Input Confirmation；通用流程的确认方式只由步骤 2 决定，无条件 Popconfirm 白名单固定为 Click Confirmation。业务影响和后果说明不属于对象回显，可依据业务证据继续展示。

## 已登记业务规则

### 超高危操作与数量阈值

系统只有同时命中下表中的操作和数量阈值时，才使用 `input-confirmation`：

| 操作 | 超高危类别 | 数量口径与阈值 | 原因 |
|---|---|---|---|
| 禁用客户端、卸载客户端 | 关闭或削弱安全防护 | 所选资产数量 ≥ 1 | 目标终端将失去或削弱客户端防护能力 |
| 隔离资产 | 造成重大终端可用性影响 | 所选资产数量 ≥ 1 | 阻断目标资产全部入站和出站网络访问，可能造成设备失联和业务中断 |
| 加入白名单 | 关闭或削弱安全防护 | 规则白名单的生效资产 ≥ 5 | 绕过对应安全检测并扩大安全绕过范围 |

- 阈值直接按当前已勾选且最终可执行的对象数量，或表中明确规定的生效对象数量计算，不设置数量未知或默认推断分支。
- 命中超高危规则后，即使已有充分业务确认承载，仍追加 Input Confirmation。例如隔离资产通过任务创建表单确认后仍需追加输入确认。
- 白名单生效资产少于 5 台时：已有充分业务确认承载则不再追加确认；没有充分承载则使用 Click Confirmation。
- 新操作即使看起来风险很高，也不得直接加入闭集；应返回待确认，由业务设计登记操作、阈值和原因。

### 常规 Click Confirmation

以下规则仅在操作没有充分业务确认承载，且未命中超高危输入确认规则时适用：

```yaml
- action: delete
  confirmation_method: click-confirmation
  scope: 所有常规删除操作
  examples:
    - 删除策略
    - 删除任务计划

- action: toggle-status
  confirmation_method: click-confirmation
  scope: 普通状态切换类操作
  examples:
    - 策略的启用和禁用切换
    - 病毒标记状态的未处置和已处置切换
```

结束进程、隔离文件、重启客户端等 Agent 处置操作，如果任务创建表单已充分确认对象、动作和主要后果，则不再追加二次确认。

## 确认容器

### Popconfirm

下列页面或功能无条件触发 Click Confirmation，并固定使用 Popconfirm；命中后不进入通用判断流程：

- 所有“导出”按钮的确认；
- 客户端下载页配置的“开启”和“关闭”确认操作。

Popconfirm 只支持 `click-confirmation` 和 `object_echo_format: none`，不支持输入“确认”、对象列表或对象表格。不得因为操作看起来简单而扩展白名单。

### Modal

未命中 Popconfirm 白名单的确认默认使用 Modal。以下场景固定使用 Modal：

- 所有 `input-confirmation`；
- 所有需要回显批量操作对象的确认；
- 需要展示较完整业务影响或风险后果的确认。

## 确认内容与组件变体

确认内容由三个独立维度组合：

```yaml
operation_scope: single | batch
confirmation_method: click-confirmation | input-confirmation
object_echo_format: none | list | table
```

- `click-confirmation` 仍是二次确认，不得误写为“不需要二次确认”。

### Modal 组件变体

Modal 根据 `confirmation_method + object_echo_format` 映射为以下六个稳定变体：

```yaml
component_variant:
  no-echo-input-confirmation:
    confirmation_method: input-confirmation
    object_echo_format: none
  no-echo-click-confirmation:
    confirmation_method: click-confirmation
    object_echo_format: none
  list-input-confirmation:
    confirmation_method: input-confirmation
    object_echo_format: list
  table-input-confirmation:
    confirmation_method: input-confirmation
    object_echo_format: table
  list-click-confirmation:
    confirmation_method: click-confirmation
    object_echo_format: list
  table-click-confirmation:
    confirmation_method: click-confirmation
    object_echo_format: table
```

`no-echo` 不等同于 `single`：单个操作和批量可逆操作都可能命中。六个变体只用于 Modal；Popconfirm 使用项目已有轻量确认组件，不设置 `component_variant`。

### 通用文案

- 标题：`{动作}{对象}`，例如“删除策略”；按钮名称已包含对象时不重复拼接。
- 单个问句：`确定要{动作}该{对象}吗？`
- 批量问句：`确定要{动作}所选的 {N}{单位}{对象}吗？`
- 主按钮：`确定`；次按钮：`取消`。
- `{N}` 必须等于 `effective_object_count`，并与对象回显数量和最终请求范围一致。
- `{动作}`、`{单位}`、`{对象}` 可由 Copy 层校准，但不得改变问句结构。

### 对象回显

`none`：

- 单个主对象由“该{对象}”表达；批量可逆操作通过问句中的 `{N}` 表达数量。
- `impact_items` 是业务影响或关联后果，不是对象回显；有证据时可以展示，没有证据时不得编造。

`list`：

- 批量不可逆操作存在一个稳定、唯一或足够辨识的字段时使用。
- 按 `1、2、3……` 编号，逐项展示 `primary_identifier_field`，例如策略名称或任务名称。
- 字段辨识度必须有业务对象定义或真实页面证据；相同值可能指向不同对象时改用 `table`。

`table`：

- 单字段无法可靠识别对象时，展示最小必要的联合标识字段。
- 至少包含“序号”和全部 `identification_fields`；不展示与识别无关的属性。
- 固定为 5 条数据的可视高度；不足 5 条时只渲染真实对象并保持容器高度，超过 5 条时表格内部纵向滚动。

通用约束：

- 列表和表格只回显最终实际操作对象，顺序与提交对象保持稳定；关闭后重新打开时按当前可执行范围重新生成。
- 已排除对象不得进入回显或 `{N}`。允许部分执行时，可说明跳过数量和原因，但不得将跳过对象显示为实际操作对象。
- 列表和表格不负责展示操作后果；风险、不可逆后果或范围变化放在回显后的说明区。
- 无法确定唯一标识或最小必要联合标识字段时返回待确认，不得随意选列。

## 输入“确认”的交互

`input-confirmation` 在单个和批量格式中均追加：

```text
{consequence_copy}，若确定{动作}请在下方输入“确认”：
[请输入“确认”]
```

- `consequence_copy` 说明业务影响、不可逆后果或安全风险，不复述表格字段。
- 占位文案固定为 `请输入“确认”`。
- 只有输入完全等于 `确认` 时，“确定”按钮才可提交；空值、空格、缺字、多字或其他文本均不匹配。
- 清空或修改为不匹配内容后，“确定”按钮恢复不可提交状态。
- `click-confirmation` 不展示输入框，直接点击“确定”即可提交。
- 点击“取消”或关闭弹窗均不执行操作，也不保留输入内容。

## 输出契约

```yaml
confirmation_contract:
  confirmation_required: true | false
  confirmation_role: standalone | additional | not-applicable
  confirmation_method: none | click-confirmation | input-confirmation
  confirmation_container: popconfirm | modal | not-applicable
  action: 操作按钮名称
  object_context: 操作对象上下文
  object_unit: 对象计量单位
  operation_scope: single | batch | not-applicable
  changes_business_data_or_state: true | false
  reversibility: reversible | irreversible | not-applicable
  effective_object_count: 0
  registered_critical_risk_rule: none | 已命中的超高危规则
  quantity_threshold_met: true | false | not-applicable
  prescribed_popconfirm: true | false
  object_echo_format: none | list | table
  component_variant: no-echo-input-confirmation | no-echo-click-confirmation | list-input-confirmation | table-input-confirmation | list-click-confirmation | table-click-confirmation | not-applicable
  primary_identifier_field: ""
  identification_fields: []
  object_rows: []
  impact_items: []
  consequence_copy: ""
  title_copy: 最终确认标题
  question_copy: 最终确认问句
  primary_confirmation_carrier_type: none | task-form | preview-page | config-review | other
  primary_confirmation_carrier_sufficient: true | false
  reference_evidence: []
```

输出约束：

- 本文要求“返回待确认”时，不生成猜测性的 `confirmation_contract`；映射到 AES Product Design 上层输出的 `status: needs_confirmation`，并把缺失信息写入 `blocking_questions`，信息补齐后重新执行本流程。
- 无需确认时：`confirmation_required: false`、`confirmation_method: none`；角色、容器和组件变体为 `not-applicable`，不生成确认文案或回显数据。
- 有充分业务承载但因超高危规则追加确认时，`confirmation_role: additional`；此前没有充分承载时为 `standalone`。
- 无条件 Popconfirm 白名单的 `confirmation_role` 为 `standalone`。
- Popconfirm 只允许与 Click Confirmation 和 `object_echo_format: none` 组合。
- `list` 只填写 `primary_identifier_field`；`table` 填写 `identification_fields`。
- Modal 根据确认方式和回显格式输出唯一 `component_variant`；Popconfirm 和无需确认时为 `not-applicable`。

## 实现绑定

- `componentId: ConfirmModal`；Modal 优先复用 [`confirm-modal.md`](../06-components/confirm-modal.md) 登记的封装，策略删除等场景可配合 `PolicyCommon` 的业务删除弹窗封装。
- 六个名称是同一确认组件的稳定 `component_variant`，不是六个独立 `componentId`；前端应通过确认方式和回显形式组合实现。
- 新封装尚未在目标分支实现并核验前标记 `encapsulation: false`；实现后以代码真实组件名更新 `componentId`，核验六个变体、Props、Events 和调用方式后才可标记 `encapsulation: true`。
- Popconfirm 复用项目现有 Popconfirm 或公共开关确认链路；编码阶段核验真实组件名和调用方式，不在本文编造组件 API。
- 封装负责确认容器、输入框和通用交互；本 Pattern 负责确认方式、触发条件、确认文案和数量口径，不负责操作成功、失败或部分成功后的反馈与业务处理。
- 封装不足或业务行为超出组件能力时，按本文规则补充实现。实现阶段不得擅自把已经确定的 Input Confirmation 降级为 Click Confirmation；用户明确表达并确认的修改除外。
- 批量列表和表格优先复用项目已有能力；不得为复用组件改变确认对象、数量口径或回显字段。

## 自检

- 已先判断是否需要二次确认；无需确认时不再继续选择形式。
- 系统只在登记的超高危操作命中阈值时使用 Input Confirmation；Popconfirm 只承载 Click Confirmation 且不回显对象。
- 批量不可逆操作的 `{N}`、回显对象和最终请求范围一致，并已正确选择 `list` 或 `table`。
