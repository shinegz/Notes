---
title: "Spec-First"
type: concept
tags: [sdd, spec-first, specification, ai-coding]
sources:
  - sdd/sources/martin-fowler-sdd-3-tools
  - sdd/sources/github-blog-spec-kit
last_updated: 2026-04-29
---

## 一句话理解

Spec-First 是在让 AI 写代码之前先写一份结构化规范，规范在任务完成后可被丢弃，核心目的是将模糊意图转化为 AI 可执行的明确指令。

## 背景

Vibe Coding 在原型阶段效率极高，但当项目复杂度超过单个文件时，模糊意图产生模糊代码——能跑但无人敢改。Spec-First 是 SDD 最轻量、最基础的层级，不需要改变现有开发流程，只需要在编码前增加"写规范"这一步。

## 核心机制

Spec-First 的工作流遵循一个简单原则：**人类写意图，AI 写实现**。

1. **意图捕获** — 用自然语言描述要解决的问题、用户旅程和成功标准
2. **规范结构化** — 将意图转化为行为导向的结构化制品（如用户故事 + acceptance criteria）
3. **AI 执行** — 将规范作为上下文输入给编码 Agent，由其生成代码
4. **验证与丢弃** — 任务完成后，规范可归档或丢弃，不强制长期维护

### 与 Memory Bank 的区别

Spec 只与特定功能相关，而 Memory Bank（如 `AGENTS.md`、`CLAUDE.md`）是跨会话的通用上下文。

| 维度 | Spec | Memory Bank |
|------|------|-------------|
| 范围 | 单个功能/任务 | 整个项目 |
| 生命周期 | 任务级，可丢弃 | 项目级，长期维护 |
| 内容 | 行为描述、验收标准 | 架构规则、技术约束 |
| 示例 | `user-login.md` | `CLAUDE.md`, `product.md` |

## 类型

| 类型 | 描述 | 代表工具 |
|------|------|---------|
| 轻量 Spec | 几段自然语言描述，不强制结构 | Vibe Coding + 简单需求文档 |
| 结构化 Spec | 用户故事 + acceptance criteria | Kiro Requirements |
| 流水线 Spec | 四阶段完整规范（Specify→Plan→Tasks→Implement） | Spec Kit |

## 关联概念

- [[sdd/concepts/Spec-Anchored|Spec-Anchored]] — Spec-First 的演进层级，规范不再丢弃而是长期维护
- [[sdd/concepts/Spec-as-Source|Spec-as-Source]] — 最高层级，规范即唯一源文件
- [[sdd/concepts/Agentic-Skills|Agentic Skills]] — 通过技能框架强制 Spec-First 流程自动执行

## 来源

- [[sdd/sources/martin-fowler-sdd-3-tools|Martin Fowler: SDD 三工具评测]] — 定义 Spec-First 为 SDD 第一层级
- [[sdd/sources/github-blog-spec-kit|GitHub Blog: Spec Kit 介绍]] — Spec Kit 主要实现 Spec-First
- [[sdd/sources/zhihu-sdd-landscape|知乎：SDD 框架全景]] — 渐进式 Spec 策略建议
