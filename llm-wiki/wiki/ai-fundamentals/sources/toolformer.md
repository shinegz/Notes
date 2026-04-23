---
title: "Toolformer: Language Models Can Teach Themselves to Use Tools"
type: source
tags: [tool-use, agent, api, self-supervised]
sources: []
last_updated: 2026-04-23
source_file: raw/ai-fundamentals/pdfs/toolformer.pdf
---

# Toolformer: Language Models Can Teach Themselves to Use Tools

**Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta Raileanu, Maria Lomeli, Eric Hambro, Luke Zettlemoyer, Nicola Cancedda, Thomas Scialom**  
*Meta AI Research, Universitat Pompeu Fabra*

## Abstract

Language models exhibit remarkable abilities to solve new tasks from few examples, but paradoxically struggle with basic functionality such as arithmetic or factual lookup where much simpler models excel. This paper shows that LMs can teach themselves to use external tools via simple APIs and achieve the best of both worlds. Toolformer is trained to decide which APIs to call, when to call them, what arguments to pass, and how to incorporate results into token-level predictions.

## Key Contributions

- **Self-supervised tool learning** — no human annotation of tool use required
- **API call annotation** — automatically adds API calls to training data where they reduce loss
- **Multiple tools** — calculator, QA system, search engine, translation, calendar
- **Best of both worlds** — retains LM's reasoning while offloading factual/arithmetic tasks to tools
- **Controllable** — model learns when tool use is beneficial vs. when to rely on parametric knowledge

## Connections

- [[llm-powered-autonomous-agents]] — Surveys Toolformer as a key tool-augmented LLM approach
- [[react-chain-of-thought|ReAct]] — ReAct reasons about tool use; Toolformer learns it via self-supervision
- [[gpt3-language-models-few-shot|GPT-3]] — Base model for Toolformer experiments

## Key Facts

- Published 2023
- Language model learns to use external tools (calculator, QA system, search engine, translation, calendar) via **self-supervised learning**
- Annotates training data with API calls by predicting which calls would reduce loss
- No human annotation of tool use required
- Enables LLMs to overcome limitations of parametric knowledge
