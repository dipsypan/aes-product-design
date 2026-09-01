# AES Template Index

> **归属：AES Product Design。** 本 Index 是 AES（深信服下一代端点安全）产线专属页面模板索引，不作为 Common Design 的通用模板索引。本文明确规定的 AES Template 优先；未覆盖事项由 `prd-design-code` 按 Coverage 调用 Common Design 补充。

Template 在 Theme 已确认业务对象、页面范围和业务不变量后读取；Theme 未命中时，也可直接接收需求与 Navigation 结果进行页面框架拼装。Theme 或用户已锁定页面类型、主容器、主要区域或顺序时，Template 只展开和验证锁定契约，不得重新决策；只有未锁定事项才由 Template 决定。区域内部方案交给 Pattern，单项完整能力交给 Feature，具体实现不得在本层决定。

当本索引存在与需求页面类型对应的 AES Template 时，先执行 AES Template 的页面级结论；Common Design 仅补充该 Template 未覆盖的通用事项。不得先采用 Common Design 的页面骨架，再把 AES 内容作为局部修补。

每个具体 Template Reference 的关系根据正文实际覆盖范围判定为 `extend` 或 `override`。正文未明确的局部事项不得按索引或文件名推断关系；应记录待确认，并只读取明确允许补充的 Common Design 事项。

| Template | 决策范围 | 命中时读取 |
| --- | --- | --- |
| `list` | 列表类型、概览区/左树/列表主区和主容器 | [`list.md`](list.md) |
| `form` | 表单容器、入口关系、单面/递进/步骤条结构、主要分区和操作区 | [`form.md`](form.md) |
| `detail` | 抽屉/下钻详情、概要区、正文组织和操作区 | [`detail.md`](detail.md) |

## 调用门禁

- Theme 已命中但未确认业务对象、页面目标或关键业务不变量时，返回 Theme；Theme 未命中时不因页面结构问题强制创建主题，直接在 Template 层补齐页面级契约。
- Theme 或用户锁定的 Template 契约无法执行时返回锁定来源层，不得在本层切换容器或页面类型。
- 一个需求包含多个页面时，每个页面分别生成 `template_contract`，不得用一个模板覆盖全部页面。
- Template 只输出 `pattern_requirements`、可直接执行的 `feature_requirements` 和待确认项，不展开组件实现细节。
- 需要改变菜单或页头 Tab 入口时返回 Navigation；需要改变业务模型时，由 `prd-design-code` 根据 AES 与 Common Design 是否存在受影响的 Theme 结论决定是否返回 Theme。

```yaml
template_contract:
  page_id: ""
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
