# Playwright 规则：Mock 与状态注入

> 适用场景：全局变量注入、API mock 数据构造、测试失败诊断。

---

## 规则 4：全局变量注入可靠性

**问题**: `page.add_init_script()` 注入的脚本虽然在页面脚本执行前运行，但页面 HTML 中的**内联 `<script>` 标签**会在 DOM 解析阶段直接执行，覆盖 `add_init_script` 的注入结果。

**触发场景**:
- `add_init_script` 已执行，但页面仍渲染服务端默认状态
- 全局变量（如 `window.__config__`、`window.__userInfo__`）始终是原始值
- Mock 状态设置后页面仍按未登录/新用户状态渲染

### 方案一（首选）：`Object.defineProperty` 冻结属性

在 `add_init_script` 中用 `Object.defineProperty` 定义属性，设置空 setter，使后续赋值**静默失效**。

```python
import json

mock_config = {"userType": "premium", "featureFlags": [100, 200, 300]}
mock_config_json = json.dumps(mock_config)

frozen_script = f"""
(function() {{
  var mockData = {mock_config_json};
  try {{
    Object.defineProperty(window, '__globalConfig__', {{
      get: function() {{ return mockData; }},
      set: function(v) {{ /* silently ignore HTML script overwrite */ }},
      configurable: false,
      enumerable: true
    }});
  }} catch(e) {{
    // Property already defined — fall back to direct assignment
    window.__globalConfig__ = mockData;
  }}
}})();
"""

page.add_init_script(frozen_script)
# ✅ 无需 HTML 拦截，init_script 在内联 <script> 之前执行，
#    Object.defineProperty 定义后，内联 <script> 的赋值被空 setter 吸收
```

### 方案二（备选）：拦截 HTML 响应替换内联脚本

当方案一不适用时（如需要完全替换 HTML 内容，或 configurable 检测有问题），拦截 HTML 响应，直接替换内联 `<script>` 中的赋值语句。

```python
import re, json

mock_config = {"userType": "premium", "featureFlags": [100, 200, 300]}

def handle_html(route, request):
    response = route.fetch()
    body = response.text()
    body = re.sub(
        r'(window\.__globalConfig__\s*=\s*)\{[^;]+\}',
        r'\g<1>' + json.dumps(mock_config),
        body
    )
    route.fulfill(response=response, body=body)

page.route("**/index.html", handle_html)
page.route("**/index.html?**", handle_html)
```

**注意事项**:
- 正则模式需匹配实际 HTML 中的赋值格式（可先截图 + view-source 确认）
- 如果全局变量赋值跨多行，需调整正则为多行模式（`re.DOTALL`）
- 同时注册 `**/index.html` 和 `**/index.html?**` 确保覆盖带参数的请求

---

## 规则 7：Console 日志捕获用于诊断

**问题**: 测试步骤阻塞时，截图只能看到 UI 状态，无法知道是 JS 报错、数据路径错误还是权限拦截导致的问题。

**适用场景**: Mock 已配置但页面仍渲染错误状态、某个步骤后 UI 突然变空白、条件渲染逻辑不符合预期时。

```python
console_errors = []
console_logs = []

def handle_console(msg):
    entry = f"[{msg.type}] {msg.text}"
    if msg.type in ("error", "warning"):
        console_errors.append(entry)
    console_logs.append(entry)

page.on("console", handle_console)

# 步骤失败后输出诊断信息
if console_errors:
    print("=== Console Errors ===")
    for err in console_errors:
        print(err)
```

**与截图配合使用**:
```python
page.screenshot(path="debug_step_N.png")
with open("debug_console.txt", "w") as f:
    f.write("\n".join(console_logs))
```

**常见诊断结论**:

| Console 错误类型 | 可能原因 |
|----------------|---------|
| `TypeError: Cannot read properties of undefined` | Mock 数据路径不匹配，某字段为 `undefined` |
| `401 Unauthorized` / `403 Forbidden` | 认证 Mock 未生效，权限检查失败 |
| `Uncaught SyntaxError` | HTML 响应拦截时正则替换破坏了 JS 语法 |
| `React warning: Each child should have a unique key` | 数据列表 Mock 中缺少 `id` 类字段 |

**原则**: 在复杂测试脚本的 setup 阶段默认开启 console 捕获，失败时自动输出 error 级别日志。

---

## 规则 9：浏览器持久化存储预填充（localStorage / IndexedDB）

**问题**: SPA 经常从 `localStorage` 或 `IndexedDB` 读取持久化状态来决定页面行为——包括但不限于：一次性弹窗的展示记录、用户偏好（暗色模式、语言）、onboarding 步骤、A/B 分组、feature flag 覆盖值。Playwright 每次都使用全新的浏览器 context，这些存储全部为空，导致**应用按「新用户首次访问」状态运行**，而不是测试所需的目标状态。

**与 Rule 4 的区别**: Rule 4 处理 `window.__globalVar__` 这类内存级全局变量（随页面刷新消失）；Rule 9 处理浏览器存储层的持久化状态（正常情况下跨会话保留）。两者互补，都需要在 Mock 分析阶段主动识别。

**典型症状**（不限于弹窗）:
- 页面渲染出「首次访问」引导流程，而非测试目标功能
- UI 呈现「新用户」默认状态（空引导、默认偏好），与 API mock 数据不符
- 测试在真实浏览器中正常，在 Playwright 中每次都触发同一初始化路径

**静态分析阶段的识别方法**:
```bash
# 搜索从持久化存储读取状态
grep_code "localStorage.getItem|sessionStorage.getItem"
grep_code "localforage.getItem|idb.*get"

# 搜索「读取 → 判断 → 写回」模式（典型的 guard 逻辑）
grep_code "getItem.*then|getItem.*await"

# key 可能含动态 ID，搜索构造模式
grep_code "\`.*\$\{.*[Ii]d\}.*\`"
```

**核心原则：`add_init_script` 预填充，而不是 `page.evaluate()`**

> ⚠️ 时机决定成败：`page.evaluate()` 在 `page.goto()` 之后执行，应用代码可能已在 mount 时读取过存储，此时写入已无效。`add_init_script` 在页面任何脚本执行前运行，是唯一可靠的时机。

```python
# ✅ 正确：在 page.goto() 之前注册 add_init_script 预填充
# key 和值从源码分析中提取，动态 ID 从 mock 配置中取

page.add_init_script(f"""
    try {{
        localStorage.setItem('{storage_key}', '{storage_value}');
    }} catch(e) {{}}
""")

page.goto(url)  # 此后页面脚本读到的已是预填充值
```

```python
# ❌ 错误：page.goto() 之后 evaluate() 写入，应用可能已读取完毕
page.goto(url)
page.wait_for_load_state("networkidle")
page.evaluate("localStorage.setItem('key', 'value')")  # 太晚了！
```

**如果项目使用异步存储库（如 localforage、idb-keyval）**:

先检查该库是否有 `localStorage` 降级（很多库默认会先尝试 localStorage）。如果有，上面的方案已足够。如果该库仅写入 IndexedDB，需要从源码或 DevTools Application 面板确认 DB 名称和 objectStore 名称，再针对性操作。**不要猜测 DB 结构**。

**Mock 分析清单补充项**（Step 3 七步法的 Step 6 之后额外检查）:

> - 目标页面或其祖先组件是否从持久化存储读取状态来影响渲染路径？
> - 如果有：key 是什么？是否含动态 ID（用户 ID、会话 ID）？该 ID 与 mock 数据中哪个字段对应？
> - 预填充值应与「已完成初始化的老用户」状态一致，而非空值

**通用原则**:
- 任何影响渲染路径的持久化存储状态，都必须在 `add_init_script` 中预填充，而不是 `page.evaluate()`
- 预填充优先用 `localStorage`（同步可靠）；IndexedDB 结构不要猜，先从源码确认
- key 中的动态 ID 从 mock 数据配置中取，保持与其他 mock 一致

---

## 规则 8：API 响应数值字段的类型与渲染层期望一致

**问题**: 前端渲染层对某些字段调用字符串方法（如 `.replace()`、`.split()`、`.toLocaleString()`）。当 API Mock 中这些字段传入 `number` 类型时，会抛出 `TypeError`，导致 React 错误边界捕获并卸载整个组件树，页面呈现空白。

**根本原因**: 后端 API 把数字以字符串格式返回（如 `"4.80"`）是常见实践，尤其对于货币、百分比、ROI 等已格式化数字。Mock 数据必须匹配渲染层的实际期望类型，而非仅看数字就自然用 `number`。

**典型症状**:
- Mock 配置后 `#root` 或根容器子节点数为 0
- Console 出现 `xxx is not a function` 或 `xxx.replace / xxx.split is not a function`
- API 返回正常、用户权限正常，但 React 完全不渲染

```python
# ❌ 错误：根据直觉用 number 类型
mock_data = {
    "price": 45.50,      # number
    "rate": 4.80,        # number
    "amount": 220.00,    # number
}

# ✅ 正确：匹配渲染层期望的字符串类型
mock_data = {
    "price": "45.50",   # string
    "rate": "4.80",     # string
    "amount": "220.00", # string
}
```

**识别方法**: 在 Mock 分析的数据流追踪阶段，搜索渲染函数中是否有字符串方法调用：

```bash
grep_code "\.replace\(|\.split\(|\.toLocaleString\(" <渲染层文件>
# 找到后确认入参类型期望：
# - API 类型定义标注 string → mock 用字符串
# - 字段已格式化（带小数点、分隔符）→ mock 用字符串
# - 字段是纯整数且渲染层直接用于计算 → mock 可用 number
```

**通用原则**:
- 字段在 API 类型定义中是 `string`，或已格式化（小数点、逗号分隔、带单位），mock 必须用字符串
- 列表区域完全空白但 API 返回正常时，优先排查渲染层字符串方法调用导致的 React 崩溃
- 不要下意识地用 number 表示看起来是数字的字段
