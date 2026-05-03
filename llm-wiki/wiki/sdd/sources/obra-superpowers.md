---
title: "Superpowers: An agentic skills framework & software development methodology"
type: source
tags: [sdd, superpowers, agentic-skills, tdd, subagent, claude-code]
last_updated: 2026-04-29
source_file: raw/sdd/articles/obra-superpowers-readme.md
source_url: https://github.com/obra/superpowers
---

## Summary

Superpowers 是 Jesse Vincent 为 Claude Code 设计的 Agentic Skills Framework，通过可组合技能自动激活机制，将开发流程从"自由编码"转变为强制工作流。核心包含 7 步工作流（brainstorming → git-worktrees → writing-plans → subagent-driven-development → TDD → code-review → finishing-branch），强调 RED-GREEN-REFACTOR 强制测试驱动和双阶段审查（spec 合规性 + 代码质量）。

## Key Claims

- **可组合技能自动激活，不是可选建议** — Agent 在执行任务前自动检查相关技能，技能是强制工作流而非提示建议。
- **7 步工作流覆盖完整开发周期** — brainstorming（苏格拉底式需求提炼）→ using-git-worktrees（隔离工作空间）→ writing-plans（2-5 分钟粒度的任务拆解）→ subagent-driven-development（子 Agent 并行执行 + 双阶段审查）→ test-driven-development（强制 RED-GREEN-REFACTOR）→ requesting-code-review（按严重度报告问题）→ finishing-a-development-branch（验证测试 + 合并决策）。
- **强制 TDD 是其核心差异化** — 写失败测试 → 看到失败 → 写最小代码 → 看到通过 → 提交。删除测试前写的代码。
- **双阶段审查机制确保质量** — 每个子任务完成后先检查 Spec 合规性，再检查代码质量。Critical issues 阻塞进度。
- **技能在压力场景下仍被遵守** — 作者用 Cialdini 说服力原则（权威、承诺、互惠）测试了 Skills 是否会被 Agent 当作权威参考而非可选建议，结论是"Claude went hard"。
- **支持 Claude Code、OpenAI Codex CLI、Cursor、GitHub Copilot CLI、Gemini CLI 等多平台** — 通过官方插件市场或 marketplace 安装。

## Connections

- [[sdd/sources/zhihu-sdd-landscape|知乎：SDD 框架全景]] — 将 Superpowers 定位为"中型/质量优先"场景的最佳选择
- [[sdd/sources/garrytan-gstack|Gstack README]] — 同为 Claude Code 生态的技能框架，但定位不同
- [[sdd/entities/Superpowers|Superpowers]] — Superpowers 项目实体页（含源码分析）
- [[sdd/concepts/Agentic-Skills|Agentic Skills]] — 可组合技能框架概念页
- [[sdd/concepts/Test-Driven-Development|Test-Driven Development]] — TDD 在 SDD 中的强制实践
- [[sdd/syntheses/framework-landscape|SDD 框架全景分析]] — 五大框架比较
