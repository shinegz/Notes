---
title: "Harness Engineering 深度解析"
type: synthesis
tags: [harness-engineering, agent, deep-dive, zh]
sources:
  - agent/harness-engineering/sources/深度解析-Harness-Engineering
  - agent/harness-engineering/sources/anthropic-effective-harnesses-long-running-agents
  - agent/harness-engineering/sources/martin-fowler-harness-engineering
  - agent/harness-engineering/sources/langchain-anatomy-of-an-agent-harness
  - agent/harness-engineering/sources/openai-harness-engineering-zh
  - agent/harness-engineering/sources/humanlayer-skill-issue-harness-engineering
  - agent/harness-engineering/sources/ignorance-emerging-harness-engineering
  - agent/harness-engineering/sources/mitchellh-ai-adoption-journey-step-5-harness
  - agent/harness-engineering/sources/anthropic-building-c-compiler
  - agent/harness-engineering/sources/parallel-what-is-an-agent-harness
  - agent/harness-engineering/sources/philschmid-agent-harness-2026
last_updated: 2026-04-24
---

# Harness Engineering 深度解析

Harness Engineering 是 2025 年前后兴起的工程领域，核心命题是：如何让 LLM 从「能说」进化到「能做事、能把事做成、能在长时间跨度内把复杂的事做成」。

---

## 核心公式

**Agent = Model + Harness**

这个等式来自 Anthropic 的官方定义[[agent/harness-engineering/sources/anthropic-effective-harnesses-long-running-agents|1]]，已在行业形成共识。关键洞察在于：评估一个 Agent 的实际能力时，评估对象是 **model + harness 的组合**，而非模型单独的性能指标。

```
┌─────────────────────────────────────────────────────────┐
│                        Agent                            │
├─────────────────────┬───────────────────────────────────┤
│       Model         │             Harness               │
│  内循环：推理生成    │   外循环：编排、验证、状态管理     │
└─────────────────────┴───────────────────────────────────┘
```

Harness 不是更长的 system prompt，不是某个框架（LangChain、CrewAI 之流），更不是可选的「锦上添花」。

Harness 是让模型能够作为 Agent 行动起来的**外循环系统**——包含计划分解、持久状态、工具编排、验证门控、反馈回路、回退机制、人机交接点和审计日志[[agent/harness-engineering/sources/parallel-what-is-an-agent-harness|2]]。

---

## 为什么需要 Harness

长程任务中，模型单独运行时面临五大根本挑战[[agent/harness-engineering/sources/深度解析-Harness-Engineering|3]]：

| 挑战 | 本质 | 为什么模型单独解决不了 |
|------|------|----------------------|
| **状态持久性** | Agent 需跨时间、跨 session 记住做过什么 | 模型无状态，context window 有上限 |
| **目标一致性** | 长任务中容易漂移、自嗨、提前宣布完成 | 模型缺少外部锚点来校准「什么才算真正完成」 |
| **行动可验证性** | 每一步都是概率性的，需区分「做了」和「做对了」 | 模型评价自己结果时存在自我表扬倾向 |
| **熵增抑制** | 持续产出累积冗余、漂移和不一致 | 模型会复制已有模式——哪怕那些模式本身是坏的 |
| **人机边界** | 何时自主、何时交给人 | 模型没有可靠的「不确定性自觉」 |

这些挑战的共性：**它们是系统性问题，不能靠更聪明的模型单独解决**。需要一个工程化的外循环来约束。

---

## 三层抽象

```
┌────────────────────────────────────────────────────────────┐
│                  Harness Engineering                       │
│              （整条流水线怎么运转）                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Context Engineering                    │  │
│  │               （每一步喂什么）                        │  │
│  │  ┌────────────────────────────────────────────────┐  │  │
│  │  │           Prompt Engineering                   │  │  │
│  │  │           （怎么问得更好）                       │  │  │
│  │  └────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

Context Engineering 是 Harness Engineering 的子集[[agent/harness-engineering/sources/深度解析-Harness-Engineering|3]]。Harness 还包含多步结构、工具中介、验证门和 durable state——这些都超出了单步 context 的范畴。

---

## 六大工程构件

### 1. 持久状态面（Durable State Surfaces）

长时 Agent 的核心痛点：每个新会话没有上一会话的记忆，就像项目组里工程师每次换班都完全失忆[[agent/harness-engineering/sources/anthropic-effective-harnesses-long-running-agents|1]]。

Anthropic 的解法是 initializer agent + coding agent 双角色策略[[agent/harness-engineering/sources/anthropic-effective-harnesses-long-running-agents|1]]：

```
session 1 (initializer):
  ├─ init.sh           # 启动脚本
  ├─ progress.txt      # 进度日志
  ├─ feature-list.json # 结构化功能清单，初始全 failing
  └─ git commit        # 基线快照

session 2+ (coding):
  ├─ 读取 feature-list + git diff
  ├─ 30 秒内续航
  └─ 增量推进，留下 clean state
```

关键规则：Agent 只能改 feature 的 `passes` 状态，不能随意修改测试定义本身[[agent/harness-engineering/sources/anthropic-effective-harnesses-long-running-agents|1]]。

Context Anxiety 问题：即使有 compaction，Agent 仍可能因「上下文太满」而行为退化。Anthropic 的解决方案是 **context reset**——直接给下一个 Agent 全新 context，通过外化状态工件传递信息[[agent/harness-engineering/sources/anthropic-effective-harnesses-long-running-agents|1]]。

### 2. 分解与计划（Decomposition & Plans）

给 Agent 说「build a clone of claude.ai」，它会一把梭——结果要么上下文爆了，要么做到一半宣布「完成」[[agent/harness-engineering/sources/深度解析-Harness-Engineering|3]]。

演进路径[[agent/harness-engineering/sources/深度解析-Harness-Engineering|3]]：

```
2025-11:  initializer + coding (二角色)
           ↓
2026-03:  planner + generator + evaluator (三角色)
```

| 角色 | 职责 |
|------|------|
| Planner | 高层描述 → product spec + feature list |
| Generator | 逐 feature 落地，完成即 commit |
| Evaluator | 独立评估，标记 pass/fail，给改进建议 |

设计原理：计划必须是 **一等工件**——写入文件系统、被版本管理、被后续 Agent 可读取、被验证门引用[[agent/harness-engineering/sources/深度解析-Harness-Engineering|3]]。存在于对话里的计划，只是一次想法。

### 3. 反馈回路（Feedback Loops）

Martin Fowler 提出的 Guides vs Sensors 2×2 矩阵[[agent/harness-engineering/sources/martin-fowler-harness-engineering|4]]：

```
                 │ Computational    │ Inferential
                 │ (确定性)        │ (推断性)
─────────────────┼─────────────────┼──────────────────
Guides           │ linter, 类型检查 │ LLM review rules
(行动前约束)      │ 架构边界规则     │ 风格指南
─────────────────┼─────────────────┼──────────────────
Sensors          │ 测试套件, CI     │ LLM code review
(行动后反馈)      │ 可观测性指标     │ UI 美观度判断
```

关键洞察[[agent/harness-engineering/sources/martin-fowler-harness-engineering|4]]：

- 只有 guides 没有 sensors → 编码了规则但不知道是否生效
- 只有 sensors 没有 guides → 不断重复同样错误再被纠正
- Computational 控制：便宜、快、确定性，可跑在每次变更
- Inferential 控制：贵、慢、非确定性，但能处理主观判断

Anthropic 发现：Evaluator 不是永远必要——当底模能力跨过阈值后，evaluator 从「必要部件」退化为「额外开销」。好的 harness 是**与模型能力边界共同演进的可裁剪系统**[[agent/harness-engineering/sources/深度解析-Harness-Engineering|3]]。

### 4. 可感知性（Legibility）

OpenAI 的判断：凡是不在 Agent 运行时可见范围内的知识，就等于不存在[[agent/harness-engineering/sources/深度解析-Harness-Engineering|3]]。

具体做法：

- 每个 git worktree 启动独立浏览器实例（CDP）
- logs、metrics、traces 全部暴露给 Agent 查询
- Repository knowledge 作为 system of record：
  - 设计原则
  - 产品意图
  - 执行计划
  - 已知技术债
  - 架构决策记录（ADR）

警告：超长 `AGENTS.md` 会快速腐烂、挤占上下文、让所有约束同时失焦[[agent/harness-engineering/sources/openai-harness-engineering-zh|5]]。更好的做法是把它变成**目录索引**，真正知识拆散到结构化文档。

### 5. 工具中介（Tool Mediation）

MCP 生态爆发后，一个 Agent 可能连接几十个 MCP 服务器、上百个工具——token 成本暴增、延迟上升、Agent 迷失方向[[agent/harness-engineering/sources/深度解析-Harness-Engineering|3]]。

Anthropic 的核心思路[[agent/harness-engineering/sources/anthropic-effective-harnesses-long-running-agents|1]]：不要让模型直接调用工具，让模型**写代码来调用工具**。

```
直接工具调用:
  工具定义加载进上下文 → 模型选择工具 → 调用
  → 结果回传上下文 → 模型继续
  (每步都消耗上下文)

代码执行模式:
  模型写代码 → 代码在沙箱运行 → 按需发现/调用工具
  → 只把最终结果回传
  (工具发现、数据过滤、中间处理全在执行环境)
```

本质：**把工具使用从模型的内循环，挪到更高效的外部执行回路**[[agent/harness-engineering/sources/深度解析-Harness-Engineering|3]]。

### 6. 熵增抑制（Entropy Control）

全自动 Agent 代码库会不断复制既有模式——哪怕那些模式不均匀、次优甚至糟糕[[agent/harness-engineering/sources/深度解析-Harness-Engineering|3]]。

OpenAI 做法[[agent/harness-engineering/sources/openai-harness-engineering-zh|5]]：

- 最初：人每周花约 20% 时间清理「AI slop」
- 后来：系统化——Documentation consistency agents、Refactor agents、Architectural enforcement (CI)

设计原理：Harness 不只负责「让 Agent 跑起来」，还负责**持续抑制 Agent 放大的系统噪声**。这是它与「Agent 框架」的本质区别——框架关心启动和编排，harness 关心长期可治性[[agent/harness-engineering/sources/深度解析-Harness-Engineering|3]]。

---

## Harnessability（可 Harness 程度）

不是每个系统都同样容易被 harness[[agent/harness-engineering/sources/philschmid-agent-harness-2026|6]]。

**高 harnessability 系统：**
- 强类型
- 测试完备
- 边界清晰
- 文档版本化
- 运行时可观测

**低 harnessability 系统：**
- 知识散落在人脑、聊天工具、口耳相传
- 即使模型再强，也会先撞上「看不见 → 无法理解 → 无法治理」的墙

判断：在 Agent 时代，团队工程基础设施质量（CI 完善度、文档结构化程度、架构边界清晰度）不再只是「工程素养」问题——它直接决定了 Agent 能在你的系统上走多远[[agent/harness-engineering/sources/深度解析-Harness-Engineering|3]]。

---

## 从 Chatbot 到 AgentOS 的演化

```
Level 1: Chatbot (2022-2023)
  单次对话，无状态，人类完全在环
  工程抽象: Prompt Engineering
  代表: ChatGPT 早期
  天花板: 能说不能做

Level 2: AI Browser / Agent IDE (2024-2025)
  多步任务，工具调用，有限自主权
  工程抽象: Context Engineering + 轻量 Harness
  代表: Claude Code, Cursor, Manus
  天花板: 单 Agent 强但长任务不稳；多 Agent 协作缺乏标准

Level 3: AgentOS (2026- 萌芽)
  Always-on、多 Agent、跨工具、跨身份的长期执行体
  需要系统层解决:
    - Agent 生命周期管理
    - 上下文调度（内存管理的 Agent 版）
    - 多 Agent 隔离与协作（进程隔离 + IPC）
    - 治理与审计
```

**定位**：Harness 是 AgentOS 的**用户态层**[[agent/harness-engineering/sources/深度解析-Harness-Engineering|3]]。AgentOS 是内核——管调度、管隔离、管资源。Harness 是用户态的 shell 和 daemon——管任务分解、管状态续航、管验证反馈、管人机交接。

---

## 五个典型症状

如果观察到这些，说明你的「Agent 系统」还停在临时搭伙阶段[[agent/harness-engineering/sources/深度解析-Harness-Engineering|3]]：

| 症状 | 表现 |
|------|------|
| **框架丛林** | LangChain + CrewAI + AutoGen 拼凑，没有完整生命周期 |
| **Chatbot 皮 + Agent 芯** | 界面是 chatbot，缺乏真正的状态管理、任务分解、验证门 |
| **工具注册 ≠ 工具治理** | 连了 50 个工具，Agent 困惑、做冗余调用、走弯路 |
| **一次性规则** | 巨大的 AGENTS.md，当一切都重要时，什么都不重要 |
| **缺乏 on-the-loop 思维** | 不满意就手改产物，而不是改 harness 让系统下次自动更好 |

---

## 实践自检三问

1. **你的 Agent 有没有 durable state surfaces？** 冷启动后能否在 30 秒内续航？
2. **你的系统有没有 machine-readable acceptance criteria？** 「完成」的定义是 Agent 的自我感觉，还是外部结构化验证面？
3. **你的 repo、工具、日志、指标、策略，是否对 Agent legible and enforceable？** 还是只有人类能读懂？

如果这三件事都没有，做的还只是「会跑命令的聊天机器人」[[agent/harness-engineering/sources/深度解析-Harness-Engineering|3]]。

---

## 来源

- [[agent/harness-engineering/sources/深度解析-Harness-Engineering|深度解析（公众号）]]
- [[agent/harness-engineering/sources/anthropic-effective-harnesses-long-running-agents|Anthropic — Long-running]]
- [[agent/harness-engineering/sources/martin-fowler-harness-engineering|Martin Fowler]]
- [[agent/harness-engineering/sources/langchain-anatomy-of-an-agent-harness|LangChain — Anatomy]]
- [[agent/harness-engineering/sources/openai-harness-engineering-zh|OpenAI 中文]]
- [[agent/harness-engineering/sources/humanlayer-skill-issue-harness-engineering|HumanLayer]]
- [[agent/harness-engineering/sources/ignorance-emerging-harness-engineering|Ignorance.ai]]
- [[agent/harness-engineering/sources/mitchellh-ai-adoption-journey-step-5-harness|Mitchell Hashimoto]]
- [[agent/harness-engineering/sources/anthropic-building-c-compiler|Anthropic — C compiler]]
- [[agent/harness-engineering/sources/parallel-what-is-an-agent-harness|Parallel]]
- [[agent/harness-engineering/sources/philschmid-agent-harness-2026|Phil Schmid]]
