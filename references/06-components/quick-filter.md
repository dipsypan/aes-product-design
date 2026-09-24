# AES 快速筛选组件

> `Coverage: extend`
> **归属：AES Product Design。** 本 Reference 是 AES（深信服下一代端点安全）产线专属组件映射，不作为 Common Design 的通用组件规范。本组件能力在 Common Design 基础上扩展 AES 实现映射；页面应在高级筛选、快速筛选和简单平铺筛选之间如何选择，由 `../04-patterns/filtering.md` 定义。

## 使用条件

- 仅当业务需要高频结构化筛选，并且需要与关键词搜索组合时使用。
- 是否选择快速筛选由 [`../04-patterns/filtering.md`](../04-patterns/filtering.md) 决定。

## 不适用与禁止事项

- 已选择高级筛选或简单平铺筛选时，不重复生成快速筛选。
- 不得把组件内部 Button、Popover、Panel 或未稳定类型当作公共 API。

## Component 身份

- `componentId: QuickFilterLayer / QuickSearchFilter`
- `encapsulation: true`
- 组件能力：快速筛选区域

## 能力边界

- 组件提供：快速筛选与关键词搜索的基础区域、激活状态和条件回显等通用交互。
- 业务提供：快速筛选字段、关键词字段、默认值、批量搜索字段和输入分隔规则。
- 筛选模式、确认与重置、分页、排序和列表刷新继续执行 [`../04-patterns/filtering.md`](../04-patterns/filtering.md) 与表格契约；封装不足时返回对应上游补充。
