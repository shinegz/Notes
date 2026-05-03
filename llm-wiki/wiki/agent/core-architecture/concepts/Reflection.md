---
title: "Reflection (Agent Self-Reflection)"
type: concept
tags: [agent, memory, self-improvement, episodic, verbal-critique]
sources:
  - agent/core-architecture/sources/memory-autonomous-llm-agents
  - agent/core-architecture/sources/agentic-ai-comprehensive-survey
last_updated: 2026-05-03
---

## 一句话理解

Reflection 是 Agent 通过**口头自我批评（verbal self-critique）**将执行结果转化为 Episodic Memory 存储的过程，使系统在后续类似任务中能主动避免重复失败，本质是"从错误中学习"的记忆机制。

## 背景

ReAct 仅依赖当前 context window 的推理轨迹，没有持久学习能力——相同错误会在每个 session 重复。Reflection 解决了"如何让 Agent 从失败中积累知识"的问题。

## 核心机制

Reflection 的工作流程（以 Generative Agents 为例）：

```
1. Execute: Agent 执行任务，产生结果
2. Evaluate: Critic Agent 评估结果，找出失败原因
3. Reflect: 主 Agent 将批评转化为简短反思语句
4. Store: 反思语句作为 Episodic Memory 写入记忆存储
5. Retrieve: 下次遇到类似任务时，从记忆中检索相关反思
```

**关键约束**：反思必须引用**具体的 Episodic 证据**（"上次在 X 步骤因为 Y 原因失败了"），而非泛化结论（"我应该更仔细"）——这叫 Reflection Grounding。

## 在记忆架构中的位置

Reflection 属于 **Reflective self-improvement** 机制家族（Memory Taxonomy 5 种机制之一）：

| 机制 | 代表系统 | 核心特征 |
|------|---------|---------|
| Context-resident compression | ReAct | 推理轨迹作为短时 working memory |
| Retrieval-augmented | RAG | 外部向量存储 + dense retriever |
| **Reflective self-improvement** | **Generative Agents, ExpeL** | **Verbal self-critiques → Episodic Memory** |
| Hierarchical virtual context | MemGPT | OS-style paging across context layers |
| Policy-learned management | AgeMem | RL 优化的存储/检索/更新策略 |

## 关键量化数据

- **Generative Agents**：去掉 Reflection 后，48 模拟小时内退化到重复无上下文响应
- **Reflexion**（Shinn et al.）：HumanEval 上 91% pass@1（vs GPT-4 baseline 80%），显著超越无 Reflection 的 baseline

## 局限性与挑战

- **无 World Model**：反思仍是语言层面的自我批评，不构成对环境因果结构的深层理解
- **幻觉风险**：如果反思内容本身包含错误假设，会形成"错误信念"写入记忆，造成复合错误
- **记忆衰减**：Episodic Memory 过多后检索质量下降，需要与 summarization/compression 配合
- **Grounding 难题**：要求每次反思必须引用具体证据，实际系统中往往难以严格执行

## 与 True Autonomy 的关系

Reflection 是 True Autonomy 中 **Persistent Memory 支柱**的关键实现机制之一——没有反思和从中学习的能力，Agent 只能在当前 session 内改进，无法跨 session 积累。

## 来源

- [[agent/core-architecture/sources/memory-autonomous-llm-agents|Memory for Autonomous LLM Agents]] — Reflection 作为五大家庭之一（Reflective self-improvement）；Generative Agents / ExpeL 代表系统；Grounding 约束；Reflexion benchmark 数据
- [[agent/core-architecture/sources/agentic-ai-comprehensive-survey|Agentic AI Comprehensive Survey]] — Neural/Generative 范式中 Self-Reflection 作为涌现能力
- [[agent/core-architecture/sources/ultimate-guide-ai-agent-architectures-2025|Ultimate Guide 2025]] — Reflexion 作为复杂架构模式之一，HumanEval 91% pass@1
