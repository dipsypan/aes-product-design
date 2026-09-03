# AES 快速筛选组件

> **归属：AES Product Design。** 本 Reference 是 AES（深信服下一代端点安全）产线专属组件映射，不作为 Common Design 的通用组件规范。本组件能力整体采用 AES `override`，本文定义的规则直接以 AES 为准，未登记的其他组件能力才由 `prd-design-code` 调用 Common Design 或依据项目已有代码处理。页面应在高级筛选、快速筛选和简单平铺筛选之间如何选择，由 `../04-patterns/filtering.md` 定义。

## 快速筛选

- 用于承载高频结构化筛选条件，并与检索框组合使用。
- 页面必须同时包含快速筛选项和搜索框，两者可组合生效。
- 快速筛选只放状态、类型、时间等高频结构化字段。
- 搜索框用于名称、ID、描述等业务配置的单个关键词检索。
- 业务命中此模式时，必须同时返回非空的 `quick_filter_fields` 和 `search_fields`。
- 仅当用户需要同时查询多个名称、ID 或实体标识时，才启用批量搜索；未启用时不得生成批量搜索入口。
- 批量搜索作为搜索框的扩展入口展示，必须明确支持的字段和输入分隔规则。
- 筛选确认后生效，重置恢复默认状态，按钮显示激活状态。
- 生效条件回显在列表上方，支持删除单项和清空全部。

示例：

```text
[快速筛选]    [请输入名称或 ID]    [批量搜索（可选）]
```

## 前端参考基准

实现快速筛选时，以 AES 前端工程 `aes-mgr-front0830` 中的以下代码为准：

- 组件源码：`app/app-lib/src/business-comp/quick_filter_layer/`
- 公开入口：`app/app-lib/src/business-comp/quick_filter_layer/index.ts`
- 主组件：`app/app-lib/src/business-comp/quick_filter_layer/src/QuickFilterSelector.vue`
- 表格组合实现：`app/app-lib/src/business-comp/table_container/src/components/QuickSearchFilter.vue`
- 查询状态处理：`app/app-lib/src/business-comp/table_container/src/composables/useQuickSearchPanel.ts`
- 条件回显：`app/app-lib/src/business-comp/selected_condition_group/`

优先参考以下真实页面：

- 策略列表：`app/aes-policy/src/view/mod_policy/components/policy_table.vue`
- 白名单列表：`app/aes-policy/src/view/mod_whitelist_management/`
- 任务列表：`app/aes-task/src/view/task_list/`
- 定时任务列表：`app/aes-task/src/view/scheduled_tasks/`

列表页面优先通过 `AES__APP_LIB/TableContainer` 的 `search.quickSearchFilter` 接入，由表格容器组合快速筛选、关键词搜索、批量搜索和条件回显。非表格场景才直接使用 `AES__APP_LIB/QuickFilterLayer`。

快速筛选仍在封装中。AI 编码时必须核对目标分支中的 `QuickFilterSelector.vue` 和实际业务调用，不得将内部 Button、Popover、Panel 或尚未稳定的类型声明当作正式公共 API。
