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
