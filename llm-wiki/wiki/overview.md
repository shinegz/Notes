---
title: "Overview"
type: synthesis
tags: [overview]
sources: []
last_updated: 2026-04-14
---

# Living overview

> 随每次 ingest / compile 更新；与其他 wiki 页用双向链接互指（见 `CLAUDE.md` 约定）。

## 当前综合

- **AI Fundamentals**：AI 理论基础知识库，涵盖 Transformer 架构、预训练、Scaling Laws、RLHF、LLM Agent 等核心概念。2026-04-19 完成初始化：6 个主题 source 摘要 + 5 篇概念页。2026-04-23 **re-ingest**：新增 18 个 source 摘要（3 articles + 2 refs + 13 PDFs），覆盖 Agent 系统、Transformer 可视化与 taxonomy、Alignment（RLHF/DPO）、效率优化（LoRA/GQA/RoPE）、Scaling Laws（Chinchilla）、经典工作（AlexNet/ResNet/word2vec/GAN）及历史趋势。2026-05-06 **Prompt Engineering 系统理论补充**：新增 4 篇 source（Anthropic Context Engineering、OpenAI Help Center 指南、Parloa 框架综述、aakashg 产品实践）+ 3 篇 PDF；更新 Prompt Engineering 概念页（结构化框架 + Context Engineering 演进）；新建 Context Engineering 概念页；新增 Prompt 写作流程综合页（五步走：定意图 → 选路径 → 填结构 → 跑 & 诊断 → 压缩）。2026-05-07 **从原理出发谈 Prompt**：新增综合页，从自回归预测、注意力机制、ICL、对齐、Context Window 五条底层原理推导 Prompt 技巧的有效性；Collect 7 个新素材（Lost in the Middle、ICL as Bayesian Inference、Prompt Engineering Survey、Context Dilution 等）。见子主题 [[ai-fundamentals/index|ai-fundamentals]]、总览 [[ai-fundamentals/overview|ai-fundamentals overview]]。

- **Harness Engineering**：多文共识是「**Agent = Model + Harness**」——可靠编码智能体取决于仓库内**可执行的**约束与反馈（短入口文档 + 结构化 `docs/`、CI/lint、测试、观测、长程任务的状态工件等）。2026-04-14 已 **re-collect**：`raw/agent/harness-engineering/articles/` 与 11 篇 `sources/` 摘要同步更新。见概念页 [[agent/harness-engineering/concepts/HarnessEngineering|Harness Engineering]]、深度解析 [[agent/harness-engineering/syntheses/harness-engineering-deep-dive|Harness Engineering 深度解析]]，与子主题 [[agent/harness-engineering/index|harness-engineering]]。
