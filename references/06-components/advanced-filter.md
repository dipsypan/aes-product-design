# AES 高级筛选组件

> `Coverage: extend`

> **归属：AES Product Design。** 本 Reference 是 AES 产线专属组件映射，不作为 Common Design 的通用组件规范。页面在高级筛选、快速筛选和简单平铺筛选之间如何选择，由 [`../04-patterns/filtering.md`](../04-patterns/filtering.md) 定义。

## 使用条件

- 仅当业务需要可组合的高级检索条件时使用。
- 是否选择高级筛选由 [`../04-patterns/filtering.md`](../04-patterns/filtering.md) 决定。

## 不适用与禁止事项

- 已选择快速筛选或简单平铺筛选时，不重复生成高级筛选。
- 不得把组件内部的字段、操作符或默认值当作业务事实。

## Component 身份

- `componentId: ConditionSearch`
- `encapsulation: true`
- 组件能力：高级筛选区域

## 能力边界

- 组件提供：高级筛选区域的基础布局，以及条件添加、修改、删除、清空和标签回显等通用交互。
- 业务提供：检索字段与类型、操作符、默认条件、时间限制、权限、查询参数映射，以及与表格和其他查询条件的联动规则。
- 筛选模式、提交时机、分页和排序继续执行 [`../04-patterns/filtering.md`](../04-patterns/filtering.md) 与表格契约；封装不足时返回对应上游补充，不得由组件自行决定。
