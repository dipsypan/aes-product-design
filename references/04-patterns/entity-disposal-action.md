# AES 实体处置操作 Pattern

> **归属：AES Product Design。** 本 Reference 是 AES（深信服下一代端点安全）产线专属 Pattern，不作为 Common Design 的通用交互规范。
> `Coverage: extend`
> 本文明确规定的 AES 方案优先；未覆盖事项由 `prd-design-code` 按 Coverage 调用 Common Design 补充。

## 目录

1. Pattern 定位与执行顺序
2. 决策输入
3. 处置动作决策
4. 单条操作资格
5. 操作解释与不可用文案
6. 批量操作资格与反馈
7. 下游依赖与职责边界
8. 输出契约与准出检查

## 1. Pattern 定位与执行顺序

本 Pattern 负责：

- 处置动作的展示顺序。
- 高程度处置对低程度动作的操作限制。
- 单条处置动作是否可执行。
- 操作按钮置灰时的原因和解释说明。
- 批量处置的可执行对象和跳过对象。
- 向 `disposal-status` 返回已完成的处置状态集合。

本 Pattern 不负责：

- 定义实体支持哪些处置动作。
- 定义业务对象和生命周期。
- 定义处置状态的标签、颜色、图标和展示位置。
- 定义启用/禁用状态。
- 定义任务表单的完整结构。
- 定义具体组件 API 和代码实现。

执行顺序：

```text
读取实体处置能力和当前状态
→ 计算处置动作优先级
→ 判断高程度动作对低程度动作的限制
→ 判断单条或批量操作资格
→ 生成不可用原因和操作解释
→ 返回已完成状态及下游展示契约
```

## 2. 决策输入

| 输入 | 含义 | 来源 |
| --- | --- | --- |
| `entity_id` | 实体唯一标识 | 接口/上游 |
| `entity_type` | 实体类型 | Theme/接口 |
| `current_disposal_statuses` | 当前已完成的处置状态集合 | 接口/产品事实 |
| `supported_actions` | 实体支持的处置动作 | Theme/需求/接口 |
| `completed_actions` | 已完成的处置动作 | 接口/产品事实 |
| `entity_disposal_capability` | 实体当前是否允许处置 | 业务规则/接口 |
| `permission` | 当前用户是否具备处置权限 | 权限事实 |
| `disabled_reasons` | 已知不可用原因 | 需求/接口/产品事实 |
| `selected_objects` | 批量操作时的选中对象 | Table Selection |
| `target_action` | 当前要判断的处置动作 | 用户操作/上游契约 |
| `display_context` | 当前实体所在页面或图形上下文 | Template/页面需求 |

```yaml
action_decision:
  entity_id: ""
  entity_type: ""
  current_disposal_statuses: []
  supported_actions: []
  completed_actions: []
  entity_disposal_capability:
    allowed: true | false | unknown
    reasons: []
  permission:
    allowed: true | false | unknown
    reasons: []
  selected_objects: []
  target_action: ""
  display_context: table | detail | process_graph | attack_path_graph
  needs_confirmation: []
```

## 3. 处置动作决策

所有处置动作按照处置程度倒序排列：

```text
重启 / 注销
  >
禁用 / 结束
  >
删除 / 隔离
  >
恢复
```

### 3.1 动作排序契约

```yaml
disposal_action_priority:
  ordered_actions:
    - restart
    - logout
    - disable
    - terminate
    - delete
    - isolate
    - restore
  priority_groups:
    - { level: highest, actions: [restart, logout] }
    - { level: high, actions: [disable, terminate] }
    - { level: medium, actions: [delete, isolate] }
    - { level: special, actions: [restore] }
  restore_position: last
```

规则：

- 同一操作菜单内按上述顺序展示。
- `恢复` 是特殊动作，始终放在最后。
- 未被上游确认的动作不得自行添加到排序中。
- 动作名称使用 AES 已确认术语，不在本 Pattern 中重新命名。

### 3.2 高程度动作对低程度动作的限制

高程度处置完成后，低程度动作不能再次操作，但已经完成的低程度处置状态仍然保留。

先执行高程度动作：

```text
服务已删除
→ 禁用服务动作不可操作
→ 禁用服务按钮置灰
→ 当前处置状态：已删除
```

先执行低程度动作，再执行高程度动作：

```text
服务已禁用
→ 再执行删除服务
→ 删除服务成功
→ 当前处置状态：已删除、已禁用
```

此时：

- 已完成的两个处置状态都保留。
- 状态展示顺序按处置程度倒序，`已删除`显示在`已禁用`之前。
- 已完成的低程度状态不能被删除或伪造为未发生。
- 低程度动作是否还能继续操作，由当前动作资格判断；如果高程度操作已使其失去意义，则低程度按钮置灰。
- 多个处置状态按处置程度从高到低展示；属于同一处置程度时，按处置完成时间从早到晚展示。`disposal-status.md` 只负责标签、展示位置和视觉形式。

本 Pattern 输出的是操作限制和已完成状态集合，不输出单一的“最终状态”覆盖值：

```yaml
action_restriction:
  action: disable
  executable: false
  reason_code: higher_action_completed
  reason_text: 服务已被删除，不支持禁用服务

completed_disposal_statuses:
  - deleted
  - disabled
display_status_source: disposal-status
```

### 3.3 已完成处置状态的保留

处置动作 Pattern 只判断动作能否继续执行，不删除已经完成的处置状态。

- 每次成功处置都进入 `completed_disposal_statuses`。
- 高程度动作完成后，低程度动作可能被限制，但低程度状态仍然保留。
- 多个已完成状态的排序由本 Pattern 的业务规则确定；`disposal-status.md` 负责标签、展示位置和视觉形式。
- 不得把“低程度动作不可再执行”误写成“低程度处置状态不存在”。

```yaml
completed_disposal_statuses:
  - status: deleted
    action: delete
    preserved: true
  - status: disabled
    action: disable
    preserved: true
display_status_contract:
  source: disposal-status
  ordering:
    primary: disposal_degree_desc
    secondary: completed_at_asc
  presentation_responsibility: disposal-status
```

## 4. 单条操作资格

### 4.1 判断流程

```text
动作是否属于实体支持能力？
├─ 否 → 不展示或置灰
└─ 是
   ├─ 已被更高程度处置限制 → 置灰
   ├─ 已重复完成同一动作 → 置灰
   ├─ 当前业务状态不允许 → 置灰
   ├─ 权限不足 → 置灰
   ├─ 关键系统实体 → 置灰
   ├─ 接口返回不可执行 → 置灰
   └─ 条件满足 → 可执行
```

### 4.2 常见不可用原因

- 当前实体不支持该处置动作。
- 当前动作已被更高程度处置限制。
- 当前实体已经完成同一个处置动作，不支持重复执行。
- 实体已从隔离区删除，不支持恢复。
- 实体尚未执行过可恢复处置，不支持恢复。
- 实体属于关键系统实体，不支持对应处置。
- 当前用户没有对应权限。
- 当前接口返回不允许执行。
- 其他产品已确认的业务限制。

### 4.3 典型规则

| 条件 | 处理 |
| --- | --- |
| 实体已完成更高程度处置 | 低程度动作置灰 |
| 实体已完成同一处置动作 | 同一动作置灰，不支持重复操作 |
| 实体已从隔离区删除 | 恢复按钮置灰 |
| 实体从未被处置 | 恢复按钮置灰 |
| 实体属于关键系统实体 | 对应处置按钮置灰 |
| 当前用户无权限 | 操作置灰或不展示，遵循权限规范 |

具体实体范围、权限和业务限制必须来自需求、Theme、接口或产品事实，不由 Pattern 自行补全。

### 4.4 置灰呈现依赖

本 Pattern 只负责计算操作资格、不可用原因和操作解释；置灰操作的视觉与交互呈现必须调用 [`button-eligibility.md`](button-eligibility.md) 的“反馈方式”规则，不得在本 Pattern 中另造一套 disabled 行为。

置灰操作必须遵循：

- 操作入口保持 `disabled` 状态，不得触发处置请求或确认流程。
- 悬浮到不可用入口时，鼠标指针使用 `cursor: not-allowed`，不得显示可点击手势。
- 悬停必须说明不可用原因；原因文案使用本 Pattern 第 5 节定义的不可用文案。
- 已有气泡或下拉说明承载时，直接在原有承载中补充“不可用原因 + 当前处置操作解释”，不叠加 Tooltip。
- 没有已有承载时，使用 Tooltip 承载“不可用原因 + 当前处置操作解释”。
- 原因必须具体；存在明确解决方式时，按产品事实补充下一步说明。

依赖关系：

```text
entity-disposal-action
├─ 计算 disabled、reason 和 explanation
└─ 调用 button-eligibility
   ├─ 承载 disabled 状态
   ├─ 设置 cursor: not-allowed
   ├─ 优先复用已有气泡或下拉说明
   └─ 无既有承载时使用 Tooltip
```

## 5. 操作解释与不可用文案

### 5.1 常态操作解释

每个处置操作都必须有对应的解释说明文案。解释说明不是只在异常时显示，而是操作的常态辅助信息。

- 操作可用时：悬浮操作名称、按钮或“更多”菜单项，显示处置操作解释。
- 操作不可用时：悬浮置灰操作，显示不可用原因和处置操作解释。
- 处置操作位于表格、详情、实体卡片或其他入口时，沿用同一份解释说明。

可用状态示例：

```text
禁用计划任务

下发后将禁用计划任务，被禁用的计划任务将无法运行，
删除或禁用计划任务可在隔离区查看或恢复。
```

```yaml
disposal_action_explanation:
  action: ""
  explanation: ""
  links: []
  display:
    available: hover
    unavailable: hover
  source: requirement | product_fact | copy_reference
```

规则：

- 每个处置操作都必须有 `explanation`。
- 可用状态只显示处置操作解释，不显示不可用原因。
- 解释说明应说明操作下发后的主要效果、影响和后续处理方式。
- 解释文案涉及隔离区、任务记录等页面时，相关文字可以作为跳转链接。
- 未提供解释说明时记录 `pattern_gap`，不得自行编造操作后果。

### 5.2 不可用状态的悬浮内容

操作不可用时，悬浮内容固定分为两行，中间使用分割线：

```text
第一行：不可用原因
────────────
第二行：处置操作解释
```

示例：

```text
计划任务已删除或已禁用，不支持重复禁用
────────────────────────
下发后将禁用计划任务，被禁用的计划任务将无法运行，
删除或禁用计划任务可在隔离区查看或恢复。
```

第一行说明为什么当前操作不可用，第二行始终复用当前处置操作的常态解释说明。

### 5.3 通用不可用文案结构

```text
[原因结论]，[当前动作限制]
[处置操作解释]
```

基本要求：

- 第一行直接说明不可用原因。
- 明确指出不支持的动作。
- 第二行说明当前处置操作的作用、影响和后续处理方式。
- 不使用“操作失败”“暂不可用”“状态异常”等模糊表达。
- 不把业务不可用、权限不足和任务执行失败混写。
- 对象名称和动作名称必须与当前页面一致。

### 5.4 常见原因文案

#### 处置程度限制

```text
{对象}已被{更高程度处置}，不支持{当前动作}
```

示例：

```text
服务已被删除，不支持禁用服务
```

#### 重复执行同一操作

```text
{对象}已{当前处置状态}，不支持重复{动作}
```

示例：

```text
计划任务已删除，不支持重复删除
```

```text
计划任务已禁用，不支持重复禁用
```

```text
进程已结束，不支持重复结束
```

```text
文件已隔离，不支持重复隔离
```

#### 隔离备份已删除

```text
{对象}已从隔离区中被删除，不支持恢复
```

#### 尚未发生可恢复处置

```text
{对象}尚未被处置，不支持恢复
```

或：

```text
{对象}没有可恢复的处置记录，不支持恢复
```

#### 关键系统实体

```text
为保障系统稳定运行，关键系统实体不支持{动作}
```

#### 权限不足

```text
当前账号无权限对{对象}执行{动作}
```

权限不足不能写成“对象不支持动作”，因为动作可能被产品支持，只是当前用户无权执行。

### 5.5 文案来源优先级

```text
用户明确文案
> 产品已确认文案
> 接口返回的业务原因
> AES Copywriting Terminology
> 本 Pattern 的文案范式
```

本 Pattern 提供句式和语义结构，不固化所有实体名称、动作名称和具体原因。

## 6. 批量操作资格与反馈

批量操作先判断：

```text
1. 所选对象中是否存在可执行对象
2. 不可执行对象的原因是否一致
3. 产品是否允许部分执行
```

### 6.1 全部可执行

当所有选中对象均满足当前处置动作的执行条件时：

- 批量按钮可用。
- 请求作用于全部选中对象。
- 不展示不可用原因。
- 操作悬浮时仍显示当前处置操作的常态解释。

```yaml
batch_all_executable:
  condition:
    executable_count: equals_selected_count
  behavior:
    button_state: enabled
    submit_allowed: true
    request_objects: selected_objects
    feedback: none
```

### 6.2 全部不可执行，原因相同

当所有选中对象都因同一种原因不可执行时：

- 批量按钮禁用。
- 不进入确认流程。
- 不发送请求。
- 批量原因文案与单条操作文案保持一致。
- 下方继续展示当前处置操作的解释说明。

```text
所选计划任务已删除，不支持重复删除
────────────────────────
下发后将删除计划任务，删除后的计划任务无法恢复。
```

```yaml
batch_unavailable_same_reason:
  condition:
    executable_count: 0
    reason_group_count: 1
  behavior:
    button_state: disabled
    presentation_source: button-eligibility
    cursor: not-allowed
    submit_allowed: false
    feedback: reason-and-explanation
  content:
    reason: same_as_single_action_copy
    explanation: current_action_explanation
```

### 6.3 全部不可执行，原因不同

当所有对象都不可执行，但不可用原因存在多个时：

- 批量按钮禁用。
- 不进入确认流程。
- 不发送请求。
- 第一行汇总不可用原因。
- 第二行展示当前处置操作的解释说明。
- 解释文案涉及隔离区、任务记录等页面时，可提供跳转链接。

示例：

```text
所选服务项已被删除或属于关键系统实体，不支持删除
────────────────────────
下发后将删除服务项，可在隔离区查看或恢复。若指定了登录账户，
恢复时无法回填原账户密码，需重新输入。
```

第二行不是临时拼接的失败原因，而是当前处置操作已有的解释说明文案。

```yaml
batch_unavailable_multiple_reasons:
  condition:
    executable_count: 0
    reason_group_count: greater_than_one
  behavior:
    button_state: disabled
    presentation_source: button-eligibility
    cursor: not-allowed
    submit_allowed: false
    feedback: reason-and-explanation
  content:
    reason_summary: ""
    operation_explanation: current_action_explanation
    links: []
```

不得使用：

```text
所选对象中有些不支持删除，有些不支持删除
```

也不得直接展示接口原因编码。

### 6.4 部分可执行，部分不可执行

当选中对象中同时存在可执行和不可执行对象时：

- 批量按钮保持可用。
- 只处理可执行对象。
- 不可执行对象自动跳过。
- 使用 Toast 提示跳过数量和原因。
- 不可执行对象不进入实际请求和执行对象列表。
- 如果存在多个跳过原因，Toast 只展示汇总，不承载完整明细。

示例：

```text
4个计划任务不支持禁用操作，已自动跳过
```

```yaml
batch_partial_execution:
  condition:
    executable_count: greater_than_zero
    skipped_count: greater_than_zero
  behavior:
    button_state: enabled
    presentation_source: button-eligibility
    submit_allowed: true
    request_objects: executable_objects
    feedback: skipped-toast
  copy:
    template: "{skipped_count}个{object_type}不支持{action}，已自动跳过"
```

### 6.5 批量场景决策表

| 场景 | 按钮状态 | 反馈形式 | 文案规则 |
| --- | --- | --- | --- |
| 全部不可用，原因相同 | 禁用 | 原因 + 解释说明 | 原因与单个对象一致 |
| 全部不可用，原因不同 | 禁用 | 原因汇总卡片 | 第一行汇总原因，第二行显示操作解释 |
| 部分可执行，部分不可用 | 可用 | Toast | `{数量}个对象不支持{动作}，已自动跳过` |
| 全部可执行 | 可用 | 正常执行 | 不展示不可用文案 |

### 6.6 批量执行契约

```yaml
batch_execution_contract:
  selected_count: 0
  executable_count: 0
  skipped_count: 0
  request_count: 0
  request_count_equals_executable_count: true
  skipped_objects: []
  skipped_reasons: []
```

## 7. 下游依赖与职责边界

| 设计问题 | 下游 Reference |
| --- | --- |
| 通用按钮是否可执行 | `button-eligibility.md` |
| 是否需要二次确认 | `tiered-confirmation.md` |
| 最终处置状态如何展示 | `disposal-status.md` |
| 使用文字、图标还是标签 | `field-display.md` |
| 批量对象选择 | `../05-features/table-selection.md` |
| 具体状态、按钮或下拉组件 | `../06-components/index.md` |
| 不可用文案统一表达 | `../07-copywriting-terminology.md` |

职责边界：

- `entity-disposal-action`：判断动作顺序、状态限制、可执行范围和业务原因。
- `button-eligibility`：承载按钮启用、禁用、`cursor: not-allowed`、已有气泡优先和 Tooltip 回退规则；文案内容由本 Pattern 提供。
- `entity-disposal-action`：确定多个已完成处置状态的排序，按处置程度降序、同程度按完成时间升序。
- `disposal-status`：展示已完成的一个或多个处置状态，负责标签、展示位置和视觉形式。
- `tiered-confirmation`：决定是否需要确认以及确认层级。
- `field-display`：决定文字、图标、标签等展示形式。
- Component：核验真实组件和 API。
- Copy：校准最终用户可见文案。

## 8. 输出契约与准出检查

```yaml
pattern_contract:
  pattern_id: entity-disposal-action
  decision_inputs:
    - entity_id
    - entity_type
    - current_disposal_statuses
    - supported_actions
    - completed_actions
    - entity_disposal_capability
    - permission
    - disabled_reasons
    - selected_objects
    - target_action
    - display_context

  selected_solution: single-action-menu | batch-action-menu | display-only

  action_priority:
    order: [restart, logout, disable, terminate, delete, isolate, restore]
    higher_action_blocks_lower_action: true
    restore_position: last

  action_contract:
    available_actions: []
    disabled_actions: []
    disabled_reasons: []
    action_order: []

  completed_disposal_statuses:
    - status: ""
      action: ""
      completed_at: ""
      preserved: true

  display_status_contract:
    source: disposal-status
    statuses: []
    display_order:
      primary: disposal_degree_desc
      secondary: completed_at_asc
    presentation_responsibility: disposal-status

  action_explanation_contract:
    actions:
      - action: ""
        explanation: ""
        links: []
        source: requirement | product_fact | copy_reference
    available_display: hover-explanation
    unavailable_display: reason-divider-explanation

  disabled_action_contract:
    single:
      action: ""
      disabled: true
      reason_code: ""
      reason_text: ""
      explanation: ""
      display_mode: tooltip | existing-popover | existing-dropdown
      presentation_source: button-eligibility
      button_state: disabled
      cursor: not-allowed
      interaction:
        submit_allowed: false
        confirmation_allowed: false
    batch:
      selected_count: 0
      executable_count: 0
      skipped_count: 0
      reason_group_count: 0
      mode: same_reason | multiple_reasons | partial_execution
      reason_summary: ""
      explanation: ""
      links: []

  batch_contract:
    selected_count: 0
    executable_count: 0
    skipped_count: 0
    request_count: 0
    request_count_equals_executable_count: true
    skipped_objects: []
    skipped_reasons: []

  required_patterns:
    - button-eligibility
  optional_patterns:
    - tiered-confirmation
    - disposal-status
    - field-display
  required_features: []
  required_components: []
  pattern_gaps: []
```

准出要求：

- 处置动作顺序符合“重启/注销 > 禁用/结束 > 删除/隔离 > 恢复”。
- 恢复始终位于操作列表最后。
- 高程度处置完成后，低程度动作不能再次操作并置灰。
- 低程度处置先完成、高程度处置后完成时，已完成的多个处置状态均保留。
- 多个处置状态按处置程度从高到低展示；同一处置程度按处置完成时间从早到晚展示。
- `disposal-status` 只负责状态标签、展示位置和视觉形式，不重新决定状态排序。
- 已完成同一操作时，使用“已完成，不支持重复操作”的原因范式。
- 关键系统实体统一使用“关键系统实体”表述。
- 每个处置操作都有常态解释说明。
- 可用操作悬浮时显示解释说明。
- 不可用操作悬浮时第一行显示原因，第二行显示处置操作解释。
- 全部批量对象不可执行时，批量按钮始终禁用。
- 全部不可执行且原因相同，文案与单条一致。
- 全部不可执行且原因不同，使用原因汇总卡片。
- 部分可执行时，仅提交可执行对象，并使用 Toast 反馈跳过对象。
- 请求数量等于最终可执行数量。
- 被跳过对象没有被伪装为执行成功。
- 业务不可用、权限不足和任务执行失败没有混用。
- 未确认的权限、状态、原因编码和操作解释没有被自行补全。
