---
title: "ReAct: Synergizing Reasoning and Acting in Language Models"
type: source
tags: [react, reasoning, agent, tool-use, chain-of-thought]
sources: []
last_updated: 2026-04-23
source_file: raw/ai-fundamentals/pdfs/react-chain-of-thought.pdf
---

# ReAct: Synergizing Reasoning and Acting in Language Models

**Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao**  
*Princeton University, Google Research*

## Abstract

While large language models have demonstrated impressive performance across tasks, their abilities for reasoning (e.g. chain-of-thought prompting) and acting (e.g. action plan generation) have primarily been studied as separate topics. This paper explores the use of LLMs to generate both reasoning traces and task-specific actions in an interleaved manner. Reasoning traces help the model induce, track, and update action plans, while actions allow it to interface with external sources to gather additional information.

## Key Contributions

- **ReAct framework** — interleaving reasoning (Thought) and acting (Action) traces
- **Outperforms both CoT-only and Act-only baselines** on knowledge-intensive and decision-making tasks
- **Reduces hallucination** in reasoning by grounding thoughts in external observations
- **Generalizes across environments** — Wikipedia, web, interactive text games, embodied tasks
- **Open-sourced** prompting templates and evaluation framework

## Connections

- [[llm-powered-autonomous-agents]] — Surveys ReAct as a key planning/self-reflection technique
- [[toolformer]] — Complementary: ReAct reasons about tools, Toolformer learns to call them
- [[gpt3-language-models-few-shot|GPT-3]] — Base model for ReAct experiments

## Key Facts

- Published at ICLR 2023
- Proposes **ReAct** — interleaving reasoning (Thought) and acting (Action) traces
- Action space combines task-specific discrete actions and language space
- Outperforms both chain-of-thought-only and action-only baselines
- Enables LLMs to interact with external environments (Wikipedia, web, tools)
- Foundation for many LLM agent frameworks
