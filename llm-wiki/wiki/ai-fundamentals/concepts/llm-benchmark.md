---
title: "LLM Benchmark"
type: concept
tags: [benchmark, evaluation, mmlu, performance]
sources:
  - ai-fundamentals/sources/mmlu
last_updated: 2026-04-26
---

# LLM Benchmark

**Benchmark = 标准化的评测任务，用于衡量 LLM 的能力。**

## 一句话理解

Benchmark 是 LLM 的「考试」——用统一标准让不同模型可以横向对比，揭示模型能力的长短板。

## 常见 Benchmark

| Benchmark | 侧重 | 说明 |
|----------|------|------|
| **MMLU** | 多学科知识 | 57 个学科，从数学到医学 |
| **GSM8K** | 数学推理 | 8K 小学数学题 |
| **MATH** | 数学竞赛 | 高中/大学数学题 |
| **HumanEval** | 代码生成 | LeetCode 风格编程题 |
| **BBH** | 复杂推理 | BigBench Hard 任务 |
| **TruthfulQA** | 真实性 | 检验幻觉和偏见 |
| **Chatbot Arena** | 人类偏好 | 盲测 ELO 排名 |

## MMLU 详解

**MMLU（大规模多任务语言理解）** 是最重要的大模型评测基准之一：

- **57 个学科**：STEM、人文、社会科学全覆盖
- **测试预训练知识**：而非快速学习能力
- **从易到难**：AMCU → 高中 → 专业考试

| 准确率 | 代表模型（参考） |
|--------|----------------|
| ~25% | Random baseline |
| ~43% | GPT-3 (5-shot) |
| ~76% | GPT-3.5 |
| ~86% | GPT-4 |
| ~91% | Claude 3 Opus |

## Benchmark 的局限性

| 问题 | 说明 |
|------|------|
| **数据污染** | 评测数据可能出现在训练集中 |
| **过拟合评测** | 模型针对 Benchmark 优化，但泛化能力差 |
| **能力偏向** | 擅长考试 ≠ 擅长实际任务 |
| **不完整性** | 没有 Benchmark 能覆盖所有能力 |

## 评测维度

| 维度 | 关键 Benchmark |
|------|---------------|
| 知识 | MMLU, TriviaQA |
| 推理 | GSM8K, MATH, BBH |
| 代码 | HumanEval, MBPP |
| 工具使用 | API-Bank, GAIA |
| 对话 | Chatbot Arena |

## 与其他概念的关系

- [[ai-fundamentals/concepts/language-model-training|Language Model Training]] — Benchmark 反映训练效果
- [[ai-fundamentals/concepts/llm-agents|Agent]] — Agent 能力需要更复杂的评测（如 GAIA）

## 来源

- [[ai-fundamentals/sources/mmlu|MMLU]] — 原始论文
