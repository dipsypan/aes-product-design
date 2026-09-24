# AES 资产范围标签组件

> `Coverage: override`
> **归属：AES Product Design。** 本 Reference 是 AES（深信服下一代端点安全）产线专属组件映射，不作为 Common Design 的通用组件规范。资产范围语义与计算规则由 [`../05-features/asset-scope.md`](../05-features/asset-scope.md) 决定。

## 使用条件

- 列表或紧凑信息区需要展示已分配资产或排除资产的摘要。
- 上游已确定当前字段表示分配或排除关系，并要求保留完整查看入口。

## 不适用与禁止事项

- 不用于展示计算后的生效资产数量；该场景使用 `EffectiveTags`。
- 不根据组件外观推断“全部资产”“暂未分配”、包含或排除等业务语义。
- 不在业务页面重新实现组件已有的标签折叠、数量摘要和点击入口。

## Component 身份

- `componentId: AssetTags`
- `encapsulation: true`
- 来源：`AES__APP_LIB/AssetTags`
- 真实实现：`app/app-lib/src/business-comp/asset_tags`

## 能力边界

- 组件提供：分配/排除资产的紧凑标签展示与打开完整详情的交互入口。
- 业务提供：范围类型、资产数据、对象 ID、默认对象标识和字段文案。
- 点击后的 Tab 和资产详情数据必须执行 `asset-scope` Feature，不由组件名称自行推断。
