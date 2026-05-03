# Collect session — Agent 核心架构设计及实现

- **Goal**: 学习 LLM Agent 的核心架构设计模式与工程实现
- **Default shelf**: `agent/core-architecture`
- **Created**: 2026-05-03

## 工具路由规则（Collect 前必读）

| 来源类型 | 路由决策 | 操作 |
|----------|----------|------|
| **arXiv/论文 PDF** | `curl -L -o raw/.../pdfs/<slug>.pdf "https://arxiv.org/pdf/<id>.pdf"` | 直接下载 PDF，不抓 HTML |
| **通用网页** | `baoyu-url-to-markdown --output raw/.../articles/<slug>.md` | HTML → Markdown |
| **GitHub repo** | `baoyu-url-to-markdown --output raw/.../refs/<slug>.md` | README 快照到 refs/ |
| **微信文章** | `wechat-article-to-markdown` | 需安装 skill |
| **YouTube 视频** | `baoyu-youtube-transcript` | 需安装 skill |

**arXiv 识别**：URL 含 `arxiv.org/html/` 或 `arxiv.org/abs/` → 改为 `/pdf/<id>.pdf` 再下载

## Candidate sources（待你确认）

| OK | Type | URL | 建议 raw 路径 | 一行理由 |
|----|------|-----|--------------|----------|
| [x] | arxiv-pdf | https://arxiv.org/pdf/2510.25445.pdf | pdfs/agentic-ai-comprehensive-survey.pdf | 25年最全 Agentic AI 综述：双范式框架（Symbolic vs Neural）、五时代演进、多领域应用 |
| [x] | web-article | https://wavesandalgorithms.com/ai-architecture/agentic-ai-workflows/core-agentic-ai-architectural-patterns | articles/core-agentic-ai-architectural-patterns.md | Simulated Agency vs True Autonomy：模块化认知架构、World Model、持久记忆、适应性规划 |
| [x] | web-article | https://dev.to/sohail-akbar/the-ultimate-guide-to-ai-agent-architectures-in-2025-2j1c | articles/ultimate-guide-ai-agent-architectures-2025.md | 5种核心架构模式含伪代码：Single Agent+Router、Hub-Spoke、层级 Agent + 并行 Agent |
| [x] | web-article | https://aws.amazon.com/blogs/machine-learning/ai-agents-in-enterprises-best-practices-with-amazon-bedrock-agentcore/ | articles/aws-bedrock-agentcore-best-practices.md | AWS 企业级 Agent 实践：Orchestrator-Worker、A2A/MCP 协议区别、Agent 观测设计 |
| [x] | web-article | https://openlayer.com/blog/post/multi-agent-system-architecture-guide | articles/multi-agent-system-architecture-guide.md | 多 Agent 协调模式：Supervisor/Hierarchical/P2P/Blackboard/Swarm 深度解析 |
| [x] | web-article | https://atlan.com/know/agent-memory-architectures/ | articles/agent-memory-architectures.md | Agent 记忆架构5种模式：In-context 到 Tiered Memory，Mem0 LOCOMO benchmark 量化对比 |
| [x] | arxiv-pdf | https://arxiv.org/pdf/2603.07670.pdf | pdfs/memory-autonomous-llm-agents.pdf | Memory for Autonomous LLM Agents：记忆机制、评估方法、Agent 记忆架构综述（补充来源，已替代 Medium SOTA） |
| [x] | paper | https://arxiv.org/pdf/2601.03328.pdf | pdfs/llm-enabled-multi-agent-systems.pdf | LLM-Enabled MAS：设计模式实证评估，电信/国防/文化遗产/公用事业多行业案例 |
| [x] | web-article | https://www.puppygraph.com/blog/ai-agent-architecture | articles/ai-agent-architecture-components-types.md | AI Agent 组件与类型：Planner/Tool Executor/Memory/Verifier/Orchestrator 图解（替代 Medium AI Architectures 2025） |
| [x] | github-repo | https://github.com/badlogic/pi-mono | refs/pi-mono-repo.md | AI agent 工具箱：@pi-ai 统一 LLM API、@pi-agent-core Agent 运行时、@pi-coding-agent CLI |
| [x] | github-repo | https://github.com/openclaw/openclaw | refs/openclaw-repo.md | 开源个人 AI 助手：20+ channel、多 Agent 路由、Local-first Gateway、Skills 系统 |
| [x] | github-repo | https://github.com/nousresearch/hermes-agent | refs/hermes-agent-repo.md | 自改进 Agent：内置学习 loop、40+ 工具、Skills 自创建、跨 session 记忆 |
| [x] | github-repo | https://github.com/anomalyco/opencode | refs/opencode-repo.md | 开源编码 Agent：build/plan 双 Agent、provider-agnostic、client/server 架构 |

## 你的批复

（在此打勾或聊天回复采纳序号 / 修改 shelf）

## Fetched（确认后由 Agent 填写）

| raw 路径 | 状态 | Fetch 方法 |
|----------|------|------------|
| `pdfs/agentic-ai-comprehensive-survey.pdf` | ✅ | curl -L |
| `pdfs/llm-enabled-multi-agent-systems.pdf` | ✅ | curl -L |
| `pdfs/memory-autonomous-llm-agents.pdf` | ✅ | curl -L（替代 Medium SOTA Agent Architecture） |
| `articles/core-agentic-ai-architectural-patterns.md` | ✅ | baoyu-fetch |
| `articles/ultimate-guide-ai-agent-architectures-2025.md` | ✅ | baoyu-fetch |
| `articles/aws-bedrock-agentcore-best-practices.md` | ✅ | baoyu-fetch |
| `articles/multi-agent-system-architecture-guide.md` | ✅ | baoyu-fetch |
| `articles/agent-memory-architectures.md` | ✅ | baoyu-fetch |
| `articles/ai-agent-architecture-components-types.md` | ✅ | baoyu-fetch（替代 Medium AI Architectures 2025） |
| `refs/pi-mono-repo.md` | ✅ | baoyu-fetch |
| `refs/openclaw-repo.md` | ✅ | baoyu-fetch |
| `refs/hermes-agent-repo.md` | ✅ | baoyu-fetch |
| `refs/opencode-repo.md` | ✅ | baoyu-fetch |
| Medium SOTA Agent Architecture | ❌ | 原文需登录 → 已用 arXiv 2603.07670 替代 |
| Medium AI Architectures 2025 | ❌ | 原文需登录 → 已用 PuppyGraph 替代 |