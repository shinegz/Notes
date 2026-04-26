---
title: "MMLU: Massive Multitask Language Understanding"
type: source
tags: [mmlu, benchmark, evaluation, multitask]
sources: []
last_updated: 2026-04-26
source_file: raw/ai-fundamentals/pdfs/mmlu.pdf
source_url: https://arxiv.org/abs/2009.03300
---

## Summary

Hendrycks et al. 提出 **MMLU（大规模多任务语言理解测试）**，涵盖 57 个学科，从初等数学到专业医学，测试模型在预训练阶段积累的世界知识和问题解决能力。

## Key Claims

- **57 个学科领域**：涵盖人文、社会科学、自然科学、技术等
- **从易到难**：包括 AMCU（初等数学）、HS（美国高中）、MCAT（医学院入学考试）等
- **测试预训练知识**：不是测试快速学习能力，而是测试模型从预训练中学到的知识
- **Few-shot 或 zero-shot**：可以用 few-shot 或 zero-shot 方式评估

## 57 个学科分类

| 类别 | 学科数量 | 示例 |
|------|----------|------|
| STEM | ~20 | 数学、物理、化学、计算机 |
| 人文 | ~15 | 历史、文学、哲学、法律 |
| 社会科学 | ~10 | 经济、心理学、政治 |
| 其他 | ~10 | 医学、会计、音乐 |

## MMLU 的意义

1. **跨学科评估**：打破单一任务评估的局限
2. **知识深度测试**：57 个学科需要广泛而深入的世界知识
3. **模型能力区分**：顶尖模型（如 GPT-4） vs 普通模型差距巨大
4. **教育应用**：可以作为入学考试、资格认证的代理

## 基准分数（参考）

| 模型 | 平均准确率 |
|------|-----------|
| Random | ~25% |
| GPT-3 (5-shot) | ~43% |
| GPT-4 | ~86% |
| Claude 3 Opus | ~91% |

## Connections

- [[ai-fundamentals/concepts/language-model-training|Language Model Training]] — MMLU 是评估预训练效果的基准
- [[ai-fundamentals/sources/llm-powered-autonomous-agents|LLM Powered Autonomous Agents]] — Agent 能力评测也会参考 MMLU
