# E2E 测试指南

本文档提供端到端测试的深入指导。当测试计划涉及完整用户流程、跨页面交互或关键业务旅程时，加载此参考。

> **通用测试原则**（黄金法则、AAA 模式、三元命名法、黑盒测试）见 `SKILL.md`，适用于所有测试类型。

---

## 目录

- [什么是 E2E 测试](#什么是-e2e-测试)
- [何时选择 E2E 测试](#何时选择-e2e-测试)
- [工具要求：agent-browser](#工具要求agent-browser)
- [E2E 测试原则](#e2e-测试原则)
- [冒烟测试](#冒烟测试)
- [Local Dev 环境：用 Mock 控制所有状态](#local-dev-环境用-mock-控制所有状态)
- [性能优化：复用登录态](#性能优化复用登录态)
- [Flaky Test 预防](#flaky-test-预防)
- [Mock 数据迭代循环](#mock-数据迭代循环强制要求)
- [阻塞场景处理](#阻塞场景处理)
- [E2E 测试产物](#e2e-测试产物)
- [常见陷阱](#常见陷阱)

---

## 什么是 E2E 测试

E2E 测试模拟真实用户与完整应用的交互。它们慢、易脆、昂贵——但它们是**唯一验证系统整体工作**的测试。谨慎用于关键用户旅程。

### E2E vs 集成测试

| 特性 | 集成测试 | E2E 测试 |
|------|----------|----------|
| 速度 | 快（秒级） | 慢（分钟级） |
| 环境 | 可 mock 边界 | 真实浏览器/环境 |
| 覆盖 | 模块间协作 | 完整用户旅程 |
| 维护成本 | 中 | 高 |
| 信心程度 | 中 | 高 |

---

## 何时选择 E2E 测试

| 场景 | 推荐 |
|------|------|
| 用户从产品页到确认页完成结账 | E2E |
| 多步向导在页面导航间保持状态 | E2E |
| 登录 → 仪表盘 → 创建项目 → 验证项目出现 | E2E |
| 跨系统的流程 | E2E |

### 选择要测试的用户旅程

不要尝试 E2E 测试所有内容——太慢太脆弱。聚焦：

1. **关键业务流程**——如果损坏意味着收入损失或用户流失的路径
2. **跨系统的流程**——集成测试无法覆盖的、需要完整技术栈的流程
3. **回归易发的流程**——历史上经常损坏且低层测试覆盖不足的路径

---

## 工具要求：agent-browser

E2E 测试**必须使用 `agent-browser` CLI**执行。它提供 AI 驱动的浏览器自动化，通过视觉理解和可访问性树而非脆弱的 CSS 选择器进行交互。

**安装检查：**
```bash
which agent-browser || npm i -g agent-browser
```

**强制执行模型：** E2E 测试如果只写成脚本不算完成。它们必须在 Phase 2 工作流中通过 `run_in_terminal` **执行**。截图和报告必须保存到仓库。

### agent-browser E2E 工作流

```bash
# 1. 打开应用（本地开发使用 --ignore-https-errors）
agent-browser --ignore-https-errors open https://localhost:9000/
agent-browser wait --load networkidle

# 2. 快照交互元素
agent-browser snapshot -i
# 输出：@e1, @e2 ... refs 有效直到下次页面变化

# 3. 使用 refs 交互
agent-browser click @e3
agent-browser fill @e5 "search query"
agent-browser wait --text "Results"

# 4. 在每个关键断言点捕获证据
agent-browser screenshot tests/e2e/screenshots/YYYYMMDD/01-scenario.png

# 5. 导航或 DOM 变化后重新快照
agent-browser snapshot -i   # refs 现在刷新了
```

### 前端 SPA 的关键模式

```bash
# 导航 SPA 路由（hash 路由常见）
agent-browser open https://localhost:9000/#!/campaign/create
agent-browser wait --load networkidle

# 等待特定文本出现（用于异步数据加载）
agent-browser wait --text "Sponsored_Max"

# 通过 CSS 选择器等待元素
agent-browser wait "[data-testid=campaign-name]"

# 验证文本内容
agent-browser get text @e5

# 滚动测试 sticky header 行为
agent-browser scroll down 500
agent-browser screenshot tests/e2e/screenshots/YYYYMMDD/sticky-header.png

# 复用已登录的浏览器 session（避免每次重新登录）
agent-browser --auto-connect state save tests/e2e/.auth-state.json
agent-browser --state tests/e2e/.auth-state.json open https://localhost:9000/
```

---

## Local Dev 环境：用 Mock 控制所有状态

> **核心认知：在 local dev 环境下测试，不存在「需要特定测试账号」这一说。** 所有用户状态——账号角色、权限开关、弹窗可见条件——都通过 mock 控制，而不是切换真实账号。

用户可见的分支行为（如新/老用户、有/无数据、不同权限角色、弹窗优先级等）全部由以下来源决定：

| 状态类型 | 控制位置 | Mock 方式 |
|---------|---------|----------|
| 用户身份 / 权限字段 | 内存中的 auth 对象 | 拦截登录接口返回值，或通过 `evaluate` 注入 |
| API 响应（列表数据、开关状态等） | 网络请求 | MSW / dev server proxy mock 返回 |
| 本地存储标记（如弹窗已展示记录） | `localStorage` | `agent-browser evaluate` 直接写入 |
| 功能权限开关 | 内存 | 拦截权限接口或直接注入 |

### 分支场景测试策略

**规则：场景差异 = 分支逻辑差异，优先用 mock 区分，而不是切换账号。**

```bash
# 示例：模拟『已登录 + 特定用户状态』场景
# ① 先登录（任意账号），保存 session
agent-browser --auto-connect state save tests/e2e/.auth-state.json

# ② 复用 session 打开页面
agent-browser --state tests/e2e/.auth-state.json --ignore-https-errors open https://localhost:9000/
agent-browser wait --load networkidle

# ③ 注入 mock 状态（而不是换账号）
agent-browser evaluate "localStorage.setItem('someFeatureFlag', 'true')"
# dev server mock 层返回目标分支所需的 API 数据
```

---

## E2E 测试原则

### 1. 测试关键用户旅程

不追求全覆盖，聚焦核心业务流。

**优先级判断：**
- 这条路径如果损坏，会造成直接业务损失吗？
- 这条路径是否涉及多个系统或复杂状态？
- 这条路径是否有历史 bug？

### 2. 数据隔离

每个测试管理自己的状态，不依赖其他测试运行留下的数据。

**在 local dev 环境下的实现方式：**
- 通过 mock 层控制 API 返回数据，每个测试按需配置
- 通过 `agent-browser evaluate` 在测试前重置 `localStorage` / 内存状态
- 永远不依赖之前测试运行留下的副作用（如残留的表单数据、弹窗记录）

### 3. 等待而非 sleep

使用显式等待，不用固定延时。

**为什么：**
- 固定 `sleep` 太慢（等待最坏情况）
- 又太脆弱（页面加载更慢时仍会失败）

**正确做法：**
```bash
# 等待元素出现
agent-browser wait --text "Results"

# 等待网络空闲
agent-browser wait --load networkidle

# 等待特定元素
agent-browser wait "[data-testid=campaign-name]"
```

### 4. 线性测试

一个测试一个流程，避免"超级测试"。

**问题：** 一个测试导航 10 个页面并断言所有内容。如果在步骤 7 失败，你不知道哪里出了问题。

**正确做法：**
- 一个测试验证一个用户旅程
- 测试名称清楚描述验证什么
- 失败时能立即定位问题

---

## 冒烟测试

冒烟测试是一种快速的完整性检查，遍历应用主要页面，确保没有明显损坏。

### 网站地图遍历示例

```bash
# agent-browser 冒烟测试
agent-browser --ignore-https-errors open https://localhost:9000/
agent-browser wait --text "Dashboard"

agent-browser open https://localhost:9000/#!/campaign
agent-browser wait --text "Campaign"

agent-browser open https://localhost:9000/#!/settings
agent-browser wait --text "Settings"
```

### 冒烟测试的价值

| 发现问题 | 传统测试 | 冒烟测试 |
|----------|----------|----------|
| 部署失败 | ❌ 可能遗漏 | ✅ 立即发现 |
| 路由损坏 | ❌ 单测无法覆盖 | ✅ 遍历发现 |
| CDN/资源加载失败 | ❌ 需要专门测试 | ✅ 自然捕获 |

---

## 性能优化：复用登录态

在 local dev 环境下，登录操作可能耗时较长。通过保存 session 并复用，避免每条测试都重新登录。

### 推荐方式：agent-browser session 复用

```bash
# 第一步：登录一次，保存 session
agent-browser --auto-connect state save tests/e2e/.auth-state.json

# 后续所有测试直接复用，无需重新登录
agent-browser --state tests/e2e/.auth-state.json --ignore-https-errors open https://localhost:9000/
agent-browser wait --load networkidle
```

### 注意事项

| 考虑点 | 建议 |
|--------|------|
| 测试隔离 | 复用 session 不意味着共享状态——每条测试的业务数据通过 mock 独立控制 |
| 并行测试 | 每个并行 worker 保存独立的 session 文件 |
| 权限分支测试 | 不同权限的场景通过 mock 注入进行区分，而不是切换账号 |
| 安全性 | `tests/e2e/.auth-state.json` 不入 git，加入 `.gitignore` |

---

## Flaky Test 预防

Flaky 测试会侵蚀对整个测试套件的信心，必须立即修复。

| 原因 | 解决方案 |
|------|---------|
| 时序问题 | 使用显式等待（`wait --text`、`wait --load networkidle`）|
| 测试顺序依赖 | 隔离测试数据，每个测试通过 mock 独立控制状态 |
| 共享状态 | 每个测试创建自己的数据 |
| 网络变化 | 使用适合 CI 的超时设置 |

---

## ⚠️ Mock 数据迭代循环（强制要求）

### 核心原则：禁止直接标记 BLOCKED 后放弃

**当 E2E 执行过程中发现 mock 数据方案不对或不足时，必须重新生成 mock 方案并重试，而不是选择直接结束。**

Mock 数据不是一次性的计划文档，而是需要根据实际执行反馈不断迭代的活数据。测试脚本执行的过程本身就是验证 mock 数据是否正确的过程。

### 迭代循环流程

```
E2E 场景执行
    │
    ▼
遇到阻塞（如 UI 未出现）
    │
    ▼
分析阻塞原因
    │
    ├─ UI bug ──────────────────────► 记录 bug，继续其他场景
    │
    │
    ├─ Mock 数据缺失/错误 ────────► 【触发迭代】
    │   │                         │
    │   │                         ▼
    │   │                    更新 Mock 数据清单
    │   │                    （补充缺失场景/修正错误数据）
    │   │                         │
    │   │                         ▼
    │   │                    重新执行该场景
    │   │                    （最多重试 2 次）
    │   │                         │
    │   │                         ├─ 成功 ──► 继续测试
    │   │                         └─ 失败 ──► 记录 BLOCKED + 已尝试的 mock 方案
    │   │
    ├─ Selector 问题 ──────────────► 修复 selector，重试
    │
    └─ 环境问题 ───────────────────► 提示用户，等待解决
```

### Mock 数据迭代检查点

当阻塞发生时，首先检查以下 mock 数据是否完整：

| 检查项 | 说明 | 典型遗漏 |
|--------|------|----------|
| API 响应结构 | 字段是否完整、嵌套层级是否正确 | 可选字段缺失、枚举值不全 |
| 用户权限状态 | 是否注入了正确的权限标记 | 管理员权限、功能开关 |
| 业务数据状态 | 是否模拟了所需的业务前置条件 | 已存在的数据、历史记录 |
| UI 状态依赖 | localStorage、sessionStorage | 弹窗关闭标记、引导完成标记 |
| 时序依赖 | 数据是否在正确时机可用 | 异步加载状态、竞态条件 |

### 迭代示例

**场景**：测试「用户设置页面」

**初始 Mock**：
```json
{
  "GET /api/user/settings": { "theme": "light" }
}
```

**执行结果**：页面显示空白，设置表单未渲染。

**分析**：设置页面需要用户权限字段才能渲染表单，mock 缺少 `permissions` 字段。

**迭代 Mock**：
```json
{
  "GET /api/user/settings": {
    "theme": "light",
    "permissions": ["read", "write"]
  }
}
```

**重新执行**：成功渲染设置表单。

### 禁止的行为

- ❌ 遇到阻塞直接标记 `BLOCKED` 并继续下一个场景
- ❌ 归咎于「账号问题」或「数据问题」而不尝试修正 mock
- ❌ 说「这个场景需要老用户账号」而不通过 mock 注入状态
- ❌ Mock 方案一次失败后就放弃

### 强制要求

- ✅ 每个阻塞必须至少尝试 **1 次重新生成 mock 并重试**
- ✅ 更新后的 mock 数据清单必须记录在报告中
- ✅ 最终 BLOCKED 的场景必须在报告中说明「已尝试的 mock 方案」

---

## 阻塞场景处理

### 阻塞级别

| 级别 | 定义 | 示例 | 处理方式 |
|-----|------|------|----------|
| L1-可绕过 | 非关键路径问题 | 次要 UI 元素未渲染 | 跳过该断言，继续测试 |
| L2-可等待 | 时序问题 | 元素加载慢 | 增加重试/等待，继续测试 |
| L3-需调试 | 定位问题 | selector 写错 | 记录问题，尝试修复后重试 |
| L4-环境阻塞 | 环境不可用 | dev server 未启动 | 记录环境问题，提示用户 |
| L5-Mock 不完整 | Mock 数据缺失/错误 | 权限未注入导致 UI 未出现 | **更新 Mock，重试** |

### 处理流程

```
遇到阻塞
    │
    ▼
UI 元素未出现？
    │
    ├─是─► 检查 Mock 数据是否完整注入 ──► Mock 缺失？
    │                                    │
    │                                    ├─是─► 更新 Mock 数据清单
    │                                    │      │
    │                                    │      ▼
    │                                    │    重新执行该场景（最多 2 次）
    │                                    │      │
    │                                    │      ├─ 成功 ──► 继续测试
    │                                    │      └─ 失败 ──► 记录 BLOCKED + 已尝试的 mock 方案
    │                                    │
    │                                    └─否─► 尝试重新 snapshot
    │                                           │
    │                                           ├─ 找到元素 ──► 继续测试
    │                                           └─ 仍找不到 ──► 检查 selector
    │
    └─否─► 页面加载失败？
              │
              ├─是─► 检查 dev server ──► 未启动？提示用户启动
              │                        └─已启动？检查 URL 路径
              │
              └─否─► 超时？
                        │
                        ├─是─► 增加等待时间，重试
                        └─否─► 记录详细错误信息，继续其他场景
```

### 处理原则

- ✅ 每个阻塞必须尝试至少 2 种解决方案
- ✅ 阻塞后继续测试其他独立场景
- ✅ 记录完整的调试信息供后续分析
- ❌ 禁止直接放弃整个测试

### BLOCKED 记录格式

```markdown
### 场景: [场景名称]

- **状态**: 🔒 BLOCKED
- **阻塞点**: [具体操作，如"点击提交按钮"]
- **阻塞原因**: [原因分析，如"元素 #submit-btn 未找到"]
- **已尝试**: [已尝试的解决方式]
- **截图**: ![阻塞截图](screenshots/YYYYMMDD/NN-blocked.png)
- **可能原因**: [UI 未完成 / selector 需更新 / 其他]
```

---

## E2E 测试产物

### 必须保存到仓库

| 产物 | 位置 | 用途 |
|------|------|------|
| 脚本文件 | `tests/e2e/scripts/<功能名>.sh` | 可重复执行 |
| 截图 | `tests/e2e/screenshots/<YYYYMMDD>/` | 视觉证据 |
| 测试报告 | `tests/e2e/reports/<功能名>-e2e-<YYYYMMDD>.md` | PASS/FAIL 历史 |
| 认证状态 | `tests/e2e/.auth-state.json` | 登录态缓存（不入 git） |

### 脚本文件模板

```sh
#!/bin/bash
# E2E Test: [功能名]
# Feature: [功能描述]
# Business behaviors tested:
#   1. [行为 1]
#   2. [行为 2]
# Re-run: bash tests/e2e/scripts/<功能名>.sh

set -e
SS="tests/e2e/screenshots/$(date +%Y%m%d)"
mkdir -p "$SS"

echo "[1/N] Testing..."
agent-browser --ignore-https-errors open https://localhost:9000/
agent-browser wait --load networkidle
agent-browser screenshot "$SS/01-scenario.png"
# ... 其他测试步骤
```

### 截图保存流程

1. 创建目录：`mkdir -p tests/e2e/screenshots/$(date +%Y%m%d)`
2. 保存截图：`agent-browser screenshot tests/e2e/screenshots/YYYYMMDD/NN-scenario.png`
3. 验证存在：`ls tests/e2e/screenshots/YYYYMMDD/` 确认文件真实存在
4. 报告引用：使用相对路径 `![](screenshots/YYYYMMDD/NN-scenario.png)`

**禁止行为**：
- ❌ 保存到 IDE 临时目录、系统临时目录、用户目录
- ❌ 在报告中引用不存在的截图
- ❌ 使用绝对路径引用截图

### E2E 报告模板

```markdown
# 测试报告：[功能名]

**执行日期**: YYYY-MM-DD HH:mm
**测试环境**: 本地开发环境 (https://localhost:9000/)
**执行者**: Agent

---

## 汇总

| 指标 | 数值 |
|-----|------|
| 总用例数 | X |
| 通过 | X |
| 失败 | X |
| 阻塞 | X |

---

## 详细结果

### ✅ 通过场景

| # | 场景描述 | 截图 |
|---|---------|------|
| 1 | [业务行为描述] | [截图链接] |

---

### ❌ 失败场景

#### 场景 N: [场景名称]

- **业务行为**: [用用户视角描述这条测试在验证什么]
- **操作步骤**:
  1. 访问 `/path/to/page`
  2. 点击 [元素名称]
- **预期结果**: [应该发生什么]
- **实际结果**: [实际发生了什么]
- **失败原因**: [具体错误信息]
- **截图**: ![失败截图](screenshots/YYYYMMDD/NN-failed.png)
- **复现命令**: `agent-browser --ignore-https-errors open https://localhost:9000/#!/path`

---

### 🔒 阻塞场景

#### 场景 M: [场景名称]

- **阻塞点**: [具体操作]
- **阻塞原因**: [原因分析]
- **已尝试方案**: [尝试过的解决方式]
- **截图**: ![阻塞截图](screenshots/YYYYMMDD/NN-blocked.png)

---

## 截图清单

| 文件名 | 验证内容 | 状态 |
|-------|---------|------|
| 01-page-loaded.png | 页面加载成功 | ✅ |

---

## 发现的问题

| # | 问题描述 | 严重程度 | 相关场景 | 截图 |
|---|---------|---------|---------|------|
| 1 | [具体 bug 描述] | 高/中/低 | 场景 N | [链接] |

---

## 执行命令

```bash
# 重新执行测试
bash tests/e2e/scripts/<功能名>.sh
```
```

**报告要求**：
- 每个失败场景必须包含：操作步骤、预期、实际、截图、复现命令
- 截图必须真实存在于 `tests/e2e/screenshots/` 目录
- 发现的问题按严重程度分类

---

## 常见陷阱

### 在一个 E2E 测试中测试太多

当它失败时，你不知道哪里出了问题。保持 E2E 测试聚焦于一个旅程。

### 容忍 flaky 测试

不要把 flaky 测试标记为"skip"或"known flaky"然后继续。修复根因。Flaky 测试侵蚀对整个测试套件的信心。

### 慢测试套件

如果 E2E 套件太慢，开发者会停止运行它。并行化、将测试移到最低适当层级。

### 不测试错误路径

Happy path E2E 测试给人错误信心。每个旅程至少测试一个关键失败场景（网络错误、auth 过期、server 500）。

### 用账号状态区分场景（而不是 mock）

**错误做法**：为每种用户状态（新客/老客、有权限/无权限等）备一个真实测试账号，切换账号来覆盖分支。

**正确做法**：任意账号登录一次，保存 session，通过 mock 注入切换用户状态。分支逻辑等价于展示在单元/集成测试中。E2E 只需要验证 UI 层的最终渲染结果。
