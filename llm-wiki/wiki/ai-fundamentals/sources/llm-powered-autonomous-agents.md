---
title: "LLM Powered Autonomous Agents"
type: source
tags: [agents, llm, planning, memory, tool-use]
last_updated: 2026-04-24
source_file: raw/ai-fundamentals/articles/llm-powered-autonomous-agents.md
source_url: https://lilianweng.github.io/posts/2023-06-23-agent/
author: Lilian Weng
---

## Summary

Lilian Weng surveys LLM-powered autonomous agents, identifying three core components: **Planning** (task decomposition, self-reflection), **Memory** (short-term via context, long-term via vector stores), and **Tool Use** (API calls, external knowledge). The paper surveys techniques like ReAct, Reflexion, and Algorithm Distillation.

## Key Claims

- **Agent = LLM + Planning + Memory + Tools** — LLM functions as the brain, complemented by these components
- **Planning** breaks down complex tasks via CoT, Tree of Thoughts, or external planners (LLM+P)
- **Self-reflection** (Reflexion) enables agents to learn from past mistakes
- **Memory hierarchy**: Sensory → Short-term (context window) → Long-term (vector stores)
- **Tool use** extends LLM capabilities beyond parametric knowledge (calculators, search, APIs)
- ReAct outperforms both CoT-only and Act-only baselines

## Key Quotes

> "In a LLM-powered autonomous agent system, LLM functions as the agent's brain, complemented by several key components."

## Techniques Covered

| Technique | Description | Citation |
|-----------|-------------|----------|
| CoT | Chain-of-thought prompting | Wei et al. 2022 |
| ToT | Tree of Thoughts | Yao et al. 2023 |
| ReAct | Reasoning + Acting interleaved | Yao et al. 2023 |
| Reflexion | Self-reflection with dynamic memory | Shinn & Labash 2023 |
| Toolformer | Self-supervised tool learning | Schick et al. 2023 |
| HuggingGPT | LLM as task planner | Shen et al. 2023 |

## Connections

- [[ai-fundamentals/sources/react-chain-of-thought|ReAct]] — Detailed ReAct framework paper
- [[ai-fundamentals/sources/toolformer|Toolformer]] — Self-supervised tool learning
- [[ai-fundamentals/concepts/llm-agents|LLM Agents]] — Concept page for Agent systems
