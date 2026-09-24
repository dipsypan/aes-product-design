# AES 列表页模板

> **归属：AES Product Design。** 本 Reference 是 AES（深信服下一代端点安全）产线专属列表模板差异规范，不作为跨产线通用规范。标准页面名称和 `templateId` 复用 Common Design；本文补充 AES 的容器决策、页面壳层、页面级操作位置和布局基线。未明确覆盖的事项由 `prd-design-code` 继续采用 Common Design。
> `Coverage: extend`

## 1. 定位与 Common Design 关系

本 Template 在 Theme 已确定页面目标后读取，通过页面级决策链确定列表角色、主容器、标准模板、主要区域和区块顺序。表格内部的筛选接入、工具栏、批量操作、勾选、导入导出、分页和局部状态继续读取 `../04-patterns/table-management.md`；页面整体状态仍由本 Template 负责，真实组件与代码映射继续读取 `../06-components/index.md`。

| 决策事项 | 与 Common Design 的关系 | 执行方式 |
| --- | --- | --- |
| 中文页面类型和 `templateId` | 一致，直接复用 | 使用 Common Design 注册的六种列表模板，不创建 AES 别名 |
| 概览、左树和列表主区的语义 | 一致，直接复用 | 按 Common Design 的标准区域组合 |
| 独立页面、Modal、Drawer 选型 | 补充决策标准 | 由本文先判断列表角色和上下文关系，不以数据条数直接决定 |
| AES 导航与页面头部 | 产品差异 | 不使用 L 型导航；独立页面头部由 AES 产品壳层承载 |
| 刷新位置 | 产品差异 | 独立主列表放页面右上角；容器内列表按需局部刷新或不展示 |
| 页面间距与内容容器 | 产品差异 | 执行本文第 5 节，不套用 Common Design 的固定像素线框 |
| 表格内部交互 | 不属于 Template | 交给 Table Management Pattern 和命中的 Feature |
| 真实组件与实现 | 不属于 Template | Component 层优先匹配 AES 稳定业务封装 |

只覆盖本文明确列出的 AES 差异；其他 Common 规则继续有效，不得将局部差异扩大为对 Common 列表模板的整体替换。

执行顺序固定为：先确定页面类型、列表角色、容器、区域和任务模式；再核对该类型的前端封装状态；随后按封装状态使用前端封装或视觉与业务参照；最后填写 `templateId` 和 `encapsulation`。视觉参照不得替代前端封装核验。

## 2. 列表模板决策链

### 2.1 第一步：判断列表角色与容器

父级页面或业务流程已经明确容器时，继承该结果并校验是否符合下表；未明确时，由当前 List Template 完成容器选型。

| `listRole` | `containerType` | 使用条件 | 不应使用的理由 |
| --- | --- | --- | --- |
| `primary` | `full-page` | 稳定入口或独立高频任务；需要路由定位、持续操作或保留查询状态 | 当前数据暂时较少 |
| `auxiliary` | `modal` | 当前流程中的短任务；临时查询或选择；完成后立即返回原流程 | 只因为数据少于某个数量 |
| `auxiliary` | `drawer` | 需要保留父页面上下文，并持续浏览、筛选或操作一组关联数据 | 只因为数据多于某个数量 |

决策顺序：

1. 菜单或页头 Tab 对应的稳定列表任务使用 `full-page`。
2. 没有稳定入口，但任务需要路由定位、长期停留、深层操作或跨页面返回时，仍应升级为 `full-page`。
3. 当前流程中的临时查询或选择，任务短且关闭后立即回到原流程时使用 `modal`。
4. 需要保留父页面上下文，同时承载较完整的筛选、浏览或行操作时使用 `drawer`。
5. 数据量只用于评估分页、搜索和性能，不作为 Modal 与 Drawer 的单一分界；不得使用“少于 20 条必选 Modal、超过 20 条必选 Drawer”的机械规则。

### 2.2 第二步：确定页面区域组合

#### 独立主列表

`containerType=full-page` 时，根据页面区域选择以下标准模板：

| 页面结构 | 区域组合 | 使用条件 |
| --- | --- | --- |
| 基础表格页 | 表格主区 | 不需要持续展示概览或稳定层级 |
| 左树表格页 | 左树 + 表格主区 | 需要按组织、分组、资产等稳定层级切换数据范围 |
| 概览表格页 | 概览区 + 表格主区 | 需要先判断持续展示的业务汇总，再查看明细 |
| 概览左树表格页 | 概览区 + 左树 + 表格主区 | 同时需要业务汇总和稳定层级范围 |

1. 用户、Theme 或当前真实页面已明确模板时直接采用。
2. 存在必须持续展示且能辅助当前任务判断的业务汇总时增加概览区。
3. 存在稳定业务层级，并且用户需要频繁按层级切换范围时增加左树。
4. 同时满足前两项时使用概览左树表格页；均不满足时使用基础表格页。
5. 字段较多、筛选较多或希望页面更丰富，均不能作为增加概览区或左树的理由。

#### 容器内辅助列表

| 页面结构 | 固定容器 |
| --- | --- |
| 弹窗列表页 | `modal` |
| 抽屉列表页 | `drawer` |

- Modal、Drawer 不再组合概览或左树形成新的 `templateId`；确需增加特殊区域时，在标准模板上记录 `optionalRegions` 和依据。
- 特殊区域改变了主要任务、主容器或标准区域顺序时，不得继续伪装成标准模板，应重新判断是否升级为独立页面。
- 列表进入详情、编辑或其他模块时只记录去向，目标容器由对应 Detail 或 Form Template 决定。

### 2.3 第三步：确定任务模式

容器确定后，继续输出列表承担的任务模式。该模式只决定模板区域、Footer 和下游能力要求，不在本层展开勾选或批量操作细节。

| `interactionMode` | 用户任务 | `selectionCommitMode` | `footerMode` |
| --- | --- | --- | --- |
| `browse` | 查看、筛选并进入详情 | `not-applicable` | `none`；平台要求时可为 `close` |
| `select` | 选择一项或多项返回原流程 | `immediate` | `none` |
| `select` | 选择一项或多项后统一提交 | `confirm` | `confirm-cancel` |
| `manage` | 在列表中新增、编辑、删除或批量操作 | `not-applicable` | `none`；平台要求时可为 `close` |

- Modal、Drawer 始终保留右上角关闭入口；Footer 不是关闭容器的唯一方式。
- `confirm-cancel` 的确定按钮必须依赖有效选择结果；取消不提交本次选择。
- `immediate` 只用于用户点击对象即可完成选择的短流程；多选默认使用 `confirm`。
- 勾选状态、数量限制和跨页选择继续读取 Table Selection Feature；Template 不重复定义。

### 2.4 第四步：页面类型、templateId 与封装状态

完成列表角色、容器、区域组合、任务模式和视觉业务参照核对后再执行本节。`templateId` 和 `encapsulation` 是页面设计结果，不参与列表结构选型；即使本节在文档中位于视觉证据之前，也不得跳过前端封装状态核验。

| 页面类型 | 已确认结构 | `templateId` | `encapsulation` |
| --- | --- | --- | --- |
| 基础表格页 | 表格主区 | `page-table-basic` | `true` |
| 左树表格页 | 左树 + 表格主区 | `page-table-tree` | `true` |
| 概览表格页 | 概览区 + 表格主区 | `page-table-overview` | `true` |
| 概览左树表格页 | 概览区 + 左树 + 表格主区 | `page-table-overview-tree` | `true` |
| 弹窗列表页 | Modal + 列表主区 | `page-list-modal` | `true` |
| 抽屉列表页 | Drawer + 列表主区 | `page-list-drawer` | `true` |
| 自定义页面类型 | 没有既有 AES Template 可承载的列表结构 | `custom` | `false` |

- `encapsulation: true` 时优先复用页面骨架，未覆盖的列表区域和内部能力继续按本 Template 及下游契约补充。
- `encapsulation: false` 时仍完整输出列表结构，不得为了获得前端封装删减概览、层级、容器或任务模式。

## 3. 页面骨架

### 3.1 页面级区域职责

列表 Template 负责页面级结构，Pattern 不得重新决定以下内容：

| 页面级内容 | Template 职责 |
| --- | --- |
| 页面头部与页面标题 | 决定标题、返回入口和页面级操作位置 |
| 概览区 | 决定是否存在、展示哪些业务汇总、展开和收起位置 |
| 左树 | 决定是否存在、范围语义、节点切换和区域顺序 |
| 顶部提示条 | 预留页面级提示区域及其位置；是否展示、内容和 `IxAlert` banner 复用由 [`page-notice`](../06-components/page-notice.md) 决定 |
| Footer | 决定关闭、取消、确认等容器级操作 |
| 刷新入口 | 决定页面右上角刷新或容器内局部刷新 |
| 页面状态 | 决定页面整体的加载、空数据、失败和无权限状态 |

Template 输出上述区域及顺序；Table Management Pattern 只处理列表主区内部的筛选接入、工具栏、表格、分页和查询结果状态。

### 3.2 页面级状态与列表状态

- 页面级加载、空状态、异常状态和权限状态由 Template 统一定义。
- 表格查询结果的加载、无结果和请求失败由 Table Management Pattern 补充。
- Pattern 不得因为筛选、勾选或批量操作改变页面容器、概览、左树、Footer 或刷新位置。

### 3.3 AES 独立主列表

```text
AES 产品壳层
├── 左侧导航
└── 页面区
    ├── 页面头部：页面标题                         页面级操作 / 刷新
    └── 页面内容
        ├── 概览区（按 templateId 可选）
        └── 工作区
            ├── 左树（按 templateId 可选）
            └── 列表主区：筛选 / 操作 / 表格 / 分页 / 页面状态
```

- 页面标题、返回入口和页头高度由 AES 产品壳层负责，页面正文不得重复生成 `IxHeader`。
- 页面级时间范围、概览显隐、自动刷新和手动刷新按业务需要进入页头操作区；只作用于表格的筛选留在列表主区。
- 独立主列表的手动刷新固定在页面头部右上角，页面内只保留一个刷新入口。
- 概览只展示 Theme 或 Pattern 已确认的业务指标；左树只用于稳定范围切换，不代替普通筛选。
- 页面存在业务提示时，Template 预留 `noticeRegion`；提示条的展示条件、内容和 `IxAlert` banner 复用读取 `../06-components/page-notice.md`。

### 3.4 Modal、Drawer 辅助列表

```text
Modal / Drawer
├── 容器标题                                      关闭 ×
├── 列表主区：筛选 / 操作 / 表格 / 分页 / 局部状态
└── Footer（按 interactionMode 与提交方式决定）
```

- 不继承独立主列表的产品页头、全局导航和页面右上角刷新。
- 数据在容器打开期间可能持续变化且用户需要主动同步时，允许在列表查询区末尾提供一个局部刷新；否则不展示刷新。
- 不生成“页面刷新 + 容器局部刷新”两个入口。
- Drawer 是否展示对象上下文由触发对象和任务目标决定；没有明确父对象时不得生成空的对象概要区。

## 4. Common Footer 兼容门禁

Common Design 正文与当前 Template Registry 对 `page-list-modal`、`page-list-drawer` 的 Footer 定义不一致。输出前必须以 `prd-design-code` 实际使用的 Template Registry 为校验基线，同时保留真实任务语义：

- `footerMode=confirm-cancel` 时直接使用标准 `templateId` 和注册表 Footer。
- `footerMode=none` 或 `close` 与注册表不一致时，只有页面结构本身没有既有 AES Template 可承载时才使用 `templateId: custom`，并在 `override.affectedRules` 记录 `footer-contract`。
- 不得为了通过校验给只读浏览或即时选择流程增加无意义的“确定 / 取消”。
- Common Design 与 `prd-design-code` 注册表统一支持可变 Footer 后，应取消上述临时 `custom` 兼容方式，恢复标准 `templateId`。

## 5. AES 布局与刷新基线

- Common Design 的 `left-shaped` 仅用于表达导航类型；AES 不使用 `l-shaped` 布局。
- 独立主列表内容与产品壳层页头之间使用当前产品的 `8px` 基础间隔，不在业务页面内重复计算页头高度。
- 标准白色列表主区以 `8px 16px 0` 作为当前实现基线，圆角为 `2px`；同类存量页面已有稳定容器时优先复用，不叠加外层卡片。
- 概览区与下方工作区使用 `8px` 基础间隔；概览高度由指标内容决定，不采用 Common Design 线框中的固定 `166px`。
- 左树与表格主区处于同一工作区并共同占满可用高度；树宽、折叠方式和内部间距交给下游 Pattern 与真实组件映射，不在 Template 固定为 `240px`。
- 分页由列表容器承载并保持底部稳定，不在 Template 固定高度或重复添加分割线。
- 独立主列表刷新使用 `page-header-top-right`；Modal、Drawer 只使用 `local-toolbar` 或 `none`。
- 用户指定参考页面或同模块已有稳定实现不同时，记录 `referencePage` 和差异依据，不静默混用两套布局基线。

## 实现绑定

- `encapsulation: true` 时在编码阶段核验目标分支中模板的真实入口和参数，未覆盖的区域按本 Template 契约实现。
- `encapsulation: false` 时不得声称复用了页面模板，按本 Template 契约和项目组件实现。
- `templateId` 不改变筛选、导入、状态和确认等 Pattern / Feature 决策。

## 视觉与业务证据

本节用于页面还原和视觉校验，不改变前面的页面类型、容器、区域、任务模式、Footer 或刷新位置判断。

- `encapsulation: true` 时，先核验并优先使用前端页面封装；本节只用于校验封装效果、补充封装未覆盖区域和还原 AES 业务差异。
- `encapsulation: false` 时，前端没有可直接调用的页面封装，本节作为页面结构和视觉还原参考，结合当前 Template 契约自行实现。
- 参考页面不自动成为当前页面的字段、操作、筛选、状态或权限规则；这些内容仍由当前需求和上游设计契约决定。

以下路径均相对于前端工程 `/Users/sangfor/Documents/aes-mgr-front0830`。

### 独立主列表

| 模板结构 | 参考页面 | 关键源码 |
| --- | --- | --- |
| 基础表格页 | 安全事件列表 | `app/aes-incident/src/view/mod_sec_event/index.vue` |
| 表格主体 | 安全事件表格 | `app/aes-incident/src/view/mod_sec_event/event_table/index.vue` |
| 概览表格页 | 病毒查杀列表 | `app/aes-virus/src/view/virus_list/index.vue`、`app/aes-virus/src/view/virus_list/components/virus_statistics.vue`、`app/aes-virus/src/view/virus_list/components/virus_table.vue` |
| 概览左树表格页 | 终端列表 | `app/aes-agent/src/view/agent_list/index.vue` |
| 左树结构 | 终端分组树 | `app/aes-agent/src/view/agent_list/components/agent_list_tree.vue` |
| 表格与概览 | 终端列表主区 | `app/aes-agent/src/view/agent_list/components/agent_list_table.vue`、`app/aes-agent/src/view/agent_list/components/agent_list_table_banner.vue` |

当前工程未找到比终端列表更完整的独立“左树表格页”基准。设计不包含概览区的左树列表时，可以参考终端列表的左右区域组合，但不得照搬其概览 Banner。

### 容器内辅助列表

| 模板结构 | 参考页面 | 关键源码 |
| --- | --- | --- |
| Modal 列表 | 资产适用策略检测 | `app/app-lib/src/business-comp/policy_common/modal/check_policy_modal/src/index.vue` |
| Drawer 列表 | 策略关联资产 | `app/app-lib/src/business-comp/policy_assets_drawer/src/index.vue` |

### 公共表格容器

- 源码：`app/app-lib/src/business-comp/table_container/src/TableContainer.vue`
- 公开入口：`AES__APP_LIB/TableContainer`

参考现有页面时，只复用与目标 `templateId` 对应的页面结构、容器关系和区域组合。业务字段、操作、筛选条件和接口逻辑仍由当前需求决定。

## 6. 输出契约

```yaml
template_contract:
  templateId: page-table-basic | page-table-tree | page-table-overview | page-table-overview-tree | page-list-modal | page-list-drawer | custom
  encapsulation: true | false
  customReason: ""
  templateSource: Common Design 标准模板 + aes-product-design/references/03-templates/list.md
  navigationType: left-shaped | ""
  navigationTypeStatus: confirmed
  navigationTypeSource: aes-product-design
  navigationTypeNote: AES 独立主列表固定使用左侧导航；Modal、Drawer 留空
  listRole: primary | auxiliary
  containerType: full-page | modal | drawer
  interactionMode: browse | select | manage
  selectionCommitMode: immediate | confirm | not-applicable
  footerMode: none | close | confirm-cancel
  refreshPlacement: page-header-top-right | local-toolbar | none
  requiredRegions: []
  optionalRegions: []
  noticeRegion: page-notice | none
  regionOrder: []
  footerContract: {}
  componentContract: {}
  wireframeContract: {}
  override:
    enabled: true | false
    source: AES Product Design
    reason: ""
    affectedRules: []
  overviewRequired: true | false
  treeRequired: true | false
  patternRequirements:
    - table-management
  referencePage: ""
  templateGaps: []
```

约束：

- `primary + full-page` 使用四种 `page-table-*` 之一，`navigationType=left-shaped`，`refreshPlacement=page-header-top-right`。
- `auxiliary + modal` 使用 `page-list-modal`；`auxiliary + drawer` 使用 `page-list-drawer`；两者的 `navigationType` 留空。
- `full-page` 的 `footerMode` 固定为 `none`；Modal、Drawer 按 `interactionMode` 和 `selectionCommitMode` 决定 Footer。
- `templateId` 按第 2.4 节填写；无论是否封装都沿用该页面模板的稳定编号，`encapsulation: true` 时该编号同时与前端页面封装编号一致。
- 没有既有 AES Template 可承载时填写 `templateId: custom`、`encapsulation: false` 和 `customReason`；Footer 差异记录在 `override.affectedRules`。
- 标准模板的 `requiredRegions`、`regionOrder` 和默认 Footer 先继承 Template Registry；本文差异通过 `override` 明确记录。
- 独立主列表的 `override.affectedRules` 至少记录 `navigation-support`、`header-owner`、`refresh-placement` 和 `spacing-baseline`。
- `componentContract` 先继承注册表的区域要求，真实组件由 Component 层核对 AES 稳定业务封装后回填；不得把 Common 的底层组件推荐直接当作 AES 最终实现。

## 7. 准出条件

- 已先确定 `listRole` 和 `containerType`，再选择标准模板，没有把六种模板无条件平铺判断。
- 容器选择基于任务独立性、父页上下文和操作深度，没有按数据条数机械切换。
- 已明确 `interactionMode`、选择提交方式、Footer 和刷新位置，四者语义一致。
- 概览区与左树均有业务依据，没有为了丰富页面而添加。
- 独立主列表的页面头部由 AES 产品壳层承载，刷新位于页面右上角且页面内唯一。
- Modal、Drawer 没有错误套用独立主列表页头；Footer 与注册表冲突时已走兼容门禁。
- 已确定主要区域和顺序，但没有在本层重新决策筛选、勾选、批量操作或组件 API。
- 已将完整表格方案交给 `../04-patterns/table-management.md`。
