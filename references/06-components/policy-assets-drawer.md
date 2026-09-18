# AES 策略资产详情抽屉组件

> `Coverage: override`
> **归属：AES Product Design。** 本 Reference 是 AES（深信服下一代端点安全）产线专属组件映射，不作为 Common Design 的通用组件规范。分配、排除和生效资产的业务关系由 [`../05-features/asset-scope.md`](../05-features/asset-scope.md) 决定。

## 使用条件

- 用户从分配资产、排除资产或生效资产摘要进入完整资产查看。
- 需要在同一抽屉内按对应 Tab 查看资产或资产组明细。

## 不适用与禁止事项

- 不用于选择或修改资产范围；配置场景使用 `AssetSelectorFormItem`。
- 不将该业务抽屉替换为自行拼装的通用详情抽屉。
- 不根据抽屉返回数据自行重新计算生效范围。

## Component 身份

- `componentId: PolicyAssetsDrawer`
- `encapsulation: true`
- 来源：`AES__APP_LIB/PolicyAssetsDrawer`
- 真实实现：`app/app-lib/src/business-comp/policy_assets_drawer`

## 复用契约

- 组件负责分配、排除和生效资产的 Tab 承载、列表展示、搜索和基础空状态。
- 当前业务负责提供对象 ID、默认 Tab、可见 Tab 和接口适配；默认 Tab 必须与用户点击的摘要类型一致。
- 无对应数据时按 `asset-scope` Feature 展示空状态，不打开无意义的错误内容。
- 编码阶段核验目标分支中的真实导出名、Props、双向可见性事件、查询函数和 Tab key。
