# Playwright 规则：选择器与元素检测

> 适用场景：定位元素、判断元素存在性、文本匹配。
>
> **注意**：规则 10（滚动到目标元素）和规则 11（截图前清理覆盖层）已毕业进入 `SKILL.md` 的 `take_screenshot_at_step()` 模板。它们不再是「遇到问题才查阅」的规则——每次截图自动执行。下方保留其实现细节作为参考。

---

## 规则 1：覆盖层存在性检测

**问题**: 绝对定位 / z-index 覆盖层（Drawer、Modal、Popover、Toast）即使已在 DOM 中渲染并可见，`is_visible()` 仍可能返回 `false`。

**根本原因**: Playwright 的 `is_visible()` 基于元素的 CSS 计算样式判断，绝对定位元素在某些情况下不满足其可见性算法。

```python
# ❌ 错误：绝对定位覆盖层 is_visible() 不可靠
if page.locator(".drawer").is_visible():
    do_something()

# ✅ 正确：用 .count() > 0 检测存在性
drawer_open = page.locator(".drawer").count() > 0

# ✅ 更好：利用组件库的状态 CSS 类检测
drawer_open = page.locator(".drawer.opened").count() > 0
drawer_open = page.locator(".drawer[aria-expanded='true']").count() > 0
```

**常见状态 CSS 类**（主流组件库）:

| 组件库 | 覆盖层打开状态类 |
|--------|----------------|
| Alifd/Next | `.next-overlay-wrapper.opened` |
| Ant Design | `.ant-drawer-open`, `.ant-modal-open` |
| Material UI | `[role='dialog']`, `.MuiDrawer-root` |
| 通用 | `[aria-expanded='true']`, `[aria-hidden='false']` |

**判断规则**: 有语义 CSS 类（如 `.opened`）优先于 `.count() > 0`，后者优先于 `is_visible()`。

---

## 规则 2：容器文本匹配精确性

**问题**: `:has-text()` 会递归匹配元素及**所有子元素**的文本内容，当行同时包含 label 和 value 时，value 中的文本也会触发匹配，导致命中错误的行。

**典型场景**: 表格行、设置项行、表单字段行——每行有 label 列和 value 列。

```python
# ❌ 错误：":has-text('Target ROAS')" 会匹配包含该文本的任意祖先容器
page.locator("[class*='settingItem']:has-text('Target ROAS')")

# ✅ 正确：遍历所有行，只对 label 子元素做文本匹配
rows = page.locator("[class*='settingItem']").all()
target_row = None
for row in rows:
    label_el = row.locator("[class*='label'], [class*='title'], th").first
    if label_el.count() > 0:
        label_text = label_el.inner_text().strip().lower()
        if "target roas" in label_text:
            target_row = row
            break
```

**通用原则**:
- 当 label 和 value 共享容器时，永远对 **label 子元素**做文本匹配
- 遍历 + 精确子元素匹配 优于 `:has-text()` 容器匹配
- label 子元素的常见选择器: `[class*='label']`, `[class*='title']`, `[class*='name']`, `th`, `dt`

---

## 规则 10：导航后滚动到目标元素

**问题**: 导航到目标页面后，并等待 `networkidle`，不代表目标内容在视口内可见。如果目标元素在页面中间或下方，截图捕获到的是页首或连管导航，而不是目标设置区域。

**两个层面的问题**:
1. **弹窗覆盖**（参见 Rule 9）：导航后嵌套弹窗出现，截图捕获到弹窗而不是背后的页面
2. **视口外**：目标内容在 DOM 中存在且已渲染，但在覆屏之外，截图截到的是页头而不是目标区域

```python
# ❌ 错误：导航 + networkidle 后立即截图
# 目标内容可能在视口外，截图截到页头
page.goto(url)
page.wait_for_load_state("networkidle")
page.screenshot(...)   # 卓点！可能才是页首

# ✅ 正确：先用 wait_for_selector 确认目标元素已渲染，再 scroll 为可见然后截图
page.goto(url)
page.wait_for_load_state("networkidle")

# 1. 等待目标元素在 DOM 中出现
target = page.wait_for_selector("[class*='targetSection']", timeout=10000)  # 替换为你的目标元素选择器

# 2. 滚动目标元素到视口中央
target.scroll_into_view_if_needed()
page.wait_for_timeout(500)  # 等待滚动动画完成

# 3. 然后截图
page.screenshot(...)
```

**应用场景**:
- 页面加载后需截图展示激活标签页 / 选中设置项的内容
- 母组件不内联展示子组件，需要点击 tab 后内容才渲染
- 长页面的中下部区域（如设置卡、表格行、表单展开器）

**与弹窗问题的组合使用顺序**:
```python
# Step 1: 预填充存储，防止弹窗（Rule 9）
page.add_init_script(preseed_storage_script)

# Step 2: 导航
# 选择 wait_until="domcontentloaded" 而非 "networkidle"，然后手动等待关键元素。
# 原因："networkidle" 在单页应用中可能超时（持续异步请求）或比实际渲染完成要晚。
page.goto(url, wait_until="domcontentloaded")

# Step 3: 关闭遗漏弹窗（Rule 9 兜底）
close_stray_dialogs(page)

# Step 4: 等待目标元素 + 滚动到可见
from playwright.sync_api import Page
target = page.wait_for_selector("[class*='targetSection']", timeout=10000)  # 替换为你的目标元素选择器
target.scroll_into_view_if_needed()
page.wait_for_timeout(500)

# Step 5: 截图
page.screenshot(...)
```

**通用原则**:
- 截图必须在目标元素滚动入视口之后执行，不得依赖时间轮询
- 等待元素用 `wait_for_selector`（语义等待），而不是 `wait_for_timeout`（盲等）
- 滚动后需留出 300-500ms 等待动画结束
- 完整顺序：关闭弹窗 → 等待元素 → 滚动 → 截图

---

## 规则 11：截图前清理非目标覆盖层

**问题**: SPA 中同一路由可能同时存在多个覆盖层（如引导弹窗、系统通知、Cookie Banner、一次性 Onboarding 提示），它们与当前测试步骤无关，但出现在截图里，导致截图无法证明被测功能正常渲染。

**根本原因**: Playwright 使用全新浏览器 context，持久化存储（localStorage）全部为空，导致应用判断为「首次访问」，触发一次性弹窗（通常用 localStorage 记录已展示标记）。此问题与 Rule 9 的持久化存储预填充互补：Rule 9 在导航前预防，Rule 11 是导航后的兜底清理。

**典型症状**: 截图被引导弹窗、营销弹窗或系统通知遮挡，背后的目标页面无法看到。

```python
# ✅ 通用：截图前调用 close_stray_overlays() 清理非目标覆盖层
def close_stray_overlays(page):
    """Close any overlay that is not the current test target.
    Uses common close button selectors that work across most component libraries."""
    closed = page.evaluate("""
        () => {
            // Priority order: semantic close btn → aria-label → class-name patterns
            const selectors = [
                '.next-dialog-close',          // Alifd/Next
                '.ant-modal-close',            // Ant Design
                '[aria-label="close"]',
                '[aria-label="Close"]',
                'button[class*="close"]:not([disabled])',
            ];
            for (const sel of selectors) {
                const btns = Array.from(document.querySelectorAll(sel));
                const visible = btns.find(b => b.offsetParent !== null);
                if (visible) { visible.click(); return sel; }
            }
            return null;
        }
    """)
    if closed:
        page.wait_for_timeout(400)  # wait for close animation
    return closed

# 在每个截图调用前调用（特别是步骤早期，引导弹窗最容易出现）
closed = close_stray_overlays(page)
if closed:
    print(f"  Closed stray overlay via: {closed}")
page.screenshot(path="step_N.png")
```

**何时调用**:
- 截图前（特别是步骤 1、2 等早期步骤）
- 每次 `page.goto()` 或路由切换后
- 测试目标弹窗打开前（避免被其他弹窗干扰点击）

**与 Rule 9 的关系**:
- Rule 9（预防）：在 `add_init_script` 中预填充 localStorage 记录，让应用认为弹窗已展示过，从而不触发
- Rule 11（兜底）：即使预防未覆盖，截图前仍执行一次清理，保证截图内容准确
- 两者配合：先用 Rule 9 减少弹窗出现概率，再用 Rule 11 兜底

**通用原则**:
- 截图前检测并关闭非目标覆盖层是测试基础卫生——任何截图都应反映被测功能，而非测试环境的副作用
- 用语义化选择器（`aria-label`、组件库专属类名）而不是模糊的 `[class*='close']` 全局匹配
- 不要用 `Escape` 关闭（参见 Rule 3：Escape 可能触发导航或 tab 切换）
