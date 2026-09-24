# AES 资产选择器组件

> `Coverage: override`
> **归属：AES Product Design。** 本 Reference 是 AES（深信服下一代端点安全）产线专属组件映射，不作为 Common Design 的通用组件规范。本组件能力整体采用 AES `override`，本文定义的规则直接以 AES 为准；未登记的其他组件能力才由 `prd-design-code` 调用 Common Design 或依据项目已有代码处理。资产范围、包含与排除关系由 `../05-features/asset-scope.md` 定义。

## 使用条件

- 业务需要选择全部资产、指定资产或资产组。
- 选择结果会影响策略、任务或规则的生效范围。
- 业务需要资产搜索、已选数量、数量上限、路径、空状态或基础校验能力。

## 不适用与禁止事项

- 固定全局生效且不允许配置资产范围时，不调用该组件。
- 不得调用通用选择器，也不得在业务页面重新实现资产或资产组选择面板。

## Component 身份

- `componentId: AssetSelectorFormItem`
- `encapsulation: true`
- 来源：`AES__APP_LIB/GroupAssetSelector`

## 能力边界

- 组件提供：资产和资产组选择、搜索、已选数量、上限、路径、空状态和基础校验；业务表单优先复用该封装，不重新实现选择面板。
- 业务提供：资产范围模式、字段名称、权限、必填条件、数量限制和数据转换。
- 生效资产计算、排除关系及展示语义由 [`../05-features/asset-scope.md`](../05-features/asset-scope.md) 决定。
- 封装能力不足时返回 [`../05-features/asset-scope.md`](../05-features/asset-scope.md) 补充，不改用通用选择器改变业务语义。
