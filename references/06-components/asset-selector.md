# AES 资产选择器组件

> **归属：AES Product Design。** 本 Reference 是 AES（深信服下一代端点安全）产线专属组件映射，不作为 Common Design 的通用组件规范。本组件能力整体采用 AES `override`，本文定义的规则直接以 AES 为准；未登记的其他组件能力才由 `prd-design-code` 调用 Common Design 或依据项目已有代码处理。资产范围、包含与排除关系由 `../05-features/asset-scope.md` 定义。

## 资产选择器

必须调用 AES 已封装的资产选择器：

```text
AssetSelectorFormItem
来源：AES__APP_LIB/GroupAssetSelector
```

禁止调用 Common Design 中的通用选择器，也不得在业务页面重新实现资产或资产组选择逻辑。

选择器统一沿用 AES 已有的资产和资产组选择、搜索、已选数量、上限、路径、空状态和校验能力。
