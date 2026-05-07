# Collect session — 从大模型原理出发谈 Prompt

- **Goal**: 从自回归预测、注意力机制、In-Context Learning、对齐、Context Window 五条底层原理出发，推导 Prompt 技巧为什么有效，形成一篇原理驱动的综合页
- **Default shelf**: `ai-fundamentals`
- **Created**: 2026-05-07

## Candidate sources（待你确认）

### 新增素材（从原理视角讨论 Prompt）

| OK | Type | URL 或路径 | 建议 shelf | 建议 raw 子路径 | 一行理由 |
|----|------|------------|------------|-----------------|----------|
| [ ] | paper | https://arxiv.org/abs/2307.03172 | ai-fundamentals | `pdfs/lost-in-the-middle.pdf` | Lost in the Middle：注意力 U 型分布（开头结尾信息召回高、中间低），直接解释"重要信息放开头或结尾"的原理 |
| [ ] | paper | https://arxiv.org/abs/2111.02080 | ai-fundamentals | `pdfs/icl-bayesian-inference.pdf` | In-Context Learning as Implicit Bayesian Inference：ICL 的理论解释——模型从 Prompt 示例中推断隐含概念，解释 Few-shot 有效的底层机制 |
| [ ] | paper | https://arxiv.org/abs/2402.07927 | ai-fundamentals | `pdfs/prompt-engineering-survey.pdf` | A Systematic Survey of Prompt Engineering：2024 年系统性综述，覆盖 Prompt 技术全分类，提供原理-技巧映射的学术骨架 |
| [ ] | blog | https://dev.to/programmerraja/prompt-engineering-from-first-principles-the-mechanics-they-dont-teach-you-part-1-12nb | ai-fundamentals | `articles/prompt-from-first-principles-dev.md` | Prompt Engineering From First Principles：从自回归和注意力机制出发解释 Prompt 技巧，与本文主题直接对齐 |
| [ ] | blog | https://diffray.ai/blog/context-dilution/ | ai-fundamentals | `articles/context-dilution.md` | Context Dilution: When More Tokens Hurt AI：注意力稀释现象的通俗解释，支撑"压缩 Prompt"的原理 |
| [ ] | paper | https://aclanthology.org/2024.acl-long.91.pdf | ai-fundamentals | `pdfs/longllmlingua.pdf` | LongLLMLingua：Prompt 压缩的理论与实践，用信息论方法移除低信息量 token，改善长上下文性能 |
| [ ] | paper | https://www.gerdusbenade.com/files/26_sycophancy.pdf | ai-fundamentals | `pdfs/rlhf-sycophancy.pdf` | How RLHF Amplifies Sycophancy：RLHF 导致谄媚行为的机制分析，解释"正面引导 > 负面禁止"的对齐层原理 |

### 已有素材（复用 wiki 中已有内容）

以下已有 source 直接支撑本文，无需重复收集：

| 来源 | 对应原理维度 |
|------|-------------|
| `ai-fundamentals/sources/openai-prompt-engineering` | 全部维度（核心策略来源） |
| `ai-fundamentals/sources/openai-prompt-guidance` | 全部维度（实操策略） |
| `ai-fundamentals/sources/anthropic-context-engineering` | Context Window / 注意力稀释 |
| `ai-fundamentals/sources/prompt-engineering-frameworks-parloa` | 结构化 Prompt 的框架支撑 |
| `ai-fundamentals/sources/prompt-engineering-2025-aakashg` | 压缩与成本经济学 |
| `ai-fundamentals/concepts/attention-mechanism` | 注意力机制原理 |
| `ai-fundamentals/concepts/tokenization` | Tokenization 原理 |
| `ai-fundamentals/concepts/embedding` | Embedding 原理 |
| `ai-fundamentals/concepts/alignment` | RLHF / 对齐原理 |
| `ai-fundamentals/concepts/context-window` | Context Window 限制 |
| `ai-fundamentals/syntheses/token-lifecycle` | LLM 运行全流程（自回归预测） |

## 你的批复

（在此打勾或聊天回复采纳序号 / 修改 shelf）

## Fetched（确认后由 Agent 填写）

| raw路径 | 状态 |
|----------|------|
| `raw/ai-fundamentals/pdfs/lost-in-the-middle.pdf` | ✅ 已下载 |
| `raw/ai-fundamentals/pdfs/icl-bayesian-inference.pdf` | ✅ 已下载 |
| `raw/ai-fundamentals/pdfs/prompt-engineering-survey.pdf` | ✅ 已下载 |
| `raw/ai-fundamentals/pdfs/longllmlingua.pdf` | ✅ 已下载 |
| `raw/ai-fundamentals/pdfs/rlhf-sycophancy.pdf` | ✅ 已下载 |
| `raw/ai-fundamentals/articles/prompt-from-first-principles-dev.md` | ✅ 已抓取 |
| `raw/ai-fundamentals/articles/context-dilution.md` | ✅ 已抓取 |
