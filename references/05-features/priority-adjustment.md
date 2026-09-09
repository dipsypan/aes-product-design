# AES 优先级调整 Feature

> `Coverage: override`

> **归属：AES Product Design。** 本 Reference 是 AES（深信服下一代端点安全）产线专属 Feature，不作为 Common Design 的通用能力规范。本文只定义具有业务优先级的策略或规则如何调整顺序；没有优先级语义的规则不得调用本 Feature。

## 使用条件

- 仅当业务对象存在明确的优先级，并且优先级会影响匹配或生效顺序时启用。
- 典型场景为安全策略列表；策略优先级数值越小，业务优先级越高。
- 规则匹配模型中所有命中的规则均生效时，不调用本 Feature。
- 内置策略、系统保留策略或其它不允许调整的对象必须禁用入口，并说明原因。

## Feature 身份

- `featureId: priority-adjustment`
- `encapsulation: true`
- 能力名称：优先级调整

## 实现绑定

- `componentId: PriorityAdjustModal`
- 来源：`AES__APP_LIB/PolicyCommon`

## 执行流程

```text
选择可调整对象
→ 打开优先级调整
→ 选择目标位置或调整方式
→ 确认
→ 保存并重新计算顺序
→ 刷新列表、详情和受影响的生效关系
```

## 业务规则

- 支持的调整方式以业务契约为准，例如“移动到”和“置顶”；不得自行增加未确认的排序方式。
- 保存后生成连续的业务优先级序号；不得向用户展示内部哨兵值或产生重复优先级。
- 调整后必须保持默认策略最低优先级等既有业务不变量。
- 请求失败时保留调整前顺序并明确反馈；成功后同步更新当前页面和关联页面的数据。
- 当前 Feature 不负责资产范围配置或资产适用检测；这两项能力分别执行 `asset-scope` 和 `asset-applicability-check`。

## 实现边界

- `PriorityAdjustModal` 负责弹窗承载、目标位置选择和通用交互；编码阶段必须核验实际导出名、路径、Props、Events 和数据提交方式。
- 业务页面负责传入可调整对象、当前顺序、权限、禁用原因和保存接口。
- 封装不足或业务行为超出组件能力时，按本 Feature 的业务规则补充实现，不得改变优先级语义。

## 输出契约

```yaml
feature_contract:
  feature_id: priority-adjustment
  enabled: true | false
  entity_type: strategy | rule
  priority_semantics: lower-value-higher-priority
  adjustment_modes: []
  selected_items: []
  protected_items: []
  permission: allowed | denied
  success_update: refresh-list-and-related-data
  failure_behavior: preserve-original-order
  required_components: [PriorityAdjustModal]
```
