# Collect session — AI E2E Testing 知识体系构建

- **Goal**: 系统收集 AI Agent 时代下 Web E2E 测试的权威理论与实践资料，为打造高质量的 web-e2e-testing skill 建立知识基础
- **Default shelf**: `agent`（拟落于 `raw/agent/e2e-testing/`；如后续测试知识持续扩展，可升级为新门类 `software-testing`）
- **Created**: 2026-04-22

## Candidate sources（待你确认）

### 一、E2E 测试核心理念与哲学（ foundational theory ）

| OK | Type | URL 或路径 | 建议 shelf | 建议 raw 子路径 | 一行理由 |
|----|------|------------|------------|-----------------|----------|
| [x] | blog | https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html | agent | `articles/google-just-say-no-to-e2e.md` | Google 官方经典文：E2E 测试的陷阱、反馈循环理论、70/20/10 测试比例原则 |
| [x] | blog | https://martinfowler.com/articles/practical-test-pyramid.html | agent | `articles/martin-fowler-test-pyramid.md` | 测试金字塔奠基文：单元/集成/E2E 的分层哲学与成本分析 |
| [x] | blog | https://www.ibm.com/think/insights/end-to-end-testing-best-practices | agent | `articles/ibm-e2e-best-practices.md` | 企业级 E2E 最佳实践：用户旅程优先、测试环境管理、左移策略 |
| [x] | blog | https://www.bunnyshell.com/blog/best-practices-for-end-to-end-testing-in-2025/ | agent | `articles/bunnyshell-e2e-best-practices-2025.md` | 2025 年 E2E 测试全景：优先级规划、持续自动化、可观测性 |

### 二、现代 E2E 工具与模式（ modern tooling & patterns ）

| OK | Type | URL 或路径 | 建议 shelf | 建议 raw 子路径 | 一行理由 |
|----|------|------------|------------|-----------------|----------|
| [x] | doc | https://playwright.dev/docs/best-practices | agent | `articles/playwright-official-best-practices.md` | Playwright 官方最佳实践：用户可见行为测试、隔离性、Locator 策略、Web-first assertions |
| [x] | blog | https://www.weekly.playwright-user-event.org/tip-12-test-data-strategies-for-e2e-tests | agent | `articles/playwright-test-data-strategies.md` | Playwright 官方社区测试数据策略：E2E 中何时 mock、何时用真实数据 |
| [x] | doc | https://mswjs.io/docs/best-practices/ | agent | `articles/msw-best-practices.md` | Mock Service Worker 官方最佳实践：网络层 mocking 的标准做法，与 Playwright 集成方案 |
| [x] | blog | https://dev.to/olhapi/playwright-e2e-testing-cheatsheet-15gl | agent | `articles/playwright-e2e-cheatsheet.md` | Playwright E2E 速查与反模式：现代测试方法 vs 常见陷阱 |

### 三、AI Agent 时代的 E2E 测试（ AI-agent-centric testing ）

| OK | Type | URL 或路径 | 建议 shelf | 建议 raw 子路径 | 一行理由 |
|----|------|------------|------------|-----------------|----------|
| [x] | paper | https://arxiv.org/abs/2504.01495 | agent | `articles/arxiv-autonomous-web-agents-testers.md` | 学术论文：自主 Web Agent 作为测试者的能力评估，E2E 自动化新范式 |
| [x] | blog | https://medium.com/transforming-testing-with-generative-ai/transforming-end-to-end-testing-with-generative-agentic-workflows-c29f4aae6a0a | agent | `articles/generative-agentic-e2e-workflows.md` | 生成式 AI Agent 工作流改造 E2E 测试：自主规划、执行、验证的闭环设计 |
| [x] | blog | https://medium.com/codex/has-anthropic-just-wiped-out-the-software-testing-industry-0bb6305adcc2 | agent | `articles/anthropic-computer-use-ui-testing.md` | Claude Computer Use 在 UI/UX 测试中的实战应用：零先验知识的自主测试场景 |
| [x] | doc | https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool | agent | `articles/anthropic-computer-use-api-docs.md` | Anthropic Computer Use API 官方文档：Agent 浏览器自动化的原语能力 |
| [x] | blog | https://dev.to/robin_xuan_nl/5-minutes-of-human-ai-interaction-from-requirements-to-e2e-test-result-1o71 | agent | `articles/e2e-test-ai-agent-dev-to.md` | 实战：从需求到 E2E 测试结果，构建组织内的 E2E Test AI Agent |

### 四、E2E Testing Skill 设计参考（ skill design patterns ）

| OK | Type | URL 或路径 | 建议 shelf | 建议 raw 子路径 | 一行理由 |
|----|------|------------|------------|-----------------|----------|
| [x] | repo | https://github.com/fugazi/test-automation-skills-agents | agent | `refs/fugazi-test-automation-skills-agents.md` | 生产级 QA Agent Skill 库：13 个专用 Agent + 10 个可复用 Skill 的架构设计 |
| [x] | site | https://qaskills.sh/categories/e2e-testing | agent | `refs/qaskills-e2e-testing.md` | E2E Testing Skill 市场：业界对 AI Agent E2E 测试能力的标准化定义 |

## 你的批复

（在此打勾或聊天回复采纳序号 / 修改 shelf / 补充来源）

## Fetched（Agent 已填写）

| raw路径 | 状态 |
|----------|------|
| `raw/agent/e2e-testing/articles/google-just-say-no-to-e2e.md` | OK |
| `raw/agent/e2e-testing/articles/martin-fowler-test-pyramid.md` | OK |
| `raw/agent/e2e-testing/articles/ibm-e2e-best-practices.md` | OK |
| `raw/agent/e2e-testing/articles/bunnyshell-e2e-best-practices-2025.md` | OK |
| `raw/agent/e2e-testing/articles/playwright-official-best-practices.md` | OK |
| `raw/agent/e2e-testing/articles/playwright-test-data-strategies.md` | **FAILED** (403) → 已写入 `refs/` 并附 fallback 提示 |
| `raw/agent/e2e-testing/articles/msw-best-practices.md` | OK (注：MSW 官网为索引页，已抓取核心原则与 Playwright 集成示例) |
| `raw/agent/e2e-testing/articles/playwright-e2e-cheatsheet.md` | OK |
| `raw/agent/e2e-testing/articles/arxiv-autonomous-web-agents-testers.md` | OK (摘要 + 关键发现) |
| `raw/agent/e2e-testing/articles/generative-agentic-e2e-workflows.md` | **FAILED** (Medium timeout) → 已写入 `refs/` 并附 fallback 提示 |
| `raw/agent/e2e-testing/articles/anthropic-computer-use-ui-testing.md` | **FAILED** (Medium timeout) → 已写入 `refs/` 并附 fallback 提示 |
| `raw/agent/e2e-testing/articles/anthropic-computer-use-api-docs.md` | **FAILED** (403) → 已写入 `refs/` 并附 fallback 提示 |
| `raw/agent/e2e-testing/articles/e2e-test-ai-agent-dev-to.md` | OK |
| `raw/agent/e2e-testing/refs/fugazi-test-automation-skills-agents.md` | OK (GitHub README 完整内容) |
| `raw/agent/e2e-testing/refs/qaskills-e2e-testing.md` | OK (目录站完整内容) |
