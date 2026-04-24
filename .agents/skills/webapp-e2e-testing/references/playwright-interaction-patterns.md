# Playwright 交互可靠性规则 — 索引

> **这些规则记录的是真实测试中遇到的边缘案例。它们不是默认脚本工作流程的一部分。如果一条规则对每一次测试都适用，它就属于 SKILL.md 模板，而不是这里。**
>
> 每条规则来自真实测试失败的经验总结，适用于所有 SPA + 组件库项目。
> 遇到具体问题时，按场景找到对应分类文件，查阅完整规则和代码示例。

---

## 规则速查表

| 规则 | 场景 | 核心结论 | 详细文件 |
|------|------|---------|------|
| **规则 1: 覆盖层存在性** | Drawer / Modal / Popover | 用 `.count() > 0` 或状态 CSS 类，不用 `is_visible()` | `patterns/selector-detection.md` |
| **规则 2: 容器文本匹配** | 表格行、设置项行 | 遍历行并匹配 label 子元素，不对容器用 `:has-text()` | `patterns/selector-detection.md` |
| **规则 3: 键盘副作用** | 关闭弹出层 vs 解除遮罩拦截 | 关闭弹出层点 Cancel/Close；解除遮罩背景拦截可用 Escape + `force=True` | `patterns/interaction-input.md` |
| **规则 4: 全局变量注入** | `add_init_script` 不生效 | 首选 `Object.defineProperty` 冻结属性；备选拦截 HTML 响应替换内联脚本 | `patterns/mock-state-injection.md` |
| **规则 5: 输入框类型过滤** | 弹出层内查找输入框 | 排除 `radio`/`checkbox`/`hidden`，按类型优先级依次尝试 | `patterns/interaction-input.md` |
| **规则 6: 文本选中与清空** | 清空并重新填写输入框 | 用 `click(click_count=3)` 代替不存在的 `triple_click()` | `patterns/interaction-input.md` |
| **规则 7: Console 日志捕获** | Mock 配置后页面仍异常 | setup 阶段注册 `page.on("console")` 捕获报错，配合截图诊断 | `patterns/mock-state-injection.md` |
| **规则 8: 数値字段类型** | Mock 配置后列表区域空白 | 货币/ROI 等格式化字段必须为字符串（`"4.80"`），不能是 number | `patterns/mock-state-injection.md` |
| **规则 9: 持久化存储预填充** | 应用进入「新用户」状态而非目标状态 | 在 `add_init_script` 中预填充 localStorage；不得在 goto 后 evaluate | `patterns/mock-state-injection.md` |
| ~~**规则 10: 滚动到目标元素**~~ | **已毕业到模板** | 已内置于 `take_screenshot_at_step()` step 2 | `patterns/selector-detection.md` |
| ~~**规则 11: 截图前清理覆盖层**~~ | **已毕业到模板** | 已内置于 `take_screenshot_at_step()` step 1 | `patterns/selector-detection.md` |
| **规则 12: 多实例相同选择器锁定** | 弹窗内多个同类名容器 | 从语义锄子（相邻 radio 文字、父容器唯一类名）定位目标，禁止用 `.first` / `querySelector` | `patterns/interaction-input.md` |
| **规则 13: iframe 指针事件拦截绕过** | 页面存在浮层 iframe 时 `.click()` 报错 | `dispatch_event('click')` 绕过命中检测；项目具体场景查阅项目本地交互说明目录 | `patterns/interaction-input.md` |
| **规则 14: Select 类下拉组件交互** | 任意 Select 组件库 | open-trigger → wait-menu → iterate-by-text；组件库类名查阅项目本地交互说明目录 | `patterns/interaction-input.md` |
| **规则 15: Confirm 按钮 disabled 诺断** | 表单填写完后按钮仍 disabled | 4 种根因 + 决策树（onChange 未触发、菜单未关、radio 索引错、校验未过） | `patterns/interaction-input.md` |

---

## 分类文件

| 文件 | 包含规则 | 适用场景 |
|------|---------|----------|
| `patterns/selector-detection.md` | 规则 1、2（Rules 10/11 已毕业） | 定位元素、判断存在性、文本匹配 |
| `patterns/interaction-input.md` | 规则 3、5、6、12、13、14、15 | 点击、键盘、填写表单、弹出层交互、iframe 绕过、下拉组件 |
| `patterns/mock-state-injection.md` | 规则 4、7、8、9 | 全局变量注入、mock 数据类型、失败诊断、持久化存储预填充 |

---

## 新增规则指引

**先过决策门，再决定是否写规则**：

```
问题：该行为是否在每次测试中都适用？
  → YES：直接修改 SKILL.md 模板，禁止在此写规则
  → NO：该行为是否由特定组件库或边缘场景触发？
         → YES：继续向下，写入 patterns/
         → NO：不需要记录

已有规则是否在 2+ 个独立测试中被触发？
  → YES：立即毕业进入 SKILL.md 模板，从速查表移除（文档可保留）
  → NO：保持在 patterns/ 中
```

将规则写入 `patterns/` 时遵循格式：
1. 判断属于哪个分类，将规则写入对应的 `patterns/` 文件
2. 格式：问题描述 → 根本原因 → ❌ 错误示例 → ✅ 正确示例 → 通用原则
3. 规则描述保持**项目无关**，不引用具体组件名称、业务字段名
4. 在本文件的速查表和 SKILL.md 的规则表中同步新增一行条目
