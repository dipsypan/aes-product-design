# AES 文字链 Feature

> **归属：AES Product Design。** 本 Reference 是 AES（深信服下一代端点安全）产线专属 Feature，不作为 Common Design 的通用能力规范。
> `Coverage: extend`
> 本文明确规定的 AES 能力规则优先；未覆盖事项由 `prd-design-code` 按 Coverage 调用 Common Design 补充。

## 1. 展示方式

根据点击后的打开方式判断：

| 点击结果 | 展示方式 |
| :--- | :--- |
| 当前页面打开抽屉、弹窗或展开内容 | 蓝色文字，不显示图标 |
| 跳转其他页面或业务模块 | 蓝色文字 + 右侧 `jumpz` 图标 |

## Feature 身份与封装

- `featureId: link-navigation`
- `encapsulation: false`
- 本 Feature 的完整跳转行为没有统一封装；文字链展示复用 `componentId: LinkText`，读取 [`../06-components/link-text.md`](../06-components/link-text.md)，路由和打开方式仍按本 Feature 契约实现。

## 2. 当前页面打开

- 当前页打开的文字链沿用 AES 既有链接样式。
- 文字使用平台标准链接蓝色。
- 不添加跳转图标、箭头或其他图标。
- 点击文字打开当前页面的抽屉、弹窗或展开内容。
- 当前页面上下文保持不变。

示例：

```text
查看详情
```

## 3. 新标签页跳转

- 新标签页跳转的文字链沿用 AES 既有链接样式和图标规则。
- 文字使用平台标准链接蓝色，右侧显示 `jumpz` 图标。
- 点击文字或图标打开新的浏览器标签页，当前页面保持不变。
- 内部平台页面使用 AES 平台跳转能力。
- 外部页面使用 `target="_blank"` 和 `rel="noopener noreferrer"`。

示例：

```text
文件隔离区 ↗
```

## 4. 调用约束

- 当前页打开：不显示图标。
- 新标签页跳转：显示右侧跳转图标。
- 不得使用普通文本加自定义样式替代 AES 封装组件。
- 非可点击文本不得使用链接蓝色。
- 文字过长时允许省略并通过 Tooltip 查看完整内容，跳转图标必须保持可见。

## 5. 业务要求

- 当前页打开的文字链为蓝色且无图标。
- 页面跳转文字链为蓝色且带右侧 `jumpz` 图标。
- 页面跳转打开新标签页，不覆盖当前页面。
- 文字和图标点击结果一致。
- 链接行为与 AES 既有模式保持一致。
