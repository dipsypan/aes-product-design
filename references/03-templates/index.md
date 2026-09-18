# AES Template Index

> **归属：AES Product Design。** 本 Index 是 AES（深信服下一代端点安全）产线专属页面模板索引，不作为 Common Design 的通用模板索引。本文明确规定的 AES Template 优先；未覆盖事项由 `prd-design-code` 按 Coverage 调用 Common Design 补充。

Template 在 Theme 已确认业务对象、页面范围和业务不变量后读取；Theme 未命中时，也可直接接收需求与 Navigation 结果进行页面框架拼装。Theme 或用户已锁定页面类型、主容器、主要区域或顺序时，Template 只展开和验证锁定契约，不得重新决策；只有未锁定事项才由 Template 决定。区域内部方案交给 Pattern，单项完整能力交给 Feature，具体实现不得在本层决定。

当本索引存在与需求页面类型对应的 AES Template 时，先执行 AES Template 的页面级结论；Common Design 仅补充该 Template 未覆盖的通用事项。不得先采用 Common Design 的页面骨架，再把 AES 内容作为局部修补。

每个具体 Template Reference 必须显式声明 `Coverage: inherit | extend | override`。不得根据正文、索引或文件名自行推断 Coverage；未声明时记录 Coverage 缺失。

| Template | 决策范围 | 命中时读取 |
| --- | --- | --- |
| `list` | 列表类型、概览区/左树/列表主区和主容器 | [`list.md`](list.md) |
| `form` | 表单容器、入口关系、单面/递进/步骤条结构、主要分区和操作区 | [`form.md`](form.md) |
| `detail` | 抽屉/下钻详情、概要区、正文组织和操作区 | [`detail.md`](detail.md) |

## AES 页面类型与模板编号

下表按阅读顺序登记页面类型、使用条件、模板编号和前端封装状态。先根据页面类型和使用条件完成页面设计，再填写 `templateId` 与 `encapsulation`；编号不参与结构选型，也不限制 AES 可设计的页面结构：

| 页面类型 | 使用条件 / 页面结构 | `templateId` | `encapsulation` | 设计 Reference |
| --- | --- | --- | --- | --- |
| 基础表格页 | 表格主区；不需要概览或稳定层级 | `page-table-basic` | `true` | [`list.md`](list.md) |
| 左树表格页 | 左树 + 表格主区；需要稳定层级切换 | `page-table-tree` | `true` | [`list.md`](list.md) |
| 概览表格页 | 概览区 + 表格主区；需要持续展示业务汇总 | `page-table-overview` | `true` | [`list.md`](list.md) |
| 概览左树表格页 | 概览区 + 左树 + 表格主区 | `page-table-overview-tree` | `true` | [`list.md`](list.md) |
| 弹窗列表页 | Modal 内临时查询或选择 | `page-list-modal` | `true` | [`list.md`](list.md) |
| 抽屉列表页 | Drawer 内保留父页上下文浏览或操作 | `page-list-drawer` | `true` | [`list.md`](list.md) |
| 页面级表单页 | Page + Stable/Drilldown + 单面或递进式结构 | `page-form-config` | `false` | [`form.md`](form.md) |
| 下钻步骤条配置页 | Page + Stable/Drilldown + Stepper；同一连续任务的多步骤配置 | `page-form-stepper` | `true` | [`form.md`](form.md) |
| 弹窗表单页 | Modal + 表单流程 | `page-form-modal` | `true` | [`form.md`](form.md) |
| 抽屉表单页 | Drawer + 表单流程；保留父页上下文 | `page-form-drawer` | `true` | [`form.md`](form.md) |
| 640px 无 Tab 抽屉详情页 | Drawer + Contextual + 640px + Sections | `drawer-detail-640` | `false` | [`detail.md`](detail.md) |
| 640px 带 Tab 抽屉详情页 | Drawer + Contextual + 640px + Tabs | `drawer-detail-640-tabs` | `false` | [`detail.md`](detail.md) |
| 960px 无 Tab 抽屉详情页 | Drawer + Contextual + 960px + Sections | `drawer-detail-960` | `false` | [`detail.md`](detail.md) |
| 960px 带 Tab 抽屉详情页 | Drawer + Contextual + 960px + Tabs | `drawer-detail-960-tabs` | `false` | [`detail.md`](detail.md) |
| 下钻详情页 | Page + Drilldown；独立路由的深度详情 | `page-detail-drilldown` | `false` | [`detail.md`](detail.md) |

- `templateId` 只标识页面模板；筛选、导入、状态、确认等能力继续由 Pattern / Feature 决定。
- `encapsulation: true` 时，表中 `templateId` 同时作为前端页面封装调用编号。
- `encapsulation: false` 时，表中 `templateId` 仍须输出，但编码按完整 Template 契约自行实现；不因没有封装而改名。
- 新增 `templateId` 必须以真实顶层容器为前缀：独立页面使用 `page-`，抽屉使用 `drawer-`，弹窗使用 `modal-`；后续变体按“任务—尺寸/结构”追加，禁止为 Drawer 或 Modal 新建 `page-` 前缀编号。
- `page-list-modal`、`page-list-drawer`、`page-form-modal`、`page-form-drawer` 是 Common Design 与前端已登记的存量编号，仅作为兼容例外保留；若未来升级命名，必须同步前端注册表和所有调用方，不得在本索引单方面改名。
- 四种抽屉详情页编号是待前端封装对齐的稳定目标；封装发布并核验对应入口后，须同步将本索引和 `detail.md` 中的 `encapsulation` 改为 `true`。Common Design 中既有的 `page-detail-drawer` 不作为第五种新模板，也不得作为新编号的命名样板。
- 没有既有 AES Template 可承载时返回 `templateId: custom`，并按完整 Template 契约实现；不得为了命中已有编号删减或改变页面结构。

## 调用门禁

- Theme 已命中但未确认业务对象、页面目标或关键业务不变量时，返回 Theme；Theme 未命中时不因页面结构问题强制创建主题，直接在 Template 层补齐页面级契约。
- Theme 或用户锁定的 Template 契约无法执行时返回锁定来源层，不得在本层切换容器或页面类型。
- 一个需求包含多个页面时，每个页面分别生成 `template_contract`，不得用一个模板覆盖全部页面。
- Template 只输出 `pattern_requirements`、可直接执行的 `feature_requirements` 和待确认项，不展开组件实现细节。
- 需要改变菜单或页头 Tab 入口时返回 Navigation；需要改变业务模型时，由 `prd-design-code` 根据 AES 与 Common Design 是否存在受影响的 Theme 结论决定是否返回 Theme。

```yaml
template_contract:
  page_id: ""
  templateId: ""
  encapsulation: true | false
  customReason: ""
  template_type: list | form | detail
  page_container: ""
  page_regions: []
  region_order: []
  noticeRegion: page-notice | none
  pattern_requirements: []
  feature_requirements: []
  return_to_stage: none | navigation | theme
  template_gaps: []
```
