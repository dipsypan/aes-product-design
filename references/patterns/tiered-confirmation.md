# AES 分级二次确认 Reference

## 调用契约

本 Reference 用于判断 AES 操作是否需要二次确认，并选择确认容器。

调用时先提取以下字段：

```yaml
operation:
  action: 操作按钮名称
  object_context: 操作对象上下文
  primary_confirmation_carrier_type: none | task-form | preview-page | config-review | other
```

字段取值规则：

- `action`：直接取用户点击的操作按钮名称，例如“删除”“禁用”“隔离文件”“隔离资产”。
- `object_context`：从页面标题、列表对象、详情对象或表单标题识别出来的操作对象上下文，例如“策略”“任务计划”“文件”“资产”“客户端”。
- `primary_confirmation_carrier_type`：操作前是否已经存在一次明确的业务确认承载；没有则填 `none`，有则按承载类型填写。

证据不足时补充：

```yaml
reference_evidence: 真实产品页面、项目代码或接口证据
```

本 Reference 返回：

- 是否触发二次确认
- 确认等级
- 确认容器
- 前端验收条件

本 Reference 不重新判断：

- 操作是否有权限执行
- 操作是否应该存在
- 操作按钮的位置和样式
- 操作执行接口和请求字段
- 操作成功、失败或部分成功后的业务处理

## 使用边界

- 先由主题 Reference 和页面框架确定业务对象、操作语义和页面入口，再调用本 Reference。
- 本 Reference 只处理确认层级和确认容器，不新增业务操作，不改变业务对象和生命周期。
- 一次明确的业务确认承载已经存在时，默认不再追加二次确认；是否足够覆盖本次操作由判断流程决定。
- `typed-confirm` 是闭集规则，只能来自本 Reference 已列明类别或已登记的确认承载例外，不得因泛泛判断“后果严重”自行新增。
- 真实产品已有明确确认方式时，优先保留已确认的产品规则。
- 用户本次明确指定的确认方式优先于本 Reference 的通用判断。

## 确认等级

```yaml
confirmation_level:
  none: 不触发二次确认
  click-confirm: 点击确认按钮即可完成二次确认
  typed-confirm: 输入“确认”后才能完成二次确认
```

### `none`

不改变业务数据、业务状态或安全状态。

### `click-confirm`

风险可控、影响范围明确，或产品已经将该操作定义为普通确认。

当前明确规则：

```yaml
- action: delete
  confirmation_level: click-confirm
  scope: 所有删除操作
  examples:
    - 删除策略
    - 删除任务计划

- action: toggle-status
  confirmation_level: click-confirm
  scope: 普通状态切换类操作
  examples:
    - 策略：启用和禁用切换
    - 病毒标记状态:未处置和已处置切换
```

### `typed-confirm`

只适用于本 Reference 已列明的高风险类别。不得开放式扩展。

## 判断流程

```text
操作是否改变状态或数据？
├─ 否 → none
└─ 是
   ├─ 已有明确业务规则 → 使用已有规则
   └─ 无明确规则
      ├─ 是否已有一次足够明确的业务确认承载？
      │  ├─ 是
      │  │  ├─ 该承载是否属于高风险操作类别且命中数量阈值？
      │  │  │  ├─ 是 → typed-confirm
      │  │  │  └─ 否 → none
      │  └─ 否 → 按风险判断：click-confirm / typed-confirm
      └─ 进入高风险类别判断
```

## 高风险操作类别

命中以下特质时，使用 `typed-confirm`。未命中时不得自行新增高风险类别。

### 1. 关闭或削弱安全防护

```yaml
- example: 禁用客户端、卸载客户端
- reason: 关闭后基本失去安全防护效果
```

### 2. 造成重大终端可用性影响

```yaml
- example: 隔离资产
- reason: 会阻断目标资产所有入站和出站网络访问，可能造成设备失联和业务中断
```

## 业务确认承载

有些操作在最终确认前已经存在一次明确的业务确认承载，例如任务创建表单、操作预览页、配置复核页。该承载如果已经覆盖操作对象、动作和后果，通常不再追加二次确认。

默认不追加二次确认：

```yaml
- action: 任务表单已足够确认的 Agent 处置类操作
  example: 结束进程、隔离文件、重启客户端
```

即使已经存在确认承载，仍需追加输入“确认”：

```yaml
- action: 造成重大终端可用性影响的承载
  example: 隔离资产
  reason: 会阻断目标资产所有入站和出站网络访问，可能造成设备业务中断

```

新的确认承载即使看起来风险较高，也不得直接追加输入“确认”；应返回待确认问题，由业务设计确认后再加入本列表。


## 数量阈值

命中以下数量阈值时，使用 `typed-confirm`。阈值按最终操作对象数量判断；需求没有特殊说明数量时，按 1 个操作对象判断；数量无法从需求、页面或业务上下文确定时返回待确认，不自行扩大数量。

```yaml
- action: 隔离资产、禁用客户端、卸载客户端
  object: 所选资产数量
  threshold: ">= 1"
  confirmation_level: typed-confirm
  reason: 任意目标被隔离、禁用或卸载，都会影响目标终端的网络可用性或客户端防护能力

- action: 加入白名单
  object: 规则白名单的生效资产
  threshold: ">= 5"
  confirmation_level: typed-confirm
  reason: 规则白名单可绕过对应安全检测，生效资产达到 5 台及以上时扩大安全绕过范围
```


## 确认容器

```yaml
confirmation_container:
  bubble-confirm: 小范围、低干扰、上下文内确认
  dialog-confirm: 常规确认和高风险确认
```

### `bubble-confirm`

用于低风险、轻量级、上下文内即可完成判断的 `click-confirm`。不得用于 `typed-confirm` 或高风险操作。

- 所有 `导出` 按钮的确认
- 当前页面已不存在的客户端下载页配置 `开启` 和 `关闭` 确认

### `dialog-confirm`

除上述场景外，所有需要二次确认的操作默认使用 `dialog-confirm`。

## 输出契约

```yaml
confirmation_contract:
  confirmation_required: true | false
  confirmation_level: none | click-confirm | typed-confirm
  confirmation_container: bubble-confirm | dialog-confirm | not-applicable
  action: 操作按钮名称
  object_context: 操作对象上下文
  primary_confirmation_carrier_type: none | task-form | preview-page | config-review | other
  reference_evidence: []
  acceptance_checks: []
```

## 验收条件

- 删除策略、删除任务计划等删除操作触发普通点击确认。
- 隔离文件、结束进程、重启客户端通过任务创建表单确认后，不再追加二次确认。
- 隔离资产即使已经通过任务创建表单确认，仍追加输入“确认”的高风险确认。
- 禁用客户端、卸载客户端数量大于等于 1 时，追加输入“确认”。
- 规则白名单的生效资产大于等于 5 台时，追加输入“确认”；小于 5 台时无需二次确认。
- 黑名单规则页的导出确认和客户端下载页配置的关闭确认使用气泡确认。
- 其余确认场景使用弹窗确认。
- 真实产品已有确认规则时，页面实现与该规则保持一致。
