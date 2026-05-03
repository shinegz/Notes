# Agent 开发学习计划

## 背景

本文档为「系统学习 Agent 开发」的完整学习路径规划，基于对以下开源项目的深度调研：

- **Hermes-Agent** (nousresearch/hermes-agent) — 127k stars，Python
- **pi-mono** (badlogic/pi-mono) — 44k stars，TypeScript，monorepo
- **OpenClaw** (openclaw/openclaw) — 367k stars，TypeScript
- **OpenCode** (anomalyco/opencode) — 152k stars，TypeScript

以及 llm-wiki 已积累的 Agent 理论基础（Harness Engineering、ReAct、Function Calling、Memory 等）。

---

## 一、现有知识基线

### 已覆盖

| 领域 | 内容 |
|------|------|
| LLM 基础 | Transformer、Attention、CoT、ReAct、Function Calling、Memory/RAG、Embedding |
| Agent 概念 | Planning/Memory/Tools/Action 四大组件、ReAct 循环 |
| Harness Engineering | 6 大工程构件、持久状态、反馈回路、Context 三层抽象、熵增抑制 |
| 软件工程 | DDD、设计模式、架构原则 |

### 缺失

| 领域 | 影响 |
|------|------|
| Multi-Agent 协作模式 | 所有高星项目都是多 Agent 系统，但缺乏协作架构的概念 |
| MCP 协议 | 工具互操作的事实标准，多个项目已支持 |
| 沙箱/安全执行 | Agent 跑代码需要隔离环境 |
| Agent 可观测性 | Tracing、调试的生产级实践 |

---

## 二、学习路径

### 第一阶段：Agent 核心实现（最优先）

**目标：理解 Agent Loop 的最小完整闭环**

| 学习对象 | 理由 |
|---------|------|
| **Hermes-Agent**（Python，127k ⭐） | 代码最简单，核心循环约 300 行，能看到完整的 `while → LLM → tool_calls → execute → loop` 闭环 |

**核心要理解的问题：**

1. Agent Loop 的终止条件是什么？（stop_reason? max_iterations? terminate 标志?）
2. 工具调用的结果如何注入回下一轮 LLM？
3. 对话历史（短期记忆）如何管理？什么时候触发压缩？
4. 工具（tools）是如何注册的？自注册模式怎么实现？
5. Skills 和 Tools 的区别是什么？

**关键文件：**

```
Hermes-Agent:
  run_agent.py                    → 核心循环
  agent/memory_manager.py         → 记忆管理
  tools/registry.py               → 工具自注册
  model_tools.py                  → 工具调用编排

pi-mono（对照读）:
  packages/agent-core/src/agent-loop.ts  → 循环终止条件
  packages/agent-core/src/types.ts       → 接口设计
  packages/coding-agent/src/agent-session.ts → 高层封装
```

### 第二阶段：补充缺失的关键领域

**在有代码手感之后，再补概念：**

| 领域 | 优先级 | 理由 |
|------|--------|------|
| **Multi-Agent 协作模式** | P0 | hierarchical vs peer-to-peer vs pipeline 三种模式 |
| **MCP (Model Context Protocol)** | P0 | 工具发现和互操作的事实标准 |
| **沙箱 / 安全执行** | P1 | docker 隔离、权限控制 |
| **Agent 可观测性** | P1 | Tracing、structured logging |

### 第三阶段：框架开阔视野

**学完前两阶段后，用框架印证：**

| 框架 | 学什么 |
|------|--------|
| **LangGraph** | 如何把"状态"建模成 graph node |
| **CrewAI** | 角色 + 团队模式，印证 hierarchical 模式 |
| **AutoGen** | 多 Agent 对话，Agent 间通信协议的设计权衡 |

框架学的是**设计思路**，不是 API 用法。

---

## 三、项目选择理由

### Hermes-Agent vs pi-mono

**不是非此即彼，是学习顺序的问题：**

```
Hermes-Agent（先读）→ 最小闭环，看懂"怎么做"
pi-mono（后读）     → 对照着看，理解"为什么这么设计"
```

**为什么不主攻框架？**

主流开源 Agent 项目（OpenClaw、OpenCode、Hermes、pi-mono）普遍选择**自研 Agent 核心**，不依赖 LangChain/AutoGen 等框架。这说明这个领域框架还不够成熟，领先者都在构建自己的抽象层。

学习框架的价值在于了解行业共识，但源码学习才能理解真实实现细节。

---

## 四、具体下一步

1. 从 Hermes-Agent 的 `run_agent.py` 开始，理解核心循环
2. 对照 pi-mono 的 `agent-core` 设计，理解架构权衡
3. 补齐 Multi-Agent 和 MCP 的知识空白
4. 用 LangGraph/CrewAI 印证设计思路

---

## 五、参考来源

- [Hermes-Agent](https://github.com/nousresearch/hermes-agent)
- [pi-mono](https://github.com/badlogic/pi-mono)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [OpenCode](https://github.com/anomalyco/opencode)
- llm-wiki/agent/harness-engineering — Harness Engineering 深度解析
- llm-wiki/ai-fundamentals/concepts/llm-agents.md — LLM Agents 概念
- llm-wiki/ai-fundamentals/concepts/function-calling.md — Function Calling
- llm-wiki/ai-fundamentals/concepts/memory.md — Memory
