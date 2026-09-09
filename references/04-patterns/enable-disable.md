# AES 启禁用 Pattern

> **归属：AES Product Design。** 本 Reference 是 AES（深信服下一代端点安全）产线专属 Pattern，不作为 Common Design 的通用交互规范。
> `Coverage: extend`
> 本文明确规定的 AES 方案优先；未覆盖事项由 `prd-design-code` 按 Coverage 调用 Common Design 补充。

## 定位与命中

本 Reference 统一业务对象「启用 / 禁用」语义在不同任务场景中的呈现与交互选择。列表、详情、抽屉、表单或批量操作中出现业务对象的启用状态时，先读取本 Pattern，再将已选方案交给对应的表单、展示或状态变更能力执行。

本 Pattern 处理的是业务对象自身是否启用，不处理按钮、字段或页面控件因权限、前置条件而进入的 disabled 状态；操作可执行性继续读取 `action-eligibility.md`。

状态值、默认值、修改权限、状态后果及是否允许变更必须来自需求、Theme、接口或真实页面，本 Pattern 不自行补充。

## 场景决策

先判断状态是否随当前表单整体保存，再判断是否为已有对象的独立状态操作：

```text
业务对象出现启用状态
├─ 状态随新增或编辑表单一起保存
│  └─ 使用 Radio：「启用 / 禁用」
├─ 已有对象支持单条即时修改
│  └─ 使用可选择目标状态的状态入口，并执行 status-change.md
├─ 当前仅允许查看状态
│  └─ 使用状态图标 + 状态文案，不显示下拉箭头
└─ 对多个已有对象执行批量修改
   └─ 使用工具栏「启用」「禁用」操作，并执行 status-change.md
```

不得只根据控件所在位置判断方案。同一表格中的编辑弹窗属于表单保存场景；详情或抽屉中不依赖整表提交的状态修改属于即时变更场景。

## 表单配置

- 新增或编辑表单中的启用状态使用 Radio，选项固定为「启用 / 禁用」。
- 状态值与其他字段一起提交，不在选择 Radio 后立即发送状态变更请求，也不单独调用 `status-change.md`。
- 新增默认值由 Theme 或需求确定；例如规则管理 Theme 已锁定新增规则默认启用时，直接执行该默认值。
- 编辑时回显当前业务真值。保存失败时保留当前表单输入，不得提前更新来源列表或详情中的状态。
- 字段位置、表单校验、依赖、dirty 保护和提交反馈继续执行 `form-management.md`。
- 不使用即时状态入口或 Switch 替代本场景的 Radio。

## 单条即时变更

- 列表、详情或抽屉中的已有对象支持独立修改启用状态时，输出“单条即时启禁用状态入口”能力要求；具体实现由后续 Component 阶段匹配。
- 状态入口使用「状态图标 + 状态文案 + 下拉箭头」，完整区域为同一点击目标。
- 状态资格、二次确认、提交、失败处理和状态回写完整执行 `status-change.md`，本 Pattern 不重复定义。
- 无修改权限或业务条件不满足时转为不可操作状态；保留状态图标与文案，不允许展开，并说明原因。
- 不使用 Switch、Radio 或另设普通按钮替代即时状态入口。

## 只读展示

- 仅展示或当前入口不可修改时，使用平台统一的启禁用状态图标和文案语义，但不显示下拉箭头。
- 启用使用平台既有启用视觉与「启用」，禁用使用平台既有禁用视觉与「禁用」；不得改写为「正常」「关闭」等近义词。
- 图标不能单独承担状态含义，必须保留状态文案。
- 普通字段的强调控制、密度和截断继续执行 `field-display.md`。

## 批量启禁用

- 表格批量操作使用工具栏「启用」「禁用」按钮；同类动作需要归组时才放入业务动作菜单。
- 不在每个已选对象上重复展开单条状态入口，也不使用 Radio 或 Switch 表达批量操作。
- 可执行范围、相同状态排除、确认数量、提交结果和刷新完整执行 `status-change.md`。

## 一致性要求

- 所有场景使用同一业务字段、状态值和「启用 / 禁用」文案，但允许根据任务目标采用不同控件。
- 表单保存与即时状态变更不得共用提交时机：Radio 随表单提交，即时状态入口选择目标状态后进入独立状态变更链路。
- 同一对象的列表、详情和抽屉必须展示同一业务真值；新增或编辑表单保存成功后再刷新来源状态。
- Pattern 只输出启禁用任务语义和交互要求，不锁定组件名称、组件路径或实现 API。

## 输出契约

```yaml
pattern_contract:
  pattern_id: enable-disable
  decision_inputs: [object_state, host_context, persistence_mode, interaction_requirement, permission]
  selected_solution: form-submit-choice | single-immediate-change | readonly-status | batch-change
  required_patterns: []
  required_features: []
  required_components: []
  downstream_component_capabilities: []
  state_contract:
    enabled_value: ""
    disabled_value: ""
    default_value: ""
    persistence_mode: form-submit | immediate-request | readonly
  return_to_template: false
  return_reason: ""
  pattern_gaps: []
```

条件补充：

- `single-immediate-change`：`required_patterns` 增加 `status-change`，`downstream_component_capabilities` 增加 `single-object-enable-disable-selector`；Pattern 不指定具体组件。
- `batch-change`：`required_patterns` 增加 `status-change`。
- `form-submit-choice`：将已选控件方案交给 `form-management` 执行。

## 业务要求

- 已先识别业务启用状态，没有把控件 disabled 状态误判为本 Pattern。
- 已根据提交时机和操作对象数量选择场景，没有仅按页面位置选择控件。
- 表单使用 Radio 并随整表保存；单条即时变更使用状态选择入口；只读状态无箭头；批量操作使用工具栏动作。
- 即时单条和批量变更均执行 `status-change.md`，没有在本 Pattern 重写确认与请求流程。
- Pattern 在没有读取具体 Component Reference 时也能完成场景决策和输出契约；组件层没有反推状态值、权限、业务后果或默认值。
