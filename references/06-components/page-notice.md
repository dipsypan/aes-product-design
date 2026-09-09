# AES 页面提示条组件

> `Coverage: extend`

> **归属：AES Product Design。** 本 Reference 只说明 `IxAlert` 在 AES 业务中的复用边界；提示条是否展示、业务语义和页面位置由 [`../04-patterns/page-notice.md`](../04-patterns/page-notice.md) 决定。

## 使用条件

- 页面已有明确的持续性业务提示，并且 Template 提供 `noticeRegion`。
- 提示内容属于页面、模块、表格或操作范围的状态说明。

## 不适用与禁止事项

- 不得用提示条替代字段校验、操作结果反馈或局部帮助。
- 不得因页面需要装饰或视觉分隔而增加提示条。

## Component 身份

- `componentId: IxAlert`
- `encapsulation: true`
- 组件能力：页面提示条

## 复用契约

- 组件负责基础提示条承载、等级样式和通用交互。
- 编码阶段必须核验目标分支的实际导出名、Props、Events 和接入方式。

## 业务补充

- 当前业务负责 `visible`、等级、标题、说明、附加信息、操作入口、关闭权限和关联范围。
- 具体展示条件与页面位置必须执行 `../04-patterns/page-notice.md`；封装不足时按该 Pattern 补充实现。
