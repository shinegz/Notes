---
title: "Compounding Knowledge"
type: concept
tags: [sdd, compounding, knowledge-management, every]
sources:
  - sdd/sources/everyinc-compound-engineering
last_updated: 2026-04-29
---

## 一句话理解

Compounding Knowledge 是让每一次工程迭代产生的经验、模式和教训被系统性地记录下来，使后续 Agent（或人类）不需要从零学习，从而降低边际成本、加速后续开发。

## 背景

传统开发中，每次功能迭代都会积累技术债务和本地知识——Bug 修复背后的原因、架构决策的权衡、性能瓶颈的位置。这些信息往往存在于某个开发者的头脑中，或散落在 Slack 对话和 PR 评论中。下一个开发者（或 AI Agent）需要重新发现这些知识。

Compound Engineering 将这一问题倒转：**每个工程单元应该让后续单元更容易**。

## 核心机制

### 80/20 规划审查比

Compound Engineering 的分配原则是：
- **80%** — 规划（brainstorm、plan）和审查（code-review、doc-review）
- **20%** — 实际编码执行

更多的前期投入换取更少的事后返工。

### 知识复利的循环

```
brainstorm → plan → work → review → compound → [下一次迭代使用累积知识]
```

每次循环产生四类知识资产：

| 知识类型 | 产出物 | 复用方式 |
|---------|--------|---------|
| 需求模式 | requirements doc | 类似功能的参考模板 |
| 架构决策 | plan doc | 后续功能的技术约束 |
| 审查发现 | review notes | 避免重复错误的 checklist |
| 经验教训 | compound notes | 新 Agent 的上下文 |

### Compound 动作

`/ce-compound` 是 Compound Engineering 的核心技能，负责：
1. 从本次迭代中提取可复用的模式
2. 将经验教训写入持久化存储
3. 更新项目上下文，使下次 Agent 自动获取

## 与其他框架的对比

| 维度 | Compounding Knowledge | 传统文档 | Memory Bank |
|------|----------------------|---------|-------------|
| 驱动力 | 每次迭代自动产生 | 手动编写 | 预定义规则 |
| 更新频率 | 每次迭代 | 不定期 | 项目级 |
| 受众 | 下一个 Agent | 团队成员 | 所有会话 |
| 形式 | 结构化笔记 | 自由文档 | 规则文件 |

## 关联概念

- [[sdd/concepts/Agentic-Skills|Agentic Skills]] — Compounding 通过 Skills 框架自动执行
- [[sdd/concepts/Spec-Anchored|Spec-Anchored]] — 规范本身也是知识复利的一种形式

## 来源

- [[sdd/sources/everyinc-compound-engineering|Compound Engineering README]] — 核心理念与 /ce-compound 技能设计
