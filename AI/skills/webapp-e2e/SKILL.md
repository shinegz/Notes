---
name: nova-e2e-testing
description: "Comprehensive E2E testing for local web applications. Supports both agent-browser CLI (simple linear flows) and Playwright Python scripts (complex multi-step flows with API mocking, HTML interception, and programmatic control). Use this skill whenever you need to test flows on localhost, validate UI behavior, walk through multi-step scenarios, capture screenshots, or verify end-to-end functionality. Triggers on: test this web app, E2E test, UI test, browser test, 验证 UI, 测试页面, walk through, check that, verify the, test the login/checkout/registration/dashboard, or any request involving localhost testing, form submission, flow validation, or screenshot capture."
license: MIT
---

# 前端 E2E 测试

支持 **agent-browser CLI**（简单线性流程）和 **Playwright Python 脚本**（复杂多步骤流程）两种模式，根据测试复杂度自动选择。

## 核心原则

1. **Real-UI 约束**：E2E 测试**禁止 mock HTML 页面**，必须与真实 UI 交互。只允许 mock 后端 API 响应。
2. **仅网络层 Mock**：只在网络层 mock API，让真实前端代码执行。
3. **强制 Mock-Retry 循环**：测试阻塞时必须迭代修正 mock 数据，修正后自动重试，禁止直接放弃。

## 工作流程

```
用户输入测试需求 → 检查需求完整性 → 检查开发服务器 → 执行 Mock 分析（七步法 + 交互分析）→ 配置 Mock → 执行测试
    ↓
[阻塞?] → 是 → 诊断原因 → 更新 Mock / 修正交互方式 → 重试测试（最多3次）
    ↓
    否 → 输出测试报告
```

### 步骤 1: 检查测试需求完整性

参照 `references/test-requirement-input-specification.md`，检查用户输入是否包含：

| 必需要素 | 说明 |
|----------|------|
| **测试场景** | 清晰的用户操作流程 |
| **前置条件** | 用户状态、数据状态 |
| **操作步骤** | 详细的点击/输入操作 |
| **预期结果** | 每步操作的预期状态 |
| **截图需求** | 需要截图的关键步骤 |

**如果信息缺失**，自动从当前项目环境收集：

**自动收集流程**:

1. **缺少用户状态**:
   ```bash
   # 搜索用户状态类型定义
   grep_code "userType|isNewUser|hasPermission"
   search_codebase "user state type definition"

   # 从现有 mock 数据中查找用户状态示例
   find tests/e2e/mock-templates/user-states -name "*.json"
   ```

2. **缺少操作步骤**:
   ```bash
   # 定位页面组件
   search_codebase "[页面名称] page component"
   read_file <page-component>

   # 从 JSX 中识别可交互元素（button, input, link）
   grep_code "onClick|onSubmit|<button|<input" <page-component>
   ```

3. **缺少预期结果**:
   ```bash
   # 从已有测试中查找类似场景
   find tests/e2e -name "*[关键词]*"

   # 从组件测试中查找预期行为
   find . -name "*.test.tsx" -o -name "*.spec.tsx"
   ```

**决策矩阵**:

| 信息缺失程度 | 处理方式 |
|-------------|---------|
| **可从项目中推断** | 自动补充，继续执行 |
| **推断不确定** | 提供推断结果，请用户确认 |
| **无法推断** | 列出缺失项，请用户补充 |

**示例**:
```
用户输入: "测试登录流程"

自动收集结果:
- ✅ 找到登录页面: /src/pages/Login.tsx
- ✅ 识别表单元素: username, password, submit button
- ⚠️ 缺少用户状态定义（新用户/老用户）

处理:
列出已收集信息 + 询问缺失部分
```

### 步骤 2: 检查开发服务器

> ⚠️ **测试前必须确认服务器已运行**

直接询问用户，获取服务器地址后验证可访问性：

```bash
# 用户未提供地址时，自动检测常见端口
for PORT in 9000 3000 8080 5173; do
  curl -sk https://localhost:$PORT > /dev/null 2>&1 && echo "✓ https://localhost:$PORT" && break
  curl -s http://localhost:$PORT > /dev/null 2>&1 && echo "✓ http://localhost:$PORT" && break
done
```

验证失败时请用户确认后继续。禁止尝试自动启动服务器。

### 步骤 3: 执行 Mock 分析（强制步骤）

> ⚠️ **此步骤不可跳过**。任何测试执行之前必须完成 Mock 分析。

#### 3.1 判断 API 可用性

| 情况 | 处理方式 |
|------|----------|
| **后端 API 可用** | 直接使用真实 API，跳过 Mock 配置 |
| **后端 API 不可用** | **必须**执行完整的 Mock 分析流程 |
| **部分 API 不可用** | 只对不可用的 API 执行 Mock 分析 |

> ⚠️ **额外注意**：API Mock 只覆盖网络请求层。如果测试流程涉及**用户状态判断**（如新/老用户、权限标志），还需额外评估是否需要 **localStorage 预填充**或**全局变量注入**（`Object.defineProperty`）——这是独立于 API Mock 的第二条 mock 向量，缺失时 UI 状态仍然不符合预期。参见 `patterns/mock-state-injection.md` 规则 4、9。

#### 3.2 深度静态分析（七步法）

> **时序说明**：七步法是**浏览器启动前的静态分析阶段**，完成后才进入浏览器交互。§4.1 的「侦察-然后-行动」是**运行时的浏览器交互策略**，两者顺序执行，不可互相替代或跳过任一。

> 使用 Agent 工具：`read_file`、`grep_code`、`search_codebase`、`lsp`

**Step 1: 定位目标页面组件**
```
search_codebase: "[页面名称] page component"
grep_code: "pages/.*[页面路径]"
```

**Step 2: 识别 API 调用入口**
```
grep_code "get\(|post\(|fetch\(|API\."
grep_code "useRequest|useSWR|useQuery"
```
> 项目特定的 import 路径和类型生成器用法，先查 `tests/e2e/` 目录下的项目交互说明或已有测试脚本中的 import 写法。

**Step 3: 查找响应类型定义** — 搜索项目中的类型定义文件（`rapper/`、`types/`、`*.d.ts`），或阅读 `references/mock-analysis-guide.md` Step 3

**Step 4: 追踪数据流** — API 响应结构 ≠ 代码期望结构，必须追踪 `.map()`/`.filter()` 等转换逻辑

**Step 5: 查找并复用已有 Mock 数据** — 先查 `tests/e2e/mock-templates/`，再查项目源文件

**Step 6: 查找条件渲染逻辑** — 确认每个交互元素在默认 DOM 中是否可达，识别状态切换条件

**Step 7: 构造完整 Mock 数据** — 匹配代码期望路径、满足条件渲染字段、预检查注入陷阱（Rules 4、7、8、9）

> 详细操作指南：读取 `references/mock-analysis-guide.md`（包含 Step 4–7 完整代码示例、模板查找流程、交互说明查阅流程）。

#### 3.3 静态交互分析（强制步骤，与七步法并列）

> ⚠️ **此步骤不可跳过**。七步法解决「数据能不能渲染出来」，静态交互分析解决「渲染出来之后能不能正确操作」。两者都是在浏览器启动前完成的静态分析，都依赖阅读组件源码，不可互相替代。

**对测试步骤中每个需要交互的 UI 元素，逐一回答以下问题**：

---

**Q1：目标元素在组件的默认 DOM 状态下是否直接可达？**

```bash
read_file <目标组件文件>
grep_code "useState|isOpen|isExpanded|activeTab|selected|show" <目标组件文件>
```

| 结论 | 行动 |
|------|------|
| ✅ 组件初始状态下即可见 | 直接写交互代码 |
| ❌ 藏在某个状态切换之后 | 脚本中**先触发前置条件**（点击 tab/radio/toggle），再操作目标元素；若有多个同类元素，用语义锚定而非 DOM 索引（规则 12） |

---

**Q2：目标输入框的值更新机制是什么？**

```bash
read_file <包含 input 的组件文件>
grep_code "onChange|value=|useController|register\(|Field|FormItem" <包含 input 的组件文件>
```

| 结论 | 行动 |
|------|------|
| ✅ 原生 input 或非受控 | `fill()` 可用 |
| ✅ 简单受控（自管 state，有 onChange） | `fill()` 或方案 A（`click(3) + fill()`） |
| ❌ Form/Field 库受控（onChange 由库托管） | 用 `click(click_count=3)` + `type()` 逐字符输入，每个字符触发库的合成事件（规则 6C） |

> 填完值后按钮仍 disabled 但输入框值正确 → onChange 未触发，切换到 `type()` 方案（规则 6C）。

---

**Q3：目标元素的点击路径上是否有拦截层？**

```bash
ls tests/e2e/interaction-notes/ 2>/dev/null  # 先查已沉淀的已知拦截说明
grep_code "<iframe|position.*fixed|z-index|overlay|backdrop" <页面根组件>
```

| 结论 | 行动 |
|------|------|
| ✅ 无拦截层 | 普通 `.click()` |
| ❌ 浮层 iframe 叠在目标上 | 改用 `dispatch_event('click')` 绕过命中检测（规则 13） |
| ❌ overlay backdrop 挡住目标 | 先关闭遮罩（点击 Close 或 Escape），再操作；必要时配合 `force=True`（规则 3） |

> Select 类组件的 trigger 通常也需要 `dispatch_event('click')`（规则 14）。

---

**Q4：提交按钮的 disabled 条件有哪些？**

```bash
read_file <表单或弹窗组件文件>
grep_code "disabled=" <表单或弹窗组件文件>
```

将所有 disabled 子条件列清单，逐项对照保障手段：

| 子条件类型 | 对应保障 |
|-----------|----------|
| 字段校验未通过（值为空/格式错误） | 确认填写方式能触发框架校验（Q2），或 mock 初始值满足格式要求 |
| 异步数据加载中（loading 状态） | 脚本中加等待加载完成的逻辑后再填写 |
| 关联数据不满足（依赖其他字段/接口） | mock 数据中保障依赖字段存在且合法（对照七步法） |
| 日期/范围校验（如 startDate/endDate） | mock 中相关日期字段必须非空且满足范围约束 |
| 其他业务条件 | 读对应判断逻辑，在 mock 数据或测试步骤中逐项满足 |

> 运行时的完整诊断决策树（4 种根因 + 快速排查流程）参见规则 15（`patterns/interaction-input.md`）。

---

**静态交互分析产出**：将结论写进脚本开头的注释块，作为当次交互实现的设计依据：

```python
# ── 静态交互分析结论 ──────────────────────────────────────────
# Q1: <ElementA> 默认不可见，需先触发 <前置条件> 才能显示 → 规则 12
# Q1: <ElementB> 默认可见，直接操作
# Q2: <ElementA> 为 Form Field 受控输入 → click(3)+type()，而非 fill() → 规则 6C
# Q3: 页面存在浮层 iframe → Select trigger 改用 dispatch_event → 规则 13/14
# Q4: 提交按钮 disabled 条件：[条件1] [条件2] → 逐项保障
# ──────────────────────────────────────────────────────────────
```

### 步骤 4: 执行测试与 Mock-Retry 循环

> ⚠️ **强制重试机制**：遇到阻塞必须尝试修正 mock 并重试

#### 4.1 执行测试

**侦察-然后-行动模式**:
1. 导航并等待 `networkidle`
2. 截图或检查 DOM
3. 从渲染状态识别选择器
4. 使用发现的选择器执行操作

**关键检查点**:
```bash
# 每个关键步骤后检查
agent-browser screenshot "step-N.png"
agent-browser snapshot -i  # 检查 DOM 状态
```

#### 4.2 Mock-Retry 循环

**触发条件**: 测试步骤阻塞，原因是数据问题（空列表、元素未找到、状态不匹配）

**循环流程**:
```
检测到阻塞
  ↓
记录: "第 N/3 次尝试"
  ↓
诊断原因（查看 DOM/API 响应）
  ↓
记录诊断结果
  ↓
更新 Mock 数据
  ├─ 方式1: 调整数据结构匹配代码期望路径
  ├─ 方式2: 修改字段值满足条件判断
  └─ 方式3: 使用不同的 mock 模板
  ↓
记录变更: "修改了 xxx 字段"
  ↓
重新配置 network route
  ↓
刷新页面或重新导航
  ↓
重试测试步骤
```

**重试限制**:
- 最多重试 **3 次**
- 每次重试前必须明确诊断问题
- 第 3 次失败后，输出详细诊断报告

**渲染失败诊断清单**:

当元素未渲染时，**依次检查**:

1. ✅ **浏览器 Console 是否有报错?**（优先，最快定位根因）
   ```bash
   # Playwright Python：在 setup 阶段注册（页面启动前）
   page.on("console", lambda msg: print(f"[{msg.type}] {msg.text}") if msg.type == "error" else None)
   # agent-browser CLI：截图后检查页面是否有错误提示
   agent-browser snapshot -i  # 查看 DOM 中是否有错误边界渲染
   ```
   > 参见规则 7（`patterns/mock-state-injection.md`）：mock 配置后页面仍异常，Console 报错通常直接指向根因。

2. ✅ **API 是否被调用?**
   ```bash
   agent-browser network list
   # 检查是否有对应的请求
   ```

3. ✅ **API 响应是否返回?**
   - 检查响应状态码
   - 检查响应体是否为空

4. ✅ **数据路径是否正确?**
   ```
   对比:
   - API 响应结构: result.<field>.<nested>
   - 代码期望结构: data.<mappedField>.<target>

   常见问题:
   - 嵌套层级不匹配
   - 字段名不一致
   - 数组 vs 对象类型不匹配
   ```

5. ✅ **条件渲染逻辑?**
   ```bash
   # 查找条件判断
   grep_code "if \(data\.|{data\.xxx &&"
   # 检查是否有隐藏/显示逻辑
   ```

6. ✅ **数据转换逻辑?**
   ```bash
   # 检查 .map(), .filter() 等转换
   read_file <组件文件>
   # 验证转换后的数据结构
   ```

**重试流程示例**:
```bash
# 第 1 次尝试
agent-browser network route "**/api/endpoint" --mock '{原始 mock 数据}'
agent-browser navigate "http://localhost:<PORT>/<route>"
# 结果: UI 元素缺失 → 诊断: 数据路径不匹配

# 第 2 次尝试（修正数据结构）
agent-browser network route "**/api/endpoint" --mock '{
  "result": {
    // 根据代码期望的数据路径调整结构
    "transformedField": {
      "nestedField": [符合期望的数据]
    }
  }
}'
agent-browser navigate "http://localhost:<PORT>/<route>"
# 结果: UI 显示正常 → 继续测试
```

#### 4.3 沉淀成功的 Mock 模板

> 测试成功后，将有价值的 mock 数据沉淀为原子化模板，供后续测试复用（在 Step 5 中检索使用）。

**触发条件**（满足任一即沉淀）:
```
Mock 构造复杂（嵌套层级 ≥ 3）||
场景常见（新用户、列表展示、创建流程）||
API 端点稳定（非实验性接口）
```

**原子化原则**（沉淀前判断）:

| 特征 | 应沉淀 ✅ | 不沉淀 ❌ |
|------|---------|----------|
| 数据维度 | 单一维度（用户状态 / 商品列表） | 多维度混合（用户+商品+订单） |
| 复用性 | 可用于多个场景 | 仅用于当前测试 |
| 独立性 | 独立存在，无操作步骤 | 包含操作步骤或 UI 状态 |
| 命名 | 描述数据维度（`premium-user.json`） | 描述场景（`profile-test.json`） |

**沉淀流程**:

1. **判断是否满足原子化条件**（见上表）
   - ✅ `user-states/new-user-no-smax.json` — 用户身份状态
   - ✅ `api-mocks/am-campaign-query-onepage-touchpoint.json` — API 响应
   - ❌ `scenarios/checkout-test.json` — 整个测试场景数据

2. **创建模板文件**（按注入方式分类）
   ```bash
   # 用户状态模板（全局变量注入）
   mkdir -p tests/e2e/mock-templates/user-states

   # API mock 模板（网络请求拦截）
   mkdir -p tests/e2e/mock-templates/api-mocks
   ```

3. **写入模板内容**
   ```json
   {
     "endpoint": "**/api/endpoint.json",
     "description": "API 用途说明",
     "mockData": { ... },
     "applicableScenarios": ["场景1", "场景2"],
     "tags": ["tag1", "tag2"],
     "version": "1.0",
     "createdAt": "YYYY-MM-DD",
     "updatedAt": "YYYY-MM-DD",
     "testedIn": "测试场景名称",
     "successCount": 1
   }
   ```

4. **更新模板索引**

   创建模板后，必须更新索引文件以便后续查找:

   ```bash
   # 在 tests/e2e/mock-templates/README.md 中添加条目
   echo "- **<category>/<template-name>.json**: <description> (version: <version>, successCount: 1)" >> tests/e2e/mock-templates/README.md
   ```

   **索引格式示例**:
   ```markdown
   # Mock Templates Index

   ## User States
   - **user-states/premium-user.json**: Premium subscriber state (version: 1.0, successCount: 5)
   - **user-states/new-user-no-smax.json**: New user without any ad history (version: 1.1, successCount: 3)

   ## API Mocks
   - **api-mocks/query-recommended-list.json**: Recommended items list response (version: 1.0, successCount: 8)
   ```

#### 4.4 沉淀成功的交互 Helper

> 对标 §4.3 的 Mock 模板沉淀机制。测试成功后，主动检查是否有值得提取为可复用 helper 函数的交互模式——不要等用户追问才记录。

**沉淀触发条件**（满足任一即沉淀）：
- Q2 相关：受控输入模式在**当前项目 2+ 个测试**中出现
- Q3 相关：同一类浮层/iframe 拦截问题在 **2+ 个测试**中出现
- Q1 相关：同一组件库的条件渲染前置操作在 **2+ 个测试**中重复

**沉淀目标**：写入项目的交互说明目录（查 `tests/e2e/` 下现有目录结构确认具体路径），不内嵌在测试脚本中。

**分离原则**：Helper 只处理「怎么操作组件」，不含「操作哪个元素」；业务层选择器由调用方传入。

> 如果项目已有 helper 文件，先阅读其中已有的函数，直接导入复用。

——

## 决策树：选择测试工具

```
用户测试需求
  │
  ├─ 静态 HTML？→ 直接读取文件识别选择器，使用 agent-browser 执行
  │
  └─ 动态 SPA（React/Vue 等）
       │
       ├─ 后端 API 可用？→ 直接测试，侦察-然后-行动
       │
       └─ 后端 API 不可用 → 必须 Mock
            │
            ├─ 是否满足任一升级条件？
            │   ├─ 需要注入全局变量（Object.defineProperty freeze）
            │   ├─ 测试步骤需要循环 / 条件逻辑 / 多分支
            │   ├─ 需要多步骤之间传递状态
            │   └─ 选择器需要回退链 / 动态推断
            │
            ├─ 是 → 升级到 Playwright Python 脚本
            │         使用 page.route() 拦截网络 + HTML 响应
            │         脚本路径: tests/e2e/scripts/
            │
            └─ 否 → 使用 agent-browser CLI
                      agent-browser network route "**/<endpoint>" --mock '<JSON>'
```

**agent-browser CLI 适合的场景**（线性流程，步骤 ≤ 4）:
- 导航 → 截图 → 验证文本
- 点击 → 填表 → 提交 → 检查跳转

**Playwright Python 升级触发条件**（满足任一即升级）:

| 条件 | 原因 |
|------|------|
| 需要注入全局变量（window.__xxx__）| agent-browser 无法在页面脚本前 freeze 属性 |
| 步骤间有条件判断 / 循环 | CLI 无编程控制流 |
| 选择器需要多级回退 | shell 脚本处理复杂性高 |
| 需要跨步骤传递变量（计数、状态） | CLI 无状态管理 |
| 步骤 ≥ 5 且有依赖关系 | 调试成本高 |

**Playwright Python 基本结构**：见 `examples/playwright-boilerplate.py`。

### 禁止行为

- ❌ **跳过 Mock 分析步骤直接执行测试**
- ❌ Mock HTML 页面或组件
- ❌ 在前端代码中注入假数据
- ❌ 跳过需要 mock 的测试场景
- ❌ 遇到阻塞直接标记 BLOCKED 并放弃
- ❌ 归咎于「账号问题」或「数据问题」而不尝试修正 mock
- ❌ 说「这个场景需要老用户账号」而不通过 mock 注入状态
- ❌ Mock 方案一次失败后就放弃
- ❌ 假设服务器已运行而不检查
- ❌ 只查找 API 类型定义，不追踪数据流
- ❌ 不使用项目现有的 mock 数据源和模板
- ❌ 重试超过 3 次后不输出诊断报告

## Playwright 交互可靠性规则

> 遇到 Playwright 交互问题时，查阅 `references/playwright-interaction-patterns.md`——该文件包含完整的规则速查表和分类文件指针。新增规则时同步更新该索引文件。

### 规则毕业策略（Rule Graduation Policy）

> **核心原则**：规则文件记录的是「假说」，不是工作流程。**任何在每次测试中都必须执行的行为，必须写进模板，而不是写成规则。**

**规则毕业条件**（满足任一即触发）：

| 条件 | 动作 |
|------|------|
| 该行为在**每一次**测试中都必须执行 | 立即写进模板，不创建规则 |
| 同一规则在 **2+ 个独立测试**中被触发 | 毕业进入对应模板位置，从规则表中移除 |

**毕业目标位置**：
- 每次截图必须执行 → `take_screenshot_at_step()` helper
- 每次 mock 设置必须执行 → `page.route()` boilerplate
- 每次测试运行必须执行 → `with sync_playwright()` scaffold

**新增规则前的决策门（Decision Gate）**：
```
问题：该行为是否在每次测试中都适用？
  → YES：直接修改 SKILL.md 模板，禁止写成规则
  → NO：该行为是否由特定组件库或边缘场景触发？
         → YES：写入 references/patterns/ 对应文件
         → NO：不需要记录

已有规则是否在 2+ 个独立测试中被触发？
  → YES：立即毕业进入模板，从规则表移除
```

#### 反向沉淀路径：测试成功后的交互规则沉淀

> 对标 §4.3 的 Mock 模板沉淀机制。**每次测试成功后**，必须主动检查是否有值得沉淀的交互操作模式——不要等用户追问才记录。

**沉淀触发条件**（满足任一即沉淀）：

| 条件 | 示例 |
|------|------|
| 解决了在 **2+ 个测试**中重复出现的同类问题 | iframe 拦截在 E3、E4 均出现 |
| 问题与**组件库或框架机制**相关（而非业务逻辑） | React 受控输入 onChange 不触发 |
| 解法**不直观**，没有文档会重复踩坑 | `dispatch_event` 绕过可见性检测 |

**沉淀目标位置**：
- 点击/输入/键盘操作 → `patterns/interaction-input.md`
- 元素定位/存在性检测 → `patterns/selector-detection.md`
- Mock 注入/全局变量 → `patterns/mock-state-injection.md`

**沉淀格式要求**（写入规则文件时）：
1. **问题描述**：什么场景会触发，典型报错信息
2. **根本原因**：为什么会发生（机制层面的解释）
3. **解法代码**：❌ 错误示例 + ✅ 正确示例，带注释
4. **通用原则**：提炼出跨项目可复用的判断规则
5. **同步更新** `SKILL.md` 参考文件索引（第744行附近）

**已毕业的规则**（不再作为需要「遇到问题才查阅」的规则）：

| 规则 | 毕业位置 | 毕业原因 |
|------|---------|--------|
| ~~规则 10: 导航后滚动到目标元素~~ | `take_screenshot_at_step()` step 2 | 每次截图都需要 |
| ~~规则 11: 截图前清理覆盖层~~ | `take_screenshot_at_step()` step 1 | 每次截图都需要 |

## 最佳实践

- 完成后始终关闭浏览器
- 使用描述性选择器（优先 `aria-label`、`data-testid`，其次 CSS 类名）

### 步骤 5: 输出并存档测试报告

测试完成后，按照 `references/test-report-specification.md` 生成规范化报告，**并必须存档到项目中**。

**存档规则**（强制）:
- **目录**: `tests/e2e/reports/`
- **报告命名**: `[SceneID]_[名称]_[YYYYMMDD].md`
  - 示例: `E3_am_campaign_list_20260330.md`
- **截图目录命名**: `tests/e2e/screenshots/[SceneID]_[名称]_[YYYYMMDD]/` （与脚本名、报告名完全对齐）
  - 示例: `E3_am_campaign_list_20260330/` 对应脚本 `test_e3_am_campaign_list.py` 和报告 `E3_am_campaign_list_20260330.md`
- **截图文件名**: `step[NN]_[描述].png`（**不含时间戳**，每次运行直接覆盖）
- **目录管理**: 每次运行前必须先清空截图目录（`shutil.rmtree`），确保每次运行只有一套截图，不堆积重复文件
- **内容准确性**: 报告描述必须与**实际最终运行结果**一致，不得使用早期调试阶段的截图/描述
- **截图内联**: 报告中的截图必须使用 `![描述](路径)` 内联展示，并放在对应步骤旁边，不得单独列在表格中
- **报告图片路径格式**: 必须使用 **workspace-relative** 路径（相对于项目根目录）。`take_screenshot()` 的返回值就是此格式，直接嵌入报告。
  - ✅ `tests/e2e/screenshots/E3_.../step01.png`
  - ❌ `/Users/绝对路径/step01.png`（绝对路径 markdown 无法渲染）

**报告语言**:
- 根据用户偏好设置报告语言（默认：中文）
- 代码、文件路径、技术术语保持英文

报告必须包含：
- **测试摘要**: 通过/失败/阻塞统计
- **步骤详情**: 每步操作、预期、实际结果对比表
- **截图证据**: 关键节点截图路径
- **Mock 配置说明**: 使用的 Mock 端点和注入方式（便于复现）

## 参考文件

- **references/** - 测试规范:
  - `test-requirement-input-specification.md` - 测试需求输入规范
  - `test-report-specification.md` - 测试报告规范
  - `mock-analysis-guide.md` - 七步法 Step 4–7 详细操作指南（数据流追踪、模板查找、条件渲染、Mock 构造）
  - `playwright-interaction-patterns.md` - Playwright 交互可靠性规则索引（可持续扩展）
    - `patterns/selector-detection.md` - 规则 1、2（Rules 10/11 已毕业进模板，小节保留为参考）
    - `patterns/interaction-input.md` - 规则 3、5、6、12、13、14、15（交互与输入、多实例选择器语义锁定、iframe 指针拦截绕过、Select 下拉交互通用模式、Confirm 按钮 disabled 诊断）
    - `patterns/mock-state-injection.md` - 规则 4、7、8、9（Mock 与状态注入、持久化存储预填充）
- **项目本地交互说明目录**（如果项目维护） - 组件库类名、覆盖层场景等项目级补充（本项目存放在 `tests/e2e/interaction-notes/`）
