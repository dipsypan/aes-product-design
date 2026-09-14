# AES 处置状态 Pattern

> **归属：AES Product Design。** 本 Reference 是 AES（深信服下一代端点安全）产线专属 Pattern，不作为 Common Design 的通用交互规范。
> `Coverage: extend`
> 本文明确规定的 AES 方案优先；未覆盖事项由 `prd-design-code` 按 Coverage 调用 Common Design 补充。

## 调用条件

本 Pattern 统一 AES 中处置状态的展示和用户变更行为。当平台支持对某个实体下发处置操作时，必须回显该实体的处置状态。

适用场景包括但不限于：

- 安全事件、告警链中的实体列表
- 病毒防护的列表和详情
- GPT 研判结果中的可疑实体列表
- 进程图、攻击阶段图的图上实体
- 实体悬浮卡片和实体详情
- 日志详情中的源实体、目标实体
- 文件、进程、IP、域名等支持处置操作的实体列表、详情、抽屉、图上实体、日志详情及批量操作

处置状态使用 AES 现有状态文案和标签样式，不自行新增状态名称或颜色。状态为空或接口未返回时，不显示空状态。

不适用于：

- 本 Pattern 不处理业务对象的「启用 / 禁用」状态。启用 / 禁用统一读取 [`enable-disable.md`](enable-disable.md)，由该 Pattern 独立决定表单保存、单条即时修改、只读展示和批量操作方案。

状态值、状态文案、可达关系、权限和处置后果由需求、Theme、接口或真实页面提供，本 Pattern 不自行补充业务事实。

## 方案选择

先判断页面是否需要显示处置状态，再判断当前入口是否允许用户修改：

```text
存在处置状态或处置能力
├─ 否 → none
└─ 是
   ├─ 只读或系统自动推进 → display-only
   ├─ 已有对象单条即时修改 → single-disposal-status-change
   └─ 多个已有对象批量修改 → batch-disposal-status-change
```

同一实体在列表、图、卡片和详情中出现时，各入口共同使用本 Pattern；展示位置可以随上下文变化，但状态值和业务真值必须一致。

## 状态分类

### 系统推进状态

- 由处置任务或平台自动推进，例如：已处置、待处置。
- 只读展示，不显示下拉箭头，不进入用户状态变更链路。
- 具体使用图标 + 文本或终态标签，遵循 [`field-display.md`](field-display.md) 与项目已有处置组件。

### 用户可变更状态

- 由用户主动选择，例如待处置、已处置或需求明确的其他处置状态。
- 状态集合、允许到达的目标状态和操作后果必须来自上游契约。
- 单条切换时，可使用 `图标 + 文本 + 下拉箭头` 作为状态切换的入口
- 批量切换时，使用表格的工具栏区作为入口，按钮的可用性遵循 [`button-eligibility`](button-eligibility.md)

## 展示规则

### 有独立处置状态字段

当列表或详情已有“处置状态”字段、列或属性时：

- 状态直接显示在该字段中；
- 同一实体名称后不再追加处置状态标签；
- 同一实体的处置状态不得重复显示；
- 字段内若允许单条修改，交互入口复用该状态位置，不额外增加操作列按钮。

示例：

```text
实体名称：malware.exe
处置状态：已结束
```

### 没有独立处置状态字段

当页面没有单独的处置状态字段，且不应通过固定字段强化处置引导时：

- 将状态标签紧跟在实体名称、目标名称或实体标题后；
- 标签与实体名称保持同一行展示；
- 实体名称过长时按页面规则省略，并通过 Tooltip 展示完整内容，状态标签保持完整且不被省略；
- 状态不得放在无关字段、操作列或页面顶部；
- 没有处置状态时不显示空标签；
- 同一区域的同一实体只展示一个处置状态。

示例：

```text
malware.exe  [已隔离]
```

```text
源实体：powershell.exe [已结束]
目标实体：malware.exe [已隔离]
```

适用场景包括可疑实体列表、GPT 研判实体卡片、图上实体、实体详情和日志详情中的实体信息。

### 标签展示规则

- 只有实际支持处置且已有状态的实体显示标签。
- 标签必须紧跟实体名称、目标名称或实体标题；
- 使用 AES 现有处置状态标签组件和状态映射；
- 标签文案统一复用平台状态文案，例如“已结束”“已隔离”“已拦截”；
- 标签和实体名称之间保留平台标准间距；
- 标签不得覆盖、挤压或替代实体名称；
- 实体名称支持省略和 Tooltip，标签不应被省略；
- 同一实体在同一区域只显示一个处置状态标签。

推荐结构：

```text
实体名称 + 处置状态标签 + 其他实体标识
```

禁止结构：

```text
实体名称 + 独立处置状态字段 + 处置状态标签
实体名称 + 处置状态放在操作按钮旁
```

### 视觉语义

- 处置过程或结果状态按项目已有 `DisposalStatus` 等能力使用图标 + 文本；
- 已隔离、已拦截等需要在实体名称旁强调的终态使用项目已有 `DisposalTag` 等终态标签；
- 状态文案、颜色、图标和间距统一复用 AES 现有映射，不自行新增视觉体系；
- 状态入口可变更时，在既定字段或实体标题位置使用“状态图标 + 状态文案 + 下拉箭头”；只读状态不显示下拉箭头；
- 可交互状态入口替代被动标签，不同时叠加两个处置状态表现。

## 单条处置状态变更

适用于已有对象的单条即时变更。

```text
执行入口在表格的处置状态列，或表格的工具栏
→ 执行 button-eligibility
→ 执行 tiered-confirmation
├─ 取消 → 保持当前状态
└─ 完成确认 → 提交处置状态变更
   ├─ 成功 → 提示结果并重新获取业务真值
   └─ 失败 → 保持当前状态并展示失败原因
```

- 入口只展示当前对象允许到达的目标状态，当前状态保持选中；
- 再次选择当前状态不触发确认、请求或反馈；
- 用户确认前不得提前显示目标状态；
- 提交期间只锁定本次入口，防止重复提交；
- 成功后重新获取业务真值，列表保留筛选、排序和页码，详情或抽屉保持当前容器、页签和阅读位置；
- 无权限或业务条件不满足时保留当前状态，但入口不可展开，并展示对应原因。

## 批量处置状态变更

批量变更可使用列表工具栏，但仍然允许每个对象上重复展开单条入口

执行目标状态前，先计算最终可执行范围：

```text
当前状态 != 目标状态 → 可执行候选
当前状态 == 目标状态 → 排除，原因：已是目标状态，无需重复操作
```

再将已选对象、可执行候选、排除对象和原因传给 [`button-eligibility.md`](button-eligibility.md)：

- 未勾选或全部不可执行：入口禁用，不进入确认，不发送请求；
- 部分可执行：仅在业务允许时继续，并在确认前说明实际操作数量、跳过数量和原因；
- 全部可执行：作用于全部已选对象。

确认数量和请求对象必须使用最终可执行范围：

```text
confirmation.object_count = executable_count = request_count
```

批量确认、提交和刷新使用 [`tiered-confirmation.md`](tiered-confirmation.md) 及当前宿主上下文的反馈规则；不得把确认前排除的对象伪装为执行成功。

## 状态同步规则

- 处置操作完成后，更新当前实体的处置状态；
- 提交中或结果未返回时，不伪造最终状态；
- 状态为空、接口未返回或局部请求失败时，不显示错误的最终状态；
- 同一实体跨列表、图、卡片和详情的状态使用同一业务真值；
- 成功刷新后不得同时保留字段状态和实体名称后的重复标签；
- 状态文案、颜色和图标必须复用 AES 现有状态映射；
- 刷新失败时保留原状态并反馈失败，不将目标状态写入本地展示。



## 依赖路由与证据

| 命中条件 | 必须读取 |
| --- | --- |
| 处置状态字段需要选择文本、图标或标签 | [`field-display.md`](field-display.md) |
| 单条或批量变更需要判断对象资格 | [`button-eligibility.md`](button-eligibility.md) |
| 单条或批量变更需要确认 | [`tiered-confirmation.md`](tiered-confirmation.md) |
| 存在复选框选择 | [`../05-features/table-selection.md`](../05-features/table-selection.md) |
| 页面存在真实处置状态组件 | [`../06-components/index.md`](../06-components/index.md) 及对应组件 Reference |

找不到真实组件、权限或业务规则证据时记录缺口，不得虚构状态入口、状态值或请求接口。

## 业务要求

- 支持处置操作的实体能够回显处置状态；
- 有独立字段时显示在字段中，无独立字段时紧跟实体名称；
- 只读处置状态不显示交互箭头；
- 可变更处置状态统一执行资格判断、分级确认、提交、失败处理和真值回写；
- 当前状态重复选择不产生确认、请求或反馈；
- 批量变更不重复提交已处于目标状态的对象；
- 同一实体在同一区域不重复显示处置状态；
- 启用 / 禁用不在本 Pattern 内处理，统一由 `enable-disable` 路由。

## 输出契约

```yaml
pattern_contract:
  pattern_id: disposal-status
  decision_inputs:
    - current_status
    - status_semantics
    - has_status_field
    - display_context
    - entity_disposal_capability
    - mutable
    - permission
    - selected_objects
  selected_solution: display-only | single-disposal-status-change | batch-disposal-status-change | none
  display_solution: field-status | entity-tag | none
  interaction_solution: readonly | single-change | batch-change | none
  required_features: []
  required_patterns: []
  required_components: []
  component_notes: 使用项目现有处置状态展示和操作能力，具体入口由 Component 层核验
  state_contract:
    current_status: ""
    reachable_statuses: []
    mutation_mode: readonly | single | batch
  return_to_template: false
  return_reason: ""
  pattern_gaps: []
```
