# AES 生效资产标签组件

> `Coverage: override`
> **归属：AES Product Design。** 本 Reference 是 AES（深信服下一代端点安全）产线专属组件映射，不作为 Common Design 的通用组件规范。生效资产口径由 [`../05-features/asset-scope.md`](../05-features/asset-scope.md) 决定。

## 使用条件

- 列表或紧凑信息区需要展示经过排除关系、必要时叠加优先级计算后的生效资产数量。
- 点击摘要需要进入生效资产详情。

## 不适用与禁止事项

- 不用于展示原始分配资产或排除资产；该场景使用 `AssetTags`。
- 组件不负责计算生效资产，不得将分配数量直接当作生效数量。
- 不在业务页面重新实现组件已有的数量标签和点击入口。

## Component 身份

- `componentId: EffectiveTags`
- `encapsulation: true`
- 来源：目标分支中的 AES app-lib 导出
- 真实实现：`app/app-lib/src/business-comp/effective_tags`

## 能力边界

- 组件提供：生效资产数量的紧凑展示和打开生效资产详情的入口。
- 业务提供：已按 `asset-scope` Feature 计算或由接口返回的生效数量与业务对象 ID。
- 不同模块存在直接导出与聚合导出差异，使用当前分支的真实入口；封装不足时返回上游 Feature 补充，不得修改生效资产语义。
