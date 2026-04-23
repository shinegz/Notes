---
title: "Direct Preference Optimization: Your Language Model is Secretly a Reward Model"
type: source
tags: [rlhf, alignment, preference-optimization, dpo]
sources: []
last_updated: 2026-04-23
source_file: raw/ai-fundamentals/pdfs/dpo.pdf
---

# Direct Preference Optimization: Your Language Model is Secretly a Reward Model

**Rafael Rafailov, Archit Sharma, Eric Mitchell, Christopher D. Manning, Stefano Ermon, Chelsea Finn**  
*Stanford University*

## Abstract

While large-scale unsupervised language models learn broad world knowledge and reasoning skills, achieving precise control of their behavior is difficult. Existing methods like RLHF collect human preference labels and fine-tune the LM, but RLHF is complex and unstable. This paper introduces a new parameterization of the reward model that enables extraction of the corresponding optimal policy in closed form, solving the RLHF problem with only a simple classification loss. The resulting algorithm, Direct Preference Optimization (DPO), is stable, performant, and computationally lightweight.

## Key Contributions

- **Closed-form policy extraction** — eliminates the need for explicit reward model training
- **Simple classification loss** — replaces complex PPO-based reinforcement learning
- **Stable training** — no sampling from the LM during fine-tuning, minimal hyperparameter tuning
- **Matches or exceeds PPO-based RLHF** in sentiment control, summarization, and single-turn dialogue
- **Theoretically grounded** — derives equivalence between Bradley-Terry model and optimal policy under KL constraint

## Connections

- [[instructgpt]] — InstructGPT uses PPO-based RLHF; DPO is a simpler alternative
- [[rlhf-from-feedback]] — Foundational RLHF work that DPO improves upon
- [[scaling-laws-kaplan|Scaling Laws]] — DPO makes alignment more feasible for very large models

## Key Facts

- Published 2023
- Proposes **DPO** as a simpler alternative to RLHF (PPO)
- Eliminates the need for explicit reward model training
- Derives a closed-form solution that directly optimizes the language model on preference data
- More stable and efficient than PPO-based RLHF while achieving comparable or better results
