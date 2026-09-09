# AES 字段内容展示 Pattern

> **归属：AES Product Design。** 本 Reference 是 AES（深信服下一代端点安全）产线专属 Pattern，不作为 Common Design 的通用交互规范。
> `Coverage: extend`
> 本文明确规定的 AES 方案优先；未覆盖事项由 `prd-design-code` 按 Coverage 调用 Common Design 补充。

用于确定 AES 页面中字段的内容展示方式。字段默认使用纯文本；只有非纯文本能够提升状态识别、等级判断、分类比较或操作理解时，才按需使用标签、图标、状态点或链接。

## 1. 展示方式总览

| 展示方式 | 适用语义 | 示例 |
| --- | --- | --- |
| 普通文本 | 名称、ID、时间、IP、路径、描述、数量 | `Security Incident-001` |
| 语义标签 | 威胁等级、重要终态、关键分类 | `[高危]`、`[已隔离]` |
| 图标 + 文本 | 处置过程、执行结果、启禁用状态 | `加载图标 正在处置中` |
| 状态点 + 文本 | 在线、离线等持续状态 | `绿色圆点 在线` |
| 链接文本 | 可进入详情或跳转外部页面的字段 | `事件名称` |
| 标签集合 | 多个用户标签或分类标签 | `[钓鱼] [APT攻击] [+3]` |

先判断字段语义，再从上表选择展示方式；不能因为字段是枚举值或接口对象就自动使用标签。

## 2. 平台统一语义基线

| 字段场景 | 默认展示方式 | 组件依赖 |
| --- | --- | --- |
| 威胁等级 | 实心语义标签 | `ThreatLevelTag` |
| 事件处置状态 | 图标 + 文本 | `DisposalStatus` |
| 实体已隔离、已拦截等终态 | 终态标签 | `DisposalTag` |
| 资产在线/离线 | 状态点或状态文本 | `AssetCard` 状态能力 |
| 启用/禁用 | 读取 [`enable-disable.md`](enable-disable.md) 判断具体场景 | 由 `enable-disable` 输出 |
| 普通业务分类 | 中性标签或普通文本 | `IxTag` / 标签组组件 |
| 可跳转字段 | 链接文本 | 项目统一链接能力 |

### 2.1 威胁等级

统一使用公共 `ThreatLevelTag`，具体入口由 Component 层核验。

等级颜色沿用公共组件：信息蓝、低危黄、中危橙、高危红、严重深红。业务页面不得自行重写颜色、圆角和等级映射。

### 2.2 处置、在线与启禁用状态

- 待处置、处置中、处置完成、忽略等过程或结果状态，按项目既有组件使用图标 + 文本；不要为了统一外观全部改成标签。
- 已隔离、已拦截等需要在实体名称旁强调的终态，可使用 `DisposalTag`；过程状态不套用终态标签。
- 在线/离线使用状态点或状态文本，不使用胶囊标签。
- 遇到业务对象的启用状态时，必须读取 [`enable-disable.md`](enable-disable.md)；本 Pattern 不决定使用 Radio、状态下拉、只读状态或批量按钮。
- 启禁用的状态文案、视觉基线和组件依赖均由 [`enable-disable.md`](enable-disable.md) 输出，本 Pattern 只继续约束字段密度、强调和可访问性。

## 3. 非纯文本展示克制原则

1. 普通字段默认使用纯文本，不主动添加标签、图标、背景块或彩色圆点。
2. 非纯文本必须对应明确语义：等级、状态、分类、结果、筛选或跳转；没有语义价值时禁止使用。
3. 威胁等级、处置状态、在线状态、启禁用状态分别使用各自的统一展示方式，不能全部做成标签。
4. 一个表格行中最多保留 1 个高强调视觉元素；避免多个强颜色同时出现。
5. 普通分类只有在需要快速比较或筛选时才使用中性标签，否则使用文本。
6. 标签集合超出空间时使用 `+N` 或浮层，不通过缩小字体、压缩间距堆叠。
7. 标签内容保持简短，复杂说明放入 Tooltip 或详情区域。
8. 图标不能单独承担含义，必须与文本或可访问提示配合。
9. 可交互字段必须明确是筛选、跳转还是打开详情，不能只用颜色暗示可操作。
10. 已有公共组件时必须复用，不得在业务页面重新定义颜色、图标、圆角和状态映射。

## 输出契约

```yaml
pattern_contract:
  pattern_id: field-display
  decision_inputs: [field_semantics, display_context, interaction_requirement]
  selected_solution: text | semantic-tag | icon-text | status-dot | link | tag-set
  required_features: [info-icon]
  required_components: []
  component_notes: ThreatLevelTag、DisposalTag 等展示能力按项目现有组件或等价实现核验；启禁用转交 enable-disable
  return_to_template: false
  return_reason: ""
  pattern_gaps: []
```
