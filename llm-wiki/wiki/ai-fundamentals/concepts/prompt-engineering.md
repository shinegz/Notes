---
title: "Prompt Engineering"
type: concept
tags: [prompt-engineering, llm, instruction]
sources:
  - ai-fundamentals/sources/openai-prompt-engineering
  - ai-fundamentals/sources/anthropic-context-engineering
  - ai-fundamentals/sources/prompt-engineering-frameworks-parloa
  - ai-fundamentals/sources/openai-prompt-guidance
  - ai-fundamentals/sources/prompt-engineering-2025-aakashg
last_updated: 2026-05-06
---

# Prompt Engineering

**Prompt Engineering = 用精心设计的输入文本（Prompt）引导 LLM 产生期望输出，是 Context Engineering 的核心子集。**

## 一句话理解

Prompt 是给 LLM 的「编程接口」——同样的模型，好的 Prompt 激发强大能力，差的 Prompt 导致幻觉或无用输出。在 Agent 时代，Prompt Engineering 正向 Context Engineering 演进：从写好单次指令，升级为在有限的注意力预算内持续编排整个上下文状态。

## 核心策略

| 策略 | 说明 | 示例 |
|------|------|------|
| **写清楚指令** | 在 Prompt 中包含所有必要细节，指令放开头 | "Explain why the sky is blue in 2 sentences" |
| **给参考文本** | 让模型基于提供的内容回答，用分隔符隔离 | "Based on this article, summarize..." |
| **拆解复杂任务** | 多步骤代替一步到位 | 先提取实体 → 再分类 → 再生成 |
| **给模型思考时间** | 链式思考，让模型先推理再回答 | "Think step by step" |
| **指定输出格式** | 用示例展示格式比描述更有效 | "Company names: <comma_separated_list>" |
| **正面引导** | 说「要做什么」而非「不要做什么」 | "Refer user to help article" > "DO NOT ASK..." |

## 结构化框架

将 Prompt 设计从直觉驱动的「手艺」升级为可复现的「工程」，核心工具是结构化框架：

| 框架 | 维度 | 适用场景 |
|------|------|----------|
| **CO-STAR** | Context, Objective, Style, Tone, Audience, Response | 全面设计，生产级部署 |
| **CRISPE** | Capacity, Insight, Statement, Personality, Experiment | 变体测试 + 品牌对齐 |
| **RACE** | Role, Action, Context, Expectation | 轻量敏捷，高吞吐 |
| **BAB** | Before, After, Bridge | 共情叙事，客服/销售 |
| **ToT** | Tree of Thought | 多步推理，技术排错 |

## 核心原则

| 原则 | 说明 |
|--------|------|
| **清晰** | 明确说明要什么，不要什么 |
| **借力** | 给参考文本、举 canonical examples |
| **顺序** | 重要信息放开头或结尾 |
| **耐心** | 让模型先推理再回答 |
| **示例** | Few-shot examples 比描述更有效 |
| **正面** | 说「要做什么」替代「不要做什么」 |

## Prompt 的进化

| 阶段 | 特点 | 核心问题 |
|------|------|----------|
| 1. Zero-shot | 直接提问 | "翻译：Hello" |
| 2. Few-shot | 给示例 | "猫→cat，狗→dog，鸟→" |
| 3. Chain-of-Thought | 加推理链 | "Think step by step" |
| 4. 结构化框架 | CO-STAR/CRISPE 等框架化设计 | 从手艺到工程 |
| 5. Context Engineering | 编排整个上下文状态 | Prompt 是子集，Context 是全集 |
| 6. Agentic | Tool + Loop + 自主检索 | 自动拆解任务、Just-in-Time 上下文 |

## 为什么重要

1. **无需训练**：Prompt 可以改变模型行为，无需重新训练
2. **成本低**：相比 Fine-tuning，Prompt 的成本接近零
3. **可控性强**：通过 Prompt 可以精确控制输出格式、风格、内容
4. **模型能力边界**：很多能力需要通过 Prompt 激发，而不是自动涌现
5. **产品竞争壁垒**：Bolt/Cluely 等产品的核心差异来自系统提示设计（2025 行业共识）
6. **成本敏感**：精简结构化 Prompt 可降低 76% 的推理成本，同时减少方差和延迟

## 关联概念

- [[ai-fundamentals/concepts/chain-of-thought-react|CoT & ReAct]] — 给模型「思考时间」的具体方法
- [[ai-fundamentals/concepts/llm-agents|Agent]] — Agent 的核心能力之一是动态生成 Prompt
- [[ai-fundamentals/concepts/fine-tuning|Fine-tuning]] — 当 Prompt 无法满足需求时的替代方案
- [[ai-fundamentals/concepts/context-window|Context Window]] — 物理限制驱动从 Prompt 向 Context Engineering 演进

## 来源

- [[ai-fundamentals/sources/openai-prompt-engineering|OpenAI Prompt Engineering Guide]] — 官方最佳实践
- [[ai-fundamentals/sources/anthropic-context-engineering|Anthropic Context Engineering]] — Prompt → Context 的范式演进
- [[ai-fundamentals/sources/prompt-engineering-frameworks-parloa|Prompt Engineering Frameworks]] — 8 大结构化框架
- [[ai-fundamentals/sources/openai-prompt-guidance|OpenAI Help Center Best Practices]] — 实操策略
- [[ai-fundamentals/sources/prompt-engineering-2025-aakashg|Prompt Engineering in 2025]] — 产品实践与成本经济学
