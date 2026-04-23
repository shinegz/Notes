# Collect session — AI Fundamentals

- **Goal**: 构建 AI 理论知识体系：历史脉络、重要论文、技术演进、LLM 原理
- **Default shelf**: `ai-fundamentals`
- **Created**: 2026-04-19

## Candidate sources（待你确认）

### 一、AI 发展历史

| OK | Type | URL 或路径 | 建议 raw 路径 | 一行理由 |
|----|------|------------|---------------|----------|
| [ ] | blog | https://en.wikipedia.org/wiki/History_of_artificial_intelligence | `articles/wikipedia-ai-history.md` | 维基百科 AI 历史词条，权威综述 |
| [ ] | blog | https://hai.stanford.edu/ | `refs/stanford-hai.md` | 斯坦福 HA.I 研究所首页，含里程碑 |
| [ ] | blog | https://blogs.nvidia.com/blog/category/deep-learning/ | `refs/nvidia-deep-learning-blog.md` | NVIDIA 官方博客，深度学习发展 |

### 二、经典论文（必读）

| OK | Type | URL 或路径 | 建议 raw 路径 | 一行理由 |
|----|------|------------|---------------|----------|
| [ ] | paper | https://arxiv.org/abs/1706.03762 | `pdfs/attention-is-all-you-need.pdf` | **Transformer 奠基论文** — Attention is All You Need |
| [ ] | paper | https://arxiv.org/abs/1810.04805 | `pdfs/bert-pre-training.pdf` | BERT — 预训练+微调范式 |
| [ ] | paper | https://arxiv.org/abs/2005.14165 | `pdfs/gpt3-language-models-few-shot.pdf` | GPT-3 — In-context Learning |
| [ ] | paper | https://arxiv.org/abs/2201.08239 | `pdfs/instructgpt.pdf` | InstructGPT — RLHF 开山 |
| [ ] | paper | https://arxiv.org/abs/2210.03629 | `pdfs/reasoning-with-language-model.pdf` | Chain-of-Thought 推理 |

### 三、Transformer 详解

| OK | Type | URL 或路径 | 建议 raw 路径 | 一行理由 |
|----|------|------------|---------------|----------|
| [ ] | blog | https://lilianweng.github.io/posts/2023-03-15-transformer/ | `articles/lilian-weng-transformer.md` | Lilian Weng 写的 Transformer 详解 |
| [ ] | blog | https://jalammar.github.io/illustrated-transformer/ | `articles/illustrated-transformer.md` | 图解 Transformer，视觉友好 |
| [ ] | blog | https://arxiv.org/abs/2101.06857 | `pdfs/chain-of-thought.pdf` | Chain-of-Thought Prompting |
| [ ] | blog | https://kipp.ly/transformer-taxonomy/ | `articles/transformer-taxonomy.md` | Transformer 架构全景分类 |

### 四、LLM 训练与优化

| OK | Type | URL 或路径 | 建议 raw 路径 | 一行理由 |
|----|------|------------|---------------|----------|
| [ ] | blog | https://huyenchip.com/2023/04/11/llm-training.html | `articles/chips-and-tacos-llm-training.md` | Chip Huyen 的 LLM 训练全景 |
| [ ] | paper | https://arxiv.org/abs/2304.15004 | `pdfs/rlhf-from-feedback.pdf` | RLHF — 从人类反馈中学习 |
| [ ] | blog | https://magazine.sebastianraschka.com/p/understanding-and-enhancing | `articles/raschka-understanding-llm.md` | Sebastian Raschka 解读 LLM |
| [ ] | blog | https://lifeinfluences.github.io/2024/02/07/llm-architecture-and-training-pipeline.html | `articles/llm-training-pipeline.md` | LLM 架构与训练流程详解 |

### 五、Agent 理论基础

| OK | Type | URL 或路径 | 建议 raw 路径 | 一行理由 |
|----|------|------------|---------------|----------|
| [ ] | paper | https://arxiv.org/abs/2210.03629 | `pdfs/react-synergizing-reasoning-acting.pdf` | ReAct — Reasoning + Acting 协同 |
| [ ] | paper | https://arxiv.org/abs/2302.04761 | `pdfs/toolformer.pdf` | Toolformer — 模型学习使用工具 |
| [ ] | blog | https://lilianweng.github.io/posts/2023-06-23-agent/ | `articles/lilian-weng-llm-agent.md` | Lilian Weng 的 LLM Agent 综述 |
| [ ] | blog | https://www.promptengguide.org/ | `articles/prompt-engineering-guide.md` | Prompt Engineering 指南 |

### 六、优质中文资料

| OK | Type | URL 或路径 | 建议 raw 路径 | 一行理由 |
|----|------|------------|---------------|----------|
| [ ] | doc | `../AI/llm/` | `refs/local-llm-notes.md` | 你已有的本地 LLM 学习笔记（00-05） |
| [ ] | doc | `../AI/thinking/Agent 时代的能力模型与学习框架.md` | `refs/agent-era-framework.md` | Agent 时代能力模型 |
| [ ] | doc | `../AI/agent/AI Agent 全面认知指南.md` | `refs/agent-guide.md` | AI Agent 全面认知 |

### 七、优质视频课程

| OK | Type | URL 或路径 | 建议 raw 路径 | 一行理由 |
|----|------|------------|---------------|----------|
| [ ] | youtube | https://www.youtube.com/@AndrejKarpathy | `refs/karpathy-youtube.md` | Karpathy 的 Neural Networks 课程 |
| [ ] | youtube | https://www.youtube.com/watch?v=kCc8FmEb1nY | `refs/nlp-from-scratch-pytorch.md` | 从零实现 NLP（PyTorch） |

### 八、Scaling Laws 与模型能力

| OK | Type | URL 或路径 | 建议 raw 路径 | 一行理由 |
|----|------|------------|---------------|----------|
| [ ] | paper | https://arxiv.org/abs/2001.08361 | `pdfs/scaling-laws-neural-language-models.pdf` | Scaling Laws — Kaplan et al. |
| [ ] | paper | https://arxiv.org/abs/2204.14111 | `pdfs/small-models-big-performance.pdf` | Chinchilla — 重新审视 scaling |
| [ ] | blog | https://www.semianalysis.com/p/gpt4-architecture | `refs/gpt4-architecture-leak.md` | GPT-4 架构泄露分析 |

---

## 你的批复

**采纳**：一、二、三、四、五、七、八（全部），移除六（本地笔记）

## Fetched（已收集）

### PDF 论文
| raw路径 | 状态 |
|---------|------|
| `pdfs/attention-is-all-you-need.pdf` | ✅ |
| `pdfs/bert-pre-training.pdf` | ✅ |
| `pdfs/gpt3-language-models-few-shot.pdf` | ✅ |
| `pdfs/instructgpt.pdf` | ✅ |
| `pdfs/react-chain-of-thought.pdf` | ✅ |
| `pdfs/toolformer.pdf` | ✅ |
| `pdfs/rlhf-from-feedback.pdf` | ✅ |
| `pdfs/scaling-laws-kaplan.pdf` | ✅ |
| `pdfs/chinchilla.pdf` | ✅ |

### 网页原文（baoyu-url-to-markdown）
| raw路径 | 状态 |
|---------|------|
| `articles/the-illustrated-transformer.md` | ✅ |
| `articles/llm-powered-autonomous-agents.md` | ✅ |
| `articles/transformer-taxonomy-the-last-lit-review.md` | ✅ |
| `articles/ahead-of-ai-sebastian-raschka-phd-substack.md` | ✅ |
| `refs/home-stanford-hai.md` | ✅ |
| `refs/nextra.md` (Prompt Engineering Guide) | ✅ |

### 未能获取
| 来源 | 原因 |
|------|------|
| Lilian Weng Transformer 文章 | URL 变更，404 |
| Chip Huyen LLM Training | 页面重定向失效 |
| Wikipedia AI History | 网络限制 |
