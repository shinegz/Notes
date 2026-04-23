---
title: "AI核心概念体系"
type: synthesis
tags: [ai-fundamentals, llm, token, context, prompt, tool, agent, mcp, skill]
sources:
  - ai-fundamentals/sources/attention-is-all-you-need
  - ai-fundamentals/sources/the-illustrated-transformer
  - ai-fundamentals/sources/gpt3-language-models-few-shot
  - ai-fundamentals/sources/instructgpt
  - ai-fundamentals/sources/scaling-laws-kaplan
  - ai-fundamentals/sources/chinchilla
  - ai-fundamentals/sources/llm-powered-autonomous-agents
  - ai-fundamentals/sources/react-chain-of-thought
  - ai-fundamentals/sources/toolformer
  - ai-fundamentals/sources/dpo
  - ai-fundamentals/sources/rlhf-from-feedback
last_updated: 2026-04-23
---

# AI核心概念体系

> 本文是 llm-wiki ai-fundamentals 门类的综合文。所有概念定义和关系陈述均基于已 ingest 的 source 资料，非主观构建。见文末 [Source 索引](#source-索引)。

AI 不是单一技术，而是一组相互关联的概念和系统。理解它们各自来自哪些 source、如何被定义、相互之间存在怎样的引用关系，是建立可靠认知的基础。

---

## 30秒心智模型

下图展示了 19 个 AI 核心概念及其关系网络。节点散布在 2D 平面，连线标注关系类型——**这不是层级架构图**，而是基于 source 资料中概念出现方式和引用关系绘制的关联地图。

![AI核心概念关系网络图](./ai-core-concepts/concept-network.svg)

**读图方法**：
- **LLM** 和 **Agent** 是两个核心枢纽（尺寸较大）
- **左侧集群**：Token → Embedding → Transformer → LLM（输入与架构流）
- **下方集群**：Scaling Laws → Fine-tuning → Alignment（训练与对齐流）
- **右侧集群**：Tool → MCP / Agent / Skill（工具与系统流）
- **右下集群**：Vector DB → Memory → RAG（记忆与检索流）
- 连线标签说明概念之间的关系类型（如"架构基础"、"Function Calling"、"ReAct 循环"等）
- 所有 18 个概念均有独立概念页，点击速查表中的链接可深入了解

---

## 核心概念逐个解析

### 1. Token —— 来自 Transformer 的输入原子

**Source**: [The Illustrated Transformer](../sources/the-illustrated-transformer.md) 将 Token 描述为"每个词被嵌入成 512 维的向量"，是 Transformer 编码器的最底层输入。[GPT-3](../sources/gpt3-language-models-few-shot.md) 使用 BPE tokenizer，vocab size 50k。

**关键认知**（source-grounded）：
- Token 是模型处理文本的最小单位，由 tokenizer 将原始文本切分而成
- 英文中 1 token ≈ 0.75 个单词；中文更复杂，一个汉字可能对应 1-2 tokens
- Token 经过 Embedding 层转化为向量后，才进入 Transformer 的 Self-Attention 计算
- 计费单位：模型按输入+输出的 token 数收费

> 注意：Token 不是 LLM "理解"语言的单位——LLM 只是通过预测下一个 token 的分布来生成文本，这一点在 GPT-3 和 [Scaling Laws](../sources/scaling-laws-kaplan.md) 中被反复强调。
>
> 详细机制见概念页 [Tokenization](../concepts/tokenization.md)。

---

### 2. Embedding —— 从符号到向量的桥梁

**Source**: [word2vec](../sources/word2vec.md) 提出了将词映射为连续向量的方法，使得语义相近的词在向量空间中距离相近。[Attention Is All You Need](../sources/attention-is-all-you-need.md) 将 Embedding 作为 Transformer 编码器的输入层（512 维）。

**关键认知**（source-grounded）：
- Embedding 解决了 one-hot 的维度灾难和无语义关系问题
- [word2vec](../sources/word2vec.md) 的经典发现：king - man + woman ≈ queen，证明向量编码了语义关系
- 从 Word Embedding（word2vec, GloVe）到 Contextual Embedding（ELMo）再到 Transformer Embedding（BERT, GPT）
- 所有现代 LLM 的第一层都是 Embedding 层——Token 必须先变成向量才能进入 Self-Attention

> 详细机制见概念页 [Embedding](../concepts/embedding.md)。

---

### 3. Context / Context Window —— LLM 的工作记忆上限

**Source**: [The Illustrated Transformer](../sources/the-illustrated-transformer.md) 指出"嵌入只发生在最底层的编码器"，所有上层编码器接收的都是相同维度的向量列表——这个列表的长度就是 context window 的长度。[GPT-3](../sources/gpt3-language-models-few-shot.md) 的 context length 为 2048 tokens。

**关键认知**（source-grounded）：
- Context Window 是模型一次能处理的 token 数量上限
- LLM 是**无状态**的——每次请求都靠 Context 传递历史（见 [LLM Agents](../concepts/llm-agents.md) 对短期记忆的讨论）
- 超出窗口的内容会被截断
- 当前趋势：窗口越来越大（从 GPT-3 的 2K 到 Gemini 的 1M+），但注意力分散问题（"Lost in the Middle"）依然存在

> 详细机制见概念页 [Tokenization](../concepts/tokenization.md)（关于 token 切分）和 [Vector Database](../concepts/vector-database.md)（关于长期记忆扩展）。

---

### 4. Transformer & Attention —— LLM 的架构基石

**Source**: [Attention Is All You Need](../sources/attention-is-all-you-need.md) 提出了 Transformer 架构，用 Self-Attention 取代了 RNN，实现了序列的完全并行处理。

**关键认知**（source-grounded）：
- **Self-Attention**: 计算序列中每个位置与其他所有位置的相关性（Query × Key^T × Value），让模型捕捉任意距离的依赖关系
- **Multi-Head Attention**: 多个 Attention 头并行计算，捕获不同子空间的语义关系
- **并行化**: RNN 必须逐字处理，Transformer 可以一次性处理整个序列
- 所有上层 Encoder 接收的都是相同维度的向量列表——Embedding + Positional Encoding 后进入 Self-Attention

> 详细机制见概念页 [Transformer](../concepts/transformer.md) 和 [Attention Mechanism](../concepts/attention-mechanism.md)。

---

### 5. LLM —— 基于 Transformer 的 Next-Token Predictor

**Source**: [Attention Is All You Need](../sources/attention-is-all-you-need.md) 提出了 Transformer 架构，成为几乎所有现代 LLM 的基石。[GPT-3](../sources/gpt3-language-models-few-shot.md) 展示了基于 Transformer decoder 的规模化训练，核心能力是"预测下一个 token"。[Scaling Laws](../sources/scaling-laws-kaplan.md) 证明模型能力随参数和数据量可预测地提升。

**关键认知**（source-grounded）：
- LLM 的核心能力只有一件：给定前 N 个 token，预测第 N+1 个 token 的概率分布
- 不是搜索引擎、不是计算器、不是知识库——[LLM Powered Autonomous Agents](../sources/llm-powered-autonomous-agents.md) 明确指出 LLM 的"幻觉"问题是其固有特性
- 能力随规模增长：Kaplan (2020) 的 scaling laws 和 [Chinchilla](../sources/chinchilla.md) 的 compute-optimal scaling 都量化了这种关系
- [InstructGPT](../sources/instructgpt.md) 和 [RLHF from Human Feedback](../sources/rlhf-from-feedback.md) 证明：通过 RLHF 可以对齐 LLM 行为，但基础能力仍来自预训练

> 架构详情见概念页 [Transformer](../concepts/transformer.md)，规模化规律见 [Scaling Laws](../concepts/scaling-laws.md)，词嵌入见 [Embedding](../concepts/embedding.md)。

---

### 6. Scaling Laws —— 性能随规模可预测增长

**Source**: [Scaling Laws](../sources/scaling-laws-kaplan.md) 证明模型性能随算力、参数量、数据量可预测增长。[Chinchilla](../sources/chinchilla.md) 修正了最优 scaling 比例（~20 tokens per parameter）。

**关键认知**（source-grounded）：
- **Kaplan (2020)**: Loss ∝ C^(-α)，算力翻倍带来可预测的性能提升
- **Chinchilla 修正**: 70B 参数 + 1.5T tokens 的 Chinchilla 优于 280B 参数 + 300B tokens 的 Gopher，证明"小模型+大数据"更优
- Scaling Laws 是预训练的**指南针**——告诉研究者给定预算下最优的模型大小和数据量
- 能力涌现（emergent abilities）可能部分来自 metric 选择（见 source 中的讨论），但 scaling 本身是不可否认的趋势

> 详细机制见概念页 [Scaling Laws](../concepts/scaling-laws.md)。

---

### 7. Fine-tuning —— 预训练后的任务适配

**Source**: [InstructGPT](../sources/instructgpt.md) 通过 SFT + RLHF 让 GPT-3 学会遵循指令。[RLHF from Human Feedback](../sources/rlhf-from-feedback.md) 提供了 RLHF 的 early 实证。[DPO](../sources/dpo.md) 提出了不依赖强化学习的直接偏好优化方法。

**关键认知**（source-grounded）：
- **SFT**（Supervised Fine-Tuning）：用人工标注的 (prompt, response) 对继续训练，让模型学会指令格式
- **RLHF**: 训练 Reward Model 预测人类偏好，再用 PPO 优化策略——ChatGPT 的核心技术
- **DPO**: 直接用偏好数据优化，省去 Reward Model 和 PPO，更简单高效
- Fine-tuning 的边界：不能教给模型预训练中没有的新知识，实时信息需要 [RAG](../concepts/rag.md)

> 详细机制见概念页 [Fine-tuning](../concepts/fine-tuning.md)。

---

### 8. Alignment —— 让 LLM 行为符合人类意图

**Source**: [InstructGPT](../sources/instructgpt.md) 展示了如何通过 RLHF 让模型输出"有用、无害、诚实"。[RLHF from Human Feedback](../sources/rlhf-from-feedback.md) 在 summarization 任务上验证了 RLHF 的有效性。[DPO](../sources/dpo.md) 提供了更简单的对齐替代方案。

**关键认知**（source-grounded）：
- **对齐问题**: 预训练模型只学会"预测下一个 token"，不会自动遵循人类意图或价值观
- **RLHF 三步法**: SFT → 训练 Reward Model（人类偏好）→ PPO 优化
- **DPO 替代**: 跳过 Reward Model，直接用偏好数据优化策略，效果相当但更简单
- 对齐的代价：过度对齐可能导致模型变得过于谨慎，拒绝合理请求（"对齐税"）

> 详细机制见概念页 [Alignment](../concepts/alignment.md)。

---

### 9. Prompt —— 与 LLM 交互的输入接口

**Source**: [GPT-3](../sources/gpt3-language-models-few-shot.md) 将 few-shot prompting 作为主要交互范式，证明通过少量示例即可引导模型完成新任务。[InstructGPT](../sources/instructgpt.md) 进一步通过指令微调让模型遵循人类意图。Lilian Weng 的 [LLM Powered Autonomous Agents](../sources/llm-powered-autonomous-agents.md) 将 in-context learning 视为模型的"短期记忆"。

**关键认知**（source-grounded）：
- Prompt 是控制 LLM 的最便宜手段——不需要改模型，只需要改输入
- Few-shot prompting 的有效性来自 GPT-3 论文的实验验证
- Chain-of-Thought prompting（见 [ReAct](../sources/react-chain-of-thought.md)）是 Prompt 的高级形式，通过显式推理步骤提升复杂任务表现
- Prompt 有天花板：复杂任务需要 Tool 和 Agent（[LLM Powered Autonomous Agents](../sources/llm-powered-autonomous-agents.md) 明确论述）

> 详细机制见概念页 [Alignment](../concepts/alignment.md)（关于指令微调与对齐）。

---

### 10. CoT / ReAct —— 让 LLM 边推理边行动

**Source**: [ReAct](../sources/react-chain-of-thought.md) 提出将推理（Thought）和行动（Action）交织执行的循环框架。[GPT-3](../sources/gpt3-language-models-few-shot.md) 的 few-shot prompting 证明示例可以引导模型行为，CoT 在此基础上让示例包含推理过程。

**关键认知**（source-grounded）：
- **CoT**（Chain-of-Thought）：在 Prompt 示例中不仅给答案，还给推理步骤——"农场有 35 头牛，买了 12 头，所以 35+12=47"
- **ReAct**: Thought → Action → Observation → Thought → ... 的循环，模型边思考边调用工具
- ReAct 优于单独的 CoT（只推理不行动）和单独的行动（只行动不推理）
- 从 CoT → ReAct → Agent 是能力递增的层级：纯推理 → 推理+工具 → 多步规划+记忆+多工具

> 详细机制见概念页 [Chain-of-Thought & ReAct](../concepts/chain-of-thought-react.md)。

---

### 11. Tool —— LLM 的外部能力扩展

**Source**: [Toolformer](../sources/toolformer.md) 证明语言模型可以自学使用外部工具（计算器、QA 系统、搜索引擎等），无需人工标注。[LLM Powered Autonomous Agents](../sources/llm-powered-autonomous-agents.md) 系统综述了 Tool Use 作为 Agent 三大组件之一，并介绍了 MRKL、TALM、HuggingGPT 等框架。

**关键认知**（source-grounded）：
- Tool 弥补 LLM 的固有缺陷：知识时效性、算术能力、专有数据访问
- [Toolformer](../sources/toolformer.md) 的核心发现：模型可以自动判断何时调用工具、传递什么参数、如何整合结果
- API-Bank（见 [LLM Powered Autonomous Agents](../sources/llm-powered-autonomous-agents.md)）将 tool use 能力分为三个层级：调用 API、检索 API、规划多步 API 调用
- LLM 负责"决定做什么"，Tool 负责"实际执行"

> 详细机制见概念页 [Vector Database](../concepts/vector-database.md)（关于 Tool 使用中的数据检索）。

---

### 12. Function Calling —— Tool 使用的标准化接口

**Source**: [Toolformer](../sources/toolformer.md) 证明模型可以自学判断何时调用工具、传递什么参数。[LLM Powered Autonomous Agents](../sources/llm-powered-autonomous-agents.md) 将 function calling 能力分为三级：调用 API、检索 API、规划多步调用。

**关键认知**（source-grounded）：
- Function Calling 是 Tool Use 的一种标准化实现：LLM 输出结构化 JSON 请求，外部程序执行后返回结果
- 模型需要预先注册可用函数的定义（名称、描述、参数 schema）
- 从单次调用到多步规划：复杂任务需要 Agent 分解为多个 function call 并按序执行
- Function Calling 是 Agent **行动层**的基础——Planning 决定"做什么"，Function Calling 决定"怎么做"

> 详细机制见概念页 [Function Calling](../concepts/function-calling.md)。

---

### 13. Memory —— Agent 的信息存储与检索

**Source**: [LLM Powered Autonomous Agents](../sources/llm-powered-autonomous-agents.md) 提出 Agent 的三组件框架，其中 Memory 分为短期记忆（in-context learning）和长期记忆（外部 Vector DB）。

**关键认知**（source-grounded）：
- **短期记忆** = Context Window：当前对话的历史，受限于模型 context length，超出即丢失
- **长期记忆** = Vector DB + ANN 检索：通过 Embedding 将历史信息向量化存储，需要时相似度召回
- **写入**：将经验、知识、对话历史通过 Embedding 存入外部数据库
- **检索**：MIPS（Maximum Inner Product Search）通过 ANN 算法（HNSW, IVF）快速找到最相关片段
- 长期记忆解决了 LLM 的两大限制：知识时效性和上下文长度限制

> 详细机制见概念页 [Memory](../concepts/memory.md)。

---

### 14. Vector DB —— 长期记忆的存储与检索基础设施

**Source**: [LLM Powered Autonomous Agents](../sources/llm-powered-autonomous-agents.md) 将 Vector DB 作为 Agent 长期记忆的实现载体。[word2vec](../sources/word2vec.md) 提供了 Embedding 向量化的基础。

**关键认知**（source-grounded）：
- Vector DB 存储的是**高维向量**（如 768 维或 1536 维），不是原始文本
- **相似度检索**：通过计算查询向量与文档向量的余弦相似度或内积，找到语义最相近的内容
- **ANN 算法**：HNSW、IVF 等近似最近邻算法让亿级向量的检索在毫秒级完成
- 在 RAG 和 Agent 记忆中的应用：将文档/历史向量化 → 存入 Vector DB → 查询时相似度召回 → 注入 Prompt

> 详细机制见概念页 [Vector Database](../concepts/vector-database.md)。

---

### 15. Agent —— 自主决策的循环系统

**Source**: [LLM Powered Autonomous Agents](../sources/llm-powered-autonomous-agents.md) 提出 Agent 的三组件框架：Planning + Memory + Tool Use。[ReAct](../sources/react-chain-of-thought.md) 证明了将 Reasoning（Thought）和 Acting（Action）交织循环的有效性。

**关键认知**（source-grounded）：
- Agent 不是"更聪明的 LLM"，而是 **LLM + 工程化包装** 的系统
- **Planning**: CoT、ToT、LLM+P（外部经典规划器）等多种任务分解技术（[LLM Powered Autonomous Agents](../sources/llm-powered-autonomous-agents.md) 详述）
- **Memory**: 短期记忆 = in-context learning（受限于 context window）；长期记忆 = 外部 vector store + 快速检索（MIPS/ANN 算法）
- **Tool Use**: 调用外部 API 获取 LLM 权重中没有的信息
- **ReAct 循环**: Thought → Action → Observation → ...（[ReAct](../sources/react-chain-of-thought.md) 证明优于单独的 reasoning 或 acting）
- 可靠性挑战：有限 context、长程规划困难、自然语言接口的不可靠性（[LLM Powered Autonomous Agents](../sources/llm-powered-autonomous-agents.md) 末尾详述）

> 详细架构见概念页 [LLM Agents](../concepts/llm-agents.md)，记忆机制见 [Vector Database](../concepts/vector-database.md)，注意力机制见 [Attention Mechanism](../concepts/attention-mechanism.md)。

---

### 16. RAG —— 检索增强生成

**Source**: [LLM Powered Autonomous Agents](../sources/llm-powered-autonomous-agents.md) 描述了将外部检索与 LLM 生成结合的方法。RAG 通过引入检索步骤解决 LLM 的知识截止和幻觉问题。

**关键认知**（source-grounded）：
- **核心流程**：用户问题 → Embedding → Vector DB 检索 → Top-K 文档注入 Prompt → LLM 基于检索结果生成
- **为什么不用 Fine-tuning**：RAG 实时更新（改文档即可），Fine-tuning 需要重新训练；RAG 更适合动态知识
- **关键组件**：Embedding 模型（向量化）、Vector DB（存储与检索）、LLM（生成）、Rerank（精排）
- RAG 是 LLM + Vector DB 的实用组合，是当前企业知识库问答的主流架构

> 详细机制见概念页 [RAG](../concepts/rag.md)。

---

### 17. MCP —— 工具标准化的工程协议

**Source 状态**: MCP（Model Context Protocol）目前**未出现在任何已 ingest 的学术论文 source 中**。它是 Anthropic 提出的工程实践协议，用于标准化 Agent 与 Tool 之间的通信。

**工程定位**:
- MCP 是**协议**（protocol），不是工具本身
- 类比 USB-C：统一接口标准，让任何 MCP Server（工具提供方）可以被任何 MCP Client（Agent）调用
- 核心价值：标准化工具发现、调用、认证机制；互操作性；动态发现

> 由于 MCP 目前缺乏学术论文 source，其定义和边界主要来自工程文档和行业实践，而非经过同行评审的研究。

---

### 18. Skill —— 可复用能力模块的工程封装

**Source 状态**: Skill 目前**未出现在任何已 ingest 的学术论文 source 中**。它是 Agent 工程生态中的概念，指模块化、可复用的能力单元。

**工程定位**:
- Skill 粒度介于 Tool（原子能力）和 Agent（完整系统）之间
- 典型形态：预优化的 Prompt 模板、预配置的 Tool 组合、完整的多步骤工作流
- 类比 App Store：开发者封装能力，用户按需加载

> 与 MCP 类似，Skill 的定义来自工程实践，尚未有学术论文对其进行系统定义。

---

## 不是什么 vs 是什么

| 误区 | 事实（source-grounded） |
|------|------------------------|
| LLM "理解"语言 | LLM 只做一件事：预测下一个 token 的分布（[GPT-3](../sources/gpt3-language-models-few-shot.md)） |
| Agent 是更聪明的 LLM | Agent 是 LLM + 外部工具 + 循环执行 + 状态管理的**系统**（[LLM Powered Autonomous Agents](../sources/llm-powered-autonomous-agents.md)） |
| MCP 是一种工具 | MCP 是**协议**——标准化接口（工程实践，无学术论文 source） |
| Skill 是 Prompt 的别名 | Skill 是**完整工作流**的封装（工程实践，无学术论文 source） |

---

## 概念关联速查

| 概念 | Source 定义 | 概念页 | 关键关联 |
|------|-------------|--------|----------|
| **Token** | Transformer 的输入原子单位 | [Tokenization](../concepts/tokenization.md) | → Embedding → Self-Attention |
| **Embedding** | 离散符号到连续向量的映射 | [Embedding](../concepts/embedding.md) | → Transformer → LLM |
| **Context** | 模型一次能处理的 token 数量上限 | [Tokenization](../concepts/tokenization.md) | → 短期记忆的物理限制 |
| **Attention** | Query×Key^T×Value 加权机制 | [Attention Mechanism](../concepts/attention-mechanism.md) | → Self-Attention → Transformer |
| **Transformer** | Attention + FFN + Positional Encoding | [Transformer](../concepts/transformer.md) | → LLM 的基石架构 |
| **LLM** | 基于 Transformer 的 next-token predictor | [Language Model Training](../concepts/language-model-training.md) | → Scaling Laws → RLHF |
| **Scaling Laws** | 性能随算力/参数/数据可预测增长 | [Scaling Laws](../concepts/scaling-laws.md) | → Kaplan → Chinchilla |
| **Fine-tuning** | 预训练后的任务适配 | [Fine-tuning](../concepts/fine-tuning.md) | → SFT → RLHF/DPO |
| **Alignment** | 让 LLM 行为符合人类意图 | [Alignment](../concepts/alignment.md) | → RLHF → InstructGPT |
| **Prompt** | Few-shot/指令输入接口 | [LLM Agents](../concepts/llm-agents.md) | → CoT → ReAct |
| **CoT / ReAct** | 显式推理 + 工具调用循环 | [Chain-of-Thought & ReAct](../concepts/chain-of-thought-react.md) | → Thought-Action-Observation |
| **Tool** | 外部 API 能力扩展 | [LLM Agents](../concepts/llm-agents.md) | → Function Calling → Agent |
| **Function Calling** | 结构化工具调用接口 | [Function Calling](../concepts/function-calling.md) | → JSON schema → Execution |
| **MCP** | 工具标准化协议（工程实践） | — | → 跨平台互操作 |
| **Vector DB** | 高维向量的存储与相似度检索 | [Vector Database](../concepts/vector-database.md) | → Memory → RAG |
| **Memory** | 短期 + 长期信息存储 | [Memory](../concepts/memory.md) | → Context / Vector DB |
| **Agent** | LLM + Planning + Memory + Tool | [LLM Agents](../concepts/llm-agents.md) | → ReAct Loop → Skill |
| **RAG** | 检索增强生成 | [RAG](../concepts/rag.md) | → Vector DB + LLM |
| **Skill** | 模块化能力封装（工程实践） | — | → Agent 的可复用组件 |

---

## 从概念到实践：Agent 调用链路

当你对一个 AI 系统说"查一下北京天气并写封邮件"，背后的完整链路基于 [ReAct](../sources/react-chain-of-thought.md) 的 Thought-Action-Observation 循环：

![Agent 调用链路时序图](./ai-core-concepts/agent-call-sequence.svg)

**Source 依据**: ReAct 论文证明，将 reasoning traces（Thought）和 task-specific actions（Action）交织执行，优于单独的 chain-of-thought 或 action-only 基线。

---

## Source 索引

本文的概念定义和关系陈述基于以下 source 资料：

### 核心架构
- [Attention Is All You Need](../sources/attention-is-all-you-need.md) — Transformer 原始论文
- [The Illustrated Transformer](../sources/the-illustrated-transformer.md) — Transformer 可视化教程

### 规模化训练
- [GPT-3](../sources/gpt3-language-models-few-shot.md) — Few-shot learning 与 next-token prediction
- [Scaling Laws](../sources/scaling-laws-kaplan.md) — 模型、数据、算力的规模化规律
- [Chinchilla](../sources/chinchilla.md) — 计算最优 scaling

### 对齐与偏好
- [InstructGPT](../sources/instructgpt.md) — RLHF 与人类反馈对齐
- [RLHF from Human Feedback](../sources/rlhf-from-feedback.md) — RLHF 奠基（summarization）
- [DPO](../sources/dpo.md) — 直接偏好优化

### Agent 系统
- [LLM Powered Autonomous Agents](../sources/llm-powered-autonomous-agents.md) — Agent 系统综述（Planning + Memory + Tool）
- [ReAct](../sources/react-chain-of-thought.md) — 推理与行动协同框架
- [Toolformer](../sources/toolformer.md) — 语言模型自学使用工具

### 未纳入 Source 的概念
- **MCP** 和 **Skill** 目前未出现在任何已 ingest 的学术论文 source 中，定义来自工程实践文档。

---

## 延伸阅读

### 输入与架构
- [Tokenization](../concepts/tokenization.md) — BPE 分词与 Token 的实际表现
- [Embedding](../concepts/embedding.md) — 从 word2vec 到 Contextual Embedding
- [Transformer](../concepts/transformer.md) — LLM 的基石架构
- [Attention Mechanism](../concepts/attention-mechanism.md) — Self-Attention 的数学原理与类型

### 训练与规模化
- [Language Model Training](../concepts/language-model-training.md) — 预训练目标与流程
- [Scaling Laws](../concepts/scaling-laws.md) — Kaplan vs Chinchilla 的 scaling 规律
- [Fine-tuning](../concepts/fine-tuning.md) — SFT、RLHF、DPO 等方法详解
- [Alignment](../concepts/alignment.md) — RLHF 三步法与 DPO

### 交互与推理
- [Chain-of-Thought & ReAct](../concepts/chain-of-thought-react.md) — 显式推理与行动循环
- [Function Calling](../concepts/function-calling.md) — 结构化工具调用机制

### Agent 系统
- [LLM Agents](../concepts/llm-agents.md) — Agent 架构深度解析（Planning + Memory + Tool）
- [Memory](../concepts/memory.md) — 短期与长期记忆机制
- [Vector Database](../concepts/vector-database.md) — 长期记忆与语义检索基础设施
- [RAG](../concepts/rag.md) — 检索增强生成的核心流程

### 其他
- [一个 Token 的一生](./token-lifecycle.md) — 从输入到输出的完整旅程
- [Harness Engineering](../../../agent/harness-engineering/concepts/HarnessEngineering.md) — 让 Agent 可靠落地的工程方法
