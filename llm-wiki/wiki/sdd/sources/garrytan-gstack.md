---
title: "gstack: Garry Tan's exact Claude Code setup"
type: source
tags: [sdd, gstack, claude-code, skills, yc, agentic-workflow]
last_updated: 2026-04-29
source_file: raw/sdd/articles/garrytan-gstack-readme.md
source_url: https://github.com/garrytan/gstack
---

## Summary

gstack 是 YC CEO Garry Tan 开源的 Claude Code 技能框架，包含 23 个 opinionated 工具，将单个 Claude Code 实例转变为虚拟工程团队（CEO、设计师、工程师、QA、安全官、发布工程师等）。核心流程为 Think → Plan → Build → Review → Test → Ship → Reflect，支持并行运行 10-15 个 sprint。2026 年逻辑代码变更产出已达到 2013 年的 240 倍。

## Key Claims

- **23 个专家角色覆盖完整软件工程流程** — 从 /office-hours（CEO 式产品拷问）到 /ship（发布工程师），每个技能代表一个专业角色。
- **2026 年生产力数据：240× 2013 全年** — 逻辑代码变更（非原始 LOC）的 2026 年运行率约为 2013 年的 810 倍，年初至今已产出 2013 全年的 240 倍。
- **Think → Plan → Build → Review → Test → Ship → Reflect 的闭环流程** — 每个技能自动喂入下游技能，/office-hours 写的设计文档被 /plan-ceo-review 读取，/plan-eng-review 写的测试计划被 /qa 拾取。
- **支持 10+ AI 工具，不仅 Claude Code** — Claude Code、OpenAI Codex CLI、Cursor、GitHub Copilot CLI、OpenCode、Gemini CLI、Kiro、Hermes、Slate、Factory Droid 等。
- **可并行运行 10-15 个 sprint** — 通过 Conductor 等工具在独立 workspace 中并行运行多个 Claude Code 会话，每个 Agent 知道何时停止。
- **/browse 技能赋予 Agent"眼睛"** — 真实 Chromium 浏览器、真实点击、真实截图，~100ms 每命令。
- **/qa 是"巨大解锁"** — Agent 能打开真实浏览器、点击流程、发现 Bug、生成回归测试、验证修复。
- **Prompt Injection 多层防御** — 22MB ML 分类器 + Claude Haiku 检查 + 随机 canary token + 双重验证。

## Connections

- [[sdd/sources/obra-superpowers|Superpowers README]] — 同为 Claude Code 技能框架，gstack 更侧重"虚拟团队"角色分工
- [[sdd/sources/everyinc-compound-engineering|Compound Engineering README]] — 同为 80/20 规划执行比的理念
- [[sdd/entities/Gstack|Gstack]] — gstack 项目实体页（含源码分析）
- [[sdd/concepts/Agentic-Skills|Agentic Skills]] — Agentic Skills 框架概念页
- [[sdd/syntheses/framework-landscape|SDD 框架全景分析]] — 技能框架比较
