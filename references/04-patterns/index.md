# AES Pattern Index

> **归属：AES Product Design。** 本 Index 是 AES（深信服下一代端点安全）产线专属 Pattern 索引，不作为 Common Design 的通用交互索引。每个 Pattern 必须显式声明 `Coverage`，本文只登记 AES 侧的覆盖声明和路由。

Pattern 在 Template 已确定页面类型、主容器和页面区域后读取。Theme 或用户已锁定具体 Pattern 及参数时，Pattern 只执行、展开和验证，不得重新选型；只有未锁定事项才根据业务条件选择并组合区域级或复杂交互方案。Pattern 可以调用 Feature 和 Component，但不修改 Theme 的业务事实，也不重新选择页面主容器。

每个具体 Pattern Reference 必须显式声明 `Coverage: inherit | extend | override`。不得根据正文、文件名或层级自行推断 Coverage；未声明时记录 Coverage 缺失。

## Pattern 清单

| Pattern | 决策链 | 命中时读取 |
| --- | --- | --- |
| `table-management` | 在列表、详情、表单、Modal 或 Drawer 中按宿主上下文组合表格内部能力 | [`table-management.md`](table-management.md) |
| `page-notice` | 上游未锁定时决定是否展示；锁定后执行内容结构和位置 | [`page-notice.md`](page-notice.md) |
| `form-management` | 组合字段组织、控件形态、依赖、校验、状态和提交保护 | [`form-management.md`](form-management.md) |
| `condition-expression-editor` | 在简单平铺、复杂条件组和对象卡片之间选择；执行条件行、AND/OR、对象关系和动态联动 | [`condition-expression-editor.md`](condition-expression-editor.md) |
| `filtering` | 上游未锁定时选择筛选方式；锁定后执行对应模式 | [`filtering.md`](filtering.md) |
| `button-eligibility` | 根据对象可执行性决定按钮启用、部分执行或阻断 | [`button-eligibility.md`](button-eligibility.md) |
| `tiered-confirmation` | 根据风险、既有承载和数量选择确认等级与容器 | [`tiered-confirmation.md`](tiered-confirmation.md) |
| `enable-disable` | 根据表单保存、单条即时修改、只读或批量任务选择启禁用呈现与交互 | [`enable-disable.md`](enable-disable.md) |
| `disposal-status` | 存在处置状态展示或用户可执行的处置状态切换时命中；系统自动推进的处置状态只执行展示规则，启用 / 禁用由 `enable-disable` 负责 | [`disposal-status.md`](disposal-status.md) |
| `field-display` | 在文本、标签、图标、状态点和链接中选择 | [`field-display.md`](field-display.md) |
| `attack-technique-display` | 决定 ATT&CK 合并/分开、单项/多项展示 | [`attack-technique-display.md`](attack-technique-display.md) |

## Pattern 编排规则

- 页面类型、主容器或页面区域未确定时返回 `../03-templates/`，不得在 Pattern 中补造页面框架。
- Theme 或用户锁定的 Pattern 无法执行时返回锁定来源层，不得在本层切换方案。
- Pattern 只选择和组合方案；选定的单项能力继续读取 `../05-features/index.md`。
- Pattern 需要真实 AES 封装时读取 `../06-components/index.md`，不在 Pattern 中重写组件 API。
- Pattern 显式输出 `componentId` 或 `required_components` 时，必须同时链接 `../06-components/index.md` 中唯一对应的 Component Reference；无法解析时记录 `component_gap`，不得只输出组件名称。
- Pattern 可以引用其他 Pattern，例如状态切换引用操作可执行性和分级确认，但必须明确主 Pattern 与依赖关系。
- Table Pattern 不以 List Template 为固定前置；调用方已确定宿主容器和区域时可直接读取。表格不得反向决定页面类型、概览、左树、提示条或 Footer。
- 用户已明确指定单项 Feature 且不存在方案选择时，不得为了经过 Pattern 而制造决策链。

## 输出契约

```yaml
pattern_contract:
  pattern_id: ""
  decision_inputs: []
  selected_solution: ""
  rejected_solutions: []
  required_features: []
  required_components: []
  return_to_template: false
  pattern_gaps: []
```
