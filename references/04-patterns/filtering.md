# AES 筛选方式 Pattern

> **归属：AES Product Design。** 本 Reference 是 AES（深信服下一代端点安全）产线专属 Pattern，不作为 Common Design 的通用交互规范。本文明确规定的 AES 方案优先；未覆盖事项由 `prd-design-code` 按 Coverage 调用 Common Design 补充。

## 1. 三种筛选方式

| 类型 | 形态 | 典型页面 |
| :--- | :--- | :--- |
| `condition-search` 高级筛选 | 表格上方独立条件检索区 | 日志调查、安全事件、告警链列表 |
| `quick-filter-search` 快速筛选 | 快速筛选项 + 搜索框 + 可选批量搜索 | 策略中心、任务中心 |
| `flat-filter` 简单平铺筛选 | 平铺筛选项 + 搜索框 + 可选批量搜索 | 安全事件详情的可疑实体列表 |

搜索框默认用于单个关键词搜索。批量搜索是搜索框的按需扩展能力，不是快速筛选或简单平铺筛选的必选项。

## 2. 选择规则

先检查上游是否已经锁定筛选方案：

- Theme 或用户已锁定 `search_mode` 时，直接执行该模式并补全交互、状态和组件契约，不得使用本节规则重新选型；
- 上游同时锁定检索字段、筛选字段、默认条件或批量搜索要求时，直接采用；只有上游未指定的参数才允许补充判断；
- 锁定方案与真实组件或接口能力冲突时返回锁定方案的来源层，不得在本 Pattern 静默切换模式；
- 只有上游没有指定 `search_mode` 时，才按以下顺序判断。

1. 条件多、需要多个操作符或复杂组合时，使用 `condition-search`。
2. 条件简单但平铺后会拥挤时，使用 `quick-filter-search`。
3. 条件少、固定且能在当前宽度内清晰展示时，优先使用 `flat-filter`。

页面层级不是硬性判断条件：

- 非第一层级列表，筛选项少时默认优先使用 `flat-filter`。
- 第一层级列表如果筛选项少且能平铺，也可以使用 `flat-filter`。
- 不得因为页面是第一层级，就强制使用快速筛选。

三种模式互斥，不得同时生成高级筛选和快速筛选，也不得在平铺筛选外重复生成快速筛选入口。

## 3. 组件调用

高级筛选组件的结构和能力见 [`../06-components/advanced-filter.md`](../06-components/advanced-filter.md)。

快速筛选组件的结构和能力见 [`../06-components/quick-filter.md`](../06-components/quick-filter.md)。

本 Pattern 只规定三种筛选方式的选择逻辑、互斥关系、页面适配和查询状态联动。

## 4. 简单平铺筛选

- 适用于少量、固定、简单的筛选字段。
- 页面必须同时包含平铺筛选项和搜索框，两者可组合生效。
- 平铺筛选项直接展示在列表上方，不收进快速筛选入口，可使用下拉、单选、多选等简单控件。
- 筛选控件不得在外部单独放置 label；未选择时使用控件自身的 `placeholder` 表达字段名称，选择后在控件内部显示当前值。
- 搜索框不得在外部单独放置 label；使用自身的 `placeholder` 表达搜索对象。
- 平铺筛选项和搜索框统一放在同一查询区域，不得在工具栏中另行拼装；样式、间距、清除和状态行为与安全事件详情的可疑实体列表一致。
- 搜索框默认用于单个关键词搜索。仅当用户需要同时查询多个实体名称、文件名、IP、域名或 ID 时，才按需启用批量搜索。
- 未启用批量搜索时不得生成批量搜索入口；启用时必须明确支持的字段和输入分隔规则。
- 条件变化后直接刷新列表并回到第一页。
- 当前宽度无法清晰容纳全部控件时，改用 `quick-filter-search`。
- 不得因为启用批量搜索，就将简单平铺筛选改为快速筛选。

示例：

```text
[实体类型]    [处置状态]    [请输入实体名称或特征]    [批量搜索（可选）]
```

选择条件后，控件内部直接显示当前值：

```text
[文件]    [未处置]    [winlogon.exe]    [批量搜索（可选）]
```

## 5. 通用联动

- 搜索、筛选、概览、左树、排序和分页使用同一查询状态。
- 搜索或筛选变化后回到第一页，并保留当前排序。
- 刷新保留当前搜索、筛选、排序和页码。
- 概览或表格字段产生的筛选必须回显到当前筛选组件。
- 返回列表时恢复搜索、筛选、排序、页码和纵向滚动位置。
- 不得同时维护两份不一致的筛选状态。
- 批量搜索与单个关键词搜索的组合或互斥关系必须由业务明确，不得隐式覆盖。

## 6. 输出契约

业务 Reference 至少返回：

```yaml
search_mode: condition-search | quick-filter-search | flat-filter
decision_source: user | theme | pattern
decision_locked: true | false
search_fields: []
quick_filter_fields: []
flat_filter_fields: []
batch_search:
  enabled: false
  fields: []
  separator: ""
default_filters: []
```

- `quick-filter-search` 必须同时返回非空的 `quick_filter_fields` 和 `search_fields`。
- `decision_locked=true` 时，本 Pattern 只执行和补全，不得重新选择 `search_mode`。
- `flat-filter` 必须同时返回非空的 `flat_filter_fields` 和 `search_fields`，且每个字段应提供控件内部使用的 `placeholder`。
- `batch_search.enabled` 默认为 `false`。设为 `true` 时，必须返回非空的 `fields` 并明确 `separator`；设为 `false` 时不展示批量搜索入口。

简单平铺筛选示例：

```yaml
search_mode: flat-filter
flat_filter_fields:
  - key: entity_type
    component: select
    placeholder: 实体类型
  - key: disposal_status
    component: select
    placeholder: 处置状态
search_fields:
  - key: keyword
    component: input
    placeholder: 请输入实体名称或特征
batch_search:
  enabled: false
  fields: []
  separator: ""
default_filters: []
```

## 7. 业务要求

- 筛选方式符合条件复杂度和实际可用宽度。
- 条件少且能清晰平铺时，未强制使用快速筛选。
- 高级筛选使用 `conditionSearch`，快速筛选使用 `quickSearchFilter`。
- 快速筛选和平铺筛选均包含单个关键词搜索框。
- 平铺筛选控件使用内部 `placeholder`，没有在控件外重复放置 label。
- 批量搜索仅在业务需要时展示，未被作为必选入口。
- 三种模式没有重复生成或叠加。
- 筛选结果、条件回显、分页、排序和刷新状态保持一致。
