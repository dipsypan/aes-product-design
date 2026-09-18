# AES 批量导入弹窗组件

> `Coverage: override`
> **归属：AES Product Design。** 本 Reference 是 AES（深信服下一代端点安全）产线专属组件映射，不作为 Common Design 的通用组件规范。导入流程、结果口径与异常规则由 [`../05-features/import.md`](../05-features/import.md) 决定。

## 使用条件

- 上游已确定采用 AES 表格导入 Feature。
- 当前业务能够提供导入业务标识及对应接口能力。

## 不适用与禁止事项

- 不用于资产身份信息导入等被 `import` Feature 明确排除的独立流程。
- 不因组件存在而跳过业务字段、冲突策略、权限和结果口径设计。

## Component 身份

- `componentId: BatchImportModal`
- `encapsulation: true`
- 来源：`AES__APP_LIB/Impex`
- 真实实现：`app/app-lib/src/business-comp/impex/modals/BatchImportModal.vue`

## 复用契约

- 组件负责导入配置弹窗及其已有的进度、结果和失败反馈承载。
- 当前业务负责提供业务标识，并执行 `import` Feature 中的模板、校验、冲突策略、数量口径和列表刷新要求。
- 编码阶段核验目标分支中的真实导出名、Props、Events、最大文件限制和任务接口；封装不足时按 Feature 补充。
