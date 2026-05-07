---
title: "Effective Context Engineering for AI Agents"
type: source
tags: [prompt-engineering, context-engineering, agent, anthropic]
last_updated: 2026-05-06
source_file: raw/ai-fundamentals/articles/anthropic-context-engineering.md
source_url: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
---

## Summary

Context Engineering 是 Prompt Engineering 的自然演进：从「写好指令」升级为「在有限的注意力预算内，为每次推理筛选最优 token 集合」。Context 的边际收益递减（context rot），使得它必须像内存一样被工程化管理，而非无限堆叠。

## Key Claims

- **Prompt → Context 的范式升级**：Prompt Engineering 关注如何写好系统指令；Context Engineering 关注推理时整个上下文状态（系统指令 + 工具 + MCP + 外部数据 + 消息历史）的持续编排。后者是前者的超集。
- **注意力预算有限**：LLM 的注意力机制产生 n² 对关系，token 越多，每对关系的权重越稀疏。所有模型都表现出 context rot 现象——上下文越长，信息召回精度越低。
- **最小高信噪比原则**：好的 Context Engineering = 找到最小的高信噪比 token 集合，使期望输出的概率最大化。Minimal ≠ short，但每个 token 都应该有存在的理由。
- **系统提示的「正确海拔」**：太具体 → 脆弱难维护；太抽象 → 模型缺乏行为锚点。正确海拔 = 具体到能引导行为，灵活到提供强启发式。
- **工具设计的最小可用集**：工具膨胀是常见失败模式——如果人类工程师也无法确定该用哪个工具，Agent 更做不到。工具应自包含、无重叠、描述无歧义。
- **Few-shot 应精选 canonical examples**：不要堆砌边界案例，而应选择少量多样化的、能刻画期望行为的典型示例。对 LLM 来说，示例是「值千言的图片」。
- **长时程任务三策略**：Compaction（压缩上下文继续）、Structured Note-taking（持久化笔记到上下文外）、Sub-agent（子 Agent 隔离上下文后只返回摘要）。
- **Hybrid 检索策略**：预计算检索提供速度，Just-in-Time 自主探索提供深度。Claude Code 即采用混合模式：CLAUDE.md 预加载 + glob/grep 实时检索。

## Key Quotes

> "Context engineering is the art and science of curating what will go into the limited context window from that constantly evolving universe of possible information."

> "Good context engineering means finding the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome."

> "If a human engineer can't definitively say which tool should be used in a given situation, an AI agent can't be expected to do better."

## Connections

- [[ai-fundamentals/concepts/prompt-engineering|Prompt Engineering]] — Context Engineering 是其自然演进
- [[ai-fundamentals/concepts/llm-agents|LLM Agents]] — Agent 在循环中运行，Context Engineering 是其可靠运行的前提
- [[ai-fundamentals/concepts/context-window|Context Window]] — 上下文窗口的物理限制是 Context Engineering 的根本约束
- [[ai-fundamentals/sources/openai-prompt-engineering|OpenAI Prompt Engineering Guide]] — 互补视角：OpenAI 侧重 Prompt 写法，Anthropic 侧重系统级上下文编排
