---
title: "Function Calling"
type: concept
tags: [function-calling, tool, api, agent]
sources:
  - ai-fundamentals/sources/toolformer
  - ai-fundamentals/sources/llm-powered-autonomous-agents
last_updated: 2026-04-23
---

# Function Calling

**Function Calling = LLM 根据用户意图，自动生成调用外部函数的参数化请求。**

## 一句话理解

你问"北京今天天气怎么样"，LLM 不会直接回答——它会输出一个结构化请求：`{"function": "get_weather", "arguments": {"city": "北京"}}`，然后由外部程序执行函数并把结果返回给它。

## 核心机制

### 1. 函数定义注册

预先向 LLM 注册可用的函数及其参数 schema：

```json
{
  "name": "get_weather",
  "description": "获取指定城市的天气",
  "parameters": {
    "type": "object",
    "properties": {
      "city": {"type": "string", "description": "城市名称"}
    },
    "required": ["city"]
  }
}
```

### 2. LLM 决策

[Toolformer](../sources/toolformer.md) 的核心发现：模型可以自动判断：
- **是否**需要调用工具
- **调用哪个**工具
- **传递什么**参数

### 3. 外部执行

LLM 输出函数调用请求 → 外部程序解析并执行 → 结果返回 LLM → LLM 生成最终回答

## 与 Tool Use 的关系

| | Function Calling | Tool Use |
|--|-----------------|----------|
| **粒度** | 单次函数调用 | 泛指所有外部能力（搜索、代码执行、API 等）|
| **形式** | 结构化 JSON | 可以是 JSON、SQL、代码等任意形式 |
| **关系** | Function Calling 是 Tool Use 的一种标准化实现 | 更广泛的范畴 |

## 能力层级

[LLM Powered Autonomous Agents](../sources/llm-powered-autonomous-agents.md) 引用 API-Bank 的研究，将 function calling 能力分为三级：

1. **调用 API**：知道什么时候用哪个 API
2. **检索 API**：从大量 API 中找到合适的
3. **规划多步 API 调用**：分解任务，按顺序调用多个 API

## Function Calling → Agent

Function Calling 是 Agent 的**行动层**基础：
- Agent 的 Planning 决定"要做什么"
- Function Calling 决定"调用什么工具、传什么参数"
- 外部程序执行后返回 Observation
- Agent 进入下一轮 ReAct 循环

## 来源

- [Toolformer](../sources/toolformer.md) — 语言模型自学使用工具的原始论文
- [LLM Powered Autonomous Agents](../sources/llm-powered-autonomous-agents.md) — Tool Use 能力分级与框架综述
