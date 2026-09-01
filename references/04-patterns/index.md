# AES Pattern Index

> **归属：AES Product Design。** 本 Index 是 AES（深信服下一代端点安全）产线专属 Pattern 索引，不作为 Common Design 的通用交互索引。本文明确规定 AES 侧 Pattern 规则；阶段是否合并或覆盖由具体 Reference 与 Common Design 联合决定。

Pattern 在 Template 已确定页面类型、主容器和页面区域后读取。Theme 或用户已锁定具体 Pattern 及参数时，Pattern 只执行、展开和验证，不得重新选型；只有未锁定事项才根据业务条件选择并组合区域级或复杂交互方案。Pattern 可以调用 Feature 和 Component，但不修改 Theme 的业务事实，也不重新选择页面主容器。

每个具体 Pattern Reference 的关系根据正文实际覆盖范围判定为 `extend` 或 `override`。Pattern Index 不预设所有 Pattern 的统一关系；正文未明确时不得按文件名推断，命中后按具体 Reference 决定是否读取 Common Design 同类 Pattern。

## Pattern 清单

| Pattern | 决策链 | 命中时读取 |
| --- | --- | --- |
| `table-management` | 在列表、详情、表单、Modal 或 Drawer 中按宿主上下文组合表格内部能力 | [`table-management.md`](table-management.md) |
| `page-notice` | 上游未锁定时决定是否展示；锁定后执行内容结构和位置 | [`page-notice.md`](page-notice.md) |
| `form-management` | 组合字段组织、控件形态、依赖、校验、状态和提交保护 | [`form-management.md`](form-management.md) |
| `filtering` | 上游未锁定时选择筛选方式；锁定后执行对应模式 | [`filtering.md`](filtering.md) |
| `action-eligibility` | 根据对象可执行性决定启用、部分执行或阻断 | [`action-eligibility.md`](action-eligibility.md) |
| `confirmation` | 根据风险、既有承载和数量选择确认等级与容器 | [`tiered-confirmation.md`](tiered-confirmation.md) |
| `status-change` | 组合单条/批量资格、确认、提交和状态回写 | [`status-change.md`](status-change.md) |
| `field-display` | 在文本、标签、图标、状态点和链接中选择 | [`field-display.md`](field-display.md) |
| `disposal-status-display` | 决定处置状态字段位置和展示方式 | [`disposal-status-display.md`](disposal-status-display.md) |
| `attack-technique-display` | 决定 ATT&CK 合并/分开、单项/多项展示 | [`attack-technique-display.md`](attack-technique-display.md) |

## Pattern 编排规则

- 页面类型、主容器或页面区域未确定时返回 `../03-templates/`，不得在 Pattern 中补造页面框架。
- Theme 或用户锁定的 Pattern 无法执行时返回锁定来源层，不得在本层切换方案。
- Pattern 只选择和组合方案；选定的单项能力继续读取 `../05-features/index.md`。
- Pattern 需要真实 AES 封装时读取 `../06-components/index.md`，不在 Pattern 中重写组件 API。
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
