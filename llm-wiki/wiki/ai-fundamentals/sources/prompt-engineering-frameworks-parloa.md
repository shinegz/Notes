---
title: "Prompt Engineering Frameworks (Parloa)"
type: source
tags: [prompt-engineering, frameworks, CO-STAR, CRISPE, costar]
last_updated: 2026-05-06
source_file: raw/ai-fundamentals/articles/prompt-engineering-frameworks-parloa.md
source_url: https://www.parloa.com/knowledge-hub/prompt-engineering-frameworks/
---

## Summary

Prompt Engineering 从直觉驱动的「手艺」走向结构化的「学科」，关键转变在于引入框架。框架提供命名规范、共享词汇、工具支持和评估对齐，使 Prompt 设计可复现、可协作、可迭代。

## Key Claims

- **框架化的必要性**：没有框架，每个 Prompt 都是定制的；有了框架，Prompt Engineering 变为结构化工程。框架提供命名规范、共享词汇、工具支持、评估对齐四个核心价值。
- **CO-STAR 框架**（Context, Objective, Style, Tone, Audience, Response）：2024 年新加坡 GPT-4 Prompt Engineering 竞赛冠军方案。将 Prompt 设计视为全栈设计挑战，从业务目标到受众到输出格式全覆盖。
- **CRISPE 框架**（Capacity/role, Insight, Statement, Personality, Experiment）：OpenAI 内部发展出的框架，平衡结构化分析与探索式实验，特别适合需要变体测试和品牌人格对齐的场景。
- **BAB 框架**（Before-After-Bridge）：源自经典文案写作，适用于需要共情叙事的场景——先建立痛点，再描绘期望状态，最后给出路径。
- **Tree of Thought（ToT）**：比 Chain-of-Thought 更高阶的推理框架，在每一步生成多个候选、递归探索、排序路径，适合需要多步推理和技术排错的场景。
- **RACE 框架**（Role, Action, Context, Expectation）：轻量敏捷框架，适合高吞吐量场景，只提供刚好够用的脚手架。
- **Five S 模型**（Set the scene, Specify task, Simplify language, Structure response, Share feedback）：源自教育领域，强调可教性和迭代，适合团队内部 Prompt 素养培养。
- **Agile Prompt Engineering**：借鉴敏捷软件开发，分层部署（basic → advanced）、跨职能评审、基于真实指标持续评估。
- **2025+ 趋势**：多模态编排（图像/语音/视频协同）、程序化生成（DSPy 等将 Prompt 视为可版本化/可优化的程序化对象）、Prompt 审计成为合规面。

## Connections

- [[ai-fundamentals/concepts/prompt-engineering|Prompt Engineering]] — 框架是 Prompt Engineering 的结构化方法论
- [[ai-fundamentals/concepts/chain-of-thought-react|CoT & ReAct]] — ToT 是 CoT 的高阶变体
- [[ai-fundamentals/sources/openai-prompt-engineering|OpenAI Prompt Engineering Guide]] — OpenAI 的基础策略是框架的底层基石
- [[ai-fundamentals/sources/anthropic-context-engineering|Anthropic Context Engineering]] — Context Engineering 是框架之上的系统级演进
