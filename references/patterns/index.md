# AES 业务处理规则索引

本层保存 AES 相对公共设计 Skill 的业务处理差异。页面框架确定后按能力读取；规则未建成时沿用公共设计结果并记录缺口。

## 能力清单

依据《业务规范 SKILL 梳理》逐步建设：

| 能力 | 内容 | 当前处理 |
| --- | --- | --- |
| `confirmation` | 高危操作使用普通确认、输入确认或密码确认 | 待建立具体 Reference |
| `filtering` | 高级筛选、快速筛选、平铺筛选的 AES 差异 | 已由 `../templates/list.md` 覆盖的先执行模板 |
| `tag-usage` | 标签使用条件、样式和颜色 | 待建立具体 Reference |
| `hierarchy-ellipsis` | 路径、资产组等层级信息省略 | 待建立具体 Reference |
| `entity-display` | ATT&CK、实体及处置状态展示 | 待建立具体 Reference |
| `detail-entry` | 表格进入详情的链接或整行交互 | 已由 `../templates/list.md` 覆盖的先执行模板 |
| `batch-actions` | 不支持批量操作项和未勾选状态 | 已由 `../templates/list.md` 覆盖的先执行模板 |
| `required-mark` | 必填与不可取消已选项的标记 | 已由 `../templates/form.md` 覆盖的先执行模板 |
| `navigation-action` | 页面跳转入口的按钮样式 | 待建立具体 Reference |

## 路由规则

- 模板已完整定义且 AES 没有额外差异时，不重复建立细则。
- 新建具体 Reference 后在本表登记路径、命中条件和对公共规则的差异关系。
- 细则改变页面区域或容器时返回模板层；改变业务模型时返回主题层。
