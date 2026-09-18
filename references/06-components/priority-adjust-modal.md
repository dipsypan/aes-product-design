# AES 优先级调整弹窗组件

> `Coverage: override`
> **归属：AES Product Design。** 本 Reference 是 AES（深信服下一代端点安全）产线专属组件映射，不作为 Common Design 的通用组件规范。优先级语义与调整规则由 [`../05-features/priority-adjustment.md`](../05-features/priority-adjustment.md) 决定。

## 使用条件

- 上游已确认对象存在影响匹配或生效顺序的业务优先级。
- 需要通过统一弹窗移动选中对象并保存新顺序。

## 不适用与禁止事项

- 没有业务优先级或所有命中项同时生效时不使用。
- 不通过组件能力自行增加“置顶”“移动到”等未确认的调整方式。

## Component 身份

- `componentId: PriorityAdjustModal`
- `encapsulation: true`
- 来源：`AES__APP_LIB/PolicyCommon`
- 真实实现：`app/app-lib/src/business-comp/policy_common/priority_adjust_modal`

## 复用契约

- 组件负责弹窗承载、目标位置选择和通用提交交互。
- 当前业务负责可调整对象、保护对象、当前顺序、权限、禁用原因和保存接口。
- 编码阶段核验目标分支中的真实导出名、可见性参数、Props、Events 和提交函数；封装不足时按上游 Feature 补充。
