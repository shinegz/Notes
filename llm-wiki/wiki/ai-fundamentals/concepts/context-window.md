---
title: "Context Window"
type: concept
tags: [context-window, llm, attention, long-context]
sources:
  - ai-fundamentals/sources/rope
last_updated: 2026-04-26
---

# Context Window

**Context Window = LLM 一次能处理的最大 token 数量，包括输入和输出。**

## 一句话理解

Context Window 是 LLM 的「工作记忆」——它一次只能看到这么多 token，超出部分会被截断或忽略。

## 核心概念

| 参数 | 说明 | 典型值（2024）|
|------|------|--------------|
| **Context Length** | 最大输入 token 数 | 4K ~ 128K |
| **Position** | 当前 token 在序列中的位置 | 0 ~ 32K |
| **Working Memory** | 模型实际能有效利用的范围 | 通常 < context length |

## Context Window 的限制

| 问题 | 表现 | 影响 |
|------|------|------|
| **截断** | 超长输入被截断 | 长文档问答丢失信息 |
| **定位困难** | 中间位置信息被稀释 | "lost in the middle" |
| **计算成本** | O(n²) 或 O(n) 随长度增加 | 长上下文推理成本高 |

## "Lost in the Middle" 问题

研究发现，当信息放在 Context 的中间位置时，模型表现最差：

```
输入：[开头信息] ... [中间信息] ... [结尾信息]
                    ↑
              模型最容易忽略这里
```

这与 Transformer 的 Attention 机制有关——开头和结尾的 token 获得更多 Attention。

## 解决方案

| 方案 | 说明 | 代表技术 |
|------|------|----------|
| **RoPE** | 旋转位置编码，支持更长序列 | LLaMA, PaLM |
| **ALiBi** | 线性偏置，不用绝对位置 | BLOOM |
| **Sparse Attention** | 只关注部分位置 | Longformer |
| **Hierarchical** | 分层处理，先摘要再全文 | ChatPDF |
| **RAG** | 只检索相关内容注入 | 外部知识库 |

## Context Window vs Long-term Memory

| 类型 | 实现 | 容量 | 速度 |
|------|------|------|------|
| **Context Window** | 工作记忆，Attention 计算 | 有限（4K-128K）| 快 |
| **Long-term Memory** | Vector DB，外部存储 | 理论上无限 | 慢（需要检索）|

见 [[ai-fundamentals/concepts/vector-database|Vector Database]] 和 [[ai-fundamentals/concepts/memory|Memory]]。

## 实际影响

| 应用 | Context Window 要求 |
|------|-----------------|
| 单轮问答 | 2K-4K |
| 文档摘要 | 8K-32K |
| 多轮对话 | 16K-128K |
| 代码仓库分析 | 32K-128K |

## 来源

- [[ai-fundamentals/sources/rope|RoPE]] — 解决 Context 长度限制的核心技术
