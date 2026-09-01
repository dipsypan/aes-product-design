# AES 表单管理 Pattern

> **归属：AES Product Design。** 本 Reference 是 AES（深信服下一代端点安全）产线专属 Pattern，不作为 Common Design 的通用表单规范。本文明确规定的 AES 表单方案优先；未覆盖事项由 `prd-design-code` 按 Coverage 调用 Common Design 补充。

## 定位

本 Pattern 在 `../03-templates/form.md` 已确定表单容器、入口关系、流程结构、业务分区和操作区后读取，负责字段组织、控件形态选择、依赖关系、状态反馈和提交保护。它不得改变表单主容器、递进层级、步骤结构或 Theme 的保存语义。

## 1. 输入

```yaml
form_pattern_input:
  form_container: page | modal | drawer
  entry_mode: stable | drilldown | contextual
  flow_structure: single-surface | progressive | stepper
  flow_levels: []
  step_contract: {}
  business_sections: []
  fields: []
  field_dependencies: []
  business_invariants: []
  interaction_contracts: []
  reference_evidence: []
```

字段语义、默认值、是否必填、权限和风险规则必须来自 Theme 或需求证据；本 Pattern 不推测业务事实。

## 2. 字段组织

- 同一分区使用单列 label 对齐；只有真实存量页面或强对照任务证明必要时使用双列。
- 最多使用两级业务标题，不创建三级标题。
- 一级标题使用 AES 存量页面的“蓝色竖条 + 加粗文字”；二级标题只加粗。样式值复用真实产品，不自行定义。
- 同一标题只显示一次；公共组件已经输出标题时直接复用。
- 有依赖关系的字段靠近放置，控制字段在前，被控制字段在后。
- 隐藏字段不占位；禁用字段保留位置并说明不可操作原因。
- 非核心、低频且不影响主流程理解的配置可以收敛到“高级设置”；高风险或影响生效范围的配置不得仅因低频而隐藏。

## 3. 控件形态决策

先按业务任务选择控件语义，再由 Common Design 和组件库补充通用 API：

| 场景 | AES 方案 |
| --- | --- |
| 互斥选项不超过 4 个 | Radio |
| 互斥选项超过 4 个 | Select；超过 8 个时支持搜索 |
| 独立多选项不超过 4 个 | Checkbox |
| 多选项超过 4 个 | 多选 Select |
| 所有选项都需要短解释和对比 | 单选/多选卡片 |
| 仅个别选项需要补充解释 | 调用 `../05-features/info-icon.md` |
| 功能总开关控制一组下属配置 | Switch |
| 策略或规则自身的启用/禁用状态 | Radio，文案使用“启用 / 禁用” |
| 单一参数是否生效且无下属配置 | Checkbox |
| 资产适用或执行范围 | 调用 `../05-features/asset-scope.md` |
| 有明确数值范围且输入时需持续知晓 | 调用 `../05-features/input-number-range-tip.md` |

当多个控件都合理且选择会显著影响任务效率时，记录决策依据；缺少关键输入时返回待确认，不按个人偏好选型。

## 4. 解释内容与卡片

- 单条短解释可跟随选项；长解释放在字段 label 下方或独立说明区。
- 卡片内容必须完整展示并允许自然换行，不使用固定高度截断、单行省略或 `line-clamp`。
- 同一选项组内卡片保持视觉等高，内容变化和国际化换行后仍需成立。
- 非纯文本字段展示必须克制；标签、图标、状态点和链接的选择继续读取 `field-display.md`。

## 5. 依赖与状态

- 控制项变化后立即更新被控制字段的显隐或可用状态。
- 被隐藏字段是否清空必须由 Theme 或接口语义决定；没有证据时不得自行清空。
- 加载、提交中、成功、失败、无权限和部分失败状态必须有明确反馈。
- 校验优先显示在字段附近；跨字段冲突同时说明冲突对象和修正方向。
- 提交失败时保留用户输入；成功后的关闭、返回或停留行为执行上游业务契约。
- 存在未保存修改时，取消、关闭或退出整个表单流程必须执行 dirty 保护。
- Stepper 步骤切换、递进流程内部返回和分区定位能够保留状态时，不触发离开确认；会清空、覆盖或使已有配置失效时，先提示用户确认。

## 6. 操作区

- 主操作只有一个，使用 Theme 确认的业务动词；次操作通常为取消或返回。
- Modal 使用弹窗底部操作区，Drawer 使用抽屉底部操作区，Page 使用页面操作区。
- 高风险提交需要确认时调用 `tiered-confirmation.md`，不得在本 Pattern 重写确认方案。
- 按钮和提示文案在业务语义确定后交给 `../07-copywriting-terminology.md` 校准。

## 7. 输出契约

```yaml
pattern_contract:
  pattern_id: form-management
  field_layout: single-column | evidence-based-two-column
  section_contracts: []
  field_presentations: []
  dependency_contracts: []
  validation_contracts: []
  state_contracts: []
  required_features: []
  required_components: []
  return_to_template: false
  return_reason: ""
  pattern_gaps: []
```

## 8. 准出条件

- 没有改变 Template 已确定的容器、递进层级、步骤和主要区域。
- 每个控件都有业务语义依据，未把全部字段装饰为非纯文本形式。
- 所需 Feature 与 Component 已显式列出，没有在 Pattern 中重写实现 API。
- 需要新页面结构时已返回 Template；需要新业务规则时已返回 Theme。
