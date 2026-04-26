# LLM Wiki — Schema & 工作流

## 核心理念

### Wiki > RAG

| | RAG | Wiki |
|--|------|------|
| 知识处理 | 每次查询时重新推导 | 入库时编译一次，持久保持 |
| 跨文档引用 | 临时发现 | 预先建立并维护 |
| 知识积累 | 无，每次从零开始 | 随每个 source 复合增长 |

### 复合效应

Wiki 是**持久、复合的 artifact**。每个 source 加入后，LLM 会更新相关页面、建立引用、标记矛盾点。越用越丰富。

### 人机分工

- **人类**：负责 sourcing、exploration、提问
- **LLM**：负责 summarizing、cross-referencing、filing、bookkeeping

> Obsidian = IDE，LLM = 程序员，Wiki = 代码库

---

## 目录布局

```
llm-wiki/
├── CLAUDE.md           ← 本文件（schema）
├── docs/               ← 工作流指南（collect、ingest 写作规范）
├── purpose.md           ← 学习目标与边界
├── taxonomy.md         ← 当前「门类」书架
├── raw/<shelf>/        ← immutable 素材
│   ├── articles/       ← 通用网页、博客、文档快照
│   ├── pdfs/          ← 原始 PDF 文件
│   ├── notes/         ← 自有笔记、剪贴
│   ├── refs/          ← 链接占位、大文件指针
│   ├── transcripts/   ← 视频字幕/逐字稿
│   ├── zhihu/         ← 知乎
│   ├── tweets/        ← X / Twitter
│   ├── wechat/        ← 微信公众号
│   └── xiaohongshu/   ← 小红书（常手动）
├── wiki/<shelf>/       ← 编译层（与 shelf 对齐）
│   ├── index.md        ← shelf 索引（必须有）
│   ├── overview.md     ← shelf 综合（可选）
│   ├── sources/        ← 扁平，kebab-case.md
│   ├── entities/       ← TitleCase.md
│   ├── concepts/       ← TitleCase.md
│   ├── syntheses/      ← kebab-case.md
│   └── comparisons/    ← 可选
├── wiki/index.md       ← 总索引
├── wiki/overview.md     ← Living synthesis（跨 shelf）
├── wiki/log.md         ← 操作日志
├── graph/              ← build_graph 输出
├── sessions/           ← Collect 候选表
└── tools/              ← CLI 工具
```

**shelf（门类）**：路径即分类。**新建 shelf 必须由用户批准**。

---

## 命名规范

| 目录 | 命名风格 | 示例 |
|------|----------|------|
| sources/ | kebab-case.md（**必须扁平**） | `attention-is-all-you-need.md` |
| entities/ | TitleCase.md | `OpenAI.md` |
| concepts/ | TitleCase.md | `ReinforcementLearning.md` |
| syntheses/ | kebab-case.md | `what-is-rag.md` |
| comparisons/ | kebab-case.md | `rag-vs-fine-tuning.md` |

**禁止**：`sources/` 内使用子目录。每篇素材一页，扁平化。

---

## 核心文件关系

| 文件 | 层级 | 用途 | 更新时机 |
|------|------|------|----------|
| `purpose.md` | 项目 | 学习目标 | 初始 + 里程碑 |
| `taxonomy.md` | 项目 | 门类清单 | shelf 增删改 |
| `wiki/index.md` | 全局 | 所有 wiki 页索引 | ingest / shelf 变更 |
| `wiki/overview.md` | 全局 | Living synthesis | ingest |
| `wiki/log.md` | 全局 | 操作日志 | 任何 wiki 操作 |
| `wiki/<shelf>/index.md` | shelf | 单 shelf 索引 | ingest / 增删页 |
| `wiki/<shelf>/overview.md` | shelf | 单 shelf 综合（可选） | ingest |

**命名语义**：
- `index` = 清单/目录（catalog）
- `overview` = 综合/概览（synthesis）
- `log` = 时序记录（append-only）
- `purpose` = 目标定义
- `taxonomy` = 分类体系

---

## Agent 能力依赖

llm-wiki 工作流依赖以下外部 skill，由 agent 在**执行对应操作前**强制检查环境。若缺失，**必须询问用户是否安装**，**未获得用户明确确认前不得执行该操作**。不允许跳过检查或静默降级到手动流程。

### Collect 阶段

| Skill | 用途 | 安装命令 |
|-------|------|---------|
| `tavily-search` | Web 搜索预验证 | `npx skills add https://github.com/tavily-ai/skills --skill tavily-search` |
| `baoyu-url-to-markdown` | 网页抓取（含 X/Twitter、知乎、通用网页） | `npx skills add https://github.com/jimliu/baoyu-skills --skill baoyu-url-to-markdown` |
| `wechat-article-to-markdown` | 微信文章抓取 | `npx skills add https://github.com/jackwener/wechat-article-to-markdown --skill wechat-article-to-markdown` |
| `baoyu-youtube-transcript` | YouTube 字幕提取 | `npx skills add https://github.com/jimliu/baoyu-skills --skill baoyu-youtube-transcript` |

### Ingest 阶段

| Skill | 用途 | 安装命令 |
|-------|------|---------|
| `pdf` | PDF 文本提取、OCR（处理扫描论文） | `npx skills add https://github.com/anthropics/skills --skill pdf` |
| `humanizer-zh` | 去 AI 味（中文成稿） | `npx skills add https://github.com/op7418 --skill humanizer-zh` |
| `fireworks-tech-graph` | 概念可视化（解释复杂概念时必需考虑） | `npx skills add https://github.com/yizhiyanhua-ai/fireworks-tech-graph --skill fireworks-tech-graph` |
| `html-ppt-skill` | 演示导出（按需） | `https://skills.sh/lewislulu/html-ppt-skill/html-ppt` |

> 这些 skill 不随 llm-wiki 打包分发。不同 coding agent（Claude Code、Codex 等）的 skill 安装方式可能不同，以上命令以 Qoder 的 `npx skills add` 为准。

## 操作总览

| 操作 | 触发 | 说明 |
|------|------|------|
| **A: collect** | 用户给出主题 | 先清单，后落盘 |
| **B: ingest** | 素材已落盘 | 写 source/更新索引 |
| **C: query** | 用户提问 | 读 wiki，作答 |
| **D: lint** | 主动或被动 | 检查断链/矛盾 |
| **E: graph** | 构建知识图谱 | 生成可视化 |

---

## 操作 A：collect（收集）

**触发**：用户给出主题或学习目标（例：「Transformer 原理」「学 React」）。

### 硬性规则

1. **不得**在用户确认前批量下载或写入 `raw/`（除用户明确给出的单链接/单文件外）。
2. 若需新建 shelf：先发起 **taxonomy 变更提案**（说明理由、命名、影响），**用户同意前**不得创建目录。
3. 在 `sessions/YYYYMMDD-HHMM-<slug>/candidates.md` 填写候选表（可用 `_template`）。
4. 用户勾选后，将内容写入 `raw/<shelf>/…`，并进入 **ingest**。

### 来源类型与提取策略

以 **`tools/source_registry.tsv`** 为准。执行 Collect 时先读 **`docs/collect-workflow.md`**。

### 新建 shelf 的联动

用户批准新建 shelf 时，**必须同时执行**：

| 顺序 | 文件 | 操作 |
|------|------|------|
| 1 | `taxonomy.md` | 登记新 shelf |
| 2 | `raw/<shelf>/` | 创建目录结构 |
| 3 | `wiki/<shelf>/` | 创建目录 |
| 4 | `wiki/<shelf>/index.md` | 创建 shelf 索引页 |
| 5 | `wiki/index.md` | 在「By shelf」小节添加入口 |
| 6 | `wiki/log.md` | 追加 `## [YYYY-MM-DD] taxonomy | new shelf: <shelf>` |
| 7 | `purpose.md` | 如涉及新学习目标则更新（可选） |

**禁止**：只改 `taxonomy.md`，不更新其他联动文件。

---

## 操作 B：ingest（消化素材）

**触发**：`ingest raw/<shelf>/articles/foo.md` 或等价描述。

### 必须同时执行的联动

| 顺序 | 文件 | 操作 |
|------|------|------|
| 1 | Read | 源文件；`wiki/index.md`；`wiki/overview.md`；`taxonomy.md` |
| 2 | `wiki/<shelf>/sources/<slug>.md` | 写 source 摘要页 |
| 3 | `wiki/<shelf>/index.md` | 添加 source 入口 |
| 4 | `wiki/index.md` | 在对应 shelf 小节登记 |
| 5 | `wiki/overview.md` | 必要时更新综合结论 |
| 6 | `wiki/<shelf>/entities/` 或 `concepts/` | 如有新实体/概念则创建 |
| 7 | `[[Contradictions]]` | 如有矛盾则标注 |
| 8 | `wiki/log.md` | 追加 `## [YYYY-MM-DD] ingest \| <标题>` |

### Ingest 成稿规范

写 `concepts/` 时读 **`docs/concept-template.md`**；写 `sources/` 时读 **`docs/source-template.md`**；写 `syntheses/`、`comparisons/`、实质性修订 `overview.md` 时读 **`docs/ingest-structure-guide.md`** 确定页面类型和结构，再读 **`docs/ingest-style-guide.md`** 润色表达。Agent 执行前**必须强制检查**环境中是否已安装以下 skill。若缺失，**必须询问用户是否安装**，**未安装完成前不得执行成稿操作**：

| Skill | 用途 | 安装命令 |
|-------|------|---------|
| `humanizer-zh` | 去 AI 味（中文成稿） | `npx skills add https://github.com/op7418 --skill humanizer-zh` |
| `fireworks-tech-graph` | 概念可视化（解释复杂概念时必需考虑） | `npx skills add https://github.com/yizhiyanhua-ai/fireworks-tech-graph --skill fireworks-tech-graph` |
| `html-ppt-skill` | 演示导出（按需） | `https://skills.sh/lewislulu/html-ppt-skill/html-ppt` |

### 收尾

用几句话汇总——本次**新建/更新了哪些路径**、**矛盾**有无、是否还需补实体/概念页。

---

## 操作 C：query（查询）

1. Read `wiki/index.md` 定位相关页。
2. Read 页面后作答，引用使用 `[[...]]`。
3. 询问用户是否将回答固化为 `wiki/<shelf>/syntheses/<slug>.md`（用户指定 shelf）。

---

## 操作 D：lint（检查）

1. **`python3 tools/lint_wiki.py <llm-wiki-root>`** — 断链、孤儿、`source_file` 存在性、`last_updated` 缺失。一键：**`bash tools/check_all.sh <llm-wiki-root>`**。
2. 修改 **`tools/source_registry.tsv`** 后运行 **`python3 tools/source_registry_cli.py validate <llm-wiki-root>`**。
3. **分工**：**结构性**问题以 check_all.sh 为准；**语义性**问题（矛盾、摘要过时）依赖阅读判断。

---

## 操作 E：graph（知识图谱）

运行：`python3 tools/build_graph.py --wiki-root <llm-wiki-root>`

生成 `graph/graph.json` 与 `graph/graph.html`（vis.js，Louvain 着色）。默认不进行需 API Key 的语义推断。

---

