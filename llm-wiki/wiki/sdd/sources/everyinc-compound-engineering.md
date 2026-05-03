---
title: "Compound Engineering: Official plugin for Claude Code, Codex, Cursor, and more"
type: source
tags: [sdd, compound-engineering, every, skills, agents, compounding]
last_updated: 2026-04-29
source_file: raw/sdd/articles/everyinc-compound-engineering-readme.md
source_url: https://github.com/EveryInc/compound-engineering-plugin
---

## Summary

Compound Engineering 是 Every（原 Basecamp 创始人 DHH 所在公司）开源的 AI 技能与 Agent 框架，核心理念是"每个工程单元应让后续单元更容易——而非更难"。采用 80/20 规划审查比，核心循环为 brainstorm → plan → work → review → compound，当前包含 36 个 skills 和 51 个 agents，支持 Claude Code、Cursor、Codex、GitHub Copilot 等 8+ 平台。

## Key Claims

- **80% 规划与审查，20% 执行** — 与传统开发积累技术债务相反，Compound Engineering 通过充分规划和审查实现"知识复利"。
- **核心循环：brainstorm → plan → work → review → compound** — 每次迭代让后续工作更容易：brainstorm  sharpen plans，plans inform future plans，reviews catch patterns，compound notes document learnings。
- **36 skills + 51 agents 的分层架构** — Skills 是用户触发的命令（/ce-brainstorm、/ce-plan、/ce-work 等），agents 是 skills 委托的自动化角色（评审员、研究员、工作流代理）。
- **知识复利是核心差异化** — /ce-compound 将学习成果文档化，使下一个 Agent 不需要从零学习同样的教训。
- **Brownfield-First 设计** — 与 OpenSpec 类似，强调在已有代码库上的持续演进，而非仅适用于新项目。
- **多平台支持通过 Bun/TypeScript 转换器实现** — Claude Code 原生插件市场安装，其他平台（Codex、Cursor、OpenCode、Pi、Gemini、Kiro、Qwen、Factory Droid）通过 Bun CLI 转换安装。
- **/ce-setup 一键环境检查与配置引导** — 自动检查环境、安装缺失工具、初始化项目配置。

## Connections

- [[sdd/sources/garrytan-gstack|Gstack README]] — 同为技能框架，都强调规划优先和流程闭环
- [[sdd/sources/obra-superpowers|Superpowers README]] — 同为 Claude Code 生态的技能框架
- [[sdd/entities/Compound-Engineering|Compound Engineering]] — Compound Engineering 项目实体页（含源码分析）
- [[sdd/concepts/Compounding-Knowledge|Compounding Knowledge]] — 知识复利的概念页
- [[sdd/syntheses/framework-landscape|SDD 框架全景分析]] — 技能框架比较
