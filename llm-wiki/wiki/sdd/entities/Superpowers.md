---
title: "Superpowers"
type: entity
tags: [sdd, superpowers, agentic-skills, jesse-vincent, claude-code]
last_updated: 2026-04-29
---

## Definition

Superpowers 是 Jesse Vincent（RT 工单系统作者）为 Claude Code 等 AI 编码工具设计的 Agentic Skills Framework，通过可组合技能自动激活机制，将开发流程从自由编码约束为强制工作流，核心包含 7 步开发流程和强制 TDD。

## Key Attributes

| 属性 | 值 |
|------|-----|
| 作者 | Jesse Vincent (Best Practical Solutions / Prime Radiant) |
| 仓库 | https://github.com/obra/superpowers |
| 许可证 | MIT |
| 支持平台 | Claude Code、OpenAI Codex CLI、Cursor、GitHub Copilot CLI、Gemini CLI、OpenCode |
| 技能数量 | 14+ |
| 核心哲学 | TDD 强制、系统化优于随意、复杂度降低、证据优于声明 |

## 源码架构

### 目录结构

```
obra/superpowers/
├── skills/                          # 核心技能目录（14 个技能）
│   ├── brainstorming/               # 苏格拉底式需求提炼
│   │   ├── SKILL.md                 # 技能定义（10KB+）
│   │   ├── scripts/                 # 辅助脚本
│   │   └── spec-document-reviewer-prompt.md
│   ├── test-driven-development/     # 强制 RED-GREEN-REFACTOR
│   ├── subagent-driven-development/ # 子 Agent 并行执行 + 双阶段审查
│   ├── writing-plans/               # 任务拆解（2-5 分钟粒度）
│   ├── using-git-worktrees/         # 隔离工作空间
│   ├── requesting-code-review/      # 代码审查（按严重度阻塞）
│   ├── finishing-a-development-branch/ # 分支收尾
│   └── ...                          # 其他技能
├── agents/                          # Agent 定义
├── commands/                        # 命令定义
├── hooks/                           # 生命周期钩子
├── .claude-plugin/                  # Claude Code 插件元数据
├── .codex-plugin/                   # Codex CLI 插件元数据
├── .cursor-plugin/                  # Cursor 插件元数据
├── .opencode/                       # OpenCode 插件配置
├── tests/                           # 测试套件（多场景）
│   ├── skill-triggering/            # 技能自动触发测试
│   ├── subagent-driven-dev/         # 子 Agent 测试项目
│   └── explicit-skill-requests/     # 显式技能请求测试
├── docs/                            # 文档与规格
│   └── superpowers/specs/           # 设计规格文档
├── CLAUDE.md                        # 贡献者指南（94% PR 拒绝率）
└── AGENTS.md                        # Agent 指令（9 字节，极精简）
```

### 技能系统架构

Superpowers 的技能系统遵循**统一目录约定**：

- 每个技能一个目录，目录名即技能名
- `SKILL.md` — 技能核心定义（行为指令、触发条件、输入输出）
- `scripts/` — 可选的辅助脚本（如元数据提取）
- `references/` — 可选的参考文件

### 多平台分发

Superpowers 通过**平台专属插件目录**实现多平台支持：

| 平台 | 插件目录 | 安装方式 |
|------|---------|---------|
| Claude Code | `.claude-plugin/` | 官方市场 / marketplace |
| Codex CLI | `.codex-plugin/` | 插件搜索 |
| Cursor | `.cursor-plugin/` | `/add-plugin` |
| OpenCode | `.opencode/` | 手动配置 |

### 关键设计决策

- **零依赖** — 不引入第三方依赖，保持轻量
- **技能即代码** — SKILL.md 不是文档，而是塑造 Agent 行为的"代码"
- **94% PR 拒绝率** — 极高的质量门槛，防止 AI slop PR

## Relationships

- [[sdd/concepts/Agentic-Skills|Agentic Skills]] — Superpowers 是 Agentic Skills 框架的代表实现
- [[sdd/concepts/Spec-First|Spec-First]] — 7 步工作流实现了 Spec-First 理念
- [[sdd/entities/Gstack|Gstack]] — 同为 Claude Code 技能框架，设计哲学不同
- [[sdd/entities/Compound-Engineering|Compound Engineering]] — 同为 Skills + Agents 架构

## Sources

- [[sdd/sources/obra-superpowers|Superpowers README]] — 官方项目介绍
