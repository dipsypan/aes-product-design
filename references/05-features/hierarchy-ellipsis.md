# AES 多级路径省略 Feature

> **归属：AES Product Design。** 本 Reference 是 AES（深信服下一代端点安全）产线专属 Feature，不作为 Common Design 的通用能力规范。
> `Coverage: extend`
> 本文明确规定的 AES 能力规则优先；未覆盖事项由 `prd-design-code` 按 Coverage 调用 Common Design 补充。

## 1. 调用场景

当资产分组、组织架构、面包屑或文件路径因空间不足需要省略时，调用本规则。

| 路径类型 | 示例 |
| :--- | :--- |
| 资产分组/组织架构 | `研发部门/前端组/前端一组` |
| 页面面包屑 | `安全事件/安全事件详情` |
| 文件路径 | `C:\users\administrator\appdata\local\winlogon.exe` |

## Feature 身份与封装

- `featureId: hierarchy-ellipsis`
- `encapsulation: false`
- 当前没有映射到 AES 前端业务封装，按本 Feature 契约实现。

## 2. 通用规则

- 空间足够时完整展示，不主动省略。
- 空间不足时，先识别路径类型，再按照对应类型规定的省略优先级处理。
- 被省略的连续内容统一使用 `...` 表示。
- 保留原有分隔符，不将 `/` 和 `\` 相互替换。
- 内容发生省略时，悬浮必须通过 Tooltip 展示完整路径。
- 禁止仅按固定字符数截断，应根据容器实际可用宽度处理。

## 3. 资产分组、组织架构和面包屑

省略优先级为：

`中间层级 → 首级 → 最后一级`

处理规则：

1. 优先省略中间层级，首级和最后一级尽量保留。
2. 空间进一步缩小时，逐步减少保留的中间层级。
3. 仍无法容纳时，可以省略首级，只保留 `.../最后一级`。
4. 最后一级至少预留约 4 个字符的展示空间；极端情况下才截断最后一级。

示例：

```text
广东区/下级单位1/研发部门/前端组/前端一组
广东区/.../研发部门/前端组/前端一组
广东区/.../前端组/前端一组
广东区/.../前端一组
.../前端一组
.../前端...
```

实际使用面包屑组件时，隐藏层级应沿用组件已有的折叠交互；本规则只约束层级保留优先级。

## 4. 文件路径

文件路径根据页面是否已单独展示文件名选择省略方式。

### 4.1 已单独展示文件名

文件路径仅用于辅助定位，空间不足时保留路径开头，从末尾截断并追加 `...`。

```text
C:\users\administrator\appdata\local\winlogon.exe
C:\users\administrator\appdata\loca...
C:\users\administrator\appdata\...
```

### 4.2 未单独展示文件名

文件名是核心信息，应优先完整保留。空间不足时省略中间目录，尽量保留盘符和文件名。

```text
C:\users\administrator\appdata\local\winlogon.exe
C:\users\administrator\appdata\...\winlogon.exe
C:\users\administrator\...\winlogon.exe
C:\...\winlogon.exe
```

仅当空间不足以展示完整文件名时，才允许截断文件名：

```text
C:\...\winlogon...
```

## 5. 业务要求

- 空间足够时展示完整路径。
- 空间不足时按照对应路径类型的省略优先级处理。
- 连续省略内容只出现一个 `...`。
- 路径分隔符保持原样。
- 文件名独立展示与未独立展示时，采用了对应策略。
- 所有被省略的路径均可通过 Tooltip 查看完整内容。
