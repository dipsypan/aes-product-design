# AES 分级确认弹窗组件

> `Coverage: override`
> **归属：AES Product Design。** 本 Reference 是 AES（深信服下一代端点安全）产线专属组件映射，不作为 Common Design 的通用组件规范。是否确认、确认等级和文案由 [`../04-patterns/tiered-confirmation.md`](../04-patterns/tiered-confirmation.md) 决定。

## 使用条件

- 上游已选择弹窗确认，并需要普通点击确认或输入确认。
- 需要统一承载标题、对象上下文、确认输入、加载状态和确认/取消动作。

## 不适用与禁止事项

- 不用于 Pattern 已确定无需确认或使用气泡确认的场景。
- 不根据组件是否支持输入框反推风险等级或确认阈值。
- 不用组件默认文案覆盖上游已经确定的业务后果说明。

## Component 身份

- `componentId: ConfirmModal`
- `encapsulation: true`
- 来源：`AES__APP_LIB/ConfirmModal`
- 真实实现：`app/app-lib/src/business-comp/confirm_modal`

## 能力边界

- 组件提供：确认弹窗、可选确认输入、加载状态及确认/取消事件。
- 业务提供：触发条件、风险等级、对象上下文、按钮文案和操作结果。
- 封装不足时返回 `tiered-confirmation` Pattern 补充，不得降低上游确认等级。
