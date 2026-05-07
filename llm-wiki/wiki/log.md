## [2026-05-07] ingest | Source 摘要页补建（7 篇）

- **Sources**（7）：lost-in-the-middle、icl-bayesian-inference、prompt-engineering-survey、longllmlingua、rlhf-sycophancy、context-dilution、prompt-from-first-principles-dev
- 更新 `wiki/ai-fundamentals/index.md`（新增「上下文与注意力」「对齐与行为」分组）
- 更新 `wiki/ai-fundamentals/syntheses/prompt-from-principles.md` 的 sources 引用，正文内链改指向新 source 页

## [2026-05-07] ingest | 从大模型原理出发谈 Prompt

- 新增 `wiki/ai-fundamentals/syntheses/prompt-from-principles.md`
- **体裁**：框架综合（原理 → 技巧映射）
- **核心内容**：从自回归预测、注意力机制、In-Context Learning、对齐训练、Context Window 五条底层原理推导 Prompt 技巧的有效性
- **素材**：Collect 7 个新素材（5 PDF + 2 articles）
  - PDFs：lost-in-the-middle、icl-bayesian-inference、prompt-engineering-survey、longllmlingua、rlhf-sycophancy
  - Articles：prompt-from-first-principles-dev、context-dilution
- 复用已有 wiki 内 11 个 source/concept 页
- 更新 `wiki/ai-fundamentals/index.md`、`wiki/index.md`、`wiki/overview.md`、`wiki/log.md`

## [2026-05-07] delete | Prompt 写作流程综合页

- 删除 `wiki/ai-fundamentals/syntheses/prompt-writing-workflow.md`
- 原因：内容被整合入 [[ai-fundamentals/syntheses/prompt-from-principles|从大模型原理出发谈 Prompt]] 原理导向综合页，避免重复
- 清理引用：`wiki/index.md`、`wiki/ai-fundamentals/index.md`、`prompt-from-principles.md` 的关联概念

## [2026-05-06] ingest | Prompt Engineering 系统理论补充

- **Collect**：7 个新素材落盘
  - Articles（4）：anthropic-context-engineering、openai-prompt-guidance、prompt-engineering-frameworks-parloa、prompt-engineering-2025-aakashg
  - PDFs（3）：anthropic-prompt-best-practices、costar-a-framework、prompt-engineering-methodology
- **Sources**：4 篇 source 摘要页
  - anthropic-context-engineering、openai-prompt-guidance、prompt-engineering-frameworks-parloa、prompt-engineering-2025-aakashg
- **Concepts**：更新 prompt-engineering 概念页（新增结构化框架、Context Engineering 演进、6 项核心原则）；新建 context-engineering 概念页
- 更新 `wiki/ai-fundamentals/index.md`、`wiki/overview.md`、`wiki/log.md`

## [2026-05-03] ingest | agent/core-architecture 补充遗漏 source + 新增 concepts

- **补充 ingest**：`openclaw-repo.md` → `wiki/agent/core-architecture/sources/openclaw-repo.md`
- **新增 concepts**（2）：`A2A`（Agent-to-Agent Protocol）、`Reflection`（Agent 自我反思机制）
- **更新 index**：Sources 12→13，Concepts 6→8

## [2026-05-03] ingest | agent/core-architecture 补全 concepts + entities

- ** Concepts**（6）：SimulatedAgency、TrueAutonomy、ReAct、MemoryTaxonomy、MultiAgentCoordinationPatterns、MCP
- **Entities**（3）：KenMendoza、NousResearch、Mem0
- **lint 通过**：source_frontmatter_errors: 0, orphan_pages: 0

## [2026-05-03] ingest | agent/core-architecture 新建子主题

- **新建 shelf**：`agent/core-architecture/`
- **落地 13 个来源**（raw/）：
  - pdfs/：`agentic-ai-comprehensive-survey.pdf`、`llm-enabled-multi-agent-systems.pdf`、`memory-autonomous-llm-agents.pdf`
  - articles/：`core-agentic-ai-architectural-patterns.md`、`ultimate-guide-ai-agent-architectures-2025.md`、`aws-bedrock-agentcore-best-practices.md`、`multi-agent-system-architecture-guide.md`、`agent-memory-architectures.md`、`ai-agent-architecture-components-types.md`
  - refs/：`pi-mono-repo.md`、`openclaw-repo.md`、`hermes-agent-repo.md`、`opencode-repo.md`
- **Medium 两篇**原文需登录，已分别用 arXiv 2603.07670 PDF 和 PuppyGraph 替代
- **Source pages**（13）：`wiki/agent/core-architecture/sources/` 下全部写完
- **Ingest 问题记录**：arXiv 论文错误抓了 HTML 而非 PDF（已补下）；工具路由规则已更新到 candidates 模板

## [2026-05-02] ingest | software-fundamentals 补全 POSD concepts + entity

- **POSD 2nd Edition OCR 完成**：使用 pypdfium2 + PaddleOCR 提取扫描版 PDF 全文
- **新增 Concepts**（4）：`InformationHiding.md`、`GeneralPurposeModules.md`、`BetterTogetherOrBetterApart.md`（来自 POSD Ch 6/9）
- **新增 Entities**（1）：`JohnOusterhout.md`
- **更新 CLAUDE.md 第 6 步**：强化 ingest 后概念/实体补全检查要求
- **lint 通过**：source_frontmatter_errors: 0

- **本次新增 Sources**（4）：
  - `frederick-brooks-official-site.md` — Brooks UNC 教授主页出版物列表与荣誉
  - `design-of-design-index.pdf` → `design-of-design-index.md` — Brooks 2010 设计的艺术（54 页 PDF）
  - `design-of-design-part1.pdf` → `design-of-design-part1.md` — Anderson 课程讲义前三章（29 页 PDF）
  - `posd-2nd-edition.pdf` → `posd-2nd-edition.md` — 扫描版，文本不可提取，待 OCR
- **lint 通过**：source_frontmatter_errors: 0
- **待办**：POSD 2nd Edition OCR 处理

## [2026-04-30] graph | rebuilt (wikilink-only)

99 nodes, 441 edges.

## [2026-04-30] graph | rebuilt (wikilink-only)

99 nodes, 428 edges.

## [2026-04-30] ingest | software-fundamentals Ingest 完成（规范重写）

- **重新执行 Ingest**，严格按照 `ingest-structure-guide.md` 和 `source-template.md` 规范
- **本次新增文件**（共 8 个）：
  - **Sources** (3): `domain-driven-design.md`, `mythical-man-month.md`, `pragmatic-programmer-20th-anniversary.md`
  - **Entities** (1): `FrederickBrooks.md`
  - **Concepts** (4): `ObjectOrientedDesign.md`, `DesignPatterns.md`, `SoftwareArchitecture.md`, `DomainDrivenDesign.md`
- **结构规范**：
  - Concepts: `Epitome` → `Boundary Clarification` → `Mechanism` → `Types/Applications` → `Connections` → `Sources`
  - Sources: `Summary`（结论先行）→ `Key Claims` → `Architecture Table`（可选）→ `Key Quotes`（可选）→ `Connections`
  - Entities: `Definition` → `Key Attributes` → `Key Works` → `Key Quotes` → `Connections`
- **风格规范**：
  - 删除 `—` 破折号连接词
  - 删除 `**加粗**` 强调（除表格标题和特定术语）
  - 使用 `humanizer-zh` skill 进行去 AI 味处理
- **lint 通过**：source_frontmatter_errors: 0, table_errors: 0
- **待办**：
  - POSD/DoD PDF 内容提取
  - DDD 官网（domainlanguage.com）交互访问

## [2026-04-30] taxonomy | new shelf: software-fundamentals

- 登记门类 `software-fundamentals`（软件工程基础理论：经典书籍、设计原则、架构方法论）
- 调整 `sdd` 说明（移除"理论基础"，强调"框架生态、源码实现、Agentic Skills"）
- 创建目录结构：`raw/software-fundamentals/{pdfs,articles,refs,notes}`、`wiki/software-fundamentals/{sources,concepts,entities,syntheses,comparisons}`
- 创建 `wiki/software-fundamentals/index.md`（预设 POSD/TPP/DoD/DDD 四书视角）
- 更新 `taxonomy.md`、`wiki/index.md`
- 更新 candidates session 为 `software-fundamentals` shelf

## [2026-04-29] optimize | llm-wiki GitHub 资源获取规范

- 发现问题：llm-wiki 对 GitHub 仓库源码分析无正式流程，此前使用 `curl` ad-hoc 调用
- 安装 `gh CLI` (v2.92.0) 作为 GitHub 资源首选工具
- 更新规范（分层放置）：
  - `CLAUDE.md` — 保持 schema 层级，**不添加** GitHub 相关小节（条件性工具细节不下沉到总纲）
  - `docs/collect-workflow.md` — 新增「GitHub 资源获取」完整小节（含 `gh api` 三级优先级表格、认证说明、存储规范）；特殊来源处理规则表格新增「GitHub 仓库源码」行
  - `raw/README.md` — `refs/` 含义扩展为包含 GitHub 源码指针，补充指针文件格式示例
- **待办**：`gh auth login` 认证后，`gh api` 可获得更高 rate limit（5000 req/hour vs 未认证 60 req/hour）

## [2026-04-29] ingest | sdd shelf Ingest 完成

- **Sources**: 6 篇 source 摘要页
  - Martin Fowler 团队 SDD 三工具评测、GitHub Blog Spec Kit 介绍、知乎框架全景
  - Superpowers README、gstack README、Compound Engineering README
- **Concepts**: 5 个核心概念页
  - Spec-First、Spec-Anchored、Spec-as-Source、Agentic Skills、Compounding Knowledge
- **Entities**: 3 个项目实体页（含 GitHub API 源码分析）
  - Superpowers（14 skills，零依赖，强制 TDD）
  - Gstack（23 skills，Chromium Daemon，多平台适配）
  - Compound Engineering（36 skills + 51 agents，跨平台转换器）
- **Syntheses**: 1 个框架全景综合
  - SDD 框架金字塔结构、渐进式 Spec 策略、技能框架选择指南
- **Comparisons**: 1 个框架对比
  - 五大框架七维度横评 + 决策建议
- 更新 `wiki/sdd/index.md`

## [2026-04-29] taxonomy | new shelf: sdd

- 登记门类 `sdd`（规范驱动开发：理论基础、框架生态、源码实现）
- 创建 `raw/sdd/`、`wiki/sdd/` 目录结构
- 更新 `taxonomy.md`、`wiki/index.md`

## [2026-04-26] collect | Prompt Engineering (OpenAI Prompt Engineering Guide)
## [2026-04-26] collect | RoPE - Rotary Position Embedding (arxiv 2104.09864)
## [2026-04-26] collect | Mixtral 8x7B - Mixture of Experts (arxiv 2401.04088)
## [2026-04-26] collect | MMLU - Measuring Massive Multitask Language Understanding (arxiv 2009.03300)

## [2026-04-26] collect | Machine Learning Overview (Wikipedia)
## [2026-04-26] collect | Deep Learning Overview (Wikipedia)
## [2026-04-26] collect | Neural Network Basics (Wikipedia)
## [2026-04-26] collect | Reinforcement Learning Overview (Wikipedia)
## [2026-04-26] collect | Backpropagation Explained (Wikipedia)
## [2026-04-26] collect | Gradient Descent Overview (Wikipedia)

## [2026-04-26] synthesis | AI Concept Architecture（三层架构 + 跨层关系）

- 新增 `wiki/ai-fundamentals/syntheses/ai-concept-architecture.md`
- **核心框架**：训练范式层 → LLM 架构层 → Agent 架构层
- **关系视角**（非分类视角）：使能 / 依赖 / 演进 / 叠加 / 手段 / 实现
- 覆盖所有 AI 核心概念，包括你提到的机器学习、神经网络、深度学习、强化学习、Transformer、Context、Token、Function Calling、Tool Use、MCP、Skill、Agent、Memory、RAG 等
- SVG 图：三层架构 + 关系类型 + 跨层连接示例（Dark Terminal 风格）
- 更新 `wiki/index.md`、`wiki/ai-fundamentals/index.md`

## [2026-04-26] synthesis | 一个 Token 的一生（重写+配图）

- 重写 `wiki/ai-fundamentals/syntheses/token-lifecycle.md`（图文版）
- 应用 `humanizer-zh` 去除 AI 写作痕迹
- 用 `fireworks-tech-graph` 生成 5 张 SVG+PNG 图：
  - `self-attention.svg` — Q/K/V 交互与注意力权重矩阵
  - `transformer-architecture.svg` — Transformer 层层堆叠架构
  - `bpe-tokenization.svg` — BPE 分词合并过程
  - `vector-arithmetic.svg` — king-man+woman≈queen 向量空间
  - `rlhf-flow.svg` — RLHF 三步法流程
- 所有图存放于 `wiki/ai-fundamentals/syntheses/token-lifecycle/`（PNG 由 Chrome headless 导出）
- 更新 `wiki/ai-fundamentals/index.md`、`wiki/index.md`、`wiki/log.md`

## [2026-04-23] ingest | PDF source summaries completed（pdf skill）

- 使用 `pdf` skill + `pypdf` 提取 13 个 PDF 的文本内容
- 10 篇 PDF 生成完整 source 摘要（Abstract + Key Contributions + Connections）
- **发现 3 个文件内容不匹配**：
  - `chinchilla.pdf` → 实际为太阳物理论文 CLEDB（非 AI 论文），已标注并建议替换
  - `rlhf-from-feedback.pdf` → 实际为 "Are Emergent Abilities of Large Language Models a Mirage?"
  - `word2vec.pdf` → 实际为 "Speech Recognition with Deep Recurrent Neural Networks"
- 已更新 `wiki/ai-fundamentals/index.md` 和对应 source 页反映实际内容

## [2026-04-23] ingest | ai-fundamentals re-ingest（18 sources）

- 新增 source 摘要 18 篇：
  - articles（3）：`llm-powered-autonomous-agents`（Lilian Weng Agent 综述）、`the-illustrated-transformer`（Jay Alammar 可视化教程）、`transformer-taxonomy`（kipply 文献综述）
  - refs（2）：`ai-index-stanford-hai`（Stanford HAI 年度报告）、`history-of-artificial-intelligence`（Wikipedia AI 发展史）
  - PDFs（13）：`agentbench`、`alexnet`、`chinchilla`、`dpo`、`gan`、`gqa`、`lora`、`react-chain-of-thought`、`resnet`、`rlhf-from-feedback`、`rope`、`toolformer`、`word2vec`
- 其中 5 篇 Markdown 文章生成完整摘要；13 篇 PDF 创建基础 source 页（标记"待补充摘要"）
- 更新 `wiki/ai-fundamentals/index.md`（按主题重新分类）、`wiki/index.md`、`wiki/overview.md`

## [2026-04-23] synthesis | AI核心概念体系（修订）

- 新增 `wiki/ai-fundamentals/syntheses/ai-core-concepts.md`
- 系统拆解 Token → Context → Prompt → LLM → Tool → MCP → Agent → Skill 的层级关系
- 用 `fireworks-tech-graph` 生成 2 张 SVG：层级架构图、Agent 调用链路时序图
- 删除冗余 Mermaid 图 2 张，延伸阅读链接改为标准 Markdown 格式（相对路径）
- 修正比喻体系："汽车引擎"→"续写者"，"洋葱"→"层级结构"
- 更新 `wiki/ai-fundamentals/index.md`、`wiki/index.md`、`wiki/overview.md`

- 新增 `wiki/ai-fundamentals/syntheses/ai-core-concepts.md`
- 系统拆解 Token → Context → Prompt → LLM → Tool → MCP → Agent → Skill 的层级关系
- 含 3 张 Mermaid 图（层级架构图、Agent 调用链路时序图、概念层级总览图）
- 更新 `wiki/ai-fundamentals/index.md`、`wiki/index.md`、`wiki/overview.md`

## [2026-04-19] taxonomy | new shelf: ai-fundamentals

- 登记门类 `ai-fundamentals`（AI 理论基础）
- 更新 `taxonomy.md`、`wiki/index.md`
- 创建 `wiki/ai-fundamentals/index.md`、`wiki/ai-fundamentals/overview.md`
- 同期 ingest 8 个主题的 source 摘要 + 5 篇概念页
- 2026-04-19 — 迁移 `sources/` 子目录结构 → 扁平文件（kebab-case.md）

## [2026-04-19] synthesis | 一个 Token 的一生

- 新增 `wiki/ai-fundamentals/syntheses/token-lifecycle.md`
- 用图文故事解释 LLM 运行原理（Tokenization → Embedding → Attention → FFN → Softmax → Sampling → Auto-Regressive）
- 更新 `wiki/ai-fundamentals/index.md`、`wiki/index.md`

---

## [2026-04-14] graph | rebuilt (wikilink-only)

17 nodes, 92 edges.

## [2026-04-14] graph | rebuilt (wikilink-only)

17 nodes, 91 edges.

## [2026-04-14] graph | rebuilt (wikilink-only)

17 nodes, 93 edges.

## [2026-04-14] synthesis | Harness Engineering 深度解析

- 新增 `wiki/agent/harness-engineering/syntheses/harness-engineering-deep-dive.md`
- 删除旧合成文 `harness-engineering-jianjie-yu-luodi.md`
- 更新 `wiki/agent/harness-engineering/index.md`、`wiki/index.md`

## [2026-04-14] ingest | 深度解析：Harness Engineering（公众号）

- 新增 `raw/agent/harness-engineering/wechat/深度解析-Harness-Engineering.md`（9 张图）
- 新增 `wiki/agent/harness-engineering/sources/深度解析-Harness-Engineering.md`
- 更新 `wiki/agent/harness-engineering/concepts/HarnessEngineering.md`、`wiki/agent/harness-engineering/index.md`、`wiki/index.md`
- 同期 re-collect `raw/agent/harness-engineering/articles/` 10 篇（含 29 张图、HTML snapshots）

## [2026-04-14] graph | rebuilt (wikilink-only)

16 nodes, 84 edges.

## [2026-04-14] graph | rebuilt (wikilink-only)

16 nodes, 83 edges.

## [2026-04-14] synthesis | Harness Engineering 介绍与落地（中文）

- 新增 `wiki/agent/harness-engineering/syntheses/harness-engineering-jianjie-yu-luodi.md`；更新 `wiki/index.md`、`wiki/agent/harness-engineering/index.md`

## [2026-04-14] graph | rebuilt (wikilink-only)

15 nodes, 69 edges.

## [2026-04-14] ingest | harness-engineering re-collect

- WebFetch 更新 `raw/agent/harness-engineering/articles/`：`humanlayer-*`、`ignorance-*`、`parallel-*`；其余篇目补 `collect_note` 与同日快照元数据
- 10 篇 `wiki/agent/harness-engineering/sources/*.md` 重写 Summary / Key claims / quotes / Connections；`concepts/HarnessEngineering.md` 增补「落地要点」与完整 `sources` 列表

## [2026-04-14] graph | rebuilt (wikilink-only)

15 nodes, 49 edges.

## [2026-04-14] ingest | Harness Engineering（10 sources）

- `raw/agent/harness-engineering/articles/*.md` 快照落盘；`wiki/agent/harness-engineering/sources/*.md` 与概念页 `concepts/HarnessEngineering.md`
- 更新 `wiki/index.md`、`wiki/overview.md`、`wiki/agent/harness-engineering/index.md`；OpenAI 中文正文以 WebFetch 快照写入 session `_openai_zh_webfetch.md`（直连 HTML 403）

## [2026-04-14] taxonomy | agent + harness-engineering

- 登记门类 `agent`；子主题 `harness-engineering/`（`raw/agent/harness-engineering/`、`wiki/agent/harness-engineering/`）
- 更新 `taxonomy.md`、`raw/README.md`、`wiki/index.md`

## [2026-04-13] graph | rebuilt (wikilink-only)

2 nodes, 1 edges.

# Wiki log（新条目 prepend 在文件顶部）

## [2026-04-13] scaffold | llm-wiki initialized

- 创建目录与 schema（`CLAUDE.md`）
