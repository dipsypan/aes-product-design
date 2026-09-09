# AES Feature Index

> **归属：AES Product Design。** 本 Index 是 AES（深信服下一代端点安全）产线专属 Feature 索引，不作为 Common Design 的通用能力索引。每项 Feature 必须显式声明 `Coverage`；未命中 AES Feature 时，由 `prd-design-code` 处理通用能力。

Feature 是已经确定采用后可完整执行的单项方案。它可以包含入口、执行步骤、状态、校验、结果和异常分支，但不负责在多套设计方案之间做选择。需要选择或组合方案时返回 `../04-patterns/index.md`；具体实现映射到 `../06-components/index.md`。

每个 Feature Reference 只使用两个实现判断：`featureId` 用于与前端编码 skill 映射，`encapsulation: true | false` 用于表示是否存在可复用前端封装。封装未覆盖的部分仍由当前 Feature 补充实现；没有封装时按业务契约自行实现。

命中 AES Feature Reference 时，以该 Feature 为当前能力的唯一业务来源，不再读取 Common Design 同层 Feature；未命中时才由 `prd-design-code` 调用 Common Design 或其他通用能力。

## Feature 清单

| Feature | 完整能力 | 命中时读取 |
| --- | --- | --- |
| `asset-scope` | 选择适用/执行对象，计算并回显生效资产 | [`asset-scope.md`](asset-scope.md) |
| `asset-applicability-check` | 检索资产，展示适用策略/规则并标识实际生效项 | [`asset-applicability-check.md`](asset-applicability-check.md) |
| `priority-adjustment` | 调整具有优先级的策略或规则生效顺序 | [`priority-adjustment.md`](priority-adjustment.md) |
| `table-selection` | 单行勾选、表头全选、数量限制、计数和状态清理 | [`table-selection.md`](table-selection.md) |
| `import` | 下载模板、上传、校验、导入进度和结果 | [`import.md`](import.md) |
| `export` | 确定导出范围、确认、任务进度和下载结果 | [`export.md`](export.md) |
| `hierarchy-ellipsis` | 多级路径在空间不足时的省略与完整查看 | [`hierarchy-ellipsis.md`](hierarchy-ellipsis.md) |
| `link-navigation` | 当前页文字链和新标签页跳转 | [`link-navigation.md`](link-navigation.md) |
| `info-icon` | 小 i 信息提示的展示和交互 | [`info-icon.md`](info-icon.md) |
| `file-size-display` | 文件大小换算、精度、单位和异常值 | [`file-size-display.md`](file-size-display.md) |
| `contextual-remark-default` | 任务和规则跨模块快速新增时回填备注 | [`contextual-remark-default.md`](contextual-remark-default.md) |

## 使用门禁

- Theme、Pattern 或用户已指定 Feature 时，直接执行对应 Feature，不在 Feature 内重新选方案。
- 用户需求已明确指定单项能力时，可以由 Template 直接调用 Feature，不强制新增 Pattern。
- Feature 需要改变页面类型、主容器或页面区域时返回 Template 层。
- Feature 出现多套候选方案且需要根据场景选择时返回 Pattern 层，不在文件内扩张为决策编排器。
- 每个 Feature Reference 必须显式声明 `Coverage: inherit | extend | override`；未声明时记录 Coverage 缺失，不得自行推断。
- Feature 不重复定义组件实现；只声明所需组件语义或 AES 组件映射。
- 读取 Feature Reference 时，必须先判断使用条件和不适用场景，再决定是否启用 `featureId`。
- `featureId` 仅用于编码映射，不代表能力自动适用；没有 `featureId` 不阻断当前需求。
- `encapsulation: true` 时优先复用封装，未覆盖部分继续补充；`encapsulation: false` 时不得声称存在可复用前端封装。
