# AES Product Design 主题层 Index

> **归属：AES Product Design。** 本 Index 是 AES（深信服下一代端点安全）产线专属主题层调用规范，不作为 Common Design 的通用主题索引。本文规定的 AES 主题路由优先；`inherit / extend` 的通用事项由 `prd-design-code` 调用 Common Design，`override` 的 AES 业务缺口进入 `reference_gaps`。

本 Index 只负责 `02-themes` 内部的主题匹配和调用顺序，不在 Index 中定义具体页面模板、交互或组件规则。具体 Theme Model 命中后可以输出完整业务方案，并锁定其中明确指定的 Template、Pattern、Feature、Component 和 Copy 要求；未指定事项才交给对应下游层决策。进入主题层后先读取本文件，不得一次读取全部主题模型。

## 调用门禁

1. 先根据需求信号匹配下表中的主题。
2. 策略类需求必须先执行本文件的“策略主题路由”章节，完成具体策略模型判断。
3. 在本文件返回明确的 `module_reference` 前，禁止读取 `security-policy-model.md` 或 `independent-policy-model.md`。
4. 规则、任务和病毒防护类需求在主题明确时，直接读取对应模块模型。
5. 主题模型输出业务对象、治理模型、生效链路、生命周期和业务不变量，并可通过 `prescribed_downstream_contracts` 直接锁定下游方案。下游 Reference 对锁定事项只负责执行和补全；只有 Theme 未指定或列入 `unresolved_items` 的事项才重新决策。

## 主题映射

| 主题 | 命中信号 | 读取路径 | 调用方式 |
| --- | --- | --- | --- |
| 策略 | 安全策略、防护配置、优先级、分配对象、生效配置 | 本文件“策略主题路由”章节 | 先路由，再读取一个具体策略模型 |
| 规则 | IOC、白名单、黑名单、Hash、IP、域名、匹配条件 | `rule-management-model.md` | 直接读取 |
| 任务 | 扫描、查杀、分发、预约、周期任务、执行结果 | `task-center-model.md` | 直接读取 |
| 病毒防护 | 病毒检测、病毒列表、病毒详情、病毒处置 | `virus-protection-model.md` | 直接读取；涉及任务时追加任务模型 |

### 规则主题补充路由

满足以下任一信号时，读取 `rule-management-model.md`：

- 以文件 Hash、IP 地址、域名、文件路径等主体值匹配；
- 配置白名单、黑名单或 IOC；
- 配置由多个行为、指标或属性组成的匹配条件；
- 规则可新增、编辑、删除、启用或禁用。

以下情况不进入规则主题：

| 情况 | 路由 |
| --- | --- |
| 策略优先级、继承或多层配置合成最终生效配置 | 执行本文件的策略主题路由 |
| 一次性执行条件 | 任务 Theme |
| 只展示检测结果，不管理匹配条件 | 事件、告警或病毒防护 Theme |
| 只展示客户端本地规则库、病毒规则库或高级威胁规则库版本 | 对应业务 Theme |

分配对象、排除对象和生效范围本身不等于策略；只有参与策略层级合成时才执行策略路由。客户端规则库是资产上安装的规则库，不属于平台规则管理。

## 策略主题路由

策略类需求必须先在本节完成业务模型判断，再决定是否读取具体策略模型。只有策略类需求需要执行本节；规则、任务和病毒防护需求不执行策略分支。

### 复用安全策略

满足以下任一条件，且没有排除证据时，优先复用 `security-policy-model.md`：

- 控制终端防护、检测、采集、隔离、信任或客户端行为；
- 配置需要下发至终端 Agent 后生效；
- 可以沿用状态、优先级、分配对象和排除对象；
- 只是增加参数、配置项或一至三级能力分类；
- 与现有安全策略的基础配置、安全配置、病毒防御或高级威胁能力边界直接相关。

### 建立独立策略

仅当需求明确存在以下业务差异时，才读取 `independent-policy-model.md`：

- 需要创建多条独立策略并分别管理；
- 需要独立列表、详情、复制、删除或生命周期；
- 具有不同于安全策略的分配、生效或冲突规则；
- 具有独立权限、审批或授权模型；
- 管理对象不是终端安全防护配置。

“新增策略”“新增页面”“希望入口更明显”或配置项较多，单独出现时都不能判定为独立策略。

### 路由输出与门禁

```yaml
theme_resolution:
  theme_type: strategy_routing
  matched_theme: policy
  routing_completed: true
  module_reference: security-policy-model.md | independent-policy-model.md
  module_status: existing | new
  business_model_confirmed: true | false
```

未确认以下事实时，`business_model_confirmed` 必须为 `false`，不得读取具体策略模型：

1. 是否需要创建多条独立配置实例并分别分配对象；
2. 是否可以沿用安全策略的优先级、分配对象和排除对象；
3. 是否存在独立审批、权限、授权、生效或冲突规则。

策略路由完成后只读取一个具体策略模型。具体模型可以锁定页面、交互、单项能力和组件方案；锁定事项由 Template、Pattern、Feature 和 Component 层直接执行，未锁定事项再按对应层级路由。

## 主题结果

主题层向 `prd-design-code` 返回：

```yaml
theme_resolution:
  theme_type: strategy_routing | module_model
  matched_theme: ""
  routing_reference: ""
  module_reference: ""
  module_status: existing | new | not_applicable
  business_model_confirmed: true | false
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
