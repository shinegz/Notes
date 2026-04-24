---
title: "ReAct: Synergizing Reasoning and Acting in Language Models"
type: source
tags: [react, reasoning, agent, tool-use, chain-of-thought]
last_updated: 2026-04-24
source_file: raw/ai-fundamentals/pdfs/react-chain-of-thought.pdf
source_url: https://arxiv.org/abs/2210.03629
---

## Summary

Yao et al. propose **ReAct**—interleaving reasoning (Thought) traces with acting (Action) steps and external observations. This synergistic approach outperforms both chain-of-thought-only and action-only baselines on knowledge-intensive reasoning and decision-making tasks, while reducing hallucination by grounding thoughts in real observations.

## Key Claims

- **ReAct loop**: `Thought → Action → Observation → Thought → ...`
- Outperforms both CoT-only and Act-only baselines
- Reduces hallucination by grounding reasoning in external observations
- Works across diverse environments: Wikipedia, web search, text games, embodied tasks
- Action space combines task-specific discrete actions with language

## ReAct Template

```
Thought: I need to find X
Action: search[X]
Observation: Result shows...
Thought: Based on the observation...
Action: finish[answer]
```

## Key Quotes

> "Reasoning traces help the model induce, track, and update action plans, while actions allow it to interface with external sources to gather additional information."

## Connections

- [[ai-fundamentals/sources/llm-powered-autonomous-agents|LLM-powered Autonomous Agents]] — Surveys ReAct as a key planning technique
- [[ai-fundamentals/sources/toolformer|Toolformer]] — ReAct reasons about tools; Toolformer learns to call them
- [[ai-fundamentals/concepts/chain-of-thought-react|CoT & ReAct]] — Concept page
