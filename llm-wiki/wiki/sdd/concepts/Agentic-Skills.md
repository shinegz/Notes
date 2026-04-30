---
title: "Agentic Skills"
type: concept
tags: [sdd, agentic-skills, skills-framework, claude-code]
sources:
  - sdd/sources/obra-superpowers
  - sdd/sources/garrytan-gstack
  - sdd/sources/everyinc-compound-engineering
last_updated: 2026-04-29
---

## 一句话理解

Agentic Skills 是通过可组合、自动激活的技能文件，将编码 Agent 的行为从"自由响应"约束为"强制工作流"，使 AI 在特定场景下自动遵循预定义的工程实践。

## 背景

传统的 AI 编码交互是"提示-响应"模式：人类给出提示，AI 自由生成代码。这种模式的问题是：
- Agent 不会自动询问澄清问题
- Agent 不会自动写测试
- Agent 不会自动进行代码审查
- Agent 容易偏离最佳实践

Agentic Skills 框架通过**技能文件**解决这些问题——不是给 Agent 更多提示，而是给它**行为约束**。

## 核心机制

### 技能自动激活

Agent 在执行任何任务前自动检查是否有相关技能适用。技能不是可选建议，而是**强制工作流**：

```
用户: "帮我加一个用户登录功能"
Agent: [检测到 brainstorming 技能适用]
Agent: "在写代码之前，让我们先澄清几个需求问题..."
```

### 技能的三种形态

| 形态 | 描述 | 示例 |
|------|------|------|
| 流程技能 | 定义多步骤工作流 | Superpowers 的 7 步开发流程 |
| 角色技能 | 定义特定专家角色的行为 | gstack 的 /office-hours（CEO 角色） |
| 工具技能 | 提供特定工具能力 | gstack 的 /browse（浏览器控制） |

### 技能的可组合性

多个技能可以链式组合：

```
brainstorming → writing-plans → subagent-driven-development → test-driven-development
```

上游技能的输出自动成为下游技能的输入。

### 技能在压力下的遵守

Superpowers 作者用 Cialdini 说服力原则（权威、承诺、互惠）测试 Skills 是否会被 Agent 在复杂场景下忽略。结论是"Claude went hard"——Skills 被当作权威参考而非可选建议。

## 代表框架

| 框架 | 技能数量 | 核心特点 | 支持平台 |
|------|---------|---------|---------|
| Superpowers | 14+ | 强制 TDD + 双阶段审查 | Claude Code、Codex、Cursor、Copilot、Gemini |
| gstack | 23+ | 虚拟团队角色分工 + 并行 sprint | Claude Code、Codex、Cursor、OpenCode、Kiro 等 10+ |
| Compound Engineering | 36 skills + 51 agents | 知识复利 + Brownfield-First | Claude Code、Cursor、Codex、Copilot 等 8+ |

## 关联概念

- [[sdd/concepts/Spec-First|Spec-First]] — Agentic Skills 是实现 Spec-First 的技术手段
- [[sdd/concepts/Compounding-Knowledge|Compounding Knowledge]] — Compound Engineering 的核心差异化理念

## 来源

- [[sdd/sources/obra-superpowers|Superpowers README]] — Agentic Skills Framework 的定义与实现
- [[sdd/sources/garrytan-gstack|Gstack README]] — 23 个专家角色的技能设计
- [[sdd/sources/everyinc-compound-engineering|Compound Engineering README]] — 36 skills + 51 agents 的分层架构
