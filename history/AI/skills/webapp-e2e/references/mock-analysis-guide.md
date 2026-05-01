# Mock 分析深度指南：七步法 Step 4–7

> 本文件是 `SKILL.md` 步骤 3（Mock 分析）中七步法后半段的详细展开。
> 完成 Step 1–3（定位组件、识别 API、查找类型）后，按本文件执行 Step 4–7。

---

## Step 4: 追踪数据流

> 关键步骤：理解数据如何从 API 流向 UI

```bash
# 找到 API 响应后的数据转换
read_file <组件文件>
# 查找 .then()、.map()、filter() 等转换逻辑

# 追踪数据如何渲染到 UI
# 搜索响应字段在 JSX 中的使用
grep_code "{data\.xxx}|{item\.xxx}|product\.xxx"
```

**数据流追踪模式**:
```
API 响应路径: result.<dataField>.<nestedField>
              ↓ (数据转换/映射)
代码期望路径: transformedData.<mappedField>.<targetField>
              ↓ (渲染逻辑)
UI 组件: <Component data={transformedData} />
```

**关键点**: API 响应结构 ≠ 代码期望结构，必须追踪转换逻辑

---

## Step 5: 查找并复用已有 Mock 数据

> 先查模板库，再查项目源文件——避免重复构造

**模板库结构**（`tests/e2e/mock-templates/`）:

| 目录 | 内容 | 示例 |
|------|------|------|
| `user-states/` | 用户身份/权限状态，注入到全局变量 | `new-user-no-smax.json` |
| `api-mocks/` | API 端点 mock 响应，拦截网络请求 | `am-campaign-query-onepage-touchpoint.json` |

**查找优先级**:

1. **先检查模板库**：
   ```bash
   ls tests/e2e/mock-templates/user-states/ 2>/dev/null
   ls tests/e2e/mock-templates/api-mocks/ 2>/dev/null
   ```
   找到匹配模板后，按模板类型读取对应字段：
   - `user-states/` 模板 → 读取 `injectionPoints` 字段，按注入方式（全局变量 / localStorage）配置
   - `api-mocks/` 模板 → 读取 `mockData` 字段，按测试模式配置：
     - Playwright Python → `page.route()` 拦截对应端点
     - agent-browser CLI → `agent-browser network route "**/<endpoint>" --mock '<JSON>'`

   调整完成后跳到 Step 6。

2. **无匹配模板时，再查项目 mock 源文件**：
   ```bash
   # 查找 mock 相关目录
   find . -type d -name "*mock*" -o -name "*fixture*"

   # 查找测试数据文件
   glob "**/*{mock,fixture,test-data}*/*.{js,ts,json}"

   # 查找开发环境 mock 配置
   glob "**/dev/**/*.{js,ts,json}"
   ```

**常见 Mock 数据位置**（按项目类型）:
- **Monorepo**: `<shared-package>/mock*` 或 `<shared-package>/commonMockData`
- **单包项目**: `src/mock/`, `test/fixtures/`, `__mocks__/`

---

## Step 6: 查找条件渲染逻辑

> 识别数据字段如何影响 UI 显示

```bash
# 查找条件判断
grep_code "if.*data\.|data\.xxx &&|data\.xxx \?"

# 查找三元表达式
grep_code "{.*\?.*:.*}"
```

**字段-UI 映射示例**:
```
字段: isNewUser === true        → UI: 显示新用户引导界面
字段: itemList.length > 0      → UI: 显示推荐列表
字段: canSubmit === true        → UI: 启用提交按钮
```

**应对元素前，先确认它在默认 DOM 中是否可达**

> 对每个需要交互的目标元素，必须先回答：
> **它在组件的默认状态下是直接可见的，还是需要先触发某个状态切换？**

如果需要状态切换，必须读目标组件的 JSX 源码，明确：
1. **默认状态**是什么（哪些元素出现 / 隐藏）
2. **状态切换条件**（需要点击哪个元素？选择哪个选项？）
3. **切换后 DOM 的差异**（新出现哪些元素？消失哪些？）

```bash
# 快速检查常见状态变量模式
grep_code "useState.*false|isOpen|isExpanded|activeTab|selected" <目标组件文件>
# 找到后读取完整组件源码，确认初始状态和切换逻辑
read_file <目标组件文件>
```

---

## Step 7: 构造完整 Mock 数据

根据数据流分析结果，构造符合代码期望的 mock：

**构造前：对照 Playwright 交互可靠性规则排查潜在陷阱**

> 重点回顾 `patterns/mock-state-injection.md`（规则 4 全局变量注入、规则 7 Console 日志捕获、规则 8 数值字段类型、规则 9 持久化存储预填充）——这四条规则在静态分析阶段就能预判，不要等到运行时才暴露。

**构造交互代码前：检查项目本地交互说明**

> 类比 Step 5 查 mock-templates，写交互代码前先检查项目是否维护了本地交互说明目录。有则查阅再写代码；没有则跳过。

该目录如存在，包含本项目特有的组件库类名、覆盖层触发场景等上下文，是通用规则（`patterns/interaction-input.md`）的项目级补充。写 Select 交互、排查 iframe 问题、诊断 disabled 按钮时尤其有用。

**构造原则**:
1. ✅ 匹配代码期望的数据路径（而非 API 类型定义）
2. ✅ 满足条件渲染逻辑的字段值
3. ✅ 提供足够的数据量（如数组长度满足测试需求）
4. ✅ 使用项目已有的 mock 数据源

**常见陷阱**:
- ❌ 只参考 API 类型定义，忽略数据转换逻辑
- ❌ 数据结构与代码期望不匹配
- ❌ 缺少必需字段导致条件渲染失败
