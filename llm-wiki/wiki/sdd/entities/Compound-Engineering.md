---
title: "Compound Engineering"
type: entity
tags: [sdd, compound-engineering, every, dhh, skills, agents]
last_updated: 2026-04-29
---

## Definition

Compound Engineering 是 Every（原 Basecamp 创始人 DHH 相关公司）开源的 AI 编码插件框架，核心理念是"每个工程单元应让后续单元更容易"。当前包含 36 个 skills 和 51 个 agents，支持 Claude Code、Cursor、Codex 等 8+ 平台，通过 Bun/TypeScript CLI 实现跨平台插件转换。

## Key Attributes

| 属性 | 值 |
|------|-----|
| 作者 | Every Inc |
| 仓库 | https://github.com/EveryInc/compound-engineering-plugin |
| 许可证 | 未明确标注（推测 MIT） |
| 支持平台 | Claude Code、Cursor、Codex、GitHub Copilot、OpenCode、Pi、Gemini CLI、Kiro、Qwen、Factory Droid |
| 技能数量 | 36 skills + 51 agents |
| 核心哲学 | 80% 规划审查 / 20% 执行，知识复利 |

## 源码架构

### 目录结构

```
EveryInc/compound-engineering-plugin/
├── plugins/
│   └── compound-engineering/        # 主插件目录
│       ├── .claude-plugin/          # Claude Code 市场元数据
│       ├── .codex-plugin/           # Codex CLI 插件元数据
│       ├── .cursor-plugin/          # Cursor 插件元数据
│       ├── AGENTS.md                # 35KB Agent 定义文件
│       ├── CHANGELOG.md             # 插件变更日志（102KB）
│       ├── skills/                  # 36 个技能目录
│       └── agents/                  # 51 个 Agent 目录
├── plugins/coding-tutor/            # 次要插件
├── src/                             # Bun/TypeScript CLI 转换器
│   ├── targets/                     # 各平台目标适配器
│   ├── converters/                  # Claude Code → 其他平台转换逻辑
│   └── utils/                       # 工具函数（含遗留清理）
├── tests/                           # 测试套件
│   ├── fixtures/sample-plugin/      # 测试固件
│   └── converter.test.ts            # 转换器测试
├── .agents/                         # 多平台 Agent 配置
├── .claude/                         # Claude Code 配置
├── .compound-engineering/           # 工程配置
├── AGENTS.md                        # 根级 Agent 指令（19KB，开发约定）
├── docs/                            # 文档（brainstorms, plans, solutions, specs）
│   ├── brainstorms/                 # 需求探索
│   ├── plans/                       # 实现计划
│   ├── solutions/                   # 已记录的问题解决方案
│   │   ├── developer-experience/    # 开发者体验
│   │   ├── integrations/            # 平台集成问题
│   │   ├── workflow/                # 工作流模式
│   │   └── skill-design/            # 技能设计模式
│   └── specs/                       # 目标平台格式规范
└── package.json                     # Bun/TypeScript 项目
```

### 转换器架构（src/）

Compound Engineering 的核心技术差异化在于**跨平台插件转换器**：

```
Claude Code 插件格式 → converters/ → targets/ → 其他平台格式
```

- **converters/** — 将 Claude Code 的 SKILL.md、agents/、hooks/ 转换为各平台原生格式
- **targets/** — 每个目标平台一个 writer 模块（codex.ts、opencode.ts 等）
- **显式映射优于隐式魔法** — 工具、权限、钩子、事件均有显式映射表

### 技能自包含约束

Compound Engineering 有一个严格的**技能隔离规则**：

> 每个 skill 目录是自包含单元，SKILL.md 只能引用本目录内的文件，禁止跨目录引用（`../other-skill/` 或绝对路径）。

原因：
- 运行时从工作目录执行，跨目录路径解析不可靠
- 插件市场安装路径含版本号，绝对路径会失效
- 转换器按目录隔离复制，跨目录引用会在转换后断裂

### 文档组织约定

| 目录 | 用途 |
|------|------|
| `docs/brainstorms/` | 需求探索与创意 |
| `docs/plans/` | 实现计划与进度跟踪 |
| `docs/solutions/` | 已记录的问题解决方案（YAML frontmatter 分类） |
| `docs/specs/` | 目标平台格式规范 |

### Agent 与 Skill 的分层

| 层级 | 数量 | 作用 | 示例 |
|------|------|------|------|
| Skills | 36 | 用户触发的命令 | `/ce-brainstorm`, `/ce-plan`, `/ce-work` |
| Agents | 51 | Skills 委托的自动化角色 | `ce-learnings-researcher`, `ce-session-historian` |

## Relationships

- [[sdd/concepts/Compounding-Knowledge|Compounding Knowledge]] — Compound Engineering 的核心理念
- [[sdd/concepts/Agentic-Skills|Agentic Skills]] — Skills + Agents 分层架构
- [[sdd/sources/everyinc-compound-engineering|Compound Engineering README]] — 官方项目介绍
- [[sdd/entities/Superpowers]] — 同为 Skills 框架，CE 更侧重跨平台转换
- [[sdd/entities/Gstack]] — 同为 Skills 框架，CE 更侧重知识复利

## Sources

- [[sdd/sources/everyinc-compound-engineering|Compound Engineering README]] — 官方项目介绍
- [[sdd/refs/compound-engineering-repo]] — 源码指针
