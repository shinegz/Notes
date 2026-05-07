---
title: "Context Dilution: When More Tokens Hurt AI"
url: "https://diffray.ai/blog/context-dilution/"
requestedUrl: "https://diffray.ai/blog/context-dilution/"
author: "diffray"
coverImage: "https://diffray.ai/og-image.jpg"
publishedAt: "2025-12-24T00:00:00+00:00"
summary: "Research from Stanford, Google, Anthropic, and Meta reveals that LLMs suffer 13.9% to 85% accuracy drops as context grows. Learn about the 'Lost in the Middle' phenomenon and why strategic context curation outperforms brute-force inclusion."
adapter: "generic"
capturedAt: "2026-05-07T02:37:37.564Z"
conversionMethod: "defuddle"
kind: "generic/article"
language: "en"
---

# Context Dilution: When More Tokens Hurt AI

Research Deep-Dive

## Context Dilution: Why More TokensCan Mean Worse AI Performance

Throwing all your code at an LLM doesn't make it smarter—it makes it confused. Research reveals predictable performance degradation with growing context windows.

Research from Stanford, Google, Anthropic, and Meta reveals that Large Language Models suffer predictable performance degradation when context windows contain too much information. This phenomenon, known as **context dilution**, causes models to "lose" critical information buried in lengthy prompts, with accuracy dropping **13.9% to 85%** as context grows—even when the model has perfect access to the relevant data.

13.9-85%

Accuracy drop as context length increases

20+ pts

Performance drop when info is in the middle

49-67%

Failure reduction with contextual retrieval

## The "Lost in the Middle" Phenomenon: Why Position Matters

The seminal 2023 paper ["Lost in the Middle: How Language Models Use Long Contexts"](https://arxiv.org/abs/2307.03172) by researchers at Stanford and Meta AI established the foundational understanding of context dilution. Testing models including GPT-3.5-Turbo, Claude-1.3, and LongChat on multi-document QA tasks, the researchers discovered a striking **U-shaped performance curve**: LLMs perform best when relevant information appears at the beginning or end of the context, but accuracy plummets when critical details are buried in the middle.

#### U-Shaped Performance Curve

Beginning

25%

Middle

75%

End

Model accuracy by position of relevant information in context

The degradation is substantial. Performance drops by **20+ percentage points** when relevant information moves from context edges to middle positions. In one striking finding, GPT-3.5-Turbo's accuracy on multi-document QA fell *below its closed-book performance* (no context at all) when relevant information was placed mid-context with 20 documents present. This means adding context actively hurt the model—a counterintuitive result that challenges the assumption that more information always helps.

Follow-up research published in ACL Findings 2024, ["Found in the Middle: Calibrating Positional Attention Bias Improves Long Context Utilization"](https://arxiv.org/abs/2406.16008) , pinpointed the root cause: an **intrinsic U-shaped attention bias** where LLMs assign higher attention weights to beginning and end tokens regardless of their semantic relevance. The paper demonstrated that LLMs *can* attend to relevant middle content but are systematically distracted by positional bias—and proposed calibration mechanisms that improved RAG performance by up to **15 percentage points**.

## Attention Sinks and Dilution: Fundamental Architectural Limits

MIT and Meta AI researchers uncovered another piece of the puzzle in their ICLR 2024 paper ["Efficient Streaming Language Models with Attention Sinks"](https://arxiv.org/abs/2309.17453) . They discovered that initial tokens receive disproportionately high attention scores even when semantically unimportant—a phenomenon they termed **attention sinks**. Because softmax normalization forces attention weights to sum to 1, models must "dump" attention somewhere when no tokens are highly relevant, and the first tokens become default receptacles.

#### Why Attention Dilution Happens

1

Softmax forces attention to sum to 1

Adding more tokens means each token gets less attention on average

2

Attention sinks absorb excess attention

First tokens become "dumping grounds" regardless of relevance

3

Irrelevant tokens steal attention from relevant ones

Each additional document progressively degrades signal quality

This architectural quirk compounds with what Meta AI researchers call **attention dilution**: since attention is zero-sum, adding more tokens monotonically increases noise in representations. Each irrelevant document in context steals attention from relevant ones, progressively degrading signal quality. The 2024 paper ["Core Context Aware Transformers"](https://arxiv.org/abs/2412.12465) confirmed that when context length reaches 128K tokens, **redundant information increases substantially**, and the attention score distribution becomes highly sparse with disproportionate scores concentrated on limited tokens.

Perhaps most surprising is Google's ICML 2023 finding that [LLMs can be easily distracted by irrelevant context](https://arxiv.org/abs/2302.00093) . Using their GSM-IC benchmark (math problems with inserted irrelevant information), they showed that model accuracy **dramatically decreases** when irrelevant—but topically related—information appears in the prompt. Factors like overlapping role names, in-range numbers, and topic-relevant distractors all trigger performance degradation.

## Empirical Benchmarks Quantify the Performance Cliff

The "Needle in a Haystack" (NIAH) test, created by researcher Greg Kamradt in 2023, became the standard evaluation for long-context retrieval. The methodology places a random fact (the "needle") at varying positions within distractor text (the "haystack") and measures whether models can retrieve it. While flagship models like Gemini 1.5 Pro achieve **\>99.7% accuracy** on standard NIAH up to 1 million tokens, this benchmark understates real-world challenges because it relies on literal matching.

The [NVIDIA RULER benchmark](https://arxiv.org/abs/2404.06654) , published in April 2024, extends NIAH with more realistic tasks: multi-hop tracing, aggregation, and question answering. The results reveal that claimed context lengths far exceed effective context lengths:

| Model | Claimed Context | Effective Context | Degradation (4K→128K) |
| --- | --- | --- | --- |
| GPT-4 | 128K | 64K | \-15.4 points |
| Yi-34B | 200K | 32K | \-16.0 points |
| Mistral 7B | 32K | 16K | \-79.8 points |
| Mixtral 8x7B | 32K | 32K | \-50.4 points |

The [Adobe Research NoLiMa benchmark](https://arxiv.org/abs/2502.05167) (February 2025) pushed further, testing retrieval when questions and target content share minimal lexical overlap—more representative of real queries. Results were sobering: **11 out of 12 models dropped below 50% of their baseline performance at just 32K tokens**. Even GPT-4o fell from 99.3% to 69.7% accuracy, demonstrating that attention mechanisms struggle significantly without literal lexical cues to guide retrieval.

## Context Length Hurts Performance Even with Perfect Retrieval

A striking October 2025 arXiv paper, ["Context Length Alone Hurts LLM Performance Despite Perfect Retrieval"](https://arxiv.org/abs/2510.05381) , delivered the most counterintuitive finding yet. Even with **100% perfect retrieval** of relevant information, performance degrades **13.9% to 85%** as input length increases. The degradation occurs even when irrelevant tokens are replaced with minimally distracting whitespace—and persists even when all irrelevant tokens are masked and models attend only to relevant content.

#### Critical Finding

This finding suggests that context dilution isn't purely an attention or retrieval problem— **sheer context length itself** imposes a cognitive tax on LLMs independent of content quality. The researchers found one mitigation: prompting models to recite retrieved evidence before solving problems improved GPT-4o performance by **4%** on the RULER benchmark, suggesting that explicit reasoning steps help models consolidate relevant information.

[Chroma's July 2025 "Context Rot" study](https://research.trychroma.com/context-rot) evaluated 18 LLMs including GPT-4.1, Claude 4, and Gemini 2.5. Their findings confirmed that performance degrades consistently with increasing input length across all models. Counterintuitively, shuffled (unstructured) haystacks produced **better performance** than coherent ones—suggesting that structural patterns in text may actually interfere with attention mechanisms. They also found that different models fail differently: Claude models tend toward conservative abstention while GPT models show higher hallucination rates when distractors are present.

## Strategic Context Curation Dramatically Improves Accuracy

Research consistently shows that **relevant context outperforms raw context quantity**. [Anthropic's September 2024 "Contextual Retrieval" paper](https://www.anthropic.com/news/contextual-retrieval) demonstrated that adding just 50-100 tokens of chunk-specific explanatory context reduces retrieval failures by **49%** (from 5.7% to 2.9%). Combined with reranking, failures dropped by **67%** (to 1.9%). The technique—prepending contextual metadata to each chunk before embedding—acknowledges that isolated chunks lack sufficient context on their own.

#### Performance Cliffs by Model

- Llama-3.1-405Bafter 32K tokens
- GPT-4-turboafter 16K tokens
- Claude-3-sonnetafter 16K tokens

Source: [Databricks Mosaic Research](https://www.databricks.com/blog/long-context-rag-performance-llms)

#### Compression Benefits

- LLMLingua compressionup to 20x
- Reasoning lossonly 1.5 points
- Inference acceleration1.7-5.7x faster

Source: [Microsoft Research LLMLingua](https://www.microsoft.com/en-us/research/blog/llmlingua-innovating-llm-efficiency-with-prompt-compression/)

## Practical Implications for AI-Powered Applications

The research points to clear strategies for building effective LLM applications:

Position matters critically

Place the most relevant information at the beginning or end of prompts. Never bury critical context in the middle of long inputs.

Less is often more

Curated, relevant context consistently outperforms comprehensive context. Adding irrelevant information can push accuracy below zero-context baselines.

Test your effective context window

Claimed context lengths rarely match effective performance. Empirically determine where your specific model-task combination begins degrading.

Implement hybrid retrieval with reranking

Combine semantic embeddings with lexical matching (BM25), then rerank top results before passing to the LLM—this combination reduces retrieval failures by 67%.

Consider compression techniques

For long-context scenarios, prompt compression can maintain quality while dramatically reducing latency and cost.

## How diffray Solves Context Dilution with Multi-Agent Architecture

Context dilution represents a fundamental limitation of current transformer architectures, not merely an engineering oversight to be patched. The attention mechanism's inherent properties—positional bias, attention sinks, and zero-sum distribution—create systematic degradation as context grows. While model context windows have expanded from 4K to 10 million tokens, effective utilization lags far behind claimed capacity.

The path forward isn't maximizing context—it's **optimizing relevance**. Research consistently demonstrates that strategic context curation outperforms brute-force inclusion by substantial margins. For applications demanding high accuracy, the evidence strongly favors selective, well-positioned context over comprehensive dumps.

#### diffray's Multi-Agent Approach

Instead of dumping everything into a single context window, diffray distributes review across 10 specialized agents—each with precisely curated context for their domain.

##### Single-Agent Problem

- • Entire codebase in one context window
- • Critical security info lost in the middle
- • Attention diluted across unrelated code
- • Performance degrades with repo size

##### Multi-Agent Solution

- • Security agent gets only security-relevant context
- • Performance agent sees benchmarks & hot paths
- • Each agent's context stays within effective limits
- • Scales to any repository size

By giving each agent **focused, curated context under 25K tokens**, we stay well within the effective performance window that research identifies—while still reviewing the entire PR comprehensively.

## The Context Series

This article is part of our deep-dive series on context in AI code review. Understanding how context works—and fails—is essential for getting real value from AI tools.

#### [Context Awareness](https://diffray.ai/blog/context-awareness/)

How intelligent AI systems understand your codebase architecture, dependencies, and patterns—not just isolated diffs.

Read article →

#### [Curated Context vs Volume](https://diffray.ai/blog/why-curated-context-beats-context-volume/)

Research proves: precision retrieval with agentic context gathering dramatically outperforms context dumping.

Read article →

#### [Meet the Agents](https://diffray.ai/blog/meet-the-agents/)

Deep dive into the 10 specialized AI agents that power diffray—each with focused context for their domain.

Read article →

#### [Why Developers Ignore AI Tools](https://diffray.ai/blog/why-developers-ignore-ai-code-review-tools/)

The root causes of developer resistance to AI code review—including context overload and false positives.

Read article →

## Key Research Sources

#### Foundational Papers

- ["Lost in the Middle: How Language Models Use Long Contexts" (Stanford/Meta, TACL 2024)](https://arxiv.org/abs/2307.03172)
- ["Found in the Middle: Calibrating Positional Attention Bias" (ACL Findings 2024)](https://arxiv.org/abs/2406.16008)
- ["Efficient Streaming Language Models with Attention Sinks" (MIT/Meta, ICLR 2024)](https://arxiv.org/abs/2309.17453)
- ["Large Language Models Can Be Easily Distracted by Irrelevant Context" (Google, ICML 2023)](https://arxiv.org/abs/2302.00093)
- ["Context Length Alone Hurts LLM Performance Despite Perfect Retrieval" (arXiv 2025)](https://arxiv.org/abs/2510.05381)

#### Context Optimization Research

- [LLMLingua (Microsoft Research, EMNLP 2023)](https://www.microsoft.com/en-us/research/blog/llmlingua-innovating-llm-efficiency-with-prompt-compression/)
- ["Core Context Aware Transformers" (arXiv 2024)](https://arxiv.org/abs/2412.12465)

### Experience Context-Aware Code Review

See how diffray's multi-agent architecture applies these research findings—curated context, specialized agents, and optimized attention—to deliver actionable code review feedback without context dilution.