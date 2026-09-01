# AES 页面提示条 Pattern

> **归属：AES Product Design。** 本 Reference 是 AES 可复用的页面级提示条方案，不作为跨产线通用组件规范。页面是否预留提示区域由 Template 决定；Theme 或用户已锁定提示条时，本 Pattern 只负责执行内容结构和交互，不得重新判断是否展示；上游未指定时才由本 Pattern 判断。

## 使用边界

- 页面存在业务效果、影响范围、容量限制、授权状态或其他需要持续提醒用户的信息时，读取本 Pattern。
- 本 Pattern 可用于列表、详情、策略、任务和规则等页面，不限定于表格页面。
- Template 只负责提供 `noticeRegion` 位置。Theme 或用户可以锁定是否生成及业务内容；本 Pattern 对锁定内容只做呈现补全。上游未指定时，本 Pattern 才判断是否生成及内容结构。
- 具体 Alert / Banner 组件由 Component 层按项目既有能力承载。

## 展示规则

- 上游锁定 `visible=true` 时必须展示，锁定 `visible=false` 时不得展示；锁定结果与实现证据冲突时返回来源层，不得自行修改。
- 上游未指定 `visible` 时，存在明确业务说明则在页面主要内容上方展示；没有明确业务说明时不生成。
- 列表场景默认位于页签下方、主内容上方。
- 复用对象白名单提示条的位置和尺寸：`margin: -8px -12px 8px`，高度保持 32px。
- 主说明与详情入口在左侧单行展示，容量等附加信息右对齐，不得换行或掉到下一行。
- 同级页签的提示条边界和下方内容起点保持一致。
- 提示条不改变页面主容器、概览、左树、Footer 或刷新入口的位置。

## 输出契约

```yaml
notice_contract:
  visible: true | false
  decision_source: user | theme | pattern
  decision_locked: true | false
  level: info | warning | error
  placement: below-page-tabs | above-content | inside-section
  title: ""
  description: ""
  supplementary_info: ""
  action:
    label: ""
    type: link | button | none
  dismissible: false
  related_scope: page | module | table | operation
  reference_evidence: []
```

## 业务检查

- 提示条在 Theme 或用户锁定展示时直接执行；上游未指定时仅在有明确业务说明时展示。
- Theme 或用户已锁定提示条时未重新判断 `visible`，仅补全呈现和交互。
- 提示等级、文案、附加信息和详情入口与业务语义一致。
- 提示条不会改变页面主要区域顺序或表格查询状态。
- 多个同级页面的提示条位置、边界和内容起点保持一致。
