---
title: "Tokenization"
type: concept
tags: [tokenization, tokenizer, bpe, preprocessing]
sources:
  - ai-fundamentals/sources/the-illustrated-transformer
  - ai-fundamentals/sources/gpt3-language-models-few-shot
last_updated: 2026-04-24
---

# Tokenization

**Tokenization = 将原始文本切分为模型可处理的 token 序列[[ai-fundamentals/sources/gpt3-language-models-few-shot|1]]。**

## 一句话理解

Tokenization 是 LLM 处理文本的第一步：把字符串切成片段，每个片段映射为一个整数 ID，再转化为 embedding 向量。

## 为什么不是按字符或按词切分

| 切分方式 | 问题 | 示例 |
|----------|------|------|
| 按字符 | 序列太长，丢失语义 | "hello" → 5 个 token |
| 按词 | 无法处理新词/复合词 | "unhappiness" 是一个词还是 "un" + "happiness"？ |
| **Subword (BPE)** | 平衡长度和语义 | "hello" ≈ 1 token，罕见词拆成子词 |

## BPE (Byte-Pair Encoding)

[[ai-fundamentals/sources/gpt3-language-models-few-shot|GPT-3]] 使用 BPE tokenizer，vocab size 为 50,257[[ai-fundamentals/sources/gpt3-language-models-few-shot|1]]。

### BPE 训练过程

```
初始：每个字符是一个 token
迭代：统计最频繁的相邻 token 对，合并成新 token
终止：达到目标 vocab size（如 50k）
```

示例：
```
语料: "low lower lowest"
初始: l o w _ l o w e r _ l o w e s t
合并 (low): low _ low er _ low est
合并 (er): low _ lower _ low est
合并 (est): low _ lower _ lowest
```

## Token 的实际表现

### 英文

| 文本 | 近似 token 数 |
|------|---------------|
| "hello" | 1 |
| "artificial intelligence" | 2-3 |
| 一段英文（~100 词） | ~130 tokens |

### 中文

中文 tokenization 更复杂：
- 常见汉字：通常 1 token/字
- 罕见汉字/生僻字：可能拆成多个 byte-level token
- 1 个汉字 ≈ 1-2 tokens（通常比英文「贵」）

### 影响

- **计费**：模型按 token 数收费（输入 + 输出）
- **Context Window**：窗口上限以 token 为单位计量
- **中文 Prompt 优化**：简洁表达 = 节省 token = 降低成本 + 容纳更多上下文

## 在 Transformer 中的位置

[[ai-fundamentals/sources/the-illustrated-transformer|The Illustrated Transformer]] 描述的流程[[ai-fundamentals/sources/the-illustrated-transformer|2]]：

```
原始文本 → Tokenizer → Token IDs → Embedding 层 → 向量 → Positional Encoding → Transformer
```

Embedding 只发生在最底层的 Encoder。所有上层 Encoder 接收的都是相同维度的向量列表。

## 来源

- [[ai-fundamentals/sources/the-illustrated-transformer|The Illustrated Transformer]] — Transformer 输入流程可视化
- [[ai-fundamentals/sources/gpt3-language-models-few-shot|GPT-3]] — BPE tokenizer, vocab size 50,257
