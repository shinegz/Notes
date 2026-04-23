---
title: "Learning to Summarize from Human Feedback"
type: source
tags: [rlhf, alignment, human-feedback, summarization]
sources: []
last_updated: 2026-04-23
source_file: raw/ai-fundamentals/pdfs/rlhf-from-feedback.pdf
---

# Learning to Summarize from Human Feedback

**Nisan Stiennon, Long Ouyang, Jeff Wu, Daniel M. Ziegler, Ryan Lowe, Chelsea Voss, Alec Radford, Dario Amodei, Paul Christiano**  
*OpenAI*

## Abstract

As language models become more powerful, training and evaluation are increasingly bottlenecked by the data and metrics used for a particular task. For example, summarization models are often trained to predict human reference summaries and evaluated using ROUGE, but both of these metrics are rough proxies for what we really care about — summary quality. In this work, we show that it is possible to significantly improve summary quality by training a model to optimize for human preferences.

## Key Contributions

- **RLHF for summarization** — one of the first large-scale applications of RLHF to language models
- **Human comparison dataset** — collected high-quality human preferences between summaries
- **Reward model training** — trained a model to predict the human-preferred summary
- **PPO fine-tuning** — used the reward model to fine-tune a summarization policy with reinforcement learning
- **Outperforms larger supervised models** — RLHF model beats much larger models fine-tuned with supervised learning alone
- **Generalization** — models transfer from Reddit TL;DR to CNN/DM news articles

## Connections

- [[instructgpt]] — Direct successor that applies the same RLHF pipeline to instruction following
- [[dpo]] — DPO is a simpler alternative to the PPO-based RLHF approach used here
- [[scaling-laws-kaplan|Scaling Laws]] — RLHF adds a post-training alignment stage beyond scaling
