---
title: "Toolformer: Language Models Can Teach Themselves to Use Tools"
type: source
tags: [tool-use, agent, api, self-supervised, fine-tuning]
last_updated: 2026-04-24
source_file: raw/ai-fundamentals/pdfs/toolformer.pdf
source_url: https://arxiv.org/abs/2302.04761
---

## Summary

Schick et al. demonstrate that language models can teach themselves to use external tools via self-supervised learning. **Toolformer** decides which APIs to call, when to call them, what arguments to pass, and how to incorporate results—without human annotation of tool use.

## Key Claims

- **Self-supervised tool learning** — no human annotation required
- Annotates training data with API calls where they reduce loss
- Multiple tools: calculator, QA system, search engine, translation, calendar
- Controllable: learns when tool use is beneficial vs. relying on parametric knowledge
- Combines LLM reasoning with factual/arithmetic precision from tools

## How It Works

```
1. For each potential API call position in training data:
   - Would adding this call reduce loss?
2. If yes, annotate with API call
3. Fine-tune model on augmented data
4. At inference: model decides whether to call tools
```

## Connections

- [[ai-fundamentals/sources/llm-powered-autonomous-agents|LLM-powered Autonomous Agents]] — Surveys Toolformer
- [[ai-fundamentals/sources/react-chain-of-thought|ReAct]] — ReAct reasons about tools; Toolformer learns them
- [[ai-fundamentals/concepts/llm-agents|LLM Agents]] — Tool use component
