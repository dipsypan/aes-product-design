# AES 小 i 信息提示 Feature

> **归属：AES Product Design。** 本 Reference 是 AES（深信服下一代端点安全）产线专属 Feature，不作为 Common Design 的通用能力规范。
> `Coverage: extend`
> 本文明确规定的 AES 能力规则优先；未覆盖事项由 `prd-design-code` 按 Coverage 调用 Common Design 补充。

## 使用边界

本 Reference 用于 AES 页面中解释字段、表头或单个选项含义的小 i 信息提示。它只定义小 i 的使用条件、颜色、位置、交互和 Tooltip 内容，不重新决定业务字段、页面容器或业务模型。

当界面中的概念、字段或选项存在理解门槛，且用户不需要持续查看这段解释时，使用小 i + Tooltip。

## Feature 身份与封装

- `featureId: info-icon`
- `encapsulation: false`
- 当前没有映射到 AES 前端业务封装，通用 Tooltip 能力按项目组件库承载。

## 适用场景

- 解释字段的定义、作用或业务口径。
- 解释列表表头字段的含义。
- 解释单个选项的适用对象、使用场景或选择建议。
- 解释用户不需要持续查看的补充信息。
- 解释技术概念、检测方式或专业术语。

## 不适用小 i 的场景

- 业务结果、风险或不可逆后果。
- 用户提交或执行操作前必须持续看到的信息。
- 默认值、输入格式、数量限制和普通校验。
- 禁用按钮、开关或菜单项的不可用原因。
- 已经通过字段文案、组件状态或校验反馈表达的信息。

命中不适用场景时，不得为了保持视觉一致而增加小 i；应继续使用该信息所属的页面、表单、状态、校验或帮助承载方式。

## 视觉与颜色

- 小 i 必须放在对应字段、表头或选项文字之后。
- 小 i 颜色固定为 `#5E6573`。
- 默认、hover、focus 和 Tooltip 展开状态均不得改变小 i 颜色。
- 不使用红色、橙色或绿色作为小 i 颜色；这些颜色保留给风险、告警和状态语义。
- 使用项目已有的信息图标和 Tooltip 组件，不自定义 SVG、浮层 DOM 或局部样式。
- 小 i 与前置文字属于同一逻辑行，垂直居中，不改变文字、控件或表头的高度和对齐。
- 表头中的小 i 位于表头文字之后、排序图标之前；列宽必须同时容纳表头文字、小 i、排序图标及平台标准间距。
- 评审标记不属于产品界面。

## 交互与内容

- 鼠标悬停或键盘聚焦时显示 Tooltip。
- 鼠标移出或键盘失焦后关闭 Tooltip。
- 如果项目公共组件已定义统一触发方式，沿用项目组件行为。
- Tooltip 文案直接解释对应概念，不重复字段或选项标题。
- Tooltip 文案不得写成操作指令，不得引入需求、业务 Reference 或接口中未定义的规则。
- 多条同层级说明使用分行结构，优先采用“概念：解释”的短句格式。
- 文案较长时允许自然换行，但不得遮挡触发字段、关键操作或相邻内容。
- 同一信息已有 Tooltip、气泡或下拉说明时，复用原有承载，不叠加第二个提示层。

## 输出契约

```yaml
info_icon:
  state: required | not-required
  target: field | table-header | option
  placement: after-label | after-header | after-option
  color: '#5E6573'
  trigger: hover-and-focus | project-default
  content:
    - title: string
      description: string
  reason: string
```

当 `state` 为 `not-required` 时，必须说明不适用原因，不得用小 i 代替原本应使用的常驻信息、校验反馈、状态反馈、禁用原因或帮助入口。

## 业务要求

- 目标文字后存在一个可见、可聚焦的小 i。
- 小 i 在所有交互状态下的颜色均为 `#5E6573`。
- 鼠标悬停和键盘聚焦都能显示对应 Tooltip。
- 移出或失焦后 Tooltip 关闭。
- Tooltip 内容与目标字段或选项一一对应，不重复标题，不包含无关业务信息。
- 表头文字、小 i 和排序图标保持单行完整展示。
- Tooltip 的内容、位置和遮挡关系符合项目既有交互规范。
