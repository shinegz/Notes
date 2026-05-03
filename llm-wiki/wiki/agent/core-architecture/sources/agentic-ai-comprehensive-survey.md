---
title: "Agentic AI: A Comprehensive Survey of Architectures, Applications, and Future Directions"
type: source
tags: [agentic-ai, survey, taxonomy, symbolic, neural, multi-agent, healthcare, finance, robotics]
last_updated: 2026-05-03
source_file: raw/agent/core-architecture/pdfs/agentic-ai-comprehensive-survey.pdf
source_url: https://arxiv.org/abs/2510.25445
---

## Summary

本文（arXiv:2510.25445, AbouAli & Dornaika, 2025）是截至 2025 年最全面的 Agentic AI 系统综述，通过 PRISMA 方法纳入 90 篇 2018–2025 年研究。核心贡献是提出**双范式框架**：将 Agentic AI 分为 Symbolic/Classical（依赖算法规划和持久状态）与 Neural/Generative（依赖随机生成和提示驱动编排）两个谱系。综述覆盖三大应用领域（医疗、金融、机器人），揭示范式选择是战略决策而非技术偏好，并指出混合 neuro-symbolic 架构是未来关键方向。

## Key Claims

- **Conceptual Retrofitting 问题**：现有综述常将 LLM-based Agent 套用 BDI/PPAR 等古典符号框架，掩盖了两类系统在随机生成 vs 算法规划上的根本差异
- **双范式框架**：
  - Symbolic/Classical：逻辑推理、显式状态维护、算法规划；适用于安全关键领域
  - Neural/Generative：随机生成、提示驱动编排、涌现 agency；适用于自适应、数据丰富环境
- **范式战略选择**：Symbolic 系统主导医疗等安全关键领域，Neural 系统主导金融等自适应领域
- **AI Agent ≠ Agentic AI**：AI Agent 是独立完成任务的自包含系统；Agentic AI 是编排多 specialized agents 协同工作的架构方法论
- **AI 五时代演进**：Symbolic AI → ML → Deep Learning → Generative AI → Agentic AI
- **Agentic AI 四大核心能力**：Proactive Planning、Contextual Memory、Sophisticated Tool Use、Environmental Feedback Adaptation
- **混合架构缺口**：当前缺乏针对 Symbolic 系统的治理模型，且混合 neuro-symbolic 架构需求迫切

## Dual-Paradigm Framework

| Dimension | Symbolic/Classical | Neural/Generative |
|-----------|------------------|-----------------|
| Core Engine | Algorithmic planner | Stochastic LLM |
| Memory | Explicit symbolic state | Emergent (context window) |
| Planning | Model-based reasoning | Prompt-driven |
| Tool Use | Structured APIs | Unstructured tool definitions |
| Multi-Agent | Contract Net, Blackboard | CrewAI, AutoGen |
| Dominant Domain | Healthcare, Safety-critical | Finance, Data-rich |

## Three Analysis Dimensions

1. **Theoretical Foundations & Architectural Principles** — 范式定义和架构原则
2. **Domain-Specific Implementations** — 医疗、金融、机器人领域的范式选择逻辑
3. **Ethical & Governance Challenges** — 范式特定的伦理和治理挑战

## Key Quotes

> "The choice of paradigm is strategic: symbolic systems dominate safety-critical domains, while neural systems prevail in adaptive, data-rich environments."

> "Agentic AI is the broader field and architectural approach concerned with creating systems that exhibit agency — often involving the orchestration of Multi-Agent Systems."

## Connections

- [[agent/core-architecture/sources/core-agentic-ai-architectural-patterns|Core Architectural Patterns]] — "Simulated Agency vs True Autonomy" 与本文 Symbolic vs Neural 框架高度对应
- [[agent/core-architecture/sources/multi-agent-system-architecture-guide|Multi-Agent Architecture Guide]] — Multi-Agent Systems 作为 Agentic AI 的协调层
- [[agent/core-architecture/sources/aws-bedrock-agentcore-best-practices|AWS Bedrock AgentCore]] — 企业级 Neural/Generative Agent 系统的实践验证