# AES 表单模板

> **归属：AES Product Design。** 本 Reference 是 AES（深信服下一代端点安全）产线专属页面模板，不作为 Common Design 的通用模板。先按 AES 业务确定容器、入口和流程结构，再映射 Common Design；不得为了匹配 Common Design 而改变 AES 方案。

## 定位

本 Template 接收 Theme 已确认的配置对象、任务目标、业务流程、业务分区、字段依赖、风险操作和业务不变量，负责确定表单容器、入口关系、流程结构、页面级主要区域、操作区位置和退出入口。

字段控件、字段排列、标题样式、高级设置、依赖显隐、校验反馈、未保存状态判断和提交反馈交给 `../04-patterns/form-management.md`。保存、取消、返回和确认的业务结果来自 Theme，不得在本层自行定义。

> 本文线框图仅用于说明结构关系。不得直接照抄图中的内容数量、排列方式、分区名称或操作按钮；只有正文明确列出的规则具有约束力。具体内容必须根据 Theme、当前产品同类页面和 Form Pattern 确定。

## 1. 决策模型

依次完成三个独立判断：

```text
表单需求
├── 承载容器：Page / Modal / Drawer
├── 入口关系：Stable / Drilldown / Contextual
└── 流程结构：Single-surface / Progressive / Stepper
```

不得将 Drawer 默认等同于单面表单，也不得将 Stepper 默认等同于下钻页面。

## 2. 容器与入口决策

按以下顺序判断，命中后停止：

1. 用户、Theme 或 AES 存量同类业务已明确容器时，直接采用。
2. 独立菜单、页头 Tab 或需要稳定入口的长期配置，使用 `page + stable`。
3. 从列表或详情进入，需要完成完整编辑并返回来源页面，使用 `page + drilldown`。
4. 当前页面内目标单一、边界明确、可短时完成的配置，使用 `modal + contextual`。
5. 需要保留来源上下文，同时承载较完整配置、递进选择或 AES 已有 Drawer 模式时，使用 `drawer + contextual`。
6. 缺少依据时返回前置确认项，不按字段数量机械选择容器。

字段数量、页面长度和分组数量只作为复杂度信号，不能单独决定容器。`confirm-modal` 只用于操作确认，不属于表单容器。

### 2.1 Page

- 适合稳定配置入口、较长编辑任务或需要完整页面空间的表单。
- `stable` 通过菜单或页头 Tab 直接进入。
- `drilldown` 从列表或详情进入，并提供明确返回路径。
- 页面正文沿用 AES 产品壳层提供的页头，不重复生成页面页头。

### 2.2 Modal

- 适合当前上下文中的短任务。
- 默认优先使用单面结构；存在明确阶段时可以使用 Stepper。
- 需要多层进入、长时间编辑或较完整配置时，重新评估 Page 或 Drawer。

### 2.3 Drawer

- 适合保留来源上下文，同时完成较完整配置或递进任务。
- 支持单面、递进式和步骤条结构。
- 不得仅因字段较多使用 Drawer；选择依据应来自用户要求、同类业务模式或上下文关系。

## 3. 流程结构决策

### 3.1 单面结构 `single-surface`

所有主要配置在同一个内容表面完成。

适用于：

- 配置目标单一；
- 不存在必须按顺序完成的阶段；
- 用户需要同时查看或对照多个业务分区；
- 拆分流程会增加来回切换成本。

字段条件显隐不等于递进式或步骤条流程。

### 3.2 递进式结构 `progressive`

递进式结构用于“先选择进入路径，再完成对应配置”的表单任务。各层具有父子关系；进入下一层时替换当前层，返回时恢复上一层，不同时叠加展示，也不持续显示步骤条。

满足以下条件时使用：

- 第一层用于选择类型、方案或处理路径；
- 不同选择对应不同的完整配置内容；
- 下一层具有独立任务目标和业务分区；
- 用户需要通过返回入口重新选择上一层内容。

如果前置选择只控制少量字段显隐，继续使用单面表单。

#### 结构示意

```text
┌──────────────────────────────────────┐
│ 第一层：[当前层级标题]          [关闭] │
├──────────────────────────────────────┤
│                                      │
│ [用于选择类型、方案或进入路径的内容] │
│                                      │
└──────────────────┬───────────────────┘
                   │ 选择一条路径
                   ▼
┌──────────────────────────────────────┐
│ [返回] 第二层：[当前任务标题]  [关闭] │
├──────────────────────────────────────┤
│                                      │
│ [当前路径对应的完整配置内容]         │
│                                      │
├──────────────────────────────────────┤
│ [根据业务需要确定的操作区]           │
└──────────────────────────────────────┘
                   │
                   └── 返回上一层
```

线框图只约束以下关系：

- 第一层负责选择进入路径，下一层负责完成所选路径对应的完整配置。
- 进入下一层时替换当前层，不同时展示或视觉叠加。
- 返回只回到上一层；关闭退出整个递进流程。
- 各分支的配置内容相互独立，不混用不适用的数据。

线框图不规定选择方式、分类数量、排列列数、业务分区、提示内容或按钮组合，这些内容必须重新根据业务确定。

#### 返回与状态

- 尚未修改当前层配置时，可以直接返回上一层。
- 已有修改且返回会丢失内容时，先提示用户确认。
- 业务要求保留草稿时，再次进入同一分支恢复已有内容；否则仅在确认放弃后清空。
- 返回后选择其他路径时，不得将上一分支不适用的数据带入新分支。

AES 任务创建可作为现有参考：第一层选择任务类型，第二层配置所选任务；两层 Drawer 轮换展示，不形成层叠。

### 3.3 步骤条结构 `stepper`

只有所有配置属于同一个连续任务流程时，才使用 Stepper。

满足以下任一条件时可以采用：

- 存在明确且固定的阶段目标；
- 后一步依赖前一步结果；
- 需要分步校验、预览确认或阶段性提交；
- 单面结构难以表达任务进度。

以下情况不使用 Stepper：

- 配置项只是平行分类；
- 用户需要频繁对照多个分区；
- 拆分只减少页面长度，没有形成阶段目标；
- 多个配置对象并不属于同一任务流程。

表单较长只能触发评估，不能单独作为拆分步骤的依据。

#### 步骤导航

根据业务流程选择一种方式：

| 导航方式 | 规则 |
| --- | --- |
| `sequential` | 只通过上一步、下一步按顺序切换 |
| `validated-direct` | 当前步骤校验通过后，可点击允许访问的步骤直接切换 |

- 必须明确每一步的目标、进入条件、返回规则、可访问范围和最终提交位置。
- 点击步骤只切换同一表单内的内容，不代表保存或离开表单。
- 校验失败时停留在当前步骤，并明确指出需要修正的内容。
- 步骤之间保留已填写内容和未保存状态。

## 4. 页面级区域

```text
表单容器
├── 容器头部
├── 页面提示区（按需，由 page-notice Pattern 决定）
├── 流程导航区（Progressive 或 Stepper）
├── 分区定位区（按需）
├── 表单正文
│   └── Theme 已确定的业务分区
└── 操作区
```

- 业务分区名称和顺序来自 Theme。
- 多个平行且较长的一级业务分区需要快速跳转时，可增加页面级分区定位。
- 分区较少或内容较短时不增加定位导航，不使用固定数量或屏数作为硬阈值。
- 高级设置、二级标题和字段排列由 Form Pattern 决定。
- 操作区位置由本层确定，按钮语义由 Theme 提供。
- 页面存在授权、风险、影响范围或其他业务提示时，预留 `noticeRegion`；提示条的展示条件和内容读取 `../04-patterns/page-notice.md`。

## 5. 未保存保护

所有可编辑表单都应保护未保存修改。

- 点击取消、关闭、返回并退出当前表单、切换平台菜单或页头 Tab、跳转其他页面以及关闭当前页面时，存在未保存修改则提示用户确认。
- Stepper 步骤切换、递进流程内部返回和单面表单内的分区定位属于表单内部导航；状态能够保留时不提示离开确认。
- 内部切换会清空、覆盖或使已有配置失效时，先说明影响并提示用户确认。
- 保存失败时保留用户输入和当前流程位置。
- 具体确认方式和按钮语义由 Theme 与 Form Pattern 确定。

## 6. Common Design 映射

映射只用于连接 `prd-design-code` 和 Common Design，不改变 AES 结论。

| AES 结构 | Common 基础 `templateId` | AES 补充信息 |
| --- | --- | --- |
| Page + Single-surface | `page-form-config` | 使用入口关系区分 Stable/Drilldown |
| Page + Stepper | `page-form-stepper` | 步骤导航按 AES 契约 |
| Page + Progressive | `page-form-config` | 增加 Progressive 变体 |
| Modal + Single-surface | `page-form-modal` | 无 |
| Modal + Progressive/Stepper | `page-form-modal` | 增加对应流程变体 |
| Drawer + Single-surface | `page-form-drawer` | 无 |
| Drawer + Progressive/Stepper | `page-form-drawer` | 增加对应流程变体 |

Common Design 没有对应组合时，使用最接近的容器模板作为基础，并通过 AES 变体补充，不得丢失流程结构。

## 7. 输出契约

```yaml
template_contract:
  template_type: form
  form_container: page | modal | drawer
  entry_mode: stable | drilldown | contextual
  flow_structure: single-surface | progressive | stepper
  entry_source: ""
  back_target: ""
  flow_levels: []
  step_contract:
    steps: []
    navigation_mode: not-applicable | sequential | validated-direct
    step_access_rule: ""
    final_submit_step: ""
  section_navigation: none | anchor
  page_regions: []
  region_order: []
  noticeRegion: page-notice | none
  business_sections: []
  operation_region: page-operation-region | modal-footer | drawer-footer
  unsaved_protection:
    protected_exits: []
    internal_navigation_behavior: preserve | confirm-before-discard
  template_mapping:
    common_template_id: ""
    aes_variant: ""
  pattern_requirements:
    - form-management
  feature_requirements: []
  reference_evidence: []
  pending_confirmations: []
  regression_scope: []
  template_gaps: []
```

未使用 Progressive 时 `flow_levels` 为空；未使用 Stepper 时 `step_contract.steps` 为空。

## 8. 准出条件

- 已分别确定容器、入口和流程结构。
- 未按字段数量直接决定容器或 Stepper。
- Progressive 的层级、替换、返回和分支状态关系明确。
- Stepper 的步骤目标、顺序、导航方式和访问范围明确。
- 线框图只被用于理解结构，没有被直接复制为业务方案。
- 保存、取消、返回和确认语义均来自 Theme。
- 未在 Template 内决定字段控件、高级设置、标题样式或具体实现。
- 已声明需要保护的退出入口，并交给 Form Pattern 处理。
- 已映射 Common 基础模板且完整保留 AES 差异。
