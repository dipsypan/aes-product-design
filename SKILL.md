---
name: aes-business-skill
description: 为深信服 AES 下一代端点安全产品提供业务设计知识路由和前端交付约束。用于 AES 的需求设计、主题建模、列表/表单/详情框架、业务处理、业务组件、页面文案、前端实现和回归验收；在公共设计 Skill 的每个设计层级中按需加载 AES 同层差异规则，并允许从细则返回框架或主题重新判断。策略、规则、任务、病毒防护等 AES 业务需求均应使用。
---

# AES 业务 Skill

## 目标

将公共设计规则和 AES 业务规则按相同设计层级组合使用。不要先执行完整公共设计再统一覆盖 AES，也不要一次加载全部 AES Reference。

固定遵循：

```text
主题场景 → 页面框架 → 业务处理 / 业务组件 → 设计结果
    ↑           ↑                 │
    └───────────┴──── 发现冲突时返回重算

需要输出页面文案时：设计结果 → AES 术语与命名校准
```

- 每个阶段先取得公共设计 Skill 的同层结论，再读取 AES 同层 Reference 进行继承、补充、覆盖、替换或禁用。
- 下层规则不能破坏已确认的主题业务不变量；下层能力无法承载时返回对应上层重算。
- 术语不参与需求理解、主题识别、页面框架或组件选择，只在生成或检查文案时调用。

## 初始加载

1. 完整读取 `references/reference-registry.md`。
2. 读取 `references/product-context.md`，建立 AES 产品边界；不要在此阶段读取术语、全部主题或全部页面模板。
3. 从用户需求、公共设计阶段输出、真实产品页面和项目代码中提取业务事实。
4. 按注册表从主题层开始逐层读取命中的 AES Reference。

将 Reference 当作本 Skill 的强制规则文件，不把它们当成可独立触发的 Skill。

## 规则合并

### 优先级

```text
用户本次明确且已确认的要求
> 已确认的 AES 主题业务不变量
> 当前层 AES 差异规则
> 当前层公共设计规则
> SD Design / iDux 基础能力
```

- 用户要求与业务不变量冲突时必须指出影响，不能静默覆盖。
- 页面模板、业务处理和组件规则只能在上层允许的范围内细化。
- AES 当前层未定义差异时，完整沿用公共设计规则。

### 差异关系

每次合并公共与 AES 规则时，按以下关系记录：

| 关系 | 执行方式 |
| --- | --- |
| `inherit` | 完整使用公共规则 |
| `extend` | 保留公共规则并增加 AES 约束 |
| `override` | 只修改公共规则的明确参数或行为，其余继续继承 |
| `replace` | 当前事项完整使用 AES 规则 |
| `disable` | AES 明确不采用该公共能力，并记录原因 |

不得用一句“AES 规则优先”替代逐项合并。

## 分层执行

### 1. 主题场景

目标：确定业务对象、业务目标、治理模型、生效链路、生命周期和页面清单。

1. 接收公共设计 Skill 对主题场景的初步判断。
2. 根据 `reference-registry.md` 读取命中的 AES 主题 Reference。
3. 先区分规则、策略及其他主题；不能因页面相似而合并业务模型。
4. 输出业务不变量、页面清单、交互契约和下一阶段需要的页面能力。

当前主题基线：

- 规则管理：`references/themes/rule-management.md`
- 策略管理：先读取 `references/themes/policy-routing.md`，再进入已有安全策略或全新策略分支。
- 尚未形成 Reference 的任务中心、病毒防护等主题：读取真实项目和需求证据，返回 `reference_gaps`，不得套用规则或策略模型。

主题阶段不得读取 `references/terminology.md` 来帮助业务分类。

### 2. 页面框架

目标：在主题返回的 `page_inventory` 和 `design_capabilities` 内确定页面结构。

对每项页面能力，先结合公共页面框架，再读取 AES 对应模板：

- `list | search | filter | sort`：`references/templates/list.md`
- `form`：`references/templates/form.md`
- `detail`：`references/templates/detail.md`

本阶段确定容器、区域、字段组织、操作位置和页面状态，不重新定义主题业务对象。主题已经固定容器或业务模块时，模板跳过对应选型，只完成其余结构。

若框架无法承载主题任务，返回主题阶段；不得通过堆叠抽屉、Tab、卡片或自定义组件勉强实现。

### 3. 业务处理与业务组件

目标：确定页面框架中命中的细粒度交互和业务组件。

1. 根据框架产生的 `pattern_capabilities` 读取 `references/patterns/index.md` 中命中的规则。
2. 根据 `component_capabilities` 读取 `references/components/index.md` 中命中的组件规则。
3. 同时执行公共设计 Skill 的同类交互/组件规则和 SD Design / iDux 组件约束。
4. AES 没有差异规则时沿用公共结果，不自行补造 AES 特例。

业务处理包括筛选、标签、二次确认、批量操作、实体展示、层级省略、跳转等；业务组件包括资产选择器、资产卡片、搜索、导入导出、动态页签等。

若细则或组件改变了页面区域、容器或信息层级，返回页面框架阶段；若改变业务对象、生效范围、生命周期或治理模型，返回主题阶段。

### 4. 文案与术语校准

仅在需要生成或检查以下内容时读取 `references/terminology.md`：

- 页面、菜单、字段和状态名称
- 按钮、操作组和跳转入口文案
- 提示、确认、错误、空状态和帮助文案
- 中英文术语、单位、实体和技术内容表达

术语规则只校准表达，不新增业务字段，不改变业务语义，不决定页面、容器和组件。文案校准发现含义不明确时返回原决策阶段确认语义，而不是用术语规则猜测。

### 5. 评估与回退

形成方案后交给公共评估 Skill。按问题归属回退：

| 问题 | 返回阶段 |
| --- | --- |
| 业务对象、治理模型、生效链路或任务闭环错误 | 主题场景 |
| 页面容器、区域、信息组织或层级错误 | 页面框架 |
| 交互状态、业务组件或组件参数错误 | 业务处理 / 业务组件 |
| 名称、按钮、提示语或术语不一致 | 文案与术语校准 |

回退时保留未受影响的已确认结论，只重算受影响阶段及其下游；禁止每次从头加载全部 Reference。

## 策略主题内部路由

策略主题读取 `references/themes/policy-routing.md`，依据业务对象和治理模型判断：

- 可复用安全策略治理模型：读取 `references/themes/policy-management-existing.md`。
- 存在独立策略对象或治理模型：读取 `references/themes/policy-management-new.md`。

规则主题直接读取 `references/themes/rule-management.md`。规则与策略分别建模：规则不得继承策略的优先级、内置策略、复制、分配冲突和继承模型；策略也不得因包含条件配置而降级为规则。

## 循环上下文包

每个阶段读取和回写同一上下文：

```yaml
original_request: 用户原始需求
target_outcome: 目标结果
delivery_scope: design | frontend | design-and-frontend
current_stage: theme | template | pattern-component | copy | acceptance
public_stage_result: 当前阶段公共设计结论
matched_aes_references: 当前阶段实际读取的 AES Reference
rule_relations:
  inherited: []
  extended: []
  overridden: []
  replaced: []
  disabled: []
business_pattern: 主题业务模式
business_invariants: 不得被下游破坏的业务规则
interaction_contracts: 前置状态、动作、结果和失败反馈
form_state_contract: 注册、校验、dirty、变更和提交映射
page_inventory: 页面、容器和关键状态
design_capabilities: 下一步所需页面能力
pattern_capabilities: 下一步所需业务处理能力
component_capabilities: 下一步所需业务组件能力
visual_contracts: 布局、组件、层级和状态规则
copy_contracts: 待生成或已校准的页面文案
reference_evidence: 需求、真实页面、项目代码和接口证据
reference_gaps: 当前缺少的 AES 业务 Reference
acceptance_checks: 可观察、可执行的验收条件
regression_scope: 可能受影响的既有行为
return_to_stage: none | theme | template | pattern-component | copy
return_reason: 回退原因
blocking_questions: 最多 3 个会改变当前阶段结论的问题
post_questions: 不阻塞主体方案的问题
```

每一轮只更新当前阶段拥有的字段。下层不得覆盖 `business_invariants`，只能发现冲突并设置 `return_to_stage`。

## 前端交付

用户要求前端实现时：

1. 重新读取命中的主题 Reference 和本次涉及的模板、业务处理及组件 Reference。
2. 编辑前冻结 `business_invariants`、`interaction_contracts`、`form_state_contract` 和 `regression_scope`。
3. 检查真实页面、路由、组件和代码实现；不得只按文字近似还原。
4. 使用 iDux 组件前执行对应组件查询，不凭记忆猜 API。
5. 修改完成后读取 `references/acceptance/frontend.md` 并执行运行验收。
6. 只有验收返回 `status: passed` 才能声明完成；构建成功、资源 200 或代码存在不能代替行为验收。

## 沟通规则

- 每个阶段最多集中询问 3 个会改变该阶段结论的问题。
- 先提供基于证据的推荐，不要求用户自行判断业务分类或页面类型。
- 不重复询问已经确认的内容。
- 不影响当前阶段成立的问题作为后置项，继续推进。
- 用户在同一页面继续反馈时，从受影响的最低阶段重入；只有触及上层不变量时才向上回退。

## 输出契约

最终输出至少包含：

1. 命中的 AES 主题和业务结论
2. 主题、框架、细则/组件各阶段实际使用的公共与 AES 规则
3. AES 对公共规则的差异关系
4. 页面结构、交互、组件和状态方案
5. 文案交付时的术语校准结果
6. 待确认项、Reference 缺口和自检结果
7. 前端交付时的验收状态、失败项和证据

## 自检

- 已从主题进入框架再进入细则/组件，没有一次加载全部规则
- 公共与 AES 规则在每个命中层级成对合并，而非前后两套串行方案
- 术语只在文案生成或检查时调用，没有参与业务与页面选型
- 规则与策略使用不同主题模型
- 下层没有覆盖主题业务不变量
- 发生冲突时返回了正确上层，只重算受影响链路
- AES 未覆盖处继续使用公共规则，没有擅造产品差异
- 前端交付已执行真实页面检查和运行验收
