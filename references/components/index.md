# AES 业务组件索引

本层保存 AES 业务组件及其相对公共组件的差异。页面框架和业务处理含义确定后按需读取。

## 组件清单

依据《业务规范 SKILL 梳理》逐步建设：

| 能力 | AES 组件或参考 | 当前处理 |
| --- | --- | --- |
| `asset-selector` | AES 资产、资产组和范围选择 | 当前由命中主题和真实参考页定义，待独立 Reference |
| `search` | 高级筛选、快速筛选、平铺筛选 | 先执行 `../templates/list.md` |
| `asset-card` | 资产身份和状态概要 | 待独立 Reference |
| `import-export` | 模板、校验、失败明细和导出范围 | 待独立 Reference |
| `dynamic-tabs-panels` | 支持增减的多标签页或多面板 | 待独立 Reference |
| `info-icon` | 小 i 的颜色、位置和说明方式 | 待独立 Reference |

## 使用规则

- 组件 Reference 负责业务组件能力、状态、数据契约和 AES 差异，不重新决定主题与页面容器。
- 具体实现同时遵循公共组件规则和 SD Design / iDux API；使用 iDux 前必须查询项目版本对应组件。
- 没有 AES 差异时直接使用公共组件，不为填满目录创建重复规范。
- 组件能力不足以承载页面任务时返回模板层；组件暴露业务模型缺口时返回主题层。

