# AES 数字输入范围提示组件

> `Coverage: extend`
> **归属：AES Product Design。** 本 Reference 是 AES（深信服下一代端点安全）产线专属组件映射，不作为 Common Design 的通用组件规范。本组件能力整体采用 AES `override`；本文定义的规则直接以 AES 为准，未登记的其他组件能力才由 `prd-design-code` 调用 Common Design 或依据项目已有代码处理。

本 Reference 只补充 AES 对 IDUX `InputNumber` 的差异，不重复定义组件本身的 API、数值输入、步进和校验能力。

## 使用条件

- 仅当 InputNumber 存在明确的可输入范围，且用户需要在输入时知道该范围，才增加范围 Tooltip。
- Tooltip 文案必须与组件实际的 `min`、`max` 保持一致。
- 没有明确范围或范围已经由相邻文案完整表达时，不额外增加 Tooltip。

## 不适用与禁止事项

- 没有明确 `min`、`max` 范围时，不生成范围提示。
- 不得把范围提示组件组合当作新的独立业务组件或公共 API。

## Component 身份

- `componentId: IxTooltip + IxInputNumber`
- `encapsulation: true`
- 组件能力：数字输入范围提示组合
- 来源：IDUX 组件组合，配合 ProForm 校验状态使用。

## Tooltip 规则

- 输入框获取焦点时显示 Tooltip；鼠标点击和键盘 Tab 获取焦点都应支持。
- 输入框失去焦点后关闭 Tooltip。
- 使用项目已有 Tooltip 组件，不自定义浮层 DOM、图标或样式。
- Tooltip 位置使用 `bottomStart`，不得被表单弹窗或其他容器裁切。
- 范围提示使用简短格式：`请输入 {最小值} ～ {最大值}`。
- 范围提示不放入 placeholder，也不使用常驻信息区承载。

## 状态优先级

- 正常状态：显示范围 Tooltip。
- `invalid` 状态：优先显示校验错误，不显示或不重复显示范围 Tooltip。
- 禁用状态：不可编辑，不触发 Tooltip。
- 必填、格式和范围校验沿用 IDUX / ProForm 的现有校验链路。

## 单位与组合布局

- 固定单位继续使用 InputNumber 的 `addonAfter` 承载，不放入 Tooltip 文案。
- Tooltip 不应改变输入框、单位或相邻文案的行高和对齐。
- 输入框与前后文案组成同一逻辑行时，沿用表单规范的行内布局规则。

## 参考场景

页面路径：`任务中心 / 任务计划 / 新增 / 快速扫描 / 执行计划`

### 扫描时长限制

- 字段文案：`扫描时长限制`
- 组合文案：`单台资产扫描最多不超过 [InputNumber] 小时`
- 输入范围：`1 ～ 72`
- Tooltip：`请输入1 ～ 72`
- 当前项目实现：`IxTooltip placement="bottomStart" trigger="click"` 包裹 `IxInputNumber`。
- 当前实现仅在字段不是 `invalid` 状态时提供 Tooltip，错误状态由表单校验提示接管。

### 错过开始时间的补扫时长

- 复用扫描时长限制的范围 Tooltip 规则。
- 根据字段实际的 `min`、`max` 生成或配置对应提示，不因字段名称不同而改变交互规则。

## 业务要求

- 鼠标点击输入框后能看到范围 Tooltip。
- 使用键盘 Tab 聚焦输入框时能看到相同 Tooltip。
- Tooltip 文案与实际 `min`、`max` 一致。
- 失焦后 Tooltip 关闭，且不会遮挡其他表单内容。
- `invalid` 状态下错误提示优先，范围 Tooltip 不叠加。
- 固定单位、输入框和相邻文案保持同一逻辑行，Tooltip 不改变布局。

## 复用契约

- 该编号代表稳定的组合基准，不代表新增的独立业务组件或公共 API。
- 编码前必须核对目标分支中 `min`、`max`、单位、校验器和错误状态；不得将页面局部实现当作额外封装。

## 业务补充

- 当前业务负责定义实际范围、单位、字段文案、权限和校验触发时机。
- Tooltip 文案必须根据真实 `min`、`max` 生成；`invalid` 状态下由校验错误接管。
- 若目标页面没有明确范围，或组合能力不足以满足业务，按现有表单规则补充实现，不假设存在完整封装。
