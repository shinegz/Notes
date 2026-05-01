# Test-Best-Practices Skill Optimization Design

## Overview

Optimize the testing-best-practices skill (formerly test-guide) to focus on integration and E2E testing capabilities, ensuring reliable reproduction of real user workflows while maintaining test reliability and comprehensive bug detection.

**Status: ✅ COMPLETED** (2026-03-24)

---

## Problem Statement

During testing of the test-guide skill, the following issues were identified:

1. ✅ **RESOLVED** - E2E tests now use `agent-browser` CLI
2. ✅ **RESOLVED** - E2E test code and records are saved to project repo (`tests/e2e/`)
3. ✅ **RESOLVED** - Unit test names follow business narrative naming convention
4. ✅ **RESOLVED** - E2E screenshots saved to `tests/e2e/screenshots/` in project repo
5. ✅ **RESOLVED** - Blocked scenarios are handled gracefully with BLOCKED status, other tests continue

---

## Design Goals

1. ✅ **Focus on integration & E2E testing** - Prioritize real workflow reproduction over unit testing
2. ✅ **Reliable artifact storage** - All E2E artifacts must be saved to project repository
3. ✅ **Graceful blocking handling** - Never give up; try alternatives, record BLOCKED status, continue other tests
4. ✅ **Actionable test reports** - Reports must contain enough information to reproduce and analyze issues
5. ✅ **Best practices integration** - Embed testing golden rules from JavaScript Testing Best Practices

---

## Core Philosophy

```
测试的终极目标是还原用户真实操作流程，确保每个业务场景都被可靠验证。
好的测试既能发现真实 bug，又不会因为测试本身的问题而误报或漏报。
```

### Key Principles

1. **测试必须是可复现的** - Each test can run independently, no uncontrolled external dependencies
2. **测试必须验证真实行为** - Avoid over-mocking that disconnects tests from reality
3. **测试失败必须有明确的修复方向** - Reports must contain sufficient information for developers to locate and fix issues
4. **集成测试优先于单元测试** - When choosing test level, prefer integration tests that verify real interactions

---

## Changes

### 1. ✅ E2E Artifact Storage Specification

**Implemented in**: `references/e2e-testing.md`

**Storage locations (mandatory):**

| Artifact | Path | Purpose |
|----------|------|---------|
| E2E scripts | `tests/e2e/scripts/<feature>.sh` | Repeatable test scripts |
| Screenshots | `tests/e2e/screenshots/<YYYYMMDD>/` | Visual evidence by execution date |
| Test reports | `tests/e2e/reports/<feature>-<YYYYMMDD>.md` | Execution results |
| Auth state | `tests/e2e/.auth-state.json` | Login state cache (not in git) |

**Screenshot workflow:**

1. Create directory: `mkdir -p tests/e2e/screenshots/$(date +%Y%m%d)`
2. Save screenshot: `agent-browser screenshot tests/e2e/screenshots/YYYYMMDD/NN-scenario.png`
3. Verify existence: Immediately `ls` to confirm file exists
4. Reference in report: Use relative path `![](screenshots/YYYYMMDD/NN-scenario.png)`

**Prohibited actions:**

- ❌ Save to IDE temp directories, system temp, or user directories
- ❌ Reference non-existent screenshots in reports
- ❌ Use absolute paths for screenshot references

---

### 2. ✅ Blocked E2E Scenario Handling (Local Dev Environment)

**Implemented in**: `references/e2e-testing.md` - "阻塞场景处理" section

**Blocking levels:**

| Level | Definition | Example | Handling |
|-------|------------|---------|----------|
| L1-Bypassable | Non-critical path issue | Secondary UI element not rendered | Skip assertion, continue |
| L2-Waitable | Timing issue | Element loading slowly | Retry/wait, continue |
| L3-Debuggable | Locator issue | Wrong selector/path | Record, attempt fix, retry |
| L4-Environment | Environment unavailable | Dev server not started | Record, prompt user |

**Handling flow:**

```
遇到阻塞
    │
    ▼
元素未找到？
    │
    ├─是─► 尝试重新 snapshot ──► 仍找不到？
    │                            │
    │                            ├─是─► 检查 selector 是否正确
    │                            │        │
    │                            │        ├─错误─► 修复 selector，重试
    │                            │        └─正确─► 记录为 BLOCKED（UI 未完成？）
    │                            │
    │                            └─否─► 继续测试
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

**BLOCKED record format:**

```markdown
### 场景: [场景名称]

- **状态**: 🔒 BLOCKED
- **阻塞点**: [具体操作，如"点击提交按钮"]
- **阻塞原因**: [如"元素 #submit-btn 未找到"]
- **已尝试**: [已尝试的解决方式]
- **截图**: ![阻塞点](screenshots/YYYYMMDD/NN-blocked.png)
- **可能原因**: [UI 未完成 / selector 需更新 / 其他]
```

**Core principles:**

- ✅ Each block must attempt at least 2 solutions
- ✅ Continue testing other independent scenarios after blocking
- ✅ Record complete debugging information
- ❌ Never give up entire test directly

---

### 3. ✅ Test Report Format

**Implemented in**: `references/e2e-testing.md` - "E2E 测试产物" section

**Report file naming:** `tests/e2e/reports/<功能名>-<YYYYMMDD>.md`

**Report template:**

```markdown
# 测试报告：[功能名]

**执行日期**: YYYY-MM-DD HH:mm
**测试环境**: 本地开发环境 (https://localhost:9000/)
**执行者**: Agent (testing-best-practices skill)

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
  3. ...
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
- **解除建议**: [如何解除阻塞]

---

## 截图清单

| 文件名 | 验证内容 | 状态 |
|-------|---------|------|
| 01-page-loaded.png | 页面加载成功 | ✅ |
| 02-submit-click.png | 点击提交按钮 | ❌ 失败 |

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

**Report requirements (mandatory):**

- ✅ Each failed scenario must include: operation steps, expected, actual, screenshot, reproduction command
- ✅ Screenshots must be referenced via Markdown in report
- ✅ Screenshots must actually exist in `tests/e2e/screenshots/` directory
- ✅ Discovered issues must be classified by severity
- ❌ No vague references like "see screenshot above"

---

### 4. ✅ Best Practices Integration

**Implemented in**: `SKILL.md` (inline golden rules) + reference files

**Golden Rules (inline in SKILL.md):**

```
## 测试黄金法则

### 测试代码设计原则

1. **测试代码要"瘦"** - 简单、短小、扁平、无抽象。测试代码应让人一眼看出目的
2. **AAA 模式** - 每个测试分为三段：准备、执行、断言
3. **黑盒测试** - 只测 public 方法，不测内部实现细节
4. **一个测试一个断言焦点** - 每个测试验证一个行为

### 测试命名规范

**三元命名法**：测试名称必须包含三部分
1. 被测什么
2. 在什么条件下
3. 期望什么结果

❌ it('returns correct object')
✅ it('When no price is specified, then the product status is pending approval')

### 集成测试原则

1. **让真实代码交互** - 最小化 mock，让实际模块协作
2. **控制边界** - 明确什么真实、什么 mock
3. **测试完整流程** - 从用户视角测试请求到响应的完整链路

### E2E 测试原则

1. **测试关键用户旅程** - 不追求全覆盖，聚焦核心业务流
2. **数据隔离** - 每个测试创建自己的数据
3. **等待而非 sleep** - 使用显式等待，不用固定延时
4. **线性测试** - 一个测试一个流程，避免"超级测试"
```

**Best practices distributed to existing reference files:**

| 内容 | 目标文件 |
|------|----------|
| 测试代码"瘦"原则、AAA 模式、黑盒测试、单断言焦点 | `unit-testing.md` |
| 三元命名法 | `unit-testing.md`（已有业务叙事命名，补充三元命名法） |
| Stub vs Spy vs Mock 选择指南 | `test-quality.md` |
| E2E 原则（关键旅程、数据隔离、等待而非 sleep、线性测试） | `integration-e2e.md` |
| Flaky test 预防策略 | `integration-e2e.md` |

**文档语言要求：** 所有参考文档使用中文（专业术语如 AAA、stub、spy、mock 等保持英文）

---

## Files Modified

| File | Status | Changes |
|------|--------|--------|
| `SKILL.md` | ✅ Done | Added golden rules, E2E workflow, blocking handling, report format |
| `INTRODUCTION.md` | ✅ Done | Synced with SKILL.md changes |
| `references/e2e-testing.md` | ✅ Done | E2E 原则、阻塞处理、Flaky 预防、产物规范 |
| `references/unit-testing.md` | ✅ Done | 黄金法则、AAA 模式、三元命名法、业务叙事命名、JSDoc 规范 |
| `references/test-quality.md` | ✅ Done | Stub/Spy/Mock 选择指南、测试数据管理 |
| `references/ci-coverage-performance.md` | ✅ Kept | CI/coverage guidance still relevant |

---

## Success Criteria

| # | Criterion | Status |
|---|-----------|--------|
| 1 | Skill renamed from "test-guide" to "testing-best-practices" | ✅ Done |
| 2 | All E2E artifacts (scripts, screenshots, reports) saved to project repository | ✅ Done |
| 3 | Blocked scenarios are properly recorded and other tests continue | ✅ Done |
| 4 | Test reports contain actionable information for issue reproduction | ✅ Done |
| 5 | Agent follows testing golden rules without explicit prompting | ✅ Done |
| 6 | All reference files optimized with best practices and converted to Chinese | ✅ Done |

---

## Implementation Summary

### Current Skill Structure

```
testing-best-practices/
├── SKILL.md              # Core workflow + golden rules (inline)
├── INTRODUCTION.md       # Human-readable navigation (Chinese)
└── references/
    ├── unit-testing.md   # 单元测试策略、业务叙事命名、JSDoc、边界值、快照、属性测试
    ├── integration-testing.md  # 集成测试策略、API测试、契约测试
    ├── e2e-testing.md    # E2E原则、agent-browser工作流、阻塞处理、Flaky预防
    ├── test-quality.md   # Mock策略、Stub/Spy/Mock选择、测试数据、隔离
    └── ci-coverage-performance.md  # 覆盖率、CI、性能测试
```

### Key Design Decisions

1. **Golden Rules in SKILL.md** - Core principles (瘦测试、AAA、三元命名、黑盒) inline for immediate visibility
2. **Reference Files for Depth** - Detailed guidance loaded on-demand per test type
3. **Chinese Language** - All outputs in Chinese per user preference
4. **E2E Environment Constraint** - Limited to local dev environment (`https://localhost:9000/`)
5. **agent-browser CLI Required** - E2E tests must actually execute, not just script

### Integration with Other Skills

- **webapp-testing**: Can be used as execution tool for E2E browser automation
  - `with_server.py` for server lifecycle management
  - Playwright scripts for reconnaissance and interaction
  - Screenshot capture for evidence
