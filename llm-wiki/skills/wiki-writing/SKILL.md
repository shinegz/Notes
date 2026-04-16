---
name: wiki-writing
description: >
  Karpathy-style llm-wiki prose for concepts/, syntheses/, and overview.md—grounded in sources, [[wikilinks]], honest claims, no marketing filler. Use when editing or drafting wiki pages, de-AI passes on Chinese technical notes, ingest summary tone, or principle-first knowledge-base writing. Always pair with skills/humanizer-zh for Chinese de-AI. URL/material collection uses skills/collect and bundled adapter skills—not this file.
---

# Wiki 写作（llm-wiki）

> 不是固定段落模版，而是 Agent 在写 **`concepts/`、`syntheses/`、实质性修订 `overview.md`** 时的原则。  
> **`sources/`** 以摘要、主张、摘录与回链为主，避免宣传腔与长篇散文。

## 路径约定

- **Wiki 根**：环境变量 **`WIKI_ROOT`**（本 pack 根目录，定义见 **`AGENTS.md`**）。下文 **`skills/`** 指 **`$WIKI_ROOT/skills/`**。
- 去 AI 味（中文）：**`skills/humanizer-zh/SKILL.md`**（见 **`skills/README.md`**）。

## 1. 好文的共性（简述）

- **读者**：尽快让人知道读完后能得到什么；技术前提或范围要清楚。
- **主线**：一篇一个可复述的核心；段落推进论证，不是素材堆砌。
- **具体先于抽象**：例子、现象、可检验陈述，再收束到概念。
- **诚实**：事实、推断、未覆盖之处分开写；弱化过度承诺。
- **结构服务理解**：标题与过渡句负责导航；列表与图表为 clarity 服务。

## 2. 去 AI 味（必读配合）

修订或撰写成稿时，**对照** **`skills/humanizer-zh/SKILL.md`**：检测并改掉典型 AI 痕迹（夸大象征、宣传语、肤浅 -ing 分析、模糊归因、破折号堆砌、三段式、套话连接词、否定排比等），并遵循其「删除填充、打破公式、变化节奏、信任读者」等原则。

**边界**：去 AI 味**不等于**编造个人经历；wiki 仍须 **`[[wikilink]]`** 与来源页对齐，不牺牲可追溯性。

## 3. 成稿前自检（非模版）

用 yes/no 快速过一遍即可，**不必写入正文**：

- 删掉这段话，读者是否仍少知道关键信息？若是，考虑删或改写。
- 是否有「具有重要意义 / 值得一提的是 / 综上所述」等可删拐杖？
- 主张是否都能回到本 wiki 页或 `sources/`？
- 是否把不确定处标出来了？

## 4. 与 `CLAUDE.md` 操作的关系

- **`ingest`**：写完 source 页后，可对照第 2 节检查 Summary/Claims 是否腔调过重。
- **`query` → syntheses**、**新建/大改 concept**：写作前读本技能；定稿前建议按 humanizer-zh 过一遍或至少做第 3 节自检。

**Collect（拉取素材）**：见 **`skills/collect/SKILL.md`** 与 **`tools/source_registry.tsv`**（adapter 列表以 TSV / `source_registry_cli.py list` 为准，不在此枚举）。
