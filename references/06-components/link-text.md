# AES 文字链组件

> `Coverage: extend`
> **归属：AES Product Design。** 本 Reference 是 AES（深信服下一代端点安全）产线专属组件映射，不作为 Common Design 的通用组件规范。打开方式和跳转规则由 [`../05-features/link-navigation.md`](../05-features/link-navigation.md) 决定。

## 使用条件

- 页面需要以 AES 既有文字链样式触发当前页交互或页面跳转。
- 上游已确定文字、打开方式和是否显示跳转图标。

## 不适用与禁止事项

- 非可点击文本不使用本组件。
- 不在 Component 层决定当前页打开、新标签页打开或目标路由。
- 不使用普通文本和自定义样式重新实现已有文字链外观。

## Component 身份

- `componentId: LinkText`
- `encapsulation: true`
- 来源：`AES__APP_LIB/PolicyCommon`
- 真实实现：`app/app-lib/src/business-comp/policy_common/common/link-text`

## 复用契约

- 组件负责文字、可选图标、图标位置和点击事件的基础承载。
- 当前业务负责路由、权限、打开目标、长文本和安全属性，并执行 `link-navigation` Feature。
- 编码阶段核验目标分支中的真实导出名、Props、Events 和图标名称；组件存在不代表完整跳转 Feature 已被封装。
