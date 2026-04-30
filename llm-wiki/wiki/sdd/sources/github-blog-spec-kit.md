---
title: "Spec-driven development with AI: Get started with a new open source toolkit"
type: source
tags: [sdd, spec-kit, github, specify, plan, tasks, implement]
last_updated: 2026-04-29
source_file: raw/sdd/articles/github-blog-spec-driven-development.md
source_url: https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/
---

## Summary

GitHub 发布的开源工具包 Spec Kit 将 SDD 定义为四阶段流水线（Specify → Plan → Tasks → Implement），核心主张是将规范从"静态文档"转变为"活的、可执行的制品"，让意图（intent）而非代码成为真相来源。每个阶段都设置人类验证检查点，适用于 Greenfield 项目、现有系统功能迭代和遗留系统现代化三种场景。

## Key Claims

- **"意图是真相"正在取代"代码是真相"** — AI 使规范变得可执行，规范决定构建什么，而不仅仅是描述。
- **四阶段流水线各有明确职责边界** — Specify（用户旅程与成功标准）→ Plan（技术架构与约束）→ Tasks（可独立验证的小粒度工作单元）→ Implement（逐任务编码与验证）。每个阶段完成前不可进入下一阶段。
- **AI 是模式完成高手，但不是读心者** — 模糊提示迫使模型猜测数千个未声明的需求，而清晰规范 + 技术计划 + 聚焦任务提供了可执行性。
- **规范驱动的迭代成本远低于传统重写** — 需要改变方向时只需更新规范、重新生成计划，而非昂贵的手动重构。
- **组织级约束可以内建于规范中** — 安全策略、合规规则、设计系统约束从第一天就 baked into the spec，而非事后补充。
- **三种场景最适合 Spec Kit** — Greenfield（从零到一，确保 AI 构建真正意图）、Feature Work（N 到 N+1，强制澄清与现有系统的交互）、Legacy Modernization（用现代规范捕获业务逻辑，让 AI 重建系统）。

## Key Quotes

> "We're moving from 'code is the source of truth' to 'intent is the source of truth.'" — 核心范式转移

> "Crucially, your role isn't just to steer. It's to verify. At each phase, you reflect and refine." — 人类在每个阶段的责任

## Connections

- [[sdd/sources/martin-fowler-sdd-3-tools|Martin Fowler: SDD 三工具评测]] — 对 Spec Kit 的独立实测与质疑
- [[sdd/entities/Spec-Kit]] — GitHub 官方 SDD 工具包实体页
- [[sdd/concepts/Spec-First]] — Spec Kit 当前主要实现的层级
- [[sdd/syntheses/framework-landscape|SDD 框架全景分析]] — 将 Spec Kit 放入五大框架比较
