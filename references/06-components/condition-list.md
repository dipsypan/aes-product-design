# AES 动态条件行组件

> `Coverage: extend`

> **归属：AES Product Design。** 本 Reference 只说明 `IxProFormList` 在 AES 业务中的复用边界；条件模式、字段语义和校验规则由 [`../04-patterns/condition-expression-editor.md`](../04-patterns/condition-expression-editor.md) 决定。

## 使用条件

- 仅在条件编辑器选择 `simple-flat` 模式时使用。
- 业务需要动态新增、删除条件行，并保持行内字段联动。

## 不适用与禁止事项

- `logical-groups` 或 `entity-cards` 不使用该组件替代条件组或对象卡片结构。
- 不得把组件的动态行能力当作条件业务语义或校验规则。

## Component 身份

- `componentId: IxProFormList`
- `encapsulation: true`
- 组件能力：动态条件行

## 能力边界

- 组件提供：动态条件行的表单承载和通用增删能力。
- 业务提供：字段目录、操作符、值类型、数量上限、默认行、必填和提交语义。
- 模式选择和条件结构执行 [`../04-patterns/condition-expression-editor.md`](../04-patterns/condition-expression-editor.md)；封装不足时返回该 Pattern 补充等价实现。
