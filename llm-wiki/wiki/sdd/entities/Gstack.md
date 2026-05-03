---
title: "Gstack"
type: entity
tags: [sdd, gstack, garry-tan, yc, claude-code, skills]
last_updated: 2026-04-29
---

## Definition

Gstack 是 YC CEO Garry Tan 开源的 Claude Code 技能框架，包含 23 个 opinionated 工具，将单个 Claude Code 实例转变为覆盖完整软件工程流程的虚拟团队（CEO、设计师、工程师、QA、安全官等），支持并行运行 10-15 个 sprint。

## Key Attributes

| 属性 | 值 |
|------|-----|
| 作者 | Garry Tan (Y Combinator President & CEO) |
| 仓库 | https://github.com/garrytan/gstack |
| 许可证 | MIT |
| 支持平台 | Claude Code、Codex CLI、Cursor、OpenCode、Gemini CLI、Kiro、Hermes、Slate、Factory Droid 等 10+ |
| 技能数量 | 23+ skills + 8 power tools + 2 standalone CLIs |
| 核心哲学 | Think → Plan → Build → Review → Test → Ship → Reflect |

## 源码架构

### 目录结构

```
garrytan/gstack/
├── office-hours/                    # CEO 式产品拷问
├── plan-ceo-review/                 # 战略审查（4 种范围模式）
├── plan-eng-review/                 # 工程架构锁定
├── plan-design-review/              # 设计质量审计
├── plan-devex-review/               # 开发者体验审查
├── design-consultation/             # 设计系统构建
├── design-shotgun/                  # AI  mockup 变体探索
├── design-html/                     # Pretext 计算布局引擎
├── review/                          # Staff Engineer 代码审查
├── qa/                              # QA Lead 真实浏览器测试
├── qa-only/                         # 纯报告模式
├── ship/                            # 发布工程师
├── land-and-deploy/                 # 合并 + 部署 + 验证
├── canary/                          # SRE 级部署后监控
├── cso/                             # 首席安全官（OWASP + STRIDE）
├── benchmark/                       # 性能基准测试
├── browse/                          # 浏览器控制（核心子系统）
│   ├── src/                         # Bun TypeScript 服务端
│   ├── bin/                         # 编译后的二进制
│   ├── test/                        # 测试套件
│   └── scripts/                     # 辅助脚本
├── browser-skills/                  # 浏览器域技能（如 HackerNews）
├── agents/                          # Agent 定义
├── design/                          # Pretext 设计引擎源码
├── hosts/                           # 多平台适配器
├── openclaw/                        # OpenClaw 原生技能
│   └── skills/                      # 4 个 OpenClaw 对话技能
├── supabase/                        # 遥测数据库（schema + edge functions）
├── lib/                             # 共享库
├── bin/                             # CLI 工具
├── scripts/                         # 构建与辅助脚本
├── docs/                            # 文档（designs, evals, images）
├── test/                            # 测试
├── ARCHITECTURE.md                  # 详细架构文档（30KB）
├── CLAUDE.md                        # Claude Code 配置（43KB）
├── BROWSER.md                       # 浏览器命令参考（57KB）
├── CHANGELOG.md                     # 变更日志（428KB）
├── ETHOS.md                         # Builder 哲学
├── DESIGN.md                        # 设计系统文档
└── package.json                     # Bun/TypeScript 项目
```

### 浏览器子系统（browse/）

Gstack 的技术硬核在浏览器控制子系统：

- **Chromium Daemon 模型** — 长驻内存的 Chromium 进程，通过 localhost HTTP 与 CLI 通信
- **Bun 编译二进制** — `bun build --compile` 产出 ~58MB 单文件可执行程序
- **双监听器安全架构** — Local listener（127.0.0.1，完整功能）+ Tunnel listener（ngrok，受限命令集）物理隔离
- **Ref 系统** — 通过 ARIA 树分配 `@e1`、`@e2` 等引用标识，避免 DOM 注入
- **多层 Prompt Injection 防御** — L1-L6 六层防御：内容安全、22MB BERT-small ONNX 分类器、Claude Haiku 检查、Canary token、双重验证组合器

### 技能组织方式

与 Superpowers 的 `skills/` 集中目录不同，gstack 的每个技能是**根级目录**，技能之间通过目录命名空间自然隔离。

### 多平台适配

Gstack 通过 `hosts/` 目录为每个目标平台生成适配配置：

| 平台 | 适配目录 | 技能安装路径 |
|------|---------|------------|
| Claude Code | `claude/` | `~/.claude/skills/` |
| Codex CLI | `codex/` | `~/.codex/skills/` |
| Cursor | `cursor/` | `~/.cursor/skills/` |
| OpenCode | `hosts/opencode` | `~/.config/opencode/skills/` |
| Kiro | `hosts/kiro` | `~/.kiro/skills/` |

## Relationships

- [[sdd/concepts/Agentic-Skills|Agentic Skills]] — gstack 是 Agentic Skills 框架的最完整实现
- [[sdd/sources/garrytan-gstack|Gstack README]] — 官方项目介绍
- [[sdd/entities/Superpowers|Superpowers]] — 同为 Claude Code 技能框架，Superpowers 更轻量
- [[sdd/entities/Compound-Engineering|Compound Engineering]] — 同为 Skills + Agents 架构，CE 侧重知识复利

## Sources

- [[sdd/sources/garrytan-gstack|Gstack README]] — 官方项目介绍
