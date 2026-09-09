---
name: aes-product-design
description: 提供 AES（深信服下一代端点安全）专属业务设计规范与设计知识，包括产品定位、业务对象、导航、主题、页面模板、Pattern、Feature、Component、交互规则、产品术语与已有资产复用规则；供 prd-design-code 在 AES 需求设计和页面规划阶段按需读取
metadata:
  skill_type: product-design
  product_id: aes,dr
  scope: b2b-product-design
  capability: product-design-knowledge
  inherits: common-design
  version: "1.3"
---

# AES Product Design

## 定位

本 Skill 是 AES 产线设计知识源，由 `prd-design-code` 按设计层级编排使用，不独立输出完整 PRD、设计说明书、HTML 或代码。

| Skill | 固定职责 |
| --- | --- |
| `prd-design-code` | 分析需求、识别产品和当前层级、编排 AES Product Design 与 Common Design、汇总最终交付物 |
| AES Product Design | 提供 AES 业务事实、产品差异、既有设计模式、业务组件映射和专属设计规则 |
| Common Design | 提供跨产线通用设计规则，按 Coverage 补充 AES 未覆盖的通用事项 |

AES Product Design 不主动调用或反向编排另外两个 Skill。需要 Common Design、需要返回上层重算或存在知识缺口时，将结构化结果返回 `prd-design-code`。

## 分层调用模型

`references/index.md` 是 AES 侧阶段路由入口。`prd-design-code` 首次进入 AES Product Design 时先读取该 Index，同时结合 Common Design 的整体阶段路由判断当前层是否命中、由哪一侧提供规则以及是否需要合并；不得把 AES 层级调用当作独立于 Common Design 的第二套流程，也不得使用旧版目录、文件名或层级名称替代下表：

```text
需求分析
  ↓
Navigation → Theme → Template → Pattern → Feature → Component → Copy
  ↓
设计说明书
```

| 层级 | 只解决什么 | 不解决什么 |
| --- | --- | --- |
| Navigation | 功能从哪里进入、菜单/页头 Tab 层级、入口变更影响 | 业务模型和页面结构 |
| Theme | 业务对象、治理模型、生效链路、生命周期和业务不变量；命中可复用主题时可直接指定并锁定下游方案 | Theme 未指定的通用事项 |
| Template | 页面类型、主容器、主要区域及区块顺序；允许页面级决策链 | 区域内部复杂交互方案 |
| Pattern | 在已确定 Template 内执行上游锁定方案，或对未锁定事项选择、组合区域级或复杂交互方案 | 改变业务模型或主容器 |
| Feature | 已确定采用后可完整执行的单项方案；可含流程、状态、校验和异常 | 在多套设计方案中选择 |
| Component | 真实组件、稳定业务封装、实现入口和复用边界；可以是 AES 业务封装、IDUX 组合或项目通用组件 | 反推上层方案 |
| Copy | 校准已确定语义的用户可见文案和 AES 术语 | 新增业务语义或改变方案 |

`Pattern`、`Feature` 与 `Component` 是三个独立层级：Pattern 对未锁定事项负责选择和组合方案，对锁定事项只负责执行；Feature 负责执行已选定的单项能力；Component 负责真实 AES 业务封装和实现映射。不得将三者合并为旧版的“业务处理 / 业务组件”阶段。

### Template、Feature 与 Component 的封装约定

- `templateId` 是 AES 页面模板的稳定编号和名称；是否采用某种页面结构仍由使用条件和上游锁定结果决定。
- `encapsulation: true` 时，`templateId` 必须与前端已有页面模板编号一致；`encapsulation: false` 时仍须填写该页面模板的稳定 `templateId`，不表示存在可直接调用的页面代码。
- `templateId` 可以为 `custom`；没有既有 AES 模板可承载时使用，不阻断当前设计或开发，也不得为了获得编号改变已确认的页面结构。
- `featureId` 仅用于与前端编码 skill 映射；是否调用 Feature 仍由使用条件和上游锁定结果决定。
- `featureId` 可以为空；没有正式 ID 不阻断当前设计或开发，也不得编造新的 ID。
- `templateId`、`featureId` 和 `componentId` 不表示一定存在可复用封装；`encapsulation: true | false` 是唯一的封装判断。
- `encapsulation: true` 时优先复用已有封装，未覆盖部分继续按当前层契约补充；`encapsulation: false` 时按当前层完整契约自行实现，不得声称复用了前端封装。
- Component 的 `componentId` 只表示实现入口，不代表所有相似页面都必须使用；使用前仍需先判断适用条件。
- 前端封装、IDUX 组合和未封装能力都必须保持同一业务契约；封装不能覆盖或改写 Theme、Template、Pattern、Feature 已确认的业务规则。

### Theme 锁定下游方案

Theme 是按需命中的完整业务方案来源。命中具体 Theme 后，Theme 可以根据稳定的 AES 业务模式直接指定 Template、Pattern、Feature、Component 和 Copy 要求，并通过 `prescribed_downstream_contracts` 标记锁定范围：

- `locked: true` 的事项由 Theme 持有决策权；对应下游层只执行、展开和验证，不得重新选型、降级或修改；
- Theme 未指定或明确列入 `unresolved_items` 的事项，才由对应下游层执行常规路由和决策；
- 下游发现锁定方案缺少实现证据、无法执行或与已确认用户要求冲突时，返回 Theme 或最早受影响的上游层，不得在下游静默改写；
- 用户确认的要求始终具有最终决策权。用户修改 Theme 方案后，将用户结论更新为新的锁定输入，并记录被覆盖的 Theme 规则及影响；
- 读取锁定方案指定的下游 Reference，是为了取得完整执行流程、状态、校验、异常和组件映射，不代表下游重新获得决策权。

```yaml
prescribed_downstream_contracts:
  template:
    - { contract_id: "", locked: true | false, values: {} }
  patterns:
    - { contract_id: "", locked: true | false, values: {} }
  features:
    - { contract_id: "", locked: true | false, enabled_when: "", values: {} }
  components:
    - { contract_id: "", locked: true | false, values: {} }
  copy:
    - { contract_id: "", locked: true | false, values: {} }
  unresolved_items: []
```

不得规定先完整读取 Common Design 或先完整读取 AES Product Design。每次只处理 `current_stage` 的具体事项，并由 `prd-design-code` 联合判断 AES 与 Common Design 在该层的命中关系；当前层完成后再进入下一层。若用户已明确当前层结论（包括入口、页面模板、业务规则、Feature 或组件），直接将用户结论作为当前层输入，不得用 Common Design 或 AES Reference 覆盖；仅对用户未说明的事项执行双方的匹配和 Coverage 判断。

### 层间返回规则

- Theme 是可选层，不是所有需求的必经层。只有 AES 或 Common Design 任一侧命中可复用主题，或双方联合判断确实需要抽取业务主题时，才进入 Theme；两侧都未命中时直接进入 Template。
- Template 发现入口不成立：返回 Navigation；发现业务模型不成立或 Theme 锁定的 Template 无法执行：返回 Theme；未命中 Theme 时保留当前层并记录缺口。
- Pattern 需要改变未被 Theme 锁定的页面类型、主容器、主要区域或区块顺序：返回 Template；若受影响事项已被 Theme 锁定，返回 Theme，不得直接修改 Template 契约。
- Feature 对未锁定事项出现多套候选方案或需要组合多个能力：返回 Pattern；需要改变页面结构时返回 Template。若受影响事项已被 Theme 锁定，返回 Theme，不得在 Feature 层重新选择。
- Component 缺少实现映射：记录缺口；若缺口涉及 Theme 锁定组件则返回 Theme，否则返回最早受影响的 Feature、Pattern 或 Template。
- Copy 与已确认业务语义冲突：锁定文案来自 Theme 时返回 Theme，否则返回产生该语义的最早层级。

层间返回以双方联合结果为准：下层发现冲突、缺口或前置结论失效时，`return_to_stage` 指向最早受影响的共同上游层；不得因为问题来自 Common Design 就跳过 AES，也不得因为当前调用的是 AES Product Design 就只返回 AES Theme。

## Coverage

Coverage 是 AES 对具体设计能力的唯一覆盖声明，必须由当前层 Index 或具体 Reference 显式给出。Coverage 只描述 AES 是否改变该能力，不负责编排其他 Skill 的读取流程。

Coverage 只能取以下值：

- `inherit`：AES 不改变该能力。
- `extend`：AES 增加产品专属规则；未冲突的通用规则继续生效，同一规则冲突时以 AES 为准。
- `override`：AES 对该能力提供完整或冲突定义，AES 规则是该能力的最终规则。

未声明 Coverage 时不得自行推断为 `inherit`、`extend` 或 `override`，必须记录 Coverage 缺失。未命中 AES Reference 时，该能力不属于 AES 覆盖范围，由 `prd-design-code` 按其流程处理通用设计基准。

| 当前阶段 | 读取原则 |
| --- | --- |
| Navigation | 业务菜单、入口和层级事实以 AES 导航 Reference 与需求/现状证据为准；Common Design 可补充通用导航约束或影响检查，但不得补造 AES 菜单、入口或层级。 |
| Theme | 先执行 AES Theme 的显式 Coverage；未命中 AES Theme 时再由 `prd-design-code` 处理通用主题。 |
| Template | 先执行 Theme 锁定的 Template；其余事项按 AES Template 的显式 Coverage 执行。未命中 AES Template 时由 `prd-design-code` 处理通用模板。 |
| Pattern | 先执行 Theme 锁定的 Pattern 及其参数；其余事项按 AES Pattern 的显式 Coverage 执行。未命中 AES Pattern 时由 `prd-design-code` 处理通用模式。 |
| Feature | Theme 或 Pattern 已锁定 Feature 时直接完整执行；其余事项按 AES Feature 的显式 Coverage 执行。未命中 AES Feature 时由 `prd-design-code` 处理通用能力。 |
| Component | Theme、Pattern 或 Feature 已锁定组件语义或映射时直接执行并验证；其余事项按 AES Component 的显式 Coverage 执行。未命中 AES Component 时由 `prd-design-code` 处理通用组件或项目代码。 |
| Copy | 固定采用 `extend`：读取 AES 术语与 Common Design 通用文案，AES 术语和表达优先。 |

Coverage 必须逐项记录，不得把“命中 AES”自动等同于 `override`。Coverage 的具体含义以本节定义为准；AES Reference 只需声明自身 Coverage 和负责的 AES 规则范围。

不得只返回“AES 优先”。必须逐项说明设计能力、Coverage、命中的 AES Reference、AES 已确定规则和知识缺口。通用设计不得补造 AES 专属业务对象、状态流转、权限、数量限制、生效关系或生命周期。

## 读取路由

首次进入本 Skill 时读取 `references/index.md`。之后只读取 `current_stage` 对应的 AES 层 Index，并由 `prd-design-code` 同步匹配 Common Design 当前层路由和具体 Reference；依据双方命中结果与具体 Coverage 决定来源，不递归加载全部文件。

读取各层 Index 只表示完成能力发现，不表示已完成该层设计。根据需求命中 Index 中的条目后，必须继续读取该条目链接的具体 Reference；仅读取 Index 时不得输出设计结论。

每层按以下顺序执行；每个阶段是否进入、是否读取 AES/Common Design、是否合并以及返回哪一层，由双方命中结果和上游契约共同决定：

```text
识别 current_stage
  ↓
读取上游锁定契约及 AES 与 Common Design 当前层 Index（按需）
  ↓
锁定事项直接执行；未指定事项联合匹配双方 Reference
  ↓
按命中能力显式声明的 `Coverage` 决定 AES 规则范围
  ↓
返回当前层契约，再进入下一层或返回上层重算
```

| `current_stage` | 首个读取入口 | 后续读取方式 |
| --- | --- | --- |
| `navigation` | `references/01-navigation/navigation.md` | 单文件完成入口判断 |
| `theme` | `references/02-themes/index.md` | 按主题映射只读取命中的模型；策略先完成 Index 内路由 |
| `template` | `references/03-templates/index.md` | 只读取 list、form、detail 中命中的模板 |
| `pattern` | `references/04-patterns/index.md` | 按决策问题读取一个主 Pattern，按需追加依赖 Pattern |
| `feature` | `references/05-features/index.md` | 只读取 Pattern 输出或用户明确指定的 Feature |
| `component` | `references/06-components/index.md` | 只读取 Feature/Pattern 要求的真实组件映射 |
| `copy` | `references/07-copywriting-terminology.md` | 业务语义和方案确定后读取 |

### 特殊路由要求

- 需求已指定菜单、页头 Tab 或页面入口时，直接遵循用户指定内容并记录为 `navigation_contract`；需求未涉及入口时，Navigation 仅按需读取，不因缺少导航信息阻断后续 Theme。若入口变更可能影响首页或跨模块入口，再补充影响检查。
- Theme 中的策略需求必须先执行 `references/02-themes/index.md` 的策略路由，禁止直接猜测具体策略模型。
- Theme 输出的 `prescribed_downstream_contracts` 是后续层的锁定输入；后续层只展开执行，禁止重新决策。
- Template 输出下游 `pattern_requirements` 和可直接调用的 `feature_requirements`，不得直接指定组件实现。
- Pattern 输出选定方案及所需 Feature/Component；没有决策链的单项能力可由 Template 直接交给 Feature。
- Feature 只执行既定能力，不为经过 Pattern 而制造无意义的选择。
- Copy 最后校准表达；不得因为文案文件在索引中出现，就提前用术语影响业务或结构决策。

## 规则优先级

```text
用户本次明确且已确认的要求
> 已确认的 AES 业务事实与主题业务不变量
> 当前事项命中的 AES Reference
> 当前事项的 Common Design 规则
> 设计系统和组件库默认能力
```

- 用户要求与 AES 业务不变量冲突时，返回冲突和影响，由 `prd-design-code` 提请用户确认。
- AES 只覆盖 Reference 明确规定的事项，不因命中一条规则而替换当前层其他能力。
- 项目代码、真实页面和接口用于确认现状与实现证据，不得凭单一历史实现覆盖已确认规则。

## Reference 身份要求

所有 `references/` 文件均属于 AES Product Design 内部知识，不作为独立 Skill 调用。每个 Reference 必须在一级标题后明确：

1. 归属 AES Product Design；
2. 是 AES 产线专属设计规范或索引；
3. 不作为 Common Design 通用规范；
4. 当前文件明确规定的 AES 规则优先，未覆盖事项按 Coverage 处理。

统一身份声明不改变 Coverage：`override` 的适用范围仍以本文件的 Coverage 声明和 Reference 正文为准。

## 输入契约

`prd-design-code` 调用时提供当前层可获得的信息，不要求首轮填满：

```yaml
original_request: 用户原始需求
product_id: aes
delivery_scope: design
current_stage: navigation | theme | template | pattern | feature | component | copy
design_questions: []
confirmed_upstream:
  navigation_contract: {}
  business_invariants: []
  page_inventory: []
  template_contracts: []
  pattern_contracts: []
  feature_contracts: []
  prescribed_downstream_contracts: {}
evidence:
  requirement: []
  existing_pages: []
  project_code: []
```

只处理 `current_stage` 和 `design_questions` 指向的事项。缺少会改变结论的信息时返回问题，不自行扩大任务范围。

## 输出契约

向 `prd-design-code` 返回当前层结果，不直接生成最终设计说明书：

```yaml
aes_stage_result:
  current_stage: navigation | theme | template | pattern | feature | component | copy
  status: resolved | needs_common_design | needs_confirmation | blocked
  matched_references: []
  resolved_design_abilities:
    - design_ability: ""
      Coverage: inherit | extend | override
      aes_references: []
      matched_aes_rules: []
      common_design_required: true | false
      common_design_fallbacks: []
      reference_gaps: []
      conflicts: []
      featureId: ""
      componentId: ""
      encapsulation: true | false
  stage_contract:
    navigation_contract: {}
    theme_contract: {}
    template_contract: {}
    pattern_contract: {}
    feature_contract: {}
    component_contract: {}
    copy_contract: {}
  downstream_requirements:
    next_stage: theme | template | pattern | feature | component | copy | complete
    required_references: []
    prescribed_downstream_contracts:
      template: []
      patterns: []
      features: []
      components: []
      copy: []
      unresolved_items: []
    design_questions: []
  return_to_stage: none | navigation | theme | template | pattern | feature | component | copy
  return_reason: ""
  common_design_fallbacks: []
  reference_gaps: []
  conflicts: []
  blocking_questions: []
```

### 字段约束

- 每项 `design_ability` 单独记录；只有 AES Reference 显式声明 `Coverage: inherit` 时才可填写 `inherit`。未命中 AES Reference 不得填写 `inherit`，应记录为 AES 未覆盖。
- `common_design_required` 按 AES 与 Common Design 的联合命中结果、当前阶段读取原则和具体 Reference 判定，不得由 `inherit / extend` 字面机械推导：AES 独占的 Navigation 业务事实、Theme、Feature、Component 可为 `false`；仅命中或需要补充 Common Design 时为 `true`；Copy 固定为 `true`；Template、Pattern 按双方命中结果和具体 Reference 的覆盖声明填写。
- `override` 的 `common_design_required` 默认 `false`，只有正文明确要求补充具体事项时才可为 `true`。
- `stage_contract` 只填当前层对应对象，其他对象留空；Theme 对下游的锁定方案统一写入 `downstream_requirements.prescribed_downstream_contracts`，不得混入其他层的 `stage_contract`。
- 一般阶段的 `downstream_requirements` 只传递已确认结论及下一层待解决事项；Theme 命中时可以通过 `prescribed_downstream_contracts` 直接锁定下游决策，后续层不得重新选择。
- `reference_gaps` 记录 AES 应定义但尚未定义的知识；不得伪装成 Common Design 可确定的事实。
- `return_to_stage` 指向最早需要重算的层级。

## 禁止事项

- 不独立输出完整 PRD、设计说明书、HTML 或代码。
- 不一次加载全部 AES Reference，不按文件名相似度猜测主题。
- 不合并 Pattern、Feature、Component 为一个模糊阶段。
- 不让 Template 直接选择具体组件，不让 Component 反推业务或页面方案。
- 不用 Common Design 覆盖已命中的 AES 规则，也不将 AES 未说明的内容擅自定义为产品差异。
- 不允许下层静默修改已确认的上层契约。
- 不允许 Template、Pattern、Feature 或 Component 对 Theme 已锁定事项重新选型；不可执行时必须返回上游。

## 自检

- 当前只处理一个层级，且已使用该层 Index 路由。
- Template、Pattern、Feature、Component 的输出边界没有混用。
- Theme 已锁定的下游事项均被直接执行，只有 `unresolved_items` 进入下游决策。
- 已逐项记录 `inherit / extend / override` 和具体知识来源。
- `override` 缺口没有自动回退 Common Design。
- 只读取本次命中的 Reference；需要重算时已返回正确上层。
- Copy 在业务与方案确定后调用。
