# AES 页面提示条（IxAlert Banner）

> `Coverage: extend`
>
> **归属：AES Product Design。** 本 Reference 是 AES 页面提示条的唯一设计与组件映射入口，不作为 Common Design 的通用组件规范。本文合并原 `page-notice` Pattern 的展示决策、布局契约与 `IxAlert` 复用规则；`page-notice` 仅作为设计能力和 `noticeRegion` 标识，真实 `componentId` 固定为 `IxAlert`。

## 使用边界

- 页面存在业务效果、影响范围、容量限制、授权状态或其他需要持续提醒用户的信息时读取本 Reference。
- 本能力可用于列表、详情、策略、任务和规则等页面，不限定于表格页面。
- Template 只负责提供 `noticeRegion` 及其页面位置；Theme 或用户可以锁定是否展示及业务内容，锁定后本文只负责执行内容结构和交互；上游未指定时才判断是否展示。

## 不适用与禁止事项

- 不得用页面提示条替代字段校验、操作结果反馈或局部帮助。
- 不得因页面需要装饰或视觉分隔而增加提示条。
- 不得把 `page-notice` 当作组件 ID，也不得另造同义的 AES 业务组件；编码入口统一使用 `IxAlert` 的 banner 形态。

## 展示与布局规则

- 上游锁定 `visible=true` 时必须展示，锁定 `visible=false` 时不得展示；锁定结果与实现证据冲突时返回来源层，不得自行修改。
- 上游未指定 `visible` 时，存在明确业务说明则在页面主要内容上方展示；没有明确业务说明时不生成。
- 列表场景默认位于页签下方、主内容上方。
- 页面提示条分为 `text-only`（紧凑文本型）和 `rich-content`（富内容型）两种样式，默认使用 `text-only`。
- `text-only` 采用图标加左侧纯文本的紧凑布局；主说明、容量或数量上限等附加信息及详情入口按阅读顺序在同一左侧内容流中展示，不设置右侧独立信息区，也不得将附加信息右对齐。
- 仅当信息无法通过纯文本和详情入口有效承载，并且必须在提示条内额外展示示意图、表格等富内容时，才使用 `rich-content`；不得仅因文案较长、存在附加信息或存在详情入口而升级样式。
- `text-only` 复用对象白名单提示条的位置和尺寸：`margin: -8px -12px 8px`，高度保持 32px；`rich-content` 根据实际富内容扩展高度，不强制套用 32px 高度。
- `rich-content` 的文字说明仍从左侧开始，示意图、表格等内容按其阅读关系排布；富内容样式不等于把容量、上限或其他附加信息放到右侧。
- 同级页签的提示条边界和下方内容起点保持一致。
- 提示条不改变页面主容器、概览、左树、Footer 或刷新入口的位置。

## Component 身份

- `componentId: IxAlert`
- `presentation: banner`
- `encapsulation: true`
- 组件能力：页面级持续提示条

## 能力边界

- 组件提供：banner 承载、信息等级样式和通用交互。
- 业务提供：`visible`、等级、标题、说明、附加信息、操作入口、关闭权限和关联范围。
- Template 提供 `noticeRegion` 与区域顺序，不由组件改变页面骨架。
- 现有封装无法执行上游锁定内容或布局时，返回锁定来源层记录冲突；未锁定部分按本文契约补全，不再读取另一份 `page-notice` Reference。

## 输出契约

```yaml
notice_contract:
  pattern_id: page-notice
  componentId: IxAlert
  presentation: banner
  encapsulation: true
  content_mode: text-only | rich-content
  visible: true | false
  decision_source: user | theme | pattern
  decision_locked: true | false
  level: info | warning | error
  placement: below-page-tabs | above-content | inside-section
  title: ""
  description: ""
  supplementary_info: ""
  rich_content:
    enabled: false
    types: [] # illustration | table
  action:
    label: ""
    type: link | button | none
  dismissible: false
  related_scope: page | module | table | operation
  required_components: [IxAlert]
  reference_evidence: []
```

## 业务检查

- Theme 或用户锁定展示时直接执行；上游未指定时仅在有明确业务说明时展示。
- Theme 或用户已锁定提示条时未重新判断 `visible`，仅补全呈现和交互。
- 提示等级、文案、附加信息和详情入口与业务语义一致。
- 未明确要求在提示条内承载示意图、表格等富内容时，`content_mode` 为 `text-only`。
- 容量、数量上限等附加信息位于左侧内容流中，没有右对齐或拆成独立右侧区域。
- 使用 `rich-content` 时有明确的非纯文本内容和业务必要性，不因文案长度或详情入口单独触发。
- 提示条不会改变页面主要区域顺序或表格查询状态。
- 多个同级页面的提示条位置、边界和内容起点保持一致。
- 输出中的 `componentId` 为 `IxAlert`，并明确采用 banner 形态。
