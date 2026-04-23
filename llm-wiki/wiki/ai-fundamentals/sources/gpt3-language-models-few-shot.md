---
title: "Language Models are Few-Shot Learners"
type: source
tags: [gpt3, few-shot, in-context-learning, nlp]
sources: []
last_updated: 2026-04-19
source_file: raw/ai-fundamentals/pdfs/gpt3-language-models-few-shot.pdf
---

# Language Models are Few-Shot Learners (GPT-3)

**Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Chris Henighan, Rewon Child, Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, Dario Amodei**  
*OpenAI*

## Abstract

Recent work has demonstrated substantial gains on many NLP tasks and benchmarks by pre-training on a large corpus of text followed by task-specific fine-tuning. We demonstrate that scaling up language models greatly improves task-agnostic, few-shot performance. GPT-3, with 175 billion parameters, achieves strong performance on many NLP datasets, including translation, question-answering, and cloze tasks, as well as several tasks that require on-the-fly reasoning or domain adaptation.

## Key Contributions

- **175B parameters**: Largest language model at time of publication
- **Few-shot learning**: Achieves competitive results without fine-tuning
- **In-context learning**: Learns from demonstrations in the prompt
- **Broad capabilities**: Translation, Q&A, reasoning, domain adaptation

## Model Sizes

| Model | Parameters |
|-------|------------|
| GPT-3 Small | 125M |
| GPT-3 Medium | 350M |
| GPT-3 Large | 760M |
| GPT-3 XL | 1.3B |
| GPT-3 2.7B | 2.7B |
| GPT-3 6.7B | 6.7B |
| GPT-3 13B | 13B |
| GPT-3 175B | **175B** |

## Few-Shot Results

| Task | SOTA (fine-tuned) | GPT-3 Few-shot |
|------|-------------------|----------------|
| SuperGLUE | 89.8 | **90.3** |
| TriviaQA | 68.9 | **71.2** |
| LAMBADA | 68.0 | **76.2** |

## Connections

- [[attention-is-all-you-need]] — GPT-3 uses Transformer decoder architecture
- [[scaling-laws-kaplan]] — Follows scaling laws for language model pre-training
- [[instructgpt]] — InstructGPT trains GPT-3 with human feedback
