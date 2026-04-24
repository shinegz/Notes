# Playwright 规则：交互与输入操作

> 适用场景：点击、键盘操作、填写表单、与弹出层交互。
>
> **项目本地补充**：部分规则（13、14）需要组件库的具体类名才能落地。如果当前项目维护了本地交互说明目录（通常在 `tests/e2e/interaction-notes/` 或类似路径），在写交互代码前先查阅该目录——它记录了本项目的组件库类名和已知覆盖层触发场景。没有该目录则跳过。

---

## 规则 3：键盘快捷键副作用

**问题**: `Escape` / `Enter` 等键盘快捷键可能被 SPA 的全局键盘监听器捕获，触发路由跳转、tab 切换、弹层关闭等**应用级副作用**，导致测试页面状态意外改变。

**典型症状**: 关闭弹出层后，页面 URL 变了，或者当前激活的 tab 切换了。

**两种场景，结论不同**:

```python
# 场景 A：关闭业务弹出层（Balloon、Drawer、Modal）
# ❌ 危险：Escape 可能触发应用级导航或 tab 切换
page.keyboard.press("Escape")

# ✅ 安全：显式点击 Cancel / Close 按钮
cancel_btn = page.locator("button:has-text('Cancel')").first
if cancel_btn.count() > 0:
    cancel_btn.click()
    page.wait_for_timeout(300)

# 场景 B：清除阻挡点击的遮罩背景
# ✅ 合理：当 overlay backdrop 拦截目标元素的点击事件时
# 先 Escape 解除遮罩，再对目标元素 force 点击
try:
    backdrop = page.locator(".next-overlay-backdrop")  # Alifd/Next 类名；其他组件库用 .backdrop / [class*='overlay-backdrop']
    if backdrop.count() > 0:
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)
except Exception:
    pass
target_input.click(force=True)  # force=True 作为兜底
```

**判断规则**:
- **关闭业务弹出层** → 点击 Cancel/Close 按钮，不用 Escape
- **解除遮罩背景拦截** → 可用 Escape，但配合 `force=True` 作为兜底
- **验证键盘行为本身** → 当然用 `page.keyboard.press()`

**调试方法**: 如果测试步骤后页面状态意外改变（URL 变化、内容消失），在该步骤前后各截一张图，对比确认是否是键盘事件触发了导航。

---

## 规则 5：输入框类型过滤

**问题**: 在弹出层中查找输入框时，`input` 选择器会同时匹配 `radio`、`checkbox`、`hidden` 等不可填写类型，导致 `fill()` 报错。

```python
# ❌ 错误：可能匹配到 radio/checkbox 类型的 input
page.locator(".balloon input").fill("100")
# Error: Input of type "radio" cannot be filled

# ✅ 正确：排除不可填写的 input 类型，按优先级依次尝试
def find_fillable_input(page, container_selector=None):
    prefix = f"{container_selector} " if container_selector else ""
    for selector in [
        f"{prefix}input[type='number']",
        f"{prefix}input[inputmode='decimal']",
        f"{prefix}input[inputmode='numeric']",
        f"{prefix}input:not([type='radio']):not([type='checkbox']):not([type='hidden'])",
    ]:
        el = page.locator(selector).first
        if el.count() > 0:
            return el
    return None
```

**通用原则**: 在弹出层（Balloon、Popover、Modal）中查找输入框时，始终排除 `radio`、`checkbox`、`hidden` 类型。

---

## 规则 6：文本选中与清空输入（含 React 受控输入标准序列）

**问题**: Playwright Python 没有 `triple_click()` 方法。更严重的是，`fill()` 在 React **受控输入框**（`value` 由 `useState` 驱动）中不会触发 `onChange`，导致 Confirm 按钮保持 disabled 状态。

```python
# ❌ 错误：triple_click() 不存在于 Python Playwright
input_el.triple_click()

# ❌ 错误：fill() 不触发 React onChange → Confirm 按钮一直 disabled
input_el.fill("10")

# ✅ 正确方案 A：click_count=3 选中全文再 fill（适用于非受控或兼容的输入框）
input_el.click(click_count=3)
input_el.fill("new_value")

# ✅ 正确方案 B（React 受控输入框标准序列）：dispatch_event focus → fill → Tab
# 原理：dispatch_event('click') 触发 React focus 事件，Tab 触发 onBlur + onChange
input_el.dispatch_event('click')   # 1. 触发 React focus（绕过 iframe 遮挡，见 Rule 13）
input_el.fill("new_value")         # 2. 写入 DOM 值
input_el.press("Tab")             # 3. 触发 React onChange + onBlur

# ✅ 备选方案 C：逐字符输入（最高兼容性，但速度慢）
input_el.click(click_count=3)
input_el.press("Backspace")
input_el.type("new_value")  # type() 逐字符触发事件
```

**选择方案的判断依据**:

| 场景 | 推荐方案 |
|------|----------|
| 普通 `<input>`，无 React 受控 | 方案 A |
| React 受控输入框（`value` 由 state 驱动）、Confirm 按钮依赖 onChange | **方案 B**（首选） |
| 方案 B 无效，或组件有复杂校验逻辑 | 方案 C |

**判断是否是受控输入框**: 如果填完值后 Confirm/Save 按钮仍是 disabled，大概率是 onChange 没触发 → 切换到方案 B。

---

## 规则 12：多实例相同选择器时用语义锁定目标

**问题**: 弹窗内有多个相同类名的相同类型容器（如多个 `customInput` 区块、多个 radio group）时，`querySelector('[class*="customInput"]')` 总是返回 DOM 里第一个。如果第一个不是目标，赋值会错进错误的容器，得到假 PASS。

**根本原因**: `querySelector` 和 `.first` 按 DOM 顺序返回，而多个同类容器通常在读取时进入 DOM，顺序可能与视觉上的上下关系不一致。

**典型场景**:
- 设置对话框里同时存在多个 `customInput` 区块（如「自定义 ROAS 输入」和「自定义预算输入」共用同一组件类名）
- 表单里多个相同布局的输入组（日期范围左/右端，价格上下限等）

```python
# ❌ 错误：querySelector 总是拿到 DOM 第一个，当目标是第二个时就会错
page.evaluate("""
    () => {
        const inp = document.querySelector('[class*="customInput"] input');
        inp.value = '200';  // 赋到第一个 customInput 而非预算输入
    }
""")

# ✅ 正确方案 A：用同组 radio 的其中一个 radio 做锤子，向上走找包含目标容器
# 适用于：目标输入邻近一个 radio 选项（常见于「自定义输入」模式）
anchor_result = page.evaluate("""
    () => {
        // Step 1: 找到同组中的做镔子 radio（如 'No Limit' radio）
        const radios = Array.from(document.querySelectorAll('input[type=radio]'));
        const anchorRadio = radios.find(r => {
            const lbl = r.closest('label') || r.parentElement;
            return lbl && lbl.textContent.toLowerCase().includes('no limit');  // 替换为实际做镔文字
        });
        if (!anchorRadio) return { ok: false, reason: 'anchor radio not found' };

        // Step 2: 从做镔素向上走，找包含目标 input 的最小容器
        let container = anchorRadio.parentElement;
        for (let i = 0; i < 6; i++) {
            if (!container) break;
            const inp = container.querySelector('input:not([type=radio]):not([type=checkbox])');
            if (inp && inp.offsetParent) {
                inp.value = '200';
                inp.dispatchEvent(new Event('input', { bubbles: true }));
                return { ok: true, depth: i };
            }
            container = container.parentElement;
        }
        return { ok: false, reason: 'input not found in ancestor chain' };
    }
""")

# ✅ 正确方案 B：querySelectAll 全部实例，按语义顺序取目标一个
# 适用于：知道目标是所有实例中的第 N 个（如最后一个）
page.evaluate("""
    () => {
        const allContainers = Array.from(
            document.querySelectorAll('[class*="customInput"]')
        ).filter(c => c.offsetParent);  // 只保留可见实例
        if (allContainers.length === 0) return;
        const target = allContainers[allContainers.length - 1];  // 或用具体索引
        const inp = target.querySelector('input:not([type=radio])');
        if (inp) inp.value = '200';
    }
""")
```

**选择方案的判断依据**:

| 场景 | 推荐方案 |
|------|----------|
| 目标输入邻近一个语义明确的 radio（如「No Limit」 / 「Free」） | **方案 A**：用 radio 做镔子 |
| 目标是所有实例中第 N 个，且 N 是固定的 | **方案 B**：全选 + 索引 |
| 目标容器有唯一的父元素类名 | 直接空间将父元素类名缩小为选择器作用域 |

**通用原则**:
- DOM 中存在多个相同类名的容器时，禁止使用 `querySelector`（返回 DOM 第一个）或 `.first`（返回文档顺序第一个）
- 优先将**语义素**（相邻的 radio 文字、label 内容、父容器唯一类名）作为销定锚子，而不是依赖 DOM 顺序
- 语义锚定使得选择器即使代码改变了元素顺序也不会失效

---

## 规则 13：iframe 指针事件拦截绕过

**问题**: 页面中存在浮层 `<iframe>` 时，Playwright 的 `.click()` 会报错：
```
Error: <element> intercepts pointer events
```
原因是 iframe 叠在目标元素上方，物理鼠标事件被 iframe 捕获而无法到达目标元素。

> 项目专项说明：如果项目维护了本地交互说明目录，查阅该目录了解具体哪些场景会触发此问题及受影响的选择器。

```python
# ❌ 错误：物理点击被 iframe 拦截
page.locator("button.submit").click()   # Error: intercepts pointer events

# ✅ 方案 A：dispatch_event（首选，Playwright 原生 API）
# dispatch_event 绕过 Playwright 的可见性 / 命中检测，直接向元素分发合成事件
btn = page.query_selector("button.submit")
btn.dispatch_event('click')

# 受控输入框完整序列（配合 Rule 6 方案 B）
input_el = page.query_selector("input.target")
input_el.dispatch_event('click')   # focus（绕过 iframe）
input_el.fill("value")
input_el.press("Tab")              # 触发 React onChange

# ✅ 方案 B：page.evaluate + dispatchEvent
page.evaluate("""
    () => {
        const el = document.querySelector('button.submit');
        if (el) el.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
    }
""")

# ✅ 方案 C：force=True（最后兜底）
page.locator("button.submit").click(force=True)
```

**方案优先级**: A → B → C

**如何判断是 iframe 拦截**: 错误消息包含 `intercepts pointer events`，或截图可见 iframe 叠加在目标元素区域。

**通用原则**:
- 当截图或日志确认目标元素**被 iframe 覆盖**时，该元素及同一 iframe 覆盖范围内的其他元素均改用 `dispatch_event('click')`
- 不要无条件全局替换所有 `.click()`：`dispatch_event` 绕过了 Playwright 的 actionability check，在没有 iframe 拦截的场景下用它会掩盖按钮隐藏、组件未渲染等真实问题
- `dispatch_event` 对按钮、输入框、radio、checkbox、select trigger 均有效
- 与 Rule 6 方案 B 配合：`dispatch_event('click')` → `fill()` → `press('Tab')` 是受控输入框的完整标准序列

---

## 规则 14：Select 类下拉组件交互

**问题**: Select 组件通常将点击触发区和下拉菜单渲染为两个独立 DOM 节点。直接对容器调用 `.click()` 通常无效（事件绑定在 trigger 子元素上），加之可能受 iframe 覆盖，需要使用 `dispatch_event`。

> 本项目如使用特定组件库（如 @alifd/next、Ant Design 等），具体类名查阅项目本地交互说明目录。

**通用交互模式**（适用于任何 Select 组件库）：

```python
# Step 1：找到点击触发区并用 dispatch_event 打开下拉
# trigger 选择器因组件库而异，查阅项目本地交互说明目录获取具体类名
trigger = page.query_selector('<trigger-selector>')   # 替换为组件库的 trigger 类名
if not trigger:
    trigger = page.query_selector('<container-selector>')  # 备选：trigger 在容器本身
trigger.dispatch_event('click')
page.wait_for_timeout(400)  # 等待动画

# Step 2：等待菜单出现
page.wait_for_selector('<menu-selector>', timeout=5000)  # 替换为下拉菜单根容器选择器

# Step 3：按文本匹配目标选项
items = page.query_selector_all('<menu-item-selector>')  # 替换为选项选择器
for item in items:
    if 'Target Option Text' in item.inner_text().strip():  # 替换为目标文本
        item.dispatch_event('click')
        break
page.wait_for_timeout(300)

# 页面有多个 Select 时，先缩小到父容器
container = page.query_selector('.parent-section')
trigger = container.query_selector('<trigger-selector>') if container else page.query_selector('<trigger-selector>')
trigger.dispatch_event('click')
```

**通用原则**:
- Select 的 trigger 交互默认使用 `dispatch_event('click')`（见 Rule 13）
- 选项匹配用 `inner_text()` + `in` 操作符，不用精确等于（避免空白字符问题）
- 菜单出现后必须用 `wait_for_selector` 等待，不要用固定 sleep
- 选完选项后，等菜单从 DOM 中移除（`state='detached'`），再继续下一步

---

## 规则 15：Confirm/Submit 按钮 disabled 诊断清单

**问题**: 表单填写完毕后，Confirm / Save / Submit 按钮仍处于 disabled 状态，测试卡在最后一步无法完成。

**根本原因有以下几类**（按频率排序）:

### 原因 1：React onChange 未被触发（最常见）
`fill()` 直接写 DOM value，但不触发 React 的合成事件，state 未更新，按钮禁用条件未解除。

```python
# 诊断：填完后立刻截图，检查 input 的显示值是否正确
page.screenshot(path="debug_after_fill.png")
# 如果显示值正确但按钮仍 disabled → 是 onChange 问题

# 修复：改用 Rule 6 方案 B
input_el.dispatch_event('click')
input_el.fill("10")
input_el.press("Tab")  # ← 触发 onChange
```

### 原因 2：下拉菜单仍处于展开状态
打开 Select 后没有等下拉关闭，下拉菜单遮挡导致 Confirm 按钮不可交互，或 form 的 submit 被拦截。

```python
# 诊断：截图检查是否有下拉菜单容器还在 DOM 中
# 各组件库的菜单选择器不同，查阅项目本地交互说明目录获取具体类名
is_menu_open = page.locator('<menu-container-selector>').count() > 0
print(f"Menu still open: {is_menu_open}")

# 修复：选完选项后等菜单从 DOM 中移除
item.dispatch_event('click')
page.wait_for_selector('<menu-container-selector>', state='detached', timeout=3000)
```

### 原因 3：Radio 选中了错误的选项
`radio[1]` 取到的是另一个 radio group 的第 2 个，而非目标 group 的第 2 个。

```python
# 诊断：打印所有 radio 的 value 和 label
radios = page.query_selector_all('input[type=radio]')
for i, r in enumerate(radios):
    val = r.get_attribute('value') or ''
    label = page.evaluate("el => { const l = el.closest('label') || el.parentElement; return l ? l.textContent.trim() : ''; }", r)
    print(f"  radio[{i}] value={val!r} label={label!r}")

# 修复：用语义锚定（见 Rule 12），而非索引
```

### 原因 4：表单校验未通过（值为空或格式错误）

```python
# 诊断：检查 input 是否有 error 状态类
has_error = page.locator('input.next-error, input[aria-invalid="true"]').count() > 0
# 或检查 error message
error_msg = page.locator('[class*="errorMsg"], [class*="error-message"]').first
if error_msg.count() > 0:
    print(f"Validation error: {error_msg.inner_text()}")
```

**快速诊断流程**:

```
Confirm 按钮 disabled
       ├─ 截图 → 有下拉菜单展开?  → 等菜单关闭（原因 2）
       ├─ 截图 → input 值显示正确?
       │         ├─ 是 → onChange 未触发 → 加 Tab（原因 1）
       │         └─ 否 → fill 本身失败 → 检查 Rule 5 / Rule 12
       └─ 打印所有 radio → 索引错误? → 语义锚定（原因 3）
```
