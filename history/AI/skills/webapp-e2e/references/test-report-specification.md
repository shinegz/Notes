# 测试报告规范

> 本规范定义了 E2E 测试报告的格式要求，包含成功和失败的测试结果。

---

## 1. 核心原则

测试报告的目标是让 AI Coding Agent 能够：
1. **确认正确实现** - 明确哪些功能已正确实现，避免重复修改
2. **快速定位问题** - 精确到文件、函数、行号
3. **理解差异** - 明确预期结果与实际结果的差距
4. **复现问题** - 提供足够的上下文信息
5. **验证修复** - 提供验证修复的方法

---

## 2. 报告结构概览

```markdown
# 测试报告

## 测试摘要
| 指标 | 数值 |
|------|------|
| 测试场景总数 | X |
| 通过 | X |
| 失败 | X |
| 阻塞 | X |

## 成功的测试
[详细的成功测试列表]

## 失败的测试
[详细的失败测试列表]
```

---

## 3. 测试摘要格式

```markdown
## 测试摘要

| 指标 | 数值 | 说明 |
|------|------|------|
| 测试场景总数 | X | 所有测试场景 |
| ✅ 通过 | X | 完全通过 |
| ⚠️ 部分通过 | X | 部分步骤通过 |
| ❌ 失败 | X | 主要步骤失败 |
| 🔒 阻塞 | X | 无法执行（依赖问题） |

### 测试环境
- **前端服务**: localhost:9000 (HTTPS)
- **浏览器**: Chrome/agent-browser
- **测试时间**: YYYY-MM-DD HH:mm:ss

### 核心发现
- **正确实现**: [已验证正确的功能列表]
- **需要修复**: [需要修复的问题列表]
- **环境问题**: [环境相关的阻塞问题]
```

---

# 4. 成功测试报告格式

截图必须**内联**在对应步骤旁边，不得单独列在"截图证据"表格中。

```markdown
### ✅ [场景标识]: [场景名称]

**测试状态**: 通过

| 步骤 | 操作 | 预期结果 | 实际结果 | 状态 |
|------|------|----------|----------|------|
| 1 | [操作描述] | [预期] | ✅ [实际] | ✅ |
| 2 | [操作描述] | [预期] | ✅ [实际] | ✅ |

**步骤截图**（按步骤顺序，内联显示）:

**步骤 1**: 导航到目标页面
![step1 - 页面加载](tests/e2e/screenshots/[场景ID]_[YYYYMMDD]/step01_navigation.png)

**步骤 2**: [操作描述]
![step2 - 功能验证](tests/e2e/screenshots/[场景ID]_[YYYYMMDD]/step02_campaign_list.png)

**已验证的正确实现**:
- ✅ [组件/功能]: [验证的具体行为]

**涉及文件**:
- `path/to/file1.tsx` - [功能说明]
```

**内联截图格式要求**:
- 使用 Markdown 图片语法 `![描述](路径)` 直接展示，而非仅列出路径
- 每张截图前写一行加粗的步骤标题，说明截图内容
- 截图顺序与步骤顺序一致

---

## 5. 失败测试报告格式

```markdown
### ❌ [场景标识]: [场景名称]

**测试状态**: 失败 / 部分通过

| 步骤 | 操作 | 预期结果 | 实际结果 | 状态 |
|------|------|----------|----------|------|
| 1 | [操作描述] | [预期] | ✅ [实际] | ✅ |
| 2 | [操作描述] | [预期] | ❌ [实际] | ❌ |

**失败步骤截图**（内联显示）:

**步骤 2 失败状态**:
![step2 失败 - 元素未找到](tests/e2e/screenshots/[场景ID]_[YYYYMMDD]/step02_failed.png)

**失败步骤详情**:
- **失败步骤**: [步骤编号 - 描述]
- **错误类型**: UI / Logic / API / Network / Data

**问题描述**:
- **预期结果**: [期望的行为]
- **实际结果**: [观察到的行为]
```

---

## 6. 截图目录命名规范

截图目录名称必须与测试脚本和报告文件名**完全对齐**——三者共享同一个前缀，包含场景 ID、场景名称和日期，便于快速关联。

**命名格式**:
```
tests/e2e/screenshots/[SceneID]_[scene_name]_[YYYYMMDD]/
```

**三者对应关系**（前缀必须完全一致）:

| 测试脚本 | 截图目录 | 测试报告 |
|----------|----------|----------|
| `test_e3_am_campaign_list.py` | `screenshots/E3_am_campaign_list_20260330/` | `E3_am_campaign_list_20260330.md` |
| `test_e1_new_customer.py` | `screenshots/E1_new_customer_20260327/` | `E1_new_customer_20260327.md` |

**截图文件命名**:
```
step[NN]_[描述].png
```
示例: `step01_navigation.png`, `step04_copy_toast.png`

> ⚠️ **文件名不含时间戳**。每次运行同名文件直接覆盖，每次运行前必须先清空截图目录。这样每次运行我就是一套截图，不会堆积重复文件。

**生成截图时的代码约定**:
```python
SCENE_ID = "E3_am_campaign_list"  # 与脚本名、报告名前缀保持一致
today_str = datetime.now().strftime("%Y%m%d")
SCREENSHOTS_DIR = Path(f"tests/e2e/screenshots/{SCENE_ID}_{today_str}")
# 报告中的图片引用路径（相对于 workspace root）
SCREENSHOTS_REL = f"tests/e2e/screenshots/{SCENE_ID}_{today_str}"


def init_screenshots_dir():
    """run_test() 开头调用：清空并重建截图目录，确保每次运行只有一套截图"""
    import shutil
    if SCREENSHOTS_DIR.exists():
        shutil.rmtree(SCREENSHOTS_DIR)
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)


def take_screenshot(page, step_name: str) -> str:
    """save screenshot, return workspace-relative path for use in report markdown"""
    filename = f"{step_name}.png"  # 不含时间戳，重覆盖
    filepath = SCREENSHOTS_DIR / filename
    page.screenshot(path=str(filepath), full_page=False)
    return f"{SCREENSHOTS_REL}/{filename}"  # workspace-relative, 直接用于 markdown
```

**报告中的图片路径格式**:
```markdown
<!-- ✅ 正确：workspace-relative 路径，相对于 workspace root -->
![step1 - 页面加载](tests/e2e/screenshots/E3_am_campaign_list_20260330/step01_navigation.png)

<!-- ❌ 错误：绝对路径， markdown 渲染器无法识别 -->
![step1](file:///absolute/path/to/screenshots/step01_navigation.png)

<!-- ❌ 错误：相对于报告文件的路径，在 workspace 根面板无法解析 -->
![step1](../screenshots/E3_am_campaign_list_20260330/step01_navigation.png)
```

> 图片路径必须是 **workspace-relative**（相对于项目根目录）。VS Code 等 markdown 渲染器将其解析为项目内的绝对路径。`take_screenshot()` 的返回值就是这种格式，直接嵌入报告。

---

## 7. 常见错误类型分类

| 错误类型 | 特征 |
|----------|------|
| **UI** | 元素未找到、点击无响应、显示异常 |
| **Logic** | 条件判断错误、状态管理问题 |
| **API** | 请求失败、响应格式错误、超时 |
| **Network** | 连接失败、CORS、证书错误 |
| **Data** | 数据格式错误、空值处理 |
