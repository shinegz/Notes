---
title: "AgentBench: Evaluating LLMs as Agents"
type: source
tags: [agent, benchmark, evaluation, llm]
sources: []
last_updated: 2026-04-23
source_file: raw/ai-fundamentals/pdfs/agentbench.pdf
---

# AgentBench: Evaluating LLMs as Agents

## Abstract

AGENTBENCH is a multi-dimensional benchmark consisting of 8 distinct environments to assess LLM-as-Agent abilities on challenging interactive tasks. It evaluates reasoning, decision-making, tool use, and multi-turn interaction across code execution, web browsing, household management, puzzle solving, and more.

## Key Contributions

- **8 diverse environments** for evaluating LLMs as agents: OS, Database, Knowledge Graph, Digital Card Game, Lateral Thinking Puzzles, Web Shopping, Home Management, and Web Browsing
- **Quantitative evaluation** of state-of-the-art LLMs showing significant capability gaps in agent tasks
- **Reveals that LLMs struggle with long-horizon planning**, environment interaction, and error recovery
- **Open-sourced benchmark** enabling reproducible comparison of LLM agent capabilities

## Connections

- [[llm-powered-autonomous-agents]] — Agent system taxonomy that AgentBench evaluates
- [[react-chain-of-thought|ReAct]] — One of the prompting strategies tested in the benchmark
- [[gpt3-language-models-few-shot|GPT-3]] — Base model for many evaluated agent systems
