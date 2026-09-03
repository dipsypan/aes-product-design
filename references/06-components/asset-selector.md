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

## 前端参考基准

实现资产选择器时，以 AES 前端工程 `aes-mgr-front0830` 中的以下代码为准：

- 公开入口：`app/app-lib/src/business-comp/group_asset_selector/index.ts`
- 表单组件：`app/app-lib/src/business-comp/group_asset_selector/components/AssetSelectorFormItem.vue`
- 选择器主体：`app/app-lib/src/business-comp/group_asset_selector/components/GroupAssetSelector.vue`
- 待选区域：`app/app-lib/src/business-comp/group_asset_selector/components/GroupAssetSelectPanel.vue`
- 已选区域：`app/app-lib/src/business-comp/group_asset_selector/components/SelectedTablePanel.vue`
- 类型定义：`app/app-lib/src/business-comp/group_asset_selector/types.ts`

优先参考以下真实页面或业务实现：

- 策略适用对象：`app/app-lib/src/business-comp/policy_common/object_form/src/index.vue`
- 策略配置页面：`app/aes-policy/src/view/mod_policy/policy_config/index.vue`
- 病毒任务执行对象：`app/aes-task/src/view/task_create/components/virus_task/execution_object.vue`
- 升级策略适用对象：`app/aes-agent/src/view/upgrade_manage/upgrade_strategy_config/index.vue`

业务表单优先从 `AES__APP_LIB/GroupAssetSelector` 引入 `AssetSelectorFormItem`，不得复制或直接拼装内部的选择面板。参考代码前必须核对目标分支中的公开入口、组件属性和实际调用，不得根据旧页面中的调用方式虚构 Props 或实例方法。
