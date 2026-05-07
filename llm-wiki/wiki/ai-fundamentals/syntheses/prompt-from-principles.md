---
title: "从大模型原理出发谈 Prompt"
type: synthesis
tags: [prompt-engineering, llm-principles, autoregressive, attention, icl, alignment, context-window]
sources:
  - ai-fundamentals/sources/openai-prompt-engineering
  - ai-fundamentals/sources/openai-prompt-guidance
  - ai-fundamentals/sources/anthropic-context-engineering
  - ai-fundamentals/sources/prompt-engineering-frameworks-parloa
  - ai-fundamentals/sources/prompt-engineering-2025-aakashg
  - ai-fundamentals/sources/lost-in-the-middle
  - ai-fundamentals/sources/icl-bayesian-inference
  - ai-fundamentals/sources/longllmlingua
  - ai-fundamentals/sources/rlhf-sycophancy
  - ai-fundamentals/sources/context-dilution
  - ai-fundamentals/sources/prompt-from-first-principles-dev
last_updated: 2026-05-07
---

# 从大模型原理出发谈 Prompt

**写 Prompt 是在操作条件概率分布。理解 LLM 的五条底层原理（自回归预测、注意力机制、In-Context Learning、对齐训练、Context Window），就能推导出所有 Prompt 技巧为什么有效，不必死记硬背。**

## 原理 → 技巧 映射总览

| 底层原理 | 核心机制 | 推导出的 Prompt 技巧 |
|----------|----------|---------------------|
| 自回归预测 | p(next_token \| context)，每次只生成一个 token | 定意图收窄分布；CoT 把大跳步拆成小跳步；任务拆解缩小输出空间 |
| 注意力机制 | n² 对 token 关系，位置偏差，注意力零和 | 结构化分组（CO-STAR）；分隔符造语义边界；重要信息放开头/结尾；压缩去噪 |
| In-Context Learning | 从示例中推断隐含概念，条件化输出分布 | Few-shot 示例偏移分布；示例 > 描述；典型示例优于边界案例 |
| 对齐训练 | RLHF 塑造"指令服从"行为，同时引入谄媚倾向 | 正面引导 > 负面禁止；说"要做什么"；明确角色锚定行为 |
| Context Window | 注意力稀释，context rot，有效上下文远小于声称 | 先爬质量山丘再压缩；精简 token 拿更高注意力份额；子 Agent 隔离上下文 |

---

## 一、自回归预测：Prompt 是对概率分布的操作

LLM 做的事：给定已有 token 序列，预测下一个 token 的概率分布 p(next_token | context)。

> 完整的运行原理见 [[ai-fundamentals/syntheses/token-lifecycle|一个 Token 的一生]]

### 定意图 = 压缩输出分布的熵

模糊的 context 产生平坦的分布，模型在多种合理的续写方向上概率分散，输出随机。精确的 context 收窄分布，概率质量集中在期望输出上。

```
❌ 模糊 Prompt："帮我处理一下这些数据"
   → 分布平坦：排序？过滤？分析？可视化？每个方向概率相近

✅ 精确 Prompt："从以下用户评价中提取痛点，按 severity（low/medium/high）和 category 分类"
   → 分布集中：提取 + 分类两个方向概率压倒性高
```

**推导**：Prompt 的首要任务是把输出分布从平坦压到尖锐。一句话说不清的任务，分布压不尖，必须拆解。

### CoT = 把概率大跳步拆成小跳步

自回归预测每次只生成一个 token。要求模型直接从问题跳到答案，是一个概率跨度极大的跳步，中间缺少条件化上下文，每步出错概率叠加。

CoT 让模型的每步输出都成为下一步的额外条件，逐步收窄分布：

```
直接回答：问题 → 答案     （一次跳步，概率跨度大）
CoT：     问题 → 步骤1 → 步骤2 → 答案  （三次小跳，每次概率跨度小）
```

**推导**：任何需要多步推理的任务，不给中间步骤就等于要求模型一次跨越巨大的概率距离。CoT 的实质是给模型铺设条件化上下文的阶梯。

### 任务拆解 = 缩小每个子任务的输出空间

与 CoT 同理，但在任务级别操作。一个复杂任务的输出空间巨大（比如"写一份数据分析报告"），但拆成"提取指标 → 计算趋势 → 生成摘要"后，每个子任务的输出空间小得多，条件概率更容易命中。

**关键阈值**：一步到位的 Prompt 超过 500 字还说不清要求，就该拆解。

---

## 二、注意力机制：Token 之间的关系决定输出质量

注意力机制计算上下文中所有 token 对之间的权重：Attention(Q, K, V) = softmax(QK^T / √d_k) × V。三个关键属性决定了 Prompt 应该怎么组织。

> 注意力机制的完整解释见 [[ai-fundamentals/concepts/attention-mechanism|Attention Mechanism]]

### 位置偏差：U 形注意力曲线

Stanford/Meta 的 [[ai-fundamentals/sources/lost-in-the-middle|Lost in the Middle]] 实验发现：LLM 对开头和结尾的 token 分配更高的注意力权重，中间位置的 token 注意力显著衰减。性能下降幅度可达 20+ 个百分点，GPT-3.5-Turbo 在信息位于中间时，准确率甚至低于无上下文的闭卷基线。

后续研究（Found in the Middle, ACL 2024）确认了根因：LLM 存在内在的 U 形注意力偏差，与语义相关性无关。

**推导**：
- 重要指令放开头——获得最高注意力权重
- 关键数据放结尾——同样获得高注意力
- 避免把关键信息埋在长文中间

### 注意力零和：多一个 token 就少一份注意力

Softmax 归一化迫使注意力权重总和为 1。加入更多 token，每个 token 平均获得的注意力份额下降，这是 [[ai-fundamentals/concepts/context-engineering|context rot]] 的来源。

MIT/Meta 的 [[ai-fundamentals/sources/context-dilution|Attention Sinks 研究（ICLR 2024）]] 发现：初始 token 接收了不成比例的高注意力分数，即使语义上不重要。Softmax 必须把注意力"倾倒"到某处，开头 token 成为默认接收者。

**推导**：
- 删掉低信噪比的 token——每个剩余 token 获得更高注意力份额，输出质量反而提升
- LLMLingua 实证：压缩到 20x，推理损失仅 1.5 个百分点，加速 1.7-5.7x
- 先爬质量山丘再压缩——不知道哪些是信号就无法正确压缩

### 结构化 + 分隔符 = 造语义边界

没有分隔符，指令 token 和数据 token 的注意力权重互相渗透（cross-contamination），模型可能把数据当指令执行，或把指令当数据处理。

CO-STAR 框架的价值在于它把同一语义维度的 token 聚集在一起（Context 块、Objective 块、Response 块），让模型更容易识别"这些 token 在说同一件事"，减少跨维度注意力噪声。

`---` 或 `"""` 分隔符在注意力矩阵中制造语义边界，相当于说"这条线两侧的 token 属于不同的语义空间"。

---

## 三、In-Context Learning：示例是一种隐含推理

### ICL 的理论解释

[[ai-fundamentals/sources/icl-bayesian-inference|Xie et al. (ICLR 2022)]] 证明：In-Context Learning 是隐含的贝叶斯推断，模型从 Prompt 示例中推断隐含的概念/模式，然后基于该概念条件化输出分布。示例不是"教模型新知识"，而是让模型推断"你想要哪种模式"。

### Few-shot = 条件化输出分布

不加示例时，模型只依赖预训练学到的分布，分布可能很宽，因为训练数据中同一个问题有多种回答模式。加入示例后，模型在推理时条件化于示例中的模式，无需修改权重即可偏移输出分布。

**推导**：
- 示例 > 描述：一个具体的 JSON 示例让模型直接条件化于该模式，比"输出 JSON 格式"这种抽象描述收窄分布更有效
- 典型示例优于边界案例：Anthropic 建议精选 canonical examples——少量多样化，不堆边界案例。边界案例让模型条件化于异常模式，反而扩大分布

### 示例顺序敏感

ICL 对示例顺序敏感（Order Matters, arXiv 2024），不同顺序导致模型推断出不同的隐含概念。实践中，把最典型、最符合目标模式的示例放在开头和结尾（呼应 U 形注意力曲线）。

---

## 四、对齐训练：RLHF 塑造了"指令服从"行为

### 从预训练到对齐

预训练模型只学会了"续写"，给它问题，它可能续写另一个问题。SFT（监督微调）教它"看到问题就该回答"，RLHF 进一步教它"回答应该有帮助、无害、诚实"。

> 对齐的完整解释见 [[ai-fundamentals/concepts/alignment|Alignment]]

### 谄媚倾向与正面引导

RLHF 有副作用：模型被训练为迎合用户偏好，产生谄媚行为（sycophancy）。当 Prompt 中包含暗示性信息时，模型倾向顺着暗示走，而非独立判断。

**推导**：
- 正面引导 > 负面禁止："Refer user to help article" 优于 "DO NOT ASK for more details"。负面禁止让模型需要先条件化于禁止行为再否定它，增加了分布中的噪声
- 说"要做什么"而非"不要做什么"——模型对正面指令的条件化更直接
- 明确角色锚定行为："你是 SaaS 产品经理" 让模型条件化于"专业、结构化"的行为模式，而非通用聊天模式

---

## 五、Context Window：注意力预算是有限资源

### 有效上下文远小于声称上下文

| 模型 | 声称上下文 | 有效上下文 | 4K→128K 退化 |
|------|-----------|-----------|-------------|
| GPT-4 | 128K | 64K | -15.4 pts |
| Yi-34B | 200K | 32K | -16.0 pts |
| Mistral 7B | 32K | 16K | -79.8 pts |

来源：[[ai-fundamentals/sources/context-dilution|RULER benchmark（NVIDIA, 2024）]]、[[ai-fundamentals/sources/longllmlingua|LongLLMLingua]]

> Context Window 的完整解释见 [[ai-fundamentals/concepts/context-window|Context Window]]

### 上下文长度本身就会降低性能

2025 年的研究发现（[[ai-fundamentals/sources/context-dilution|Context Length Alone Hurts LLM Performance]]）：即使 100% 完美检索到相关信息，性能仍随上下文长度增长退化 13.9%-85%。退化在把无关 token 替换为空白后仍然存在，说明长度本身就是负担，与内容质量无关。

### 压缩与编排策略

| 策略 | 机制 | 适用场景 |
|------|------|----------|
| Prompt 压缩 | 移除低信息量 token，提高剩余 token 的注意力份额 | 长上下文 RAG |
| Compaction | 压缩历史上下文继续 | 需要大量来回交互 |
| Structured Note-taking | 持久化笔记到上下文外 | 迭代开发，有里程碑 |
| Sub-agent | 子 Agent 隔离上下文后只返回摘要 | 复杂研究，并行探索 |

**推导**：上下文是零和博弈，每个 token 都在争夺注意力份额。写得越多，每个 token 被看到的概率越低。Prompt 优化的方向是"写得精"而非"写得全"，每个 token 都有存在的理由。

---

## 边界说明

1. **原理不等于全部**：理解原理能解释技巧为什么有效，但不能替代实验，同一原理在不同模型上的表现可能不同（如 Claude 倾向保守回避，GPT 倾向幻觉）
2. **技巧有交互效应**：压缩和 CoT 可能矛盾（压缩移除中间推理 token），需要权衡
3. **模型在进化**：更大的上下文窗口和更好的训练可能削弱某些问题的严重程度，但自回归预测和注意力零和是架构层面的约束，不会消失

## 关联概念

- [[ai-fundamentals/concepts/prompt-engineering|Prompt Engineering]] — 核心策略与原则
- [[ai-fundamentals/concepts/context-engineering|Context Engineering]] — 从单次 Prompt 到系统级上下文编排
- [[ai-fundamentals/concepts/attention-mechanism|Attention Mechanism]] — 注意力权重分布是本文技巧的底层原理
- [[ai-fundamentals/concepts/context-window|Context Window]] — token 数量限制驱动压缩和 Context Engineering
- [[ai-fundamentals/concepts/alignment|Alignment]] — RLHF 塑造的指令服从行为

## 来源

- [[ai-fundamentals/sources/lost-in-the-middle|Lost in the Middle]] — U 形位置偏差
- [[ai-fundamentals/sources/icl-bayesian-inference|ICL as Bayesian Inference]] — Few-shot 的理论解释
- [[ai-fundamentals/sources/longllmlingua|LongLLMLingua]] — 问题感知 Prompt 压缩
- [[ai-fundamentals/sources/rlhf-sycophancy|RLHF Sycophancy]] — RLHF 放大谄媚行为
- [[ai-fundamentals/sources/context-dilution|Context Dilution]] — 注意力零和与上下文稀释
- [[ai-fundamentals/sources/prompt-from-first-principles-dev|Prompt From First Principles]] — 从 LLM 机制推导 Prompt 技巧
- [[ai-fundamentals/sources/prompt-engineering-survey|Prompt Engineering Survey]] — 41 种 Prompt 技术综述
- [[ai-fundamentals/sources/openai-prompt-engineering|OpenAI Prompt Engineering Guide]] — 官方核心策略
- [[ai-fundamentals/sources/openai-prompt-guidance|OpenAI Help Center Best Practices]] — 实操策略与参数调优
- [[ai-fundamentals/sources/anthropic-context-engineering|Anthropic Context Engineering]] — 最小高信噪比原则
- [[ai-fundamentals/sources/prompt-engineering-frameworks-parloa|Prompt Engineering Frameworks]] — CO-STAR 等结构化框架
- [[ai-fundamentals/sources/prompt-engineering-2025-aakashg|Prompt Engineering in 2025]] — 先爬质量山丘再降成本
