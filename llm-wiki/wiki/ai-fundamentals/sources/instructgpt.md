---
title: "Training Language Models to Follow Instructions with Human Feedback"
type: source
tags: [instructgpt, rlhf, alignment, instruction-following]
sources: []
last_updated: 2026-04-19
source_file: raw/ai-fundamentals/pdfs/instructgpt.pdf
---

# Training Language Models to Follow Instructions with Human Feedback (InstructGPT)

**Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, John Schulman, Jacob Hilton, Fraser Kelton, Luke Miller, Maddie Simens, Amanda Askell, Peter Welinder, Paul Christiano, Jan Leike, Ryan Lowe**  
*OpenAI*

## Abstract

Making language models larger does not inherently make them better at following a user's intent. While the 175B GPT-3 is few-shot capable, it can generate outputs that are untruthful, toxic, or simply not helpful. We train large language models using a combination of human feedback to make them more helpful, truthful, and harmless. Our technique, called Reinforcement Learning from Human Feedback (RLHF), consists of three steps: supervised fine-tuning (SFT), reward model training, and proximal policy optimization (PPO).

## Key Contributions

- **RLHF pipeline**: Three-step training process (SFT → Reward Model → PPO)
- **Helpful, harmless, and honest**: Alignment with human preferences
- **GPT-3.5 series**: Powers ChatGPT and API
- **Significantly reduced hallucinations**: Better truthfulness than fine-tuned GPT-3

## Three-Stage Training

| Stage | Description |
|-------|-------------|
| SFT | Supervised fine-tuning with demonstrations |
| Reward Model | Train model to predict human preference |
| PPO | Fine-tune with RL using reward model |

## Results

| Model | Preference Rate vs. SFT |
|-------|------------------------|
| 1.3B SFT | 0% (baseline) |
| 1.3B PPO | 61% |
| 175B SFT | 0% (baseline) |
| 175B PPO | **71%** |

## Connections

- [[gpt3-language-models-few-shot|GPT-3]] — InstructGPT is trained from GPT-3 base model
