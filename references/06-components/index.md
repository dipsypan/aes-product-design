# AES Component Index

> **归属：AES Product Design。** 本 Index 是 AES（深信服下一代端点安全）产线专属组件映射，不作为 Common Design 的通用组件索引。本 Index 登记的每一个组件能力均为 AES `override`，应直接采用对应 AES Component Reference；未登记的组件能力由 `prd-design-code` 调用 Common Design 或依据项目已有代码选择实现映射。

Component 是 Feature 和 Pattern 的具体实现载体。进入本层前必须已经确定页面框架、方案和单项能力。Theme、Pattern、Feature 或用户已锁定组件时，本层只验证真实可用性、补全引用方式和能力边界，不得替换组件；未锁定时才选择真实 AES 业务封装或其他实现映射。

## 组件清单

| 组件能力 | AES 实现 | 命中时读取 |
| --- | --- | --- |
| `asset-selector` | AES 资产选择能力 | [`asset-selector.md`](asset-selector.md) |
| `asset-card` | AES 现有 `AssetCard` 业务组件 | [`asset-card.md`](asset-card.md) |
| `advanced-filter` | 高级检索区域 | [`advanced-filter.md`](advanced-filter.md) |
| `quick-filter` | 快速筛选区域 | [`quick-filter.md`](quick-filter.md) |
| `input-number-range-tip` | AES 数字输入范围提示组合 | [`input-number-range-tip.md`](input-number-range-tip.md) |

## 使用规则

- 只有存在真实 AES 业务封装、稳定组件语义或明确复用基线时才建立 Component Reference。
- 小 i 提示等单项交互方案仍属于 Feature；数字范围提示已作为 AES `InputNumber` 的组件组合基准登记在本层。
- 没有 AES Component Reference 的组件能力，不属于本 Index 的覆盖范围；返回 `prd-design-code` 读取 Common Design 组件映射或当前项目已有代码，不得将未登记能力推断为 AES 专属组件。
- 上游已锁定但尚未登记为 AES Component Reference 的组件，可以使用 Common Design、组件库文档或项目代码验证；验证通过不等于将其登记为 AES 专属组件，验证失败必须返回锁定来源层。
- 不根据组件名称反向推导 Theme、Template、Pattern 或 Feature。
- Component Reference 负责组件用途、使用条件、能力边界和 AES 复用关系；具体实现遵循项目既有组件库。
