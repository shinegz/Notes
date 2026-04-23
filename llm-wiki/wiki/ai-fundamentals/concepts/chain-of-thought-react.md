---
title: "Chain-of-Thought & ReAct"
type: concept
tags: [chain-of-thought, react, reasoning, agent]
sources:
  - ai-fundamentals/sources/react-chain-of-thought
  - ai-fundamentals/sources/llm-powered-autonomous-agents
last_updated: 2026-04-23
---

# Chain-of-Thought & ReAct

**CoT = 让 LLM 显式写出推理步骤；ReAct = CoT + 行动，让 LLM 边思考边调用工具。**

## 一句话理解

不要直接问 LLM 答案——让它先"打草稿"列出推理过程（CoT），如果还需要查资料/算数据，就边想边做（ReAct）。

## Chain-of-Thought（CoT）

### 核心思想

[GPT-3](../sources/gpt3-language-models-few-shot.md) 的 few-shot prompting 证明，给模型几个示例就能引导它完成新任务。CoT 更进一步：**示例中不仅给答案，还给推理过程**。

### 标准 Prompt vs CoT Prompt

**标准**：
```
Q: 一个农场有 35 头牛，又买了 12 头，现在有多少头？
A: 47
```

**CoT**：
```
Q: 一个农场有 35 头牛，又买了 12 头，现在有多少头？
A: 农场原来有 35 头，买了 12 头，所以 35 + 12 = 47。答案是 47。
```

### 效果

- 在算术、常识推理、符号推理等任务上显著提升准确率
- 模型规模越大，CoT 效果越明显（小模型可能学不会）

## ReAct（Reasoning + Acting）

### 核心思想

[ReAct](../sources/react-chain-of-thought.md) 提出：将**推理痕迹（Thought）**和**任务行动（Action）**交织执行，形成一个循环。

### ReAct 循环

```
Thought（思考）→ Action（行动/工具调用）→ Observation（观察结果）→ Thought → ...
```

### 示例

```
Question: 2024 年诺贝尔文学奖得主是谁？

Thought 1: 我需要搜索 2024 年诺贝尔文学奖得主的信息。
Action 1: search("2024 Nobel Prize in Literature winner")
Observation 1: 韩江（Han Kang）获得 2024 年诺贝尔文学奖。

Thought 2: 我已经找到了答案。
Action 2: finish("韩江")
```

### ReAct 的优势

[ReAct](../sources/react-chain-of-thought.md) 实验证明：
- 优于单独的 CoT（只推理不行动）
- 优于单独的 Action（只行动不推理）
- 推理痕迹提高了可解释性和可信度

## CoT → ReAct → Agent

| 层级 | 能力 | 典型应用 |
|------|------|----------|
| **CoT** | 显式推理步骤 | 数学题、逻辑推理题 |
| **ReAct** | 推理 + 工具调用 | 需要查资料/算数的问答 |
| **Agent** | 多步规划 + 记忆 + 多工具 | 复杂任务自动化 |

## 来源

- [ReAct](../sources/react-chain-of-thought.md) — 推理与行动协同框架原始论文
- [LLM Powered Autonomous Agents](../sources/llm-powered-autonomous-agents.md) — CoT 变体综述（CoT-SC, ToT, Reflexion 等）
