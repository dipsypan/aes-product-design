# AES 业务设计 Reference 注册表

本文件只负责阶段路由。开始设计时完整读取；其余 Reference 按命中条件逐层读取，不得一次全部加载。

## 1. 基础上下文

| Reference | 读取时机 | 不负责 |
| --- | --- | --- |
| `product-context.md` | 每次 AES 设计开始时 | 页面框架、组件和文案命名 |
| `terminology.md` | 生成或校准页面文案时 | 需求理解、主题、框架和组件选型 |

## 2. 主题层

| 主题 | 命中信号 | 读取顺序 |
| --- | --- | --- |
| 规则管理 | IOC、白名单、匹配规则、条件规则、命中结果、有效期 | `themes/rule-management.md` |
| 策略管理 | 安全策略、防护配置、独立策略、优先级、分配对象 | `themes/policy-routing.md` → 命中的策略分支 |
| 任务中心 | 扫描、处置、分发、定时或周期任务 | 尚未建模；读取真实证据并返回缺口 |
| 病毒防护 | 病毒检测、病毒列表、病毒详情、处置 | 尚未建模；读取真实证据并返回缺口 |

策略分支：

- 复用已有安全策略：`themes/policy-management-existing.md`
- 全新独立策略：`themes/policy-management-new.md`

主题 Reference 返回 `design_capabilities` 后才进入页面框架层。

## 3. 页面框架层

| 能力 | AES Reference |
| --- | --- |
| `list`、`search`、`filter`、`sort` | `templates/list.md` |
| `form` | `templates/form.md` |
| `detail` | `templates/detail.md` |

同一需求涉及多个页面时可以读取多个模板，但每个模板都必须接收主题阶段的业务不变量和页面清单。

## 4. 细则与组件层

- 命中业务处理能力时读取 `patterns/index.md`，再按其中路由读取具体规则。
- 命中 AES 业务组件时读取 `components/index.md`，再按其中路由读取具体组件。
- AES 暂无具体 Reference 的能力继续沿用公共规则，并记录 `reference_gaps`；不得只凭目录项创造规则。

## 5. 文案阶段

仅当输出包含用户可见文案时读取 `terminology.md`。术语校准必须发生在业务语义、页面框架和操作含义已确定之后。

## 6. 验收层

`delivery_scope` 包含 `frontend` 时，完成代码修改后读取 `acceptance/frontend.md`。

## 7. 回退路由

```yaml
business_model_error: theme
page_structure_error: template
interaction_or_component_error: pattern-component
copy_or_term_error: copy
```

回退目标以上的已确认结论保持不变；目标阶段及其下游重新执行。

