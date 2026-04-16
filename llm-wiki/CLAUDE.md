# LLM Wiki — Schema & 工作流

> SPDX-License-Identifier: MIT  
> 设计融合：[llm-wiki-agent](https://github.com/SamurAIGPT/llm-wiki-agent) 的 wiki 分层与 ingest/query/lint/graph；[llm-wiki-skill](https://github.com/sdyckjq-lab/llm-wiki-skill) 的来源分类与外链处理思路；[graphify](https://github.com/safishamsi/graphify) 强调的图结构视角（本 pack 内工具为**无 API Key**的确定性 wikilink 图 + Louvain）。
>
> **自洽**：文档与 `tools/` 脚本只假定「本 pack 根目录」（与 `CLAUDE.md` 同级）；不依赖父仓库、编辑器技能目录或其它本地路径。可单独拷贝本目录树使用；许可证与总览见同级 **`LICENSE`**、**`README.md`**。

---

## 核心理念（Karpathy llm-wiki）

用 LLM **增量编译**成持久 wiki（Markdown + `[[wikilink]]`），而不是每次提问都从原始片段临时拼答案。每一批素材应更新：来源页、概念/实体页、`overview.md`、矛盾标注与索引。

**写作与去 AI 味**：撰写或修订 **`wiki/` 下成稿**（`concepts/`、`syntheses/`、`overview` 等）时，须遵循 **`skills/wiki-writing/SKILL.md`**，并对照 **`skills/humanizer-zh/SKILL.md`**（见 **`skills/README.md`**）。

**Collect（URL/素材拉取）**：**`tools/source_registry.tsv`** 为来源类型 / **`raw_dir`** / adapter 的**唯一事实来源**（改表后 `validate`）。**`taxonomy.md`** 只管**有哪些顶层门类**（及子主题说明）；**`raw/README.md`** 只解释分桶含义，不复制 TSV。操作顺序与 CLI 见 **`skills/collect/SKILL.md`**（其中**不**粘贴整张路由表，用 `source_registry_cli.py list` / `get` 查行）。

---

## 目录布局

```text
llm-wiki/
├── CLAUDE.md           ← 本文件（schema）
├── AGENTS.md           ← Agent 快速入口
├── purpose.md          ← 学习目标与边界
├── taxonomy.md         ← 当前「门类」书架（动态；结构变更须人审）
├── skills/             ← Agent 能力：collect 路由、URL 适配器、wiki-writing、humanizer-zh（见 skills/README.md）
├── raw/<shelf>/        ← immutable素材；子目录见 raw/README.md（articles/pdfs/transcripts/notes/refs + 平台桶）
├── wiki/<shelf>/       ← 编译层（与 shelf 对齐）
│   ├── sources/        ← 每篇素材对应一页
│   ├── entities/
│   ├── concepts/
│   ├── syntheses/      ← 可查后固化的问答
│   └── comparisons/    ← 可选：对比文
├── wiki/index.md       ← 总索引（跨 shelf）
├── wiki/overview.md    ← Living synthesis
├── wiki/log.md         ← 操作日志
├── graph/              ← build_graph 输出
├── sessions/           ← Collect 候选表（先审后拉）
└── tools/              ← source_registry_cli（validate / match-url / layout）+ lint + graph
```

**shelf（门类）**：路径即分类，例如 `前端`、`数据库`、`agent`。新建 shelf 必须先由用户批准，再创建目录并更新 `taxonomy.md`。

---

## 页面 frontmatter（与 llm-wiki-agent 对齐）

```yaml
---
title: "Page Title"
type: source | entity | concept | synthesis
tags: []
sources: []       # 来源 slug 或相对路径
last_updated: YYYY-MM-DD
---
```

使用 `[[相对wiki的路径|显示名]]` 互链（路径相对 `wiki/`，不含 `wiki/` 前缀）；跨 shelf 或含子主题时写全路径，如 `[[agent/harness-engineering/concepts/HarnessEngineering|Harness Engineering]]`。

**日期字段**：凡带 `type:` 的页统一使用 **`last_updated: YYYY-MM-DD`**，勿用 `date:`。

### Source 页模板（`wiki/<shelf>/sources/<slug>.md`）

```markdown
---
title: "Source Title"
type: source
tags: []
last_updated: YYYY-MM-DD
source_file: raw/<shelf>/[<子主题>/]articles/....md
source_url: https://...
---

## Summary
2–4 句。

## Key claims
- 

## Key quotes
>

## Connections
- [[EntityOrConcept]] — 

## Contradictions
- 与 [[OtherPage]] 在 … 上不一致（如有）
```

---

## 操作 A：`collect`（收集 — 先清单，后落盘）

**触发**：用户给出主题或学习目标（例：「Transformer 原理」「学 React」「Harness Engineering」）。

**硬性规则**：

1. **不得**在用户确认前批量下载或写入 `raw/`（除用户明确给出的单链接/单文件外）。
2. 若当前 shelf 不合适或需新建门类：先发起 **taxonomy 变更提案**（说明理由、命名、影响），**用户同意前**不得创建 `raw/<新shelf>/`。
3. 在 `sessions/YYYYMMDD-HHMM-<slug>/candidates.md` 填写候选表（可用 `_template`）。
4. 用户勾选或回复采纳项后，再将内容写入 `raw/<shelf>/…`，并进入 **ingest**。

**来源类型与提取策略**：以 **`tools/source_registry.tsv`** 为准（**`dependency_*`**、**`source_category`**、**`raw_dir`**、**`match_rule`**；**`default`** 行唯一且对应 **`web_article`**）。执行 Collect 时先读 **`skills/collect/SKILL.md`**。适配器不可用或 **`adapter_name`** 为 `-` 时按 **`fallback_hint`** 手动处理。

---

## 操作 B：`ingest`（消化单篇已落盘素材）

**触发**：`ingest raw/<shelf>/articles/foo.md` 或等价描述。

**步骤**（顺序）：

1. Read 源文件全文；Read `wiki/index.md`、`wiki/overview.md`、`taxonomy.md`。
2. 写 `wiki/<shelf>/sources/<slug>.md`（slug 与文件名一致，kebab-case）。
3. 更新 `wiki/index.md`（在对应 shelf 小节登记）。
4. 更新 `wiki/overview.md`（必要时修订综合结论）。
5. 更新/新建 `wiki/<shelf>/entities/`、`concepts/` 相关页。
6. 标注与既有页面的**矛盾**（写在 source 或 concept 页 `Contradictions`）。
7. 追加 `wiki/log.md`：`## [YYYY-MM-DD] ingest | <标题>`
8. **收尾（与 [llm-wiki-agent](https://github.com/SamurAIGPT/llm-wiki-agent) `/wiki-ingest` 一致）**：用几句话汇总——本次**新建/更新了哪些路径**、**矛盾**有无、是否还需补实体/概念页；便于用户核对，不要求长报告。

---

## 操作 C：`query`

1. Read `wiki/index.md` 定位相关页。
2. Read 页面后作答，引用使用 `[[...]]`。
3. 询问用户是否将回答固化为 `wiki/<shelf>/syntheses/<slug>.md`（用户指定 shelf）。

---

## 操作 D：`lint`

1. **`python3 tools/lint_wiki.py <llm-wiki-root>`** — 断链、孤儿（启发式）、**`type: source` 的 `source_file` 存在性**、**frontmatter**（凡含 **`type:`** 的页须 **`last_updated`**；**禁止 `date:`**；source 另须 **`title` / `source_file`**；缺 `source_url` 仅警告）、**`thin_key_claims`**（仍含「ingest 占位」的统计）。一键：**`bash tools/check_all.sh <llm-wiki-root>`**。精读达标后可 **`--strict-ingest`** 强制无占位。
2. 修改 **`tools/source_registry.tsv`** 后运行 **`python3 tools/source_registry_cli.py validate <llm-wiki-root>`**（或兼容脚本 **`validate_source_registry.py`**）。需要查 URL/本地路径对应行时：**`python3 tools/source_registry_cli.py match-url '<url>'`** / **`match-file '<path>'`**。新拷贝目录可 **`layout <llm-wiki-root>`** 做最小结构检查。Collect 字段契约见 **`tools/source_record_contract.tsv`**。
3. **分工（参考 llm-wiki-agent `wiki-lint`）**：**结构性**问题（断链、孤儿、登记表、`source_file`、frontmatter）以 **`bash tools/check_all.sh`** 为准；**语义性**问题（跨页矛盾、摘要是否过时、知识缺口）依赖**阅读与判断**，可记入 `wiki/lint-report.md` 或另开会话，**不**要求在本 pack 内调用 LLM API 做自动 lint。

---

## 操作 E：`graph`

运行：`python3 tools/build_graph.py --wiki-root <llm-wiki-root>`  
生成 `graph/graph.json` 与 `graph/graph.html`（vis.js，来自 wikilink 的 **EXTRACTED** 边；Louvain 着色）。**默认不进行**需 API Key 的语义推断边；若未来扩展，须单独配置。

---

## 命名约定

- Source slug：`kebab-case`，与 `raw` 主文件名一致。
- Entity：`TitleCase.md`
- Concept：`TitleCase.md` 或子目录 `wiki/<shelf>/concepts/<topic>/index.md` + 分面页

---

## index.md 维护建议

保持顶层 `# Wiki Index` 下分节：**Overview**、**By shelf**（链接到各 shelf 的 index 可选）、**Sources / Entities / Concepts / Syntheses**。每个 shelf 可在 `wiki/<shelf>/index.md` 再设分索引（可选）。
