# AES 资产适用检测弹窗组件

> `Coverage: override`
> **归属：AES Product Design。** 本 Reference 是 AES（深信服下一代端点安全）产线专属组件映射，不作为 Common Design 的通用组件规范。检测对象、结果字段与实际生效语义由 [`../05-features/asset-applicability-check.md`](../05-features/asset-applicability-check.md) 决定。

## 使用条件

- Theme 或上游 Feature 已启用资产适用策略/规则检测。
- 用户需要检索单个资产并查看其适用项与实际生效项。

## 不适用与禁止事项

- 固定全局生效、不存在资产范围差异时不使用。
- 不在组件层推断检测实体、结果字段或实际生效项。

## Component 身份

- `componentId: CheckPolicyModal`
- `encapsulation: true`
- 来源：`AES__APP_LIB/PolicyCommon`
- 真实实现：`app/app-lib/src/business-comp/policy_common/modal/check_policy_modal`

## 能力边界

- 组件提供：检测弹窗、资产检索、选择对象和结果区的通用交互承载。
- 业务提供：实体类型、接口配置、结果字段、权限和详情跳转。
- 封装不足时返回 `asset-applicability-check` Feature 补充，不得改变检测流程。
