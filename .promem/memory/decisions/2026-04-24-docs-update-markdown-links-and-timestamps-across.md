# [决策]: docs: update markdown links and timestamps across multiple files

## 日期
2026-04-24

## 背景
Co-developed-by: Aone Copilot <noreply@alibaba-inc.com>

## 决策
docs: update markdown links and timestamps across multiple files

## 影响范围
- .promem/promem.log
- .../concepts/HarnessEngineering.md
- ...350\247\243\346\236\220-Harness-Engineering.md"
- .../syntheses/harness-engineering-deep-dive.md
- .../wiki/ai-fundamentals/concepts/alignment.md
- .../concepts/attention-mechanism.md
- .../concepts/chain-of-thought-react.md
- .../wiki/ai-fundamentals/concepts/embedding.md
- .../wiki/ai-fundamentals/concepts/fine-tuning.md
- .../ai-fundamentals/concepts/function-calling.md
- .../concepts/language-model-training.md
- .../wiki/ai-fundamentals/concepts/llm-agents.md
- llm-wiki/wiki/ai-fundamentals/concepts/memory.md
- llm-wiki/wiki/ai-fundamentals/concepts/rag.md
- .../wiki/ai-fundamentals/concepts/scaling-laws.md
- .../wiki/ai-fundamentals/concepts/tokenization.md
- .../wiki/ai-fundamentals/concepts/transformer.md
- .../ai-fundamentals/concepts/vector-database.md
- llm-wiki/wiki/ai-fundamentals/overview.md
- .../wiki/ai-fundamentals/sources/agentbench.md
- llm-wiki/wiki/ai-fundamentals/sources/alexnet.md
- .../sources/attention-is-all-you-need.md
- .../ai-fundamentals/sources/bert-pre-training.md
- .../wiki/ai-fundamentals/sources/chinchilla.md
- llm-wiki/wiki/ai-fundamentals/sources/dpo.md
- .../ai-fundamentals/sources/flash-attention.md
- llm-wiki/wiki/ai-fundamentals/sources/gan.md
- .../sources/gpt3-language-models-few-shot.md
- llm-wiki/wiki/ai-fundamentals/sources/gqa.md
- .../wiki/ai-fundamentals/sources/instructgpt.md
- .../sources/llm-powered-autonomous-agents.md
- llm-wiki/wiki/ai-fundamentals/sources/lora.md
- .../sources/react-chain-of-thought.md
- llm-wiki/wiki/ai-fundamentals/sources/resnet.md
- .../ai-fundamentals/sources/rlhf-from-feedback.md
- llm-wiki/wiki/ai-fundamentals/sources/rope.md
- .../ai-fundamentals/sources/scaling-laws-kaplan.md
- .../sources/the-illustrated-transformer.md
- .../wiki/ai-fundamentals/sources/toolformer.md
- .../sources/transformer-taxonomy.md
- llm-wiki/wiki/ai-fundamentals/sources/word2vec.md
- .../ai-fundamentals/syntheses/ai-core-concepts.md
## 删除的函数/类
- `Attention(Q, K, V) = softmax(QK^T / √d_k) × V`
- `MultiHead(Q, K, V) = Concat(head_1, ..., head_h) × W^O`

## 相关注释
> **核心公式：Agent = Model + Harness**
> ## 为什么需要 Harness
> ### 1. 持久状态面（Durable State Surfaces）
> ### 2. 分解与计划（Decomposition & Plans）
> ### 3. 反馈回路（Feedback Loops）


## 相关链接
- Commit: 29d008fef42d46260d136ad2c0cd236b5b7ca655
