# AES 条件表达式编辑器 Pattern

> **归属：AES Product Design。** 本 Reference 是 AES（深信服下一代端点安全）产线专属 Pattern，不作为 Common Design 的通用条件编辑规范。本文明确规定的 AES 方案优先，未覆盖事项由 `prd-design-code` 按 Coverage 调用 Common Design 补充。上游已锁定的模式和参数只执行、展开和验证；未锁定时才按本文选择方案。本 Pattern 不决定业务字段、操作符集合、对象语义、关系语义或提交后的业务结果。

## 1. 定位与输入

本 Pattern 适用于以“字段 + 条件运算符 + 值”配置一组业务条件的场景。不适用于一行一值的单主体批量录入、自由文本/脚本表达式，以及策略优先级、继承或覆盖关系。

```yaml
condition_expression_input:
  purpose: rule-match | policy-condition | trigger-condition | exception-condition | other
  editor_mode:
    value: simple-flat | logical-groups | entity-cards | ""
    decision_source: user | theme | business-reference | pattern | ""
    decision_locked: true | false
  field_catalog: []
  group_contract:
    max_group_levels: 2
    level_source: pattern-default | user | theme
    root_group: {}
    child_group: {}
  entity_contract:
    count_mode: fixed | user-expandable | none
    min_objects: 0
    max_objects: null
    entity_cards: []
    entity_relations: []
  empty_expression:
    mode: forbidden | match-all
    decision_source: user | theme | business-reference | ""
    confirmed: true | false
    runtime_confirmation: required | not-required
    display_message: ""
  limits:
    max_conditions_per_group: null
    max_groups: null
    max_total_conditions: null
  business_validation: []
  submission:
    output: structured-expression
    business_semantics: ""
```

输入约束：

- 字段目录、字段允许的操作符和值类型必须来自需求、Theme 或业务 Reference；Pattern 不创建业务事实。
- 上游已锁定 `editor_mode` 时直接执行；无法执行时返回锁定来源层，不得换成其他模式。
- 默认最多两层条件组，即根条件组和子条件组。用户明确指定时可以放开，但必须提供具体上限，不允许无限嵌套。
- `submission.business_semantics` 由调用方定义，例如“生成一条规则”或“作为策略适用条件”。

## 2. 模式选择

三种模式互斥，只能选择一种：

| 模式 | 适用条件 | 核心能力 |
| --- | --- | --- |
| `simple-flat` | 无对象语义，不需要新增条件组或调整 AND/OR | 动态条件行，隐式固定 AND |
| `logical-groups` | 需要新增条件组，或配置组间/组内 AND、OR | 根组、子组和可视逻辑关系 |
| `entity-cards` | 有明显多对象语义，需要强调对象边界或对象关系 | 对象卡片、卡片内条件编辑、对象关系 |

未锁定时按以下分支判断：

```text
是否存在需要强调的多对象语义？
├── 是 → entity-cards
└── 否
    ├── 是否需要新增条件组或配置 AND/OR？
    │   ├── 是 → logical-groups
    │   └── 否 → simple-flat
```

字段多、字段来自不同接口，或字段名出现“源”“目的”“主体”“客体”，均不足以单独触发对象卡片。缺少关键证据且模式选择会明显改变页面结构时，输出待确认项。

## 3. 条件语义模型

必须区分三个层级：

```text
单条条件内部：condition_operator
条件组直接成员之间：group_relation
对象卡片之间：entity_relation
```

```yaml
condition:
  key: ""
  field: ""
  operator: ""
  value: {}

condition_group:
  key: ""
  relation: AND | OR
  relation_editability: locked | user-adjustable
  allowed_relations: []
  items:
    - condition | condition_group
```

- `equals`、`contains`、`in`、`not_in`、`is_empty` 等是连接字段和值的 `condition_operator`；AND 和 OR 不属于条件运算符。
- 每个条件组只有一个统一的 `group_relation`，只连接该组的直接成员；不得为每条条件生成独立 AND/OR。
- 子条件组整体作为父组的一个直接成员。父组和子组分别维护关系，互不影响。
- `entity_relation` 描述对象之间的业务关系，不得替代条件组的 AND/OR。

字段目录至少声明：

```yaml
field_catalog:
  - field_key: ""
    label: ""
    allowed_operators: []
    value_component: input | textarea | select | tree-select | number | composite | none
    value_required: true | false
    multiple: true | false
    validation_rules: []
    placeholder: ""
    help: ""
```

## 4. 简单平铺模式

`simple-flat` 固定使用 `IxProFormList` 动态表单组件，只启用条件行的动态管理能力。

```text
隐式根条件组：AND
├── 条件 1
├── 条件 2
└── 添加条件
```

```yaml
simple_flat_contract:
  condition_list:
    component: IxProFormList
    component_mode: condition-rows-only
    initial_rows: 1
    allow_add_condition: true
    allow_delete_condition: true
    allow_add_group: false
  root_group:
    implicit: true
    relation: AND
    relation_editability: locked
    relation_visible: false
```

执行规则：

- 默认生成一条条件行；“添加条件”在底部追加条件行。
- 不生成条件组卡片、“新增条件组”、AND/OR 连接轨道或切换控件。
- 多条条件在数据语义上固定使用 AND，但不在界面展示组关系。
- 达到条件数量上限后禁用添加入口，并按需求显示当前数量和上限。
- 不得使用静态表单行替代 `IxProFormList`，也不得因 AND 不可见而省略结构化列表数据。
- 每条条件内部继续使用 `IxProFormDependency` 执行字段、操作符和值的联动。

## 5. 复杂条件模式

`logical-groups` 支持根条件组、子条件组，以及各组独立的 AND/OR。

```text
根条件组：AND
├── 条件 A
├── 条件 B
└── 子条件组：OR
    ├── 条件 C
    └── 条件 D
```

默认最多两层：

```text
第 1 层：根条件组
└── 第 2 层：子条件组
    └── 条件
```

用户明确要求超过两层时，记录用户指定的 `max_group_levels`；达到上限后只允许新增条件，不再显示新增条件组。

### 5.1 AND/OR 位置

条件组关系使用 AES 的“左侧垂直连接轨道 + AND/OR 标签”形式：

- 连接轨道覆盖当前条件组的直接成员范围。
- 根组和每个子组使用各自独立的连接轨道。
- 父组轨道不得替代或覆盖子组轨道。
- 当前组只有一个直接成员时，隐藏轨道和关系标签；有两个及以上直接成员时显示。
- 父组同时包含条件和子组时，子组整体作为父组的一个直接成员。

### 5.2 AND/OR 权限

- `relation_editability=locked`：静态展示固定关系，不生成切换控件。
- `relation_editability=user-adjustable`：只能在 `allowed_relations` 中切换。
- 切换只修改当前组，不改变父组、子组、其他组或对象关系。
- 切换不清空字段、操作符和值，不改变条件数量和组结构，不需要确认。
- 不得把 `AND_OR` 渲染成第三种关系；混合逻辑通过不同条件组分别使用 AND 或 OR 表达。

### 5.3 新增作用域

- 根区域“新增条件”追加到根组；“新增条件组”在根组中创建子组。
- 子组内“新增条件”只追加到当前子组。
- 默认两层时，子组内不显示“新增条件组”。
- 新增子组按上游契约初始化关系和编辑权限，不得改变父组关系。

## 6. 对象卡片模式

`entity-cards` 是条件组编辑器的特殊化形式：每张对象卡片是带对象语义的条件组宿主，用于明确多对象的角色、字段归属和对象关系。

```yaml
entity_card:
  key: ""
  label: ""
  role: ""
  required: true | false
  allowed_fields: []
  empty_semantics: ""
  condition_editor:
    mode: simple-flat | logical-groups
    root_group: {}
```

- 对象名称、角色、字段和数量来自上游，不默认命名为主体或客体，也不默认只有两个对象。
- 每张卡片内部按需求执行 `simple-flat` 或 `logical-groups`，并保持对应的新增条件、条件组及 AND/OR 规则。
- 卡片内部的 AND/OR 只控制本卡片条件，不代表对象之间的关系。
- `count_mode=fixed` 时不生成“添加对象”；`user-expandable` 时在对象区域底部提供该入口。
- 新增对象时创建该对象的条件编辑器；删除对象时同步处理其条件和关系；必填对象不得删除。

对象关系按以下契约执行：

```yaml
entity_relation:
  key: ""
  from: entity_card_key
  to: entity_card_key
  relation: ""
  display_mode: inline-type-tag | connector
  display_source: builtin | type-field | user-relation
  display_symbol: ""
  display_label: ""
  editability: locked | user-adjustable
  allowed_relations: []
```

- `locked` 静态展示关系标签、连接线和方向，不生成关系选择器。
- `user-adjustable` 为每条关系提供选择器，但只能使用 `allowed_relations`。
- 调整对象关系不得改变对象端点、角色、字段归属或卡片内部条件。
- 对象关系展示器与条件组 AND/OR 连接轨道必须视觉独立。

## 7. 空表达式与任意匹配

默认 `empty_expression.mode=forbidden`：至少保留一条有效条件，不允许提交空条件或空条件组。

仅当业务需要且用户在设计阶段确认后，才允许：

```yaml
empty_expression:
  mode: match-all
  confirmed: true
  runtime_confirmation: required
  display_message: 未配置条件，将匹配任意条件
```

此时：

- 允许删除全部条件和条件组，空表达式明确表示任意匹配。
- 删除最后一个有效条件前必须执行运行时高风险确认，文案必须说明会扩大匹配范围。
- 任意匹配状态持续显示明确文案，隐藏 AND/OR，且不保留虚假的空条件组。
- 点击“新增条件”时重新创建根组和第一条条件。
- 数据契约必须区分“尚未完成配置”和“已确认任意匹配”，不得只用同一个空数组表达。

## 8. 联动、删除与校验

- 字段变化后，只显示该字段允许的操作符，并清理不兼容的操作符、值和校验状态。
- 操作符变化后切换值控件，清理不兼容值并重新校验当前行。
- 无值操作符不渲染值控件；多值操作符按字段格式逐项校验。
- 删除非空条件组会删除全部子项；是否确认按风险执行 `tiered-confirmation.md`。
- `empty_expression.mode=forbidden` 时禁止删除最后一个有效条件。
- 错误定位到具体条件、条件组、对象或对象关系；提交失败保留完整表达式。
- Pattern 负责结构完整性、字段/操作符兼容性、值格式、数量、层级、对象字段归属和关系端点校验。
- 规则重复、规则冲突、策略冲突、生效范围、权限和业务状态由调用方校验。
- 加载、提交、只读和 dirty 保护继续执行 `form-management.md`。

## 9. 组件锁定

条件行和条件组锁定使用 `IxProFormList`：

- `simple-flat` 只启用条件行的新增、删除和排序能力。
- `logical-groups` 启用条件行、条件组、嵌套和排序能力。
- `entity-cards` 在每张对象卡片内部执行对应模式。
- 条件组关系绑定到条件组节点，不使用条件行局部状态保存组关系。

同一条件内“字段 → 操作符 → 值”的联动锁定使用 `IxProFormDependency`：

- `names` 使用当前条件行的字段路径数组，并采用本行局部依赖范围。
- 只负责联动渲染和重新校验，不作为条件列表或条件组的数据容器。
- 不管理 AND/OR，也不管理对象关系。

真实组件无法执行锁定方案时返回上游，不得改变表达式结构。

## 10. 输出契约

```yaml
pattern_contract:
  pattern_id: condition-expression-editor
  editor_mode:
    value: simple-flat | logical-groups | entity-cards
    decision_source: user | theme | business-reference | pattern
    decision_locked: true
  condition_contract:
    field_catalog: []
    operator_dependencies: []
    value_dependencies: []
  simple_flat_contract: {}
  logical_groups_contract:
    max_group_levels: 2
    level_source: pattern-default | user | theme
    root_group: {}
    child_group: {}
    relation_visual: left-vertical-rail
  entity_contract:
    count_mode: fixed | user-expandable | none
    entity_cards: []
    entity_relations: []
  empty_expression_contract: {}
  interaction_contracts: []
  validation_contracts: []
  state_contracts: []
  required_patterns: [form-management]
  required_components: [IxProFormList, IxProFormDependency]
  return_to_stage: none | theme | template
  return_reason: ""
  pattern_gaps: []
```

## 11. 准出条件

- 已选择且只选择一种编辑模式。
- `simple-flat` 使用 `IxProFormList`，固定隐式 AND，未生成条件组或关系控件。
- `logical-groups` 的每个组只有一个统一关系，连接轨道只覆盖当前组直接成员。
- 默认最多两层；超过两层具有用户确认和明确上限。
- 对象卡片仅在明确多对象语义下使用，卡片内部条件关系没有替代对象关系。
- 条件运算符、条件组关系和对象关系没有混用。
- 空表达式语义明确；任意匹配经过设计确认和运行时高风险确认。
- `IxProFormList` 与 `IxProFormDependency` 职责未互换。
- Pattern 未修改调用方的字段、业务校验或提交语义。
