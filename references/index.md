# AES Product Design Reference Index

> **归属：AES Product Design。** 本 Index 是 AES（深信服下一代端点安全）产线专属设计规范的阶段入口索引，不作为 Common Design 的通用索引。本文明确规定 AES 侧的路由；阶段是否进入、合并或返回由主 `SKILL.md` 与 Common Design 联合决定。

本文件只提供阶段入口，不定义具体设计规则。由 `prd-design-code` 根据 `current_stage` 读取一行，不得递归加载全部 Reference。

| 顺序 | 层级 | 命中事项 | 读取入口 |
| --- | --- | --- | --- |
| 01 | Navigation | 菜单、页面入口、页头 Tab、首页和变更影响 | `01-navigation/navigation.md` |
| 02 | Theme | 业务对象、治理模型、生效链路和生命周期 | `02-themes/index.md` |
| 03 | Template | 页面类型、主容器、主要区域和区块顺序 | `03-templates/index.md` |
| 04 | Pattern | 区域级或复杂交互方案的选择与组合 | `04-patterns/index.md` |
| 05 | Feature | 已选定、可完整执行的单项方案 | `05-features/index.md` |
| 06 | Component | AES 真实业务组件和稳定实现映射 | `06-components/index.md` |
| 07 | Copy | 用户可见文案和 AES 专属术语 | `07-copywriting-terminology.md` |

正常顺序为 `Navigation → Theme → Template → Pattern → Feature → Component → Copy`。这是 AES 与 Common Design 联合编排的阶段顺序，不是 AES 单侧流程。Theme 不是必经层：由双方共同匹配主题；命中 AES Theme 时按 AES 规则处理，AES 未命中但命中 Common Design Theme 时采用通用主题，两侧都未命中时直接由 Template 拼装页面框架。其他层级同样允许由 AES、Common Design 或双方共同命中，也可以跳过；下层触发返回条件时回到双方共同结果中最早实际受影响的上层，不为补齐层级虚构 Theme。
