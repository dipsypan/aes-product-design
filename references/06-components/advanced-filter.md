# AES 高级筛选组件

> **归属：AES Product Design。** 本 Reference 是 AES（深信服下一代端点安全）产线专属组件映射，不作为 Common Design 的通用组件规范。本组件能力整体采用 AES `override`；本文定义的规则直接以 AES 为准，未登记的其他组件能力才由 `prd-design-code` 调用 Common Design 或依据项目已有代码处理。页面应在高级筛选、快速筛选和简单平铺筛选之间如何选择，由 `../04-patterns/filtering.md` 定义。

## 高级筛选

- 用于承载可组合的高级检索条件，不与快速筛选重复生成。
- 检索字段、操作符、默认条件、时间快捷范围和最大跨度由业务 Reference 或远程配置提供。
- 条件支持添加、修改、删除和清空，并以条件标签回显。
- 关键时间可作为默认条件；不可清除的默认条件必须始终保留。
- 存在检索按钮时，编辑条件后点击检索才提交。
- 执行检索后回到第一页，并保留当前排序。

## 前端参考基准

实现高级筛选时，以 AES 前端工程 `aes-mgr-front0830` 中的以下代码为准：

- 组件源码：`app/app-lib/src/business-comp/condition_search/`
- 公开入口：`app/app-lib/src/business-comp/condition_search/index.ts`
- 字段类型：`app/app-lib/src/business-comp/condition_search/types/fields.ts`
- 表格接入：`app/app-lib/src/business-comp/table_container/src/TableContainer.vue`
- 表格配置类型：`app/app-lib/src/business-comp/table_container/src/types/container.ts`

优先参考以下真实页面：

- 安全事件列表：`app/aes-incident/src/view/mod_sec_event/event_table/`
- 告警列表：`app/aes-incident/src/view/mod_sec_alert/alert_list/`
- 日志调查：`app/aes-incident/src/view/mod_log_analysis/`
- 病毒列表：`app/aes-virus/src/view/virus_list/`

列表页面优先通过 `AES__APP_LIB/TableContainer` 的 `search.conditionSearch` 接入，不重新拼装筛选区域。非表格场景才直接使用 `AES__APP_LIB/ConditionSearch`。

参考代码前必须核对目标分支中的公开类型和实际调用，不得根据文档虚构字段类型、Props、Events 或实例方法。
